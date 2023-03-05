"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021,2022,2023 Goffredo Baroncelli <kreijack@inwind.it>

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


import sys, tempfile

from PySide2.QtWidgets import QScrollArea, QStatusBar, QProgressDialog
from PySide2.QtWidgets import QMenu, QFileDialog, QAbstractItemView
from PySide2.QtWidgets import QSplitter, QTreeView, QLineEdit
from PySide2.QtWidgets import QGridLayout, QApplication, QPushButton
from PySide2.QtWidgets import QMessageBox, QAction, QDialog, QHeaderView
from PySide2.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush
from PySide2.QtCore import Qt, QItemSelectionModel

from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import QUrl, QMimeData, QByteArray
from PySide2.QtWidgets import QComboBox, QCheckBox
import os, zipfile

import pprint, shutil

import db, codegui, codecontextmenu, checker, customize
import exporter, utils, selectdategui, bbwindow, importer, diffgui
import cfg, listcodegui

class ExportDialog(QDialog):
    def __init__(self, parent, top, data):
        QDialog.__init__(self, parent)
        self._data = data
        self._top = top
        
        self._init_gui()
        
        max_date = db.days_to_iso(data[top]["date_from_days"])
        #pprint.pprint(data)
        for k, v in data.items():
            d = db.days_to_iso(v["date_from_days"])
            if d > max_date:
                max_date = d
        self._max_date = max_date
        self._fn = "%s_%d_rev%s@%s"%(data[top]["code"], data[top]["iter"],
                data[top]["ver"], self._max_date)

        self.setWindowTitle("Export: "+data[top]["code"]+" @ " +
                                    self._max_date)
        i = None
        
        while True:
            fn = self._fn
            if i is None:
                i = 1
            else:
                fn += "_%d"%(i)
            
            path = os.path.join(tempfile.gettempdir(), fn)
            if not os.path.exists(path):
                break
            i += 1
        self._dfolder.setText(path)

    def _set_dest_path(self):
        dest = QFileDialog.getExistingDirectory(self, "Export to to...",
                                                "",
                                                QFileDialog.ShowDirsOnly)
        if dest == "":
            return
        self._dfolder.setText(dest)

    def _export_bom(self, template, ext):
        e = exporter.Exporter(self._top , self._data)
        nf = os.path.join(self._dfolder.text(),
            "bom-" + self._fn + ext)
        e.export_as_file_by_template2(nf, template)
        
        return nf

    def _init_gui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self._dfolder = QLineEdit()
        grid.addWidget(self._dfolder, 10, 10)
        b = QPushButton("...")
        grid.addWidget(b, 10, 11)
        b.clicked.connect(self._set_dest_path)

        self._bom_format = QComboBox()
        self._exporter = []
        grid.addWidget(self._bom_format, 15, 10, 1, 2)
        self._bom_format.addItem("No BOM export")
        self._exporter.append((None, None))
        for name, descr in exporter.get_template_list():
            for ext in [".xls", ".csv"]:
                if name == "template_simple":
                    self._bom_format.addItem("Export BOM with default format (%s)"%(
                        ext))
                else:
                    self._bom_format.addItem("Export BOM with format '%s' (%s)"%(
                        descr, ext))
                self._exporter.append((utils.Callable(self._export_bom, name, ext), name))
        
            self._bom_format.setCurrentIndex(1)
        
        self._cb_export_files = QCheckBox("Export files")
        self._cb_export_files.setChecked(True)
        grid.addWidget(self._cb_export_files, 21, 10, 1, 2)
        self._cb_zip_all = QCheckBox("Zip all")
        self._cb_zip_all.setChecked(True)
        grid.addWidget(self._cb_zip_all, 22, 10, 1, 2)
        self._cb_copy_link = QCheckBox("Copy link")
        self._cb_copy_link.setChecked(True)
        grid.addWidget(self._cb_copy_link, 23, 10, 1, 2)
        self._cb_open_dest_folder = QCheckBox("Open destination folder")
        self._cb_open_dest_folder.setChecked(True)
        grid.addWidget(self._cb_open_dest_folder, 24, 10, 1, 2)

        self._cb_max_size = QCheckBox("Max file size to copy (MB)")
        self._cb_max_size.setChecked(True)
        grid.addWidget(self._cb_max_size, 25, 10)
        self._le_max_size = QLineEdit("30")
        grid.addWidget(self._le_max_size, 25, 11)

        b = QPushButton("Close")
        grid.addWidget(b, 30, 10)
        b.clicked.connect(self.close)
        
        b = QPushButton("Export...")
        grid.addWidget(b, 30, 11)
        b.clicked.connect(self._do_export)    

    def _get_file_size(self, path):
        if os.path.isfile(path):
            return os.path.getsize(path)
        if not os.path.isdir(path):
            return 0

        tsize = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                if not os.path.isfile(fp):
                    continue
                tsize += os.path.getsize(fp)

        return tsize

    def _do_export(self):
    
        QApplication.setOverrideCursor(Qt.WaitCursor)
        progress = QProgressDialog("Getting information...",
            "Abort Copy", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.forceShow()
        progress.setValue(0)

        try:
            self._do_export1(progress)
        finally:
            QApplication.restoreOverrideCursor()
            progress.close()
            self.close()

    def _do_export_get_info(self, progress):
        progress.setWindowTitle("Extracting data from DB")
        progress.setLabelText("Querying the database")
        progress.setValue(0)

        maxsize = 0
        if self._cb_max_size.isChecked():
            maxsize = int(self._le_max_size.text()) * 1024 * 1024

        missing_files = []
        bigger_files = []
        irregular_files = []
        fnl = []
        d = db.DB()
        for k in self._data:
            rid = self._data[k]["rid"]
            drawings = d.get_drawings_by_rid(rid)
            fnl += [utils.find_filename(x[1]) for x in drawings]

        fnl2 = []
        progress.setMaximum(len(fnl) + 1)

        for i in range(len(fnl)):
            fname = fnl[i]
            progress.setValue(i + 1)
            progress.setLabelText(fname)

            if progress.wasCanceled():
                progress.close()
                return (1, [])

            if not os.path.exists(fname):
                missing_files.append(fname)
                continue

            if not os.path.isdir(fname) and not os.path.isfile(fname):
                irregular_files.append(fname)
                continue

            if maxsize > 0 and self._get_file_size(fname) > maxsize:
                bigger_files.append(fname)
                continue

            fnl2.append(fname)

        if (len(missing_files) > 0 or len(irregular_files) > 0 or
            len(bigger_files) > 0):
                msg = "The following file will not be copied:\n\n"
                for i in missing_files:
                    msg += "Missing file: %s\n"%(i)
                for i in bigger_files:
                    msg += "File too big: %s\n"%(i)
                for i in irregular_files:
                    msg += "Irregular file: %s\n"%(i)
                msg += "\nEnd the copy ?"
                QApplication.setOverrideCursor(Qt.ArrowCursor)
                ret = QMessageBox.question(self, "BOMBrowser", msg)
                QApplication.restoreOverrideCursor()
                if ret == QMessageBox.Yes:
                    return (1, [])

        return (0, fnl2)

    def _do_export_copy_files(self, progress, fnl, dest):
        progress.setWindowTitle("Copying files...")
        progress.setLabelText("Querying the database")
        progress.setMaximum(len(fnl))
        progress.setValue(0)

        for i in range(len(fnl)):
            fname = fnl[i]
            progress.setValue(i)
            progress.setLabelText(fname)

            if progress.wasCanceled():
                return 1

            try:
                if os.path.isdir(fname):
                    fulldest = os.path.join(dest, os.path.basename(fname))
                    shutil.copytree(fname, fulldest)
                else:
                    shutil.copy(fname, dest)
            except Exception as e:
                QApplication.setOverrideCursor(Qt.ArrowCursor)
                ret = QMessageBox.question(self, "BOMBrowser",
                    "Error during the copy of '%s'\nEnd the copy ?"%(fname))
                QApplication.restoreOverrideCursor()
                if ret == QMessageBox.Yes:
                    return 1

        return 0

    def _do_export_zip_files(self, progress, bom_file, fnl, dest):
        progress.setWindowTitle("Zipping files...")
        progress.setLabelText("Querying the database")
        progress.setMaximum(len(fnl) + 1)
        progress.setValue(0)

        nf = os.path.join(dest, self._fn + ".zip")
        with zipfile.ZipFile(nf, "w", compression=zipfile.ZIP_DEFLATED) as z:
            if bom_file:
                z.write(bom_file, arcname=os.path.basename(bom_file))
                progress.setValue(0)
                progress.setLabelText("bom-file")

            j = 1
            for i in fnl:
                progress.setValue(j)
                j += 1
                progress.setLabelText(i)

                nf2 = os.path.join(dest, os.path.basename(i))
                # copy only if the file exists
                if os.path.exists(i):
                    z.write(nf2, arcname = os.path.basename(i))

            return nf

    def _do_export1(self, progress):

        dest = self._dfolder.text()
        if not os.path.exists(dest):
            os.makedirs(dest)
        fnl = []

        if self._cb_export_files.isChecked():
            (r, fnl) = self._do_export_get_info(progress)

            if r != 0:
                return

            r = self._do_export_copy_files(progress, fnl, dest)

            if r != 0:
                return

            progress.setValue(len(fnl))
        
        (cmd, name) = self._exporter[self._bom_format.currentIndex()]
        bom_file = None
        if not cmd is None:
            bom_file = cmd()

        link = dest
        if self._cb_zip_all.isChecked():
            link = self._do_export_zip_files(progress, bom_file, fnl, dest)

            progress.setValue(len(fnl) + 1)
        
        if self._cb_open_dest_folder.isChecked():
            QDesktopServices.openUrl(QUrl.fromLocalFile(dest))
        
        if self._cb_copy_link.isChecked():
            self._copy_file(link) 

        QApplication.setOverrideCursor(Qt.ArrowCursor)
        QMessageBox.information(self, "BOMBrowser", "Export ended")
        QApplication.restoreOverrideCursor()

    def _copy_file(self, fn):
        md = QMimeData()

        # the life is sometime very complicated !

        # windows
        md.setUrls([QUrl.fromLocalFile(fn)])
        # mate
        md.setData("x-special/mate-copied-files",
            QByteArray(("copy\nfile://"+fn).encode("utf-8")))
        # nautilus
        md.setText("x-special/nautilus-clipboard\ncopy\nfile://"+
            fn+"\n")
        # gnome
        md.setData("x-special/gnome-copied-files",
            QByteArray(("copy\nfile://"+fn).encode("utf-8")))
        # dolphin
        md.setData("text/uri-list",
            QByteArray(("file:"+fn).encode("utf-8")))

        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setMimeData(md)

    
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
            if not selection.currentIndex().isValid():
                self._tree.setCurrentIndex(self._tree.model().index(0,0))
                self._first_search = True

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


class AssemblyWindow(bbwindow.BBMainWindow):
    def __init__(self, parent, mode="asm"):
        bbwindow.BBMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        assert mode in ["asm", "where_used", "valid_where_used",
                            "smart_where_used"]

        self._mode = mode
        self._data = dict()
        self._bom_reload = None
        self._top_reference = ''

        self._init_gui()
        self.resize(1024, 600)


    def _create_statusbar(self):
        self._my_statusbar = QStatusBar()
        self._my_statusbar.showMessage("Status Bar Is Ready", 3000)
        self.setStatusBar(self._my_statusbar)


    def _create_menu(self):
        mainMenu = self.menuBar()

        m = mainMenu.addMenu("File")

        a = QAction("Refresh", self)
        a.setShortcut("F5")
        a.triggered.connect(self.bom_reload)
        m.addAction(a)
        m.addSeparator()

        a = QAction("Export bom as JSON file format...", self)
        a.triggered.connect(self._export_assemblies_list)
        m.addAction(a)
        for name, descr in exporter.get_template_list():
            if name == "template_simple":
                a = QAction("Export bom ...", self)
                a.triggered.connect(utils.Callable(self._export_as_template, name))
            else:
                a = QAction("Export bom (%s)"%(descr), self)
                a.triggered.connect(utils.Callable(self._export_as_template, name))
            m.addAction(a)

        m.addSeparator()
        a = QAction("Export data ...", self)
        a.triggered.connect(self._export_data)
        m.addAction(a)
        m.addSeparator()
        a = QAction("Reload config", self)
        a.triggered.connect(utils.reload_config_or_warn)
        m.addAction(a)
        m.addSeparator()
        a = QAction("Close", self)
        a.setShortcut("Ctrl+Q")
        a.triggered.connect(self.close)
        m.addAction(a)
        a = QAction("Exit", self)
        a.setShortcut("Ctrl+X")
        a.triggered.connect(self._exit_app)
        m.addAction(a)

        m = mainMenu.addMenu("Edit")
        for name, descr in exporter.get_template_list():
            if name == "template_simple":
                a = QAction("Copy", self)
                a.triggered.connect(utils.Callable(self._copy_as_template, name))
            else:
                a = QAction("Copy bom (%s)"%(descr), self)
                a.triggered.connect(utils.Callable(self._copy_as_template, name))
            m.addAction(a)

        m = mainMenu.addMenu("View")
        for i in range(9):
            a = QAction("Show up to level %d"%(i+1), self)
            a.setShortcut("Ctrl+%d"%(i+1))
            a.triggered.connect(utils.Callable(self._show_up_to, i+1))
            m.addAction(a)

        a = QAction("Show all levels", self)
        a.setShortcut("Ctrl+A")
        a.triggered.connect(utils.Callable(self._show_up_to, -1))
        m.addAction(a)

        m = mainMenu.addMenu("Search")
        a = QAction("Find", self)
        a.setShortcut("Ctrl+F")
        a.triggered.connect(self._start_find)
        m.addAction(a)

        a = QAction("Advanced search", self)
        a.triggered.connect(self._advanced_search)
        m.addAction(a)

        if self._mode == "asm":
            m = mainMenu.addMenu("Tools")
            a = QAction("Check bom", self)
            a.triggered.connect(self._check_bom)
            m.addAction(a)

            l = importer.get_diff_importer_list()
            if len(l):
                m.addSeparator()
                for (importer_name, name, open_fn, import_fn) in l:
                    a = QAction("Diff against '%s'..."%(name), self)
                    a.triggered.connect(utils.Callable(self._diff_bom,
                            importer_name, name, open_fn, import_fn))
                    m.addAction(a)

            l = customize.get_asm_tool_menu_list()
            if len(l):
                m.addSeparator()
                for (name, func) in l:
                    a = QAction(name, self)
                    a.triggered.connect(lambda : func(self._top, self._data))
                    m.addAction(a)

        self._windowsMenu = self.build_windows_menu(mainMenu)

        m = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : self._show_about(db.connection))
        m.addAction(a)

    def _advanced_search(self):
        w = listcodegui.CodesWindow(bom=self._data, bomdesc=self._top_reference)
        w.show()

    def _diff_bom(self, importer_name, name, open_fn, import_fn):
        bom1 = diffgui.CodeDateSingle(self._data[self._top]["id"],
            self._data[self._top]["code"], 
            self._bom_date)
        fn = open_fn()
        bom2 = diffgui.BomImported(name, import_fn, open_fn, fn)
        
        w = diffgui.DiffWindow(bom1, bom2)
        w.do_diff()
        w.show()

    def _check_bom(self):
        checker.run_bom_tests(self._top, self._data, self._top_reference)

    def _export_data(self):
        d = ExportDialog(self, self._top, self._data)
        d.exec_()

    def _export_assemblies_list(self):
        nf = QFileDialog.getSaveFileName(self, "BOMBrowser - export bom",
                                    filter="Json file format (*.json);; All files (*.*)",
                                    selectedFilter="Json file format (*.json)")
        if nf[0] == '':
            return
        e = exporter.Exporter(self._top , self._data)
        e.export_as_json(nf[0])

    def _export_as_template(self, template):
        nf, _ = QFileDialog.getSaveFileName(self, "BOMBrowser - export bom",
                                    filter="CSV file (*.csv);; Excel file (*.xls)",
                                    selectedFilter="Excel file (*.xls)")
        if nf == '':
            return
        if (not nf.lower().endswith(".xls") and
            not nf.lower().endswith(".csv")):
                QMessageBox.critical(self, "BOMBrowser", "Unsupported file format")
                return
        e = exporter.Exporter(self._top , self._data)
        e.export_as_file_by_template2(nf, template)

    def _copy_as_template(self, template):
        e = exporter.Exporter(self._top , self._data)
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        data = e.export_as_table_by_template2(template)
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
        self._find = FindDialog(self, self._tree)
        self._find.show()

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

        self._code_widget = codegui.CodeWidget()
        scrollarea = QScrollArea()
        scrollarea.setWidget(self._code_widget)
        scrollarea.setWidgetResizable(True)
        qs.addWidget(scrollarea)

        qs.setSizes([700, 1024-700])
        self.setCentralWidget(qs)

        self._tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._tree_context_menu)

    def _tree_context_menu(self, point):
        idx = self._tree.indexAt(point);
        if not idx.isValid():
            return

        path = self._get_path()
        if len(path) == 0:
            return

        id_ = self._data[path[-1]]["id"]

        contextMenu = QMenu(self)
        codecontextmenu.generate_codes_context_menu(code_id = id_, menu=contextMenu,
            parent=self)
        contextMenu.exec_(self._tree.viewport().mapToGlobal(point))

    def _set_bom_colors(self, path, colors_filter, item):
        if len(path) == 0:
            return

        def match(k, v):
            if k.startswith("*"):
                k = k[1:]
                l = range(len(path))
            else:
                l = [len(path) - 1]

            for idx in l:
                i = path[idx]
                tmp = self._data[i]
                if k in tmp:
                    if v.startswith("!") and str(tmp[k]) != v[1:]:
                        return True
                    if str(tmp[k]) == v:
                        return True

                if idx == 0:
                    continue

                j = path[idx-1]
                tmp2 = self._data[j]["deps"][i]
                if k in tmp2:
                    if v.startswith("!") and str(tmp2[k]) != v[1:]:
                        return True
                    if str(tmp2[k]) == v:
                        return True

            return False

        def apply_actions(actions):
            for action in actions:
                if action.startswith("bg="):
                    item.setBackground(QColor(action[3:]))
                elif action.startswith("fg="):
                    item.setForeground(QColor(action[3:]))
                elif action.startswith("italic"):
                    f = item.font()
                    f.setItalic(True)
                    item.setFont(f)
                elif action.startswith("bold"):
                    f = item.font()
                    f.setBold(True)
                    item.setFont(f)
                else:
                    print("WARNING: unknown action '%s'"%(action))

        for (filters, actions) in colors_filter:
            for f in filters:
                k,v = f.split("=")[:2]
                if not match(k, v):
                    break
            else:
                apply_actions(actions)

    def populate(self, top, data, bom_date=None):
        top_code = data[top]["code"]

        colors_filter = []
        self._top_reference = top_code
        if self._mode == "asm":
                if bom_date == db.prototype_date -1:
                    dt2 = "LATEST"
                elif bom_date == db.end_of_the_world:
                    dt2 = "PROTOTYPE"
                elif bom_date == db.prototype_date:
                    dt2 = "PROTOTYPE"
                else:
                    dt2 = db.days_to_iso(bom_date)

                self._bom_date = bom_date
                self._top_reference = top_code + " @ " + dt2
                self.setWindowTitle("Assembly: " + self._top_reference)

                colors_filter = cfg.get_bomcolors()
        elif self._mode == "valid_where_used":
                self.setWindowTitle("Valid where used: " + self._top_reference)
        elif self._mode == "smart_where_used":
                self.setWindowTitle("Smart where used: " + self._top_reference)
        else: # mode == "where used"
                self.setWindowTitle("Where used: "+self._top_reference)
        self._data = data
        self._top = top

        model = QStandardItemModel()
        self._tree.setModel(model)
        model.setHorizontalHeaderLabels(["Code", "Description"])
        recursive_error = set()

        def rec_update(n, path):
            d = data[n]
            #if self._valid_where_used and d["date_to"] != "":
            #    return None
            i =  QStandardItem(d["code"])
            i.setData(n)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            i2 =  QStandardItem(d["descr"])
            i2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            if len(colors_filter):
                self._set_bom_colors(path, colors_filter, i)
                self._set_bom_colors(path, colors_filter, i2)
            for c in data[n]["deps"]:
                if c in path:
                    recursive_error.add((d["code"], d["descr"]))
                    continue
                ci = rec_update(c, path+[c])
                if not ci is None:
                    i.appendRow(ci)
            return (i, i2)

        root_items = rec_update(top, [top])
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

        if len(recursive_error):
            QMessageBox.critical(self, "BOMBrowser",
                "ERROR: loop detected after the following code(s):\n\n"+
                "\n".join(
                    "%d) %s - %s"%(x[0] + 1, x[1][0], x[1][1]) for x
                                    in enumerate(recursive_error)
                ) + "\n\n" +
                "Execute Menu->Tool->Check bom in the assembly window\n" +
                "for further information."
            )

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

        qty = ""
        each = ""
        unit = ""
        ref = ""
        gavals = dict()

        date_from_days = self._data[data_key]["date_from_days"]
        id_ = self._data[data_key]["id"]

        if len(path) > 1:
            parent = path[-2]
            d3 = self._data[parent]["deps"][data_key]
            if "qty" in d3:
                qty = float(d3["qty"])
            else:
                qty = 1
            if "each" in d3:
                each = float(d3["each"])
            else:
                each = 1

            unit = self._data[parent]["deps"][data_key]["unit"]
            ref = self._data[parent]["deps"][data_key]["ref"]
            for i in range(db.gavals_count):
                k = "gaval%d"%(i+1)
                if k in self._data[parent]["deps"][data_key]:
                    gavals[k] = self._data[parent]["deps"][data_key][k]

        self._code_widget.populate(id_, date_from_days, qty, each,
                                    unit, ref, gavals)

        self._my_statusbar.showMessage("/".join(map(lambda x : self._data[x]["code"], path)))

    def bom_reload(self):
        if self._bom_reload:
            self._bom_reload()

    def set_bom_reload(self, f):
        self._bom_reload = f

