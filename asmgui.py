"""
BOM Browser - tool to browse a bom
Copyright (C) 2020 Goffredo Baroncelli <kreijack@inwind.it>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


import sys

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar, QProgressDialog
from PySide2.QtWidgets import QMenu, QTableView, QFileDialog, QAbstractItemView
from PySide2.QtWidgets import QSplitter, QTreeView, QLabel, QLineEdit
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication, QPushButton
from PySide2.QtWidgets import QMessageBox, QAction, QDialog, QHeaderView
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import Qt, QItemSelectionModel, QAbstractTableModel
import pprint, shutil

import db, codegui, diffgui, copycodegui
import exporter, utils, selectdategui, editcode


class FindDialog(QDialog):
    def __init__(self, parent, tree):
        QDialog.__init__(self, parent)

        self._tree = tree
        self._first_search = True

        grid = QGridLayout()

        self._stext = QLineEdit()
        #self._stext.returnPressed.connect(self._search_next)

        grid.addWidget(self._stext, 0, 0, 1, 3)

        b = QPushButton("Prev")
        b.clicked.connect(self._search_prev)
        grid.addWidget(b, 1, 0)

        b = QPushButton("Next")
        b.setDefault(True)
        b.clicked.connect(self._search_next)
        grid.addWidget(b, 1, 1)

        b = QPushButton("Close")
        b.clicked.connect(self.close)
        grid.addWidget(b, 1, 2)

        self.setLayout(grid)
        self.setWindowTitle("Search")

    def _move_next(self, selection, idx):
        item = self._tree.model().itemFromIndex(idx)

        # check if exists a child
        if item.hasChildren():
            idx = self._tree.model().index(0, 0, idx)
            return idx

        # check if exist a next sibling
        parent_item = self._tree.model().itemFromIndex(idx.parent())
        if parent_item.rowCount() > item.row() + 1:
            idx = self._tree.model().index(item.row() + 1, 0, idx.parent())
            return idx

        # ok, we should go up
        while self._tree.model().itemFromIndex(idx.parent()):
            parent_item = self._tree.model().itemFromIndex(idx.parent())
            if idx.row() +1 < parent_item.rowCount():
                idx = self._tree.model().index(idx.row() + 1, 0, idx.parent())
                return idx
            idx = idx.parent()
        return None

    def _move_prev(self, selection, idx):
        item = self._tree.model().itemFromIndex(idx)

        # check if exist a previous sibling
        parent_item = self._tree.model().itemFromIndex(idx.parent())
        if item.row() > 0:
            idx = self._tree.model().index(item.row() - 1, 0, idx.parent())

            # move to the last item
            item = self._tree.model().itemFromIndex(idx)
            while item.hasChildren():
                idx = self._tree.model().index(item.rowCount() - 1, 0, idx)
                item = self._tree.model().itemFromIndex(idx)

            return idx

        # ok, we should go up
        if (self._tree.model().itemFromIndex(idx.parent())):
            idx = idx.parent()
            return idx

        return None

    def _get_item(self, idx):
        item = self._tree.model().itemFromIndex(idx)
        item2 = self._tree.model().itemFromIndex(idx.siblingAtColumn(1))
        return item, item2

    def _do_search(self, next=True):
        if next:
            move = self._move_next
        else:
            move = self._move_prev

        selection = self._tree.selectionModel()

        if not selection.hasSelection():
            selection.select(selection.currentIndex(),
                QItemSelectionModel.Select|QItemSelectionModel.Rows)
        idx = selection.selectedIndexes()[0]

        while True:
            if not self._first_search:
                idx = move(selection, idx)
                if idx is None:
                    QApplication.beep()
                    QMessageBox.information(self, "BOMBrowser", "Data not found")
                    return


            self._first_search = False
            item1, item2 = self._get_item(idx)

            if self._stext.text().lower() in item1.text().lower():
                break;
            if self._stext.text().lower() in item2.text().lower():
                break;

        selection.clearSelection()
        selection.select(idx,
                QItemSelectionModel.Select|QItemSelectionModel.Rows)
        self._tree.scrollTo(idx,
            QAbstractItemView.ScrollHint.EnsureVisible)

    def _search_prev(self):
        self._do_search(next=False)

    def _search_next(self):
        self._do_search(next=True)


class AssemblyWindow(utils.BBMainWindow):
    def __init__(self, parent, asm=True, valid_where_used=False):
        utils.BBMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._asm = asm
        self._valid_where_used = valid_where_used
        self._data = dict()

        self._init_gui()
        self.resize(1024, 600)


    def _create_statusbar(self):
        self._my_statusbar = QStatusBar()
        self._my_statusbar.showMessage("Status Bar Is Ready", 3000)
        self.setStatusBar(self._my_statusbar)


    def _create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        editMenu = mainMenu.addMenu("Edit")
        viewMenu = mainMenu.addMenu("View")
        searchMenu = mainMenu.addMenu("Search")
        self._windowsMenu = mainMenu.addMenu("Windows")

        self._windowsMenu.aboutToShow.connect(self._build_windows_menu)

        export_bom = QAction("Export bom as CSV file...", self)
        export_bom.triggered.connect(self._export_bom)
        export_assy = QAction("Export bom as JSON file format...", self)
        export_assy.triggered.connect(self._export_assemblies_list)

        class Caller:
            def __init__(self, f, arg):
                self._f = f
                self._arg = arg
            def __call__(self):
                self._f(self._arg)

        export_as = []
        for tmpl in exporter.get_template_list():
            m = QAction("Export bom as CSV template '%s'"%(tmpl), self)
            m.triggered.connect(Caller(self._export_as_template, tmpl))
            export_as.append(m)

        copyFiles = QAction("Copy files ...", self)
        copyFiles.triggered.connect(self._copy_all_bom_files)

        closeAction = QAction("Close", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.triggered.connect(self.close)
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+X")
        exitAction.triggered.connect(self._exit_app)
        copyAction = QAction("Copy", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self._copy_info_action)

        copy_as = []
        for tmpl in exporter.get_template_list():
            m = QAction("Copy bom as template '%s'"%(tmpl), self)
            m.triggered.connect(Caller(self._copy_as_template, tmpl))
            copy_as.append(m)

        findAction = QAction("Find", self)
        findAction.setShortcut("Ctrl+F")
        findAction.triggered.connect(self._start_find)

        for i in range(9):
            a = QAction("Show up to level %d"%(i+1), self)
            a.setShortcut("Ctrl+%d"%(i+1))

            a.triggered.connect(Caller(self._show_up_to, i+1))

            viewMenu.addAction(a)

        a = QAction("Show all levels", self)
        a.setShortcut("Ctrl+A")
        a.triggered.connect(Caller(self._show_up_to, -1))

        viewMenu.addAction(a)

        fileMenu.addAction(export_bom)
        fileMenu.addAction(export_assy)
        for m in export_as:
            fileMenu.addAction(m)
        fileMenu.addSeparator()
        fileMenu.addAction(copyFiles)
        fileMenu.addSeparator()
        fileMenu.addAction(closeAction)
        fileMenu.addAction(exitAction)
        editMenu.addAction(copyAction)
        editMenu.addSeparator()
        for m in copy_as:
            editMenu.addAction(m)
        searchMenu.addAction(findAction)

        self._build_windows_menu()

        helpMenu = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : utils.about(self, db.connection))
        helpMenu.addAction(a)

    def _copy_all_bom_files(self):
        dest = QFileDialog.getExistingDirectory(self, "Save to...",
                                                "",
                                                QFileDialog.ShowDirsOnly)
        if dest == "":
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        d = db.DB()
        fnl = []
        for k in self._data:
            rid = self._data[k]["rid"]
            drawings = d.get_drawings_by_code_id(rid)
            fnl += [x[1] for x in drawings]

        fname = ''

        progress = QProgressDialog("Copying files...", "Abort Copy", 0, len(fnl), self)
        progress.setWindowModality(Qt.WindowModal)

        for i in range(len(fnl)):
            fname = fnl[i]
            progress.setValue(i)

            if progress.wasCanceled():
                break
            #... copy one file

            progress.setLabelText(fname)
            try:
                shutil.copy(fname, dest)
            except Exception as e:
                progress.forceShow()
                ret = QMessageBox.question(self, "BOMBrowser",
                    "Error during the copy of '%s'\nEnd the copy ?"%(fname))
                if ret == QMessageBox.Yes:
                    print(er)
                    QApplication.restoreOverrideCursor()
        progress.setValue(len(fnl))

        QApplication.restoreOverrideCursor()

    def _build_windows_menu(self):
        utils.build_windows_menu(self._windowsMenu, self)

    def _copy_info_action(self):
        e = exporter.Exporter(self._top , self._data)
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(e.export_bom_as_string(), mode=cb.Clipboard)

    def _export_bom(self):
        nf = QFileDialog.getSaveFileName(self, "BOMBrowser - export bom",
                                    filter="CSV file (*.csv);; All files (*.*)",
                                    selectedFilter="*.csv")
        if nf[0] == '':
            return
        e = exporter.Exporter(self._top , self._data)
        e.export_as_bom(nf[0])

    def _export_assemblies_list(self):
        nf = QFileDialog.getSaveFileName(self, "BOMBrowser - export bom",
                                    filter="Json file format (*.json);; All files (*.*)",
                                    selectedFilter="*.json")
        if nf[0] == '':
            return
        e = exporter.Exporter(self._top , self._data)
        e.export_as_json(nf[0])

    def _export_as_template(self, template):
        nf = QFileDialog.getSaveFileName(self, "BOMBrowser - export bom",
                                    filter="CSV file (*.csv);; All files (*.*)",
                                    selectedFilter="*.csv")
        if nf[0] == '':
            return
        e = exporter.Exporter(self._top , self._data)
        data = e.export_as_csv_table_by_template(template)
        open(nf[0], "w").write(data)

    def _copy_as_template(self, template):
        e = exporter.Exporter(self._top , self._data)
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        data = e.export_as_table_by_template(template)
        cb.setText(data, mode=cb.Clipboard)

    def _show_up_to(self, lev):
        if lev == -1:
            self._tree.expandAll()
            return

        parent_item = self._tree.model().item(0,0)

        def rec_iterate(parent, l):
            c = parent.rowCount()
            if c == 0:
                return

            for i in range(c):
                child = parent.child(i, 0)
                child_idx = child.index()
                if l >= lev:
                    if self._tree.isExpanded(child_idx):
                        self._tree.setExpanded(child_idx, False)
                else:
                    if not self._tree.isExpanded(child_idx):
                        self._tree.setExpanded(child_idx, True)
                    rec_iterate(child, l+1)

        QApplication.setOverrideCursor(Qt.WaitCursor)
        rec_iterate(parent_item, 1)
        QApplication.restoreOverrideCursor()

    def _start_find(self):
        f = FindDialog(self, self._tree)
        f.exec_()

    def _exit_app(self):
        ret = QMessageBox.question(self, "BOMBrowser", "Do you want to exit from the application ?")
        if ret == QMessageBox.Yes:
            sys.exit(0)

    def _init_gui(self):
        self._create_menu()
        # create toolbar
        self._create_statusbar()

        qs = QSplitter()
        self._splitter = qs

        self._tree = QTreeView()
        self._tree.setAlternatingRowColors(True)
        qs.addWidget(self._tree)

        self._w = QWidget()
        qs.addWidget(self._w)
        qs.setSizes([700, 1024-700])
        self.setCentralWidget(qs)

        self._tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._tree_context_menu)

    def _tree_context_menu(self, point):
        idx = self._tree.indexAt(point);
        if not idx.isValid():
            return

        contextMenu = QMenu(self)
        showLatestAssembly = contextMenu.addAction("Show latest assembly")
        showLatestAssembly.triggered.connect(self._show_latest_assembly)
        whereUsed = contextMenu.addAction("Where used")
        whereUsed.triggered.connect(self._show_where_used)
        validWhereUsed = contextMenu.addAction("Valid where used")
        validWhereUsed.triggered.connect(self._show_valid_where_used)
        showAssembly = contextMenu.addAction("Show assembly by date")
        showAssembly.triggered.connect(self._show_assembly)

        contextMenu.addSeparator()
        reviseCode = contextMenu.addAction("Copy/revise code ...")
        reviseCode.triggered.connect(self._revise_code)
        editCode = contextMenu.addAction("Edit code ...")
        editCode.triggered.connect(self._edit_code)
        contextMenu.addSeparator()

        doDiff1 = contextMenu.addAction("Diff from...")
        doDiff1.triggered.connect(self._set_diff_from)
        doDiff2 = contextMenu.addAction("Diff to...")
        doDiff2.triggered.connect(self._set_diff_to)

        contextMenu.exec_(self._tree.viewport().mapToGlobal(point))

    def _edit_code(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        editcode.edit_code_by_code_id(id_)

    def _revise_code(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        copycodegui.revise_copy_code(id_, self)

    def _set_diff_from(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        diffgui.set_from(id_, self)

    def _set_diff_to(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        diffgui.set_to(id_, self)

    def _show_assembly(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        show_assembly(id_, self.parent())

    def _show_latest_assembly(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        show_latest_assembly(id_)

    def _show_where_used(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        where_used(id_, self.parent())

    def _show_valid_where_used(self):
        path = self._get_path()
        if len(path) == 0:
            return
        id_ = self._data[path[-1]]["id"]

        valid_where_used(id_, self.parent())

    def populate(self, top, data, date_from=None):
        top_code = data[top]["code"]

        if self._asm:
                dt2 = date_from
                if date_from == db.days_to_iso(db.end_of_the_world):
                    dt2 = "LATEST"
                self.setWindowTitle(utils.window_title +
                        " - Assembly: " + top_code + " @ " + dt2)
        elif self._valid_where_used:
                self.setWindowTitle(utils.window_title +
                        " - Valid where used: " + top_code)
        else:
                self.setWindowTitle(utils.window_title +
                        " - Where used: "+top_code)
        self._data = data
        self._top = top

        model = QStandardItemModel()
        self._tree.setModel(model)
        model.setHorizontalHeaderLabels(["Code", "Description"])

        def rec_update(n, path=[]):
            d = data[n]
            #if self._valid_where_used and d["date_to"] != "":
            #    return None
            i =  QStandardItem(d["code"])
            i.setData(n)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            i2 =  QStandardItem(d["descr"])
            i2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            for c in data[n]["deps"]:
                if c in path:
                    # ERROR: a recursive path
                    i3 = QStandardItem("<REC-ERROR>")
                    i3.setData(-1)
                    i3.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    i.appendRow((
                        i3,
                        QStandardItem("<REC-ERROR>"))
                    )
                    continue
                ci = rec_update(c, path+[c])
                if not ci is None:
                    i.appendRow(ci)
            return (i, i2)

        root_items = rec_update(top)
        if root_items is None:
            model.appendRow((QStandardItem("Empty"),))
        else:
            model.appendRow(root_items)
        idx = model.indexFromItem(root_items[0])
        self._tree.expandAll()
        self._tree.selectionModel().selectionChanged.connect(self._change_selection)
        self._tree.selectionModel().select(idx, self._tree.selectionModel().Rows)

        self._tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        sizes = []
        for i in range(self._tree.header().count()):
            sizes.append(self._tree.header().sectionSize(i))
        self._tree.header().setSectionResizeMode(QHeaderView.Interactive)
        for i in range(self._tree.header().count()):
            self._tree.header().resizeSection(i, sizes[i])
        self._update_metadata([top])

    def _get_path(self):
        idxs = self._tree.selectionModel().selectedIndexes()
        if idxs is None:
            return []

        idx = idxs[0]

        path = []
        while self._tree.model().itemFromIndex(idx):
            path.insert(0, self._tree.model().itemFromIndex(idx).data())
            idx = idx.parent()

        return path

    def _change_selection(self, to, from_):
        if len(to.indexes()) < 1:
            return

        idx = to.indexes()[0]

        path = []
        while self._tree.model().itemFromIndex(idx):
            path.insert(0, self._tree.model().itemFromIndex(idx).data())
            idx = idx.parent()

        #path = self._get_path()

        self._update_metadata(path)

    def _update_metadata(self, path):
        data_key = path[-1]
        #pprint.pprint(self._data[data_key])


        if len(path) > 1:
            k1 = path[-2]
            k2 = path[-1]
            d3 = self._data[k1]["deps"][k2]
            if "qty" in d3:
                qty = float(d3["qty"])
            else:
                qty = 1
            if "each" in d3:
                each = float(d3["each"])
            else:
                each = 1
        else:
            qty = ""
            each = ""

        unit = None
        date_from = None
        date_to = None
        ref = None
        date_to = self._data[data_key]["date_to"]
        date_from = self._data[data_key]["date_from"]
        date_from_days = self._data[data_key]["date_from_days"]
        if len(path) > 1:
            #pprint.pprint(self._data[path[-2]])
            unit = self._data[path[-2]]["deps"][path[-1]]["unit"]
            ref = self._data[path[-2]]["deps"][path[-1]]["ref"]
        scrollarea = QScrollArea()
        scrollarea.setWidget(
            codegui.CodeWidget(self._data[data_key]["id"],
                date_from_days=self._data[data_key]["date_from_days"],
                qty=qty, each=each, unit=unit,
                date_from = date_from,
                date_to = date_to,
                ref = ref,
                winParent = self.parent(),
                rid=self._data[data_key]["rid"]))

        # this to avoid unexpected crash
        w = self._splitter.widget(1)
        self._splitter.replaceWidget(1, scrollarea)
        self._grid_widget = scrollarea
        self._my_statusbar.showMessage("/".join(map(lambda x : self._data[x]["code"], path)))


class WhereUsedWindow(AssemblyWindow):
    def __init__(self, parent):
        AssemblyWindow.__init__(self, parent, asm = False)


class ValidWhereUsedWindow(AssemblyWindow):
    def __init__(self, parent):
        AssemblyWindow.__init__(self, parent, asm = False,
            valid_where_used = True)


def where_used(code_id, winParent, valid=False):
    if not code_id:
        QApplication.beep()
        return

    d = db.DB()
    QApplication.setOverrideCursor(Qt.WaitCursor)

    (top, data) = d.get_where_used_from_id_code(code_id, valid)

    if len(data) == 1:
        QApplication.restoreOverrideCursor()
        QApplication.beep()
        QMessageBox.critical(winParent, "BOMBrowser", "The item is not in an assembly")
        return

    if valid:
        w = ValidWhereUsedWindow(None)
    else:
        w = WhereUsedWindow(None)

    w.show()
    w.populate(top, data)
    QApplication.restoreOverrideCursor()

def valid_where_used(code_id, winParent):
    return where_used(code_id, winParent, valid=True)

def show_assembly(code_id, winParent):
    if not code_id:
        QApplication.beep()
        return

    d = db.DB()
    if not d.is_assembly(code_id):
        QApplication.beep()
        QMessageBox.critical(winParent, "BOMBrowser", "The item is not an assembly")
        return

    dlg = selectdategui.SelectDate(code_id, winParent)
    ret = dlg.exec_()
    if not ret:
        QApplication.restoreOverrideCursor()
        return

    QApplication.setOverrideCursor(Qt.WaitCursor)
    w = AssemblyWindow(None)
    w.show()
    res = dlg.get_result()
    data = d.get_bom_by_code_id2(code_id, res[1])
    w.populate(*data, date_from=res[1])
    QApplication.restoreOverrideCursor()

def show_latest_assembly(code_id):
    if not code_id:
        QApplication.beep()
        return

    d = db.DB()
    if not d.is_assembly(code_id):
        QApplication.beep()
        QMessageBox.critical(None, "BOMBrowser", "The item is not an assembly")
        return

    w = AssemblyWindow(None)
    w.show()
    dates = d.get_dates_by_code_id2(code_id)

    dt = dates[0][4]
    if dt == "":
        dt = db.days_to_iso(db.end_of_the_world)

    data = d.get_bom_by_code_id2(code_id, dt)
    w.populate(*data, date_from=dt)
    QApplication.restoreOverrideCursor()