def _smart_filter(top, data):
    top_node = data[top]
    first_level_keys = top_node["deps"].keys()

    def find_tails(key):
        ret = set()
        todo = set([key])
        done = set()

        while len(todo):
            key = todo.pop()
            done.add(key)

            if len(data[key]["deps"]) == 0:
                if not data[key]["code"].startswith("[...] "):
                    data[key]["code"] = "[...] " + data[key]["code"]
                ret.add(key)
            else:
                for key2 in data[key]["deps"]:
                    if not key2 in done:
                        todo.add(key2)

        return ret

    for key in first_level_keys:
        fl_node = data[key]
        if len(fl_node["deps"]) == 0:
            continue
        tails = find_tails(key)
        fl_node["__deps"] = {}
        for tail in tails:
            fl_node["__deps"][tail] = {
                "code": data[tail]["code"],
                "qty": 0,
                "each": 0,
                "ref": "",
                "unit": "",
            }

    for key in first_level_keys:
        if "__deps" in data[key]:
            data[key]["deps"] = data[key]["__deps"]

    return data


def where_used(code_id, mode="where_used"):
    if not code_id:
        QApplication.beep()
        return

    w = AssemblyWindow(None, mode)

    w.show()

    def bom_reload():
        d = db.DB()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        valid = mode in ["smart_where_used", "valid_where_used"]
        (top, data) = d.get_where_used_from_id_code(code_id, valid)
        if mode == "smart_where_used":
            data = _smart_filter(top, data)
        w.populate(top, data)
        QApplication.restoreOverrideCursor()

    w.set_bom_reload(bom_reload)
    w.bom_reload()

def valid_where_used(code_id):
    return where_used(code_id, mode="valid_where_used")
def smart_where_used(code_id):
    return where_used(code_id, mode="smart_where_used")

def show_assembly(code_id, winParent):
    if not code_id:
        QApplication.beep()
        return

    dlg = selectdategui.SelectDate(code_id, winParent)
    ret = dlg.exec_()
    if not ret:
        QApplication.restoreOverrideCursor()
        return
    (code, date_from_days) = dlg.get_code_and_date_from_days()

    w = AssemblyWindow(None)
    w.show()

    def bom_reload():
        d = db.DB()
        QApplication.setOverrideCursor(Qt.WaitCursor)

        data = d.get_bom_by_code_id3(code_id, date_from_days)
        w.populate(*data, bom_date=date_from_days)
        QApplication.restoreOverrideCursor()
    w.set_bom_reload(bom_reload)
    w.bom_reload()

def show_latest_assembly(code_id):
    if not code_id:
        QApplication.beep()
        return

    w = AssemblyWindow(None)
    w.show()

    def bom_reload():
        d = db.DB()
        dates = d.get_dates_by_code_id3(code_id)

        # get the prototype date ONLY if there is the only option
        # otherwise get the latest "non prototype" date
        if dates[0][2] >= db.prototype_date:
            if len(dates) > 1:
                dt = min(db.prototype_date - 1, dates[1][3])
            else:
                dt = db.prototype_date
        else:
            dt = min(db.prototype_date - 1, dates[0][3])

        QApplication.setOverrideCursor(Qt.WaitCursor)
        data = d.get_bom_by_code_id3(code_id, dt)
        w.populate(*data, bom_date=dt)
        QApplication.restoreOverrideCursor()
    w.set_bom_reload(bom_reload)
    w.bom_reload()

def show_proto_assembly(code_id):
    if not code_id:
        QApplication.beep()
        return

    w = AssemblyWindow(None)
    w.show()

    def bom_reload():
        d = db.DB()
        dates = d.get_dates_by_code_id3(code_id)
        dt = min(db.end_of_the_world, dates[0][3])
        QApplication.setOverrideCursor(Qt.WaitCursor)
        data = d.get_bom_by_code_id3(code_id, dates[0][3])
        w.populate(*data, bom_date=db.end_of_the_world)
        QApplication.restoreOverrideCursor()
    w.set_bom_reload(bom_reload)
    w.bom_reload()

def show_assembly_by_date(code_id, dt):
    if not code_id:
        QApplication.beep()
        return

    w = AssemblyWindow(None)
    w.show()
    def bom_reload():
        d = db.DB()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        data = d.get_bom_by_code_id3(code_id, dt)
        w.populate(*data, bom_date=dt)
        QApplication.restoreOverrideCursor()
    w.set_bom_reload(bom_reload)
    w.bom_reload()

