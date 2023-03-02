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

import  sys, os, re, shutil

from PySide2.QtWidgets import  QComboBox, QAbstractScrollArea
from PySide2.QtWidgets import  QTableView, QTableWidgetItem, QLabel
from PySide2.QtWidgets import  QGridLayout, QApplication, QWidget, QFileDialog
from PySide2.QtWidgets import  QMessageBox, QAction, QLineEdit
from PySide2.QtWidgets import  QPushButton, QHBoxLayout, QTabWidget, QDialog
from PySide2.QtWidgets import  QHeaderView, QMenu, QGroupBox, QTableWidget
from PySide2.QtGui import  QColor, QDesktopServices
from PySide2.QtCore import  QItemSelectionModel, QItemSelection
from PySide2.QtCore import  QUrl, Signal, Qt, QEvent

import  utils, listcodegui, db, cfg
import  importer, customize, bbwindow, codecontextmenu
import bbdate

class SelectCode(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self._init_gui()

    def _init_gui(self):
        grid = QGridLayout()

        self._search_widget = listcodegui.CodesListWidget()
        self._search_widget.doubleClicked.connect(self.accept)
        grid.addWidget(self._search_widget, 10, 1, 1, 3)

        b = QPushButton("Cancel")
        b.clicked.connect(self.reject)
        grid.addWidget(b, 20, 1)

        b = QPushButton("OK")
        b.clicked.connect(self.accept)
        grid.addWidget(b, 20, 3)

        self.setLayout(grid)

        self.setWindowTitle("Search code")
        self.setAttribute(Qt.WA_DeleteOnClose)

    def getCodeId(self):
        return self._search_widget.getCodeId()

    def getCode(self):
        return self._search_widget.getCode()


class EditDates(QDialog):
    def __init__(self, code_id, parent):
        QDialog.__init__(self, parent)
        self._code_id = code_id

        self._init_gui()
        self._populate()
        self.resize(800, 600)

    def _init_gui(self):

        g = QGridLayout()

        self._table = QTableWidget()
        g.addWidget(self._table, 20, 1, 1, 2)

        b = QPushButton("Cancel")
        b.clicked.connect(self._cancel)
        g.addWidget(b, 30, 1)

        b = QPushButton("Save")
        b.clicked.connect(self._save)
        g.addWidget(b, 30, 2)

        self.setLayout(g)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def _save(self):

        d = db.DB()

        dates = []
        row_cnt = self._table.rowCount()
        min_date_from_days = None
        max_date_to_days = None
        for row in range(row_cnt):
            rid = int(self._table.item(row, 0).text())
            date_from = self._get_table_cell(row, 4).text().upper()
            date_to = self._get_table_cell(row, 5).text()

            try:
                if date_from == "PROTOTYPE":
                    date_from_days = db.prototype_date
                else:
                    date_from_days = db.iso_to_days(date_from)
                if date_to != '':
                    date_to_days = db.iso_to_days(date_to)
                else:
                    date_to_days = db.end_of_the_world
            except:
                utils.show_exception(msg="Error in date format row %d"%(row+1))
                return

            if min_date_from_days is None or min_date_from_days > date_from_days:
                min_date_from_days = date_from_days
            if max_date_to_days is None or max_date_to_days < date_to_days:
                 max_date_to_days = date_to_days

            dates.append([rid, date_from, date_from_days, date_to, date_to_days])

            # check that the date range has a shorter life than
            # the children
            for (cid, cdate_from_days, cdate_to_days) in d.get_children_dates_range_by_rid(rid):

                if (cdate_from_days > date_from_days or
                    cdate_to_days < date_to_days):

                        QMessageBox.critical(self, "BOMBrowser",
                            "The code dates (row=%d) are wider than the child id=%d ones"%(
                                row+1, cid))
                        return

        # check that the date range has a wider life than
        # any parents
        for (pid, pdate_from_days, pdate_to_days) in d.get_parent_dates_range_by_code_id(self._code_id):
            if (pdate_from_days < min_date_from_days or
                pdate_to_days > max_date_to_days):

                    QMessageBox.critical(self, "BOMBrowser",
                        "The code dates range are shorter than the parent id=%i one"%(
                            pid))
                    return

        if dates[0][3] != "" and dates[0][2] > dates[0][4]:
            QMessageBox.critical(self, "BOMBrowser",
                "Error in dates at row %d"%(row+1))
            return

        for i in range(1, row_cnt):
            if dates[i - 1][2] <= dates[i][2]:
                QMessageBox.critical(self, "BOMBrowser",
                    "Error in date row %d and %d"%(i, i+1))
                return

        if dates[0][3] == "":
            dates[0][4] = db.end_of_the_world

        # case where there is a prototype
        if len(dates) > 1 and dates[1][3] == "":
            dates[1][4] = db.prototype_date -1

        try:
            d.update_dates(dates)
        except Exception as e:
            utils.show_exception(msg="Error during the data saving\n" +
                    str(e))
            return

        QMessageBox.information(self, "BOMBrowser",
                "Data saved")

        self.accept()

    def _cancel(self):
        self.reject()

    def _populate(self):
        d = db.DB()
        data = d.get_dates_by_code_id3(self._code_id)

        self._table.clear()
        self._table.setSortingEnabled(False)
        #self._table.setSelectionBehavior(QTableView.SelectCell);
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionMode(self._table.SingleSelection)
        self._table.setColumnCount(6)
        self._table.setRowCount(len(data))
        self._table.setHorizontalHeaderLabels(["id", "Description",
            "Rev", "Iter", "From date", "To date"])

        row = 0
        for line in data:
            (code, descr, date_from_days, date_to_days,
                rid, rev, iter_) = line[:7]

            i = QTableWidgetItem(str(rid))
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            f = i.font()
            f.setItalic(True)
            i.setFont(f)
            self._table.setItem(row, 0, i)

            i = QTableWidgetItem(descr)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            i.setFont(f)
            self._table.setItem(row, 1, i)

            i = QTableWidgetItem(rev)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            i.setFont(f)
            self._table.setItem(row, 2, i)

            i = QTableWidgetItem(str(iter_))
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            i.setFont(f)
            self._table.setItem(row, 3, i)

            i = bbdate.BBDatesLineEdit(db.days_to_txt(date_from_days),
                                        allow_cmp=False,
                                        allow_prototype = row == 0)
            self._table.setCellWidget(row, 4, i)
            i.textChanged.connect(utils.Callable(
                    lambda *x:self._cell_changed(*x[1:])
                    , row, 4))

            if row != 0:
                i = QTableWidgetItem(db.days_to_txt(date_to_days))
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                i.setFont(f)
                self._table.setItem(row, 5, i)
            else:
                i = bbdate.BBDatesLineEdit(db.days_to_txt(date_to_days),
                                        allow_cmp=False,
                                        allow_prototype=False)
                self._table.setCellWidget(row, 5, i)

                if date_from_days == db.prototype_date:
                    self._table.cellWidget(row, 5).setReadOnly(True)

                i.textChanged.connect(utils.Callable(
                    lambda *x:self._cell_changed(*x[1:])
                    , row, 5))

            row += 1

        self.setWindowTitle("Edit dates: %s"%(code))
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        QApplication.instance().processEvents()
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def _get_table_cell(self, row, col):
        if col == 4 or (row == 0 and col == 5):
            return self._table.cellWidget(row, col)
        else:
            return self._table.item(row, col)

    def _cell_changed(self, row, col):
        # check the date from column
        # and check the date to in row 0 cell
        if col != 4 and not (col == 5 and row == 0):
            return

        if row == 0 and col == 4:
            if self._table.cellWidget(0, 4).text().upper() == "PROTOTYPE":
                self._table.cellWidget(0, 5).setText("")
                self._table.cellWidget(0, 5).setReadOnly(True)

                if self._table.rowCount() > 1:
                    self._table.item(1, 5).setText("")
                    return
            else:
                self._table.cellWidget(0, 5).setReadOnly(False)

        dt = self._get_table_cell(row, col).text()
        err = False

        if row == 0 and col == 5:
            if dt != "":
                try:
                    from_date = db.iso_to_days(dt)
                except:
                    err = True
                if not err:
                    err = self._get_table_cell(row, 4).text() > dt
        else:
            try:
                from_date = db.iso_to_days(dt)
            except:
                err = True

            if not err:
                if row > 0 and (self._get_table_cell(row -1 , col).text() <= dt):
                    err = True
                if ((row < self._table.rowCount() - 1) and
                    (self._get_table_cell(row +1 , col).text() >= dt)):
                        err = True

        if err:
            self._table.clearSelection()
            return

        if col == 4 and row < self._table.rowCount() - 1:
            to_date = from_date - 1
            to_date = db.days_to_iso(to_date)
            self._get_table_cell(row+1, col+1).setText(to_date)


class CopyFilesDialog(QDialog):
    def __init__(self,files, parent=None):
        super().__init__(parent=parent)

        l = QGridLayout()
        self.setLayout(l)

        self._table = QTableWidget()

        self._table.clear()
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        #self._table.setSelectionBehavior(QTableView.SelectRows);
        self._table.setAlternatingRowColors(True)
        #self._table.setSelectionMode(self._table.SingleSelection)

        self._table.setColumnCount(3)
        self._table.setRowCount(len(files))
        self._table.setHorizontalHeaderLabels(["Action", "Source", "Destination"])

        r = 0
        for act, src, dst in files:
            """i = QTableWidgetItem(act)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._table.setItem(r, 0, i)"""
            w = QComboBoxCList()
            w.addItem("Copy")
            w.addItem("Link")
            w.addItem("Ignore")
            w.setText(act)
            self._table.setCellWidget(r, 0, w)

            i = QTableWidgetItem(src)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._table.setItem(r, 1, i)

            i = QTableWidgetItem(dst)
            if act == "Link":
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._table.setItem(r, 2, i)

            w.currentTextChanged.connect(utils.Callable(
                lambda x, y, z: self._change_dest(y, z), w, i))

            r += 1

        self._table.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self._table.resizeColumnsToContents()

        l.addWidget(self._table, 1, 1, 1, 2)

        b = QPushButton("Ok")
        l.addWidget(b, 10, 1)
        b.clicked.connect(self.accept)

        b = QPushButton("Cancel")
        l.addWidget(b, 10, 2)
        b.clicked.connect(self.reject)

        self.setWindowTitle("Upload files window")

    def _change_dest(self, w, i):
        if w.text() == "Link":
            i.setFlags(Qt.NoItemFlags)
        else:
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)

    def get_results(self):
        res = []
        for r in range(self._table.rowCount()):
            line = []
            line.append(self._table.cellWidget(r, 0).text())
            line.append(self._table.item(r, 1).text())
            line.append(self._table.item(r, 2).text())
            res.append(line)
        return res


class DrawingTable(QTableWidget):

    rowChanged = Signal()

    _clipboard = []

    def __init__(self):
        QTableWidget.__init__(self)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(
            self._drawing_menu)

        self.setSelectionMode(self.ContiguousSelection)

        self.doubleClicked.connect(self._view_drawing)

    def _opt_copy_and_add_drawings(self, files):
        method = "none"
        if cfg.config().has_section("FILES_UPLOAD"):
            method = cfg.config()["FILES_UPLOAD"]["method"]

        if method == "simple":
            dst_dir = cfg.config()["FILES_UPLOAD"]["simple_destination_dir"]
            t = [("Copy", x, dst_dir) for x in files]

            files = self._copy_link_files(t)

        elif method == "regexp":
            sep = cfg.config()["FILES_UPLOAD"]["regexpmap_separator"]
            casesens = int(cfg.config()["FILES_UPLOAD"]["regexpmap_case_sensitive"])
            regtable = cfg.config()["FILES_UPLOAD"]["regexpmap_table"].split("\n")
            regtable = [x.strip().split(sep)
                        for x in regtable
                        if len(x.strip().split(sep)) in [2,3]]
            res = []
            flags = 0
            if not casesens:
                flags |= re.IGNORECASE
            for fn in files:
                for reg in regtable:
                    if re.search(reg[0], fn, flags):
                        if reg[1] == "Link":
                            res.append(("Link", fn, ""))
                        else:
                            dst = ""
                            if len(reg) > 2:
                                dst = reg[2]
                            res.append(("Copy", fn, dst))
                        break
                else:
                    res.append(("Link", fn, ""))

            files = self._copy_link_files(res)

        for f in files:
            self._add_filename_to_table(f)

    def _copy_link_files(self, src_files):
        d = CopyFilesDialog(src_files, parent=self)
        if not d.exec_():
            return []

        files = d.get_results()
        files_to_link = []
        for act, src, destdir in files:
            if act == "Ignore":
                continue
            if not os.path.exists(src):
                QMessageBox.critical(self, "BOMBrowser - error",
                        "File '" + src + "' doesn't exists.\nAbort.\n")
                return []
            if act == "Link":
                files_to_link.append(src)
                continue
            try:
                if not os.path.exists(destdir):
                    os.makedirs(destdir)
                newdest = shutil.copy(src, destdir)
                files_to_link.append(newdest)

            except Exception as e:
                QMessageBox.critical(self, "BOMBrowser - error",
                        "Cannot copy\n" +
                        "   " + src + " -> \n" +
                        "   " + destdir + "\nAbort.\n" +
                        "-"*30 + "\n" +
                        str(e) + "\n" +
                        "-"*30)
                return []

        return files_to_link

    def _drawing_menu(self, point):
        idxs = self.selectedIndexes()

        contextMenu = QMenu(self)
        m = contextMenu.addAction("View drawing")
        m.triggered.connect(self._view_drawing)
        m.setEnabled(len(idxs) > 0)
        m = contextMenu.addAction("Delete drawing")
        m.triggered.connect(self._delete_drawing)
        m.setEnabled(len(idxs) > 0)

        m = contextMenu.addAction("Add drawings link...")
        m.triggered.connect(self._link_drawing_with_dialog)
        m = contextMenu.addAction("Add drawings...")
        m.triggered.connect(self._add_drawing_with_dialog)

        contextMenu.addSeparator()

        m = contextMenu.addAction("Copy drawings lines")
        m.triggered.connect(self._copy_drawing)
        m.setEnabled(len(idxs) > 0)
        m = contextMenu.addAction("Paste drawings lines")
        m.triggered.connect(self._paste_drawing)
        m.setEnabled(len(DrawingTable._clipboard) > 0)

        contextMenu.exec_(self.viewport().mapToGlobal(point))

    def _copy_drawing(self):
        idxs = self.selectedIndexes()
        if len(idxs) == 0:
            return

        rows = list(set([idx.row() for idx in idxs]))

        data = []
        for row in rows:
            data.append(self.item(row, 1).text())

        DrawingTable._clipboard = data

    def _paste_drawing(self):
        if len(DrawingTable._clipboard) < 1:
            return

        for fn in DrawingTable._clipboard:
            self._add_filename_to_table(fn)

    def _view_drawing(self):
        idxs = self.selectedIndexes()
        if len(idxs) == 0:
            return

        rows = list(set([idx.row() for idx in idxs]))
        for r in rows:
            path = self.item(r, 1).text()
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _delete_drawing(self):
        idxs = self.selectedIndexes()
        if len(idxs) == 0:
            return

        rows = list(set([idx.row() for idx in idxs]))
        rows.sort(reverse=True)

        for row in rows:
            self.removeRow(row)

        self.rowChanged.emit()

    def _add_drawing_with_dialog(self):
        (fns, _) = QFileDialog.getOpenFileNames(self, "Select a file")
        if len(fns):
            self._opt_copy_and_add_drawings(fns)

    def _link_drawing_with_dialog(self):
        (fns, _) = QFileDialog.getOpenFileNames(self, "Select a file")
        for fn in fns:
            self._add_filename_to_table(fn)

    def _add_filename_to_table(self, fn):
        row = self.rowCount()
        self.setRowCount(row+1)
        self.setItem(row, 0, QTableWidgetItem(os.path.basename(fn)))
        self.setItem(row, 1, QTableWidgetItem(fn))
        self.rowChanged.emit()

    def add_drawings(self, fns):
        if len(fns):
            self._opt_copy_and_add_drawings(fns)

class QComboBoxCList(QComboBox):
    def __init__(self, parent_=None):
        QComboBox.__init__(self, parent=parent_)
        self._originalIndex = self.currentIndex()
    def text(self):
        i = self.currentIndex()
        return self.itemText(i)
    def setText(self, s):
        i = self.findText(s)
        if i >= 0:
            self.setCurrentIndex(i)
        self._originalIndex = self.currentIndex()
    def isModified(self):
        return self._originalIndex != self.currentIndex()
    def addItem(self, v):
        QComboBox.addItem(self, v)
        self._originalIndex = self.currentIndex()


class SelectFromList(QDialog):
    def __init__(self, parent, title, header, data):
        QDialog.__init__(self, parent)

        self.setWindowTitle(title)

        self._return_index = None

        grid = QGridLayout()
        self._table = QTableWidget()

        self._table.clear()
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QTableView.SelectRows);
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionMode(self._table.SingleSelection)

        if isinstance(header, list):
            ncol = len(header)
            #header = ["id"] + header
        else:
            ncol = 1
            header = [header]
            data = [[x] for x in data]
        self._table.setColumnCount(ncol)
        self._table.setRowCount(len(data))
        self._table.setHorizontalHeaderLabels(header)
        for nrow, line in enumerate(data):
            #line = ["%4d"%(nrow)] + line
            for c, v in enumerate(line):
                i = QTableWidgetItem(v)
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                if c == 0:
                    i.setData(Qt.UserRole, nrow)
                self._table.setItem(nrow, c, i)

        self._table.doubleClicked.connect(self.accept)
        self._table.itemSelectionChanged.connect(self._change_selection)

        self._table.selectRow(0)
        grid.addWidget(self._table, 0, 0, 1, 2)

        b = QPushButton("Close")
        b.clicked.connect(self._close)
        grid.addWidget(b, 10, 0)
        b = QPushButton("Select")
        b.clicked.connect(self.accept)
        grid.addWidget(b, 10, 1)

        self.setLayout(grid)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def _change_selection(self):
        idxs = self._table.selectedIndexes()
        if len(idxs) < 1:
            row = 0
        else:
            row = idxs[0].row()

        self._return_index = int(self._table.item(row, 0).data(Qt.UserRole))

    def _close(self):
        self._return_index = None
        self.reject()

    def getIndex(self):
        return self._return_index


class EditWindow(bbwindow.BBMainWindow):

    _clipboard = []

    def __init__(self, code_id, dt=None, parent=None):
        bbwindow.BBMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._code_id = code_id
        self._rid = None
        self._orig_revision = None
        self._descr_force_uppercase = cfg.config()["BOMBROWSER"]["description_force_uppercase"] != "0"
        self._case_sens = cfg.config()["BOMBROWSER"]["ignore_case_during_search"] == "0"
        self._dates_list_info = None
        self._children_modified = False
        self._drawing_modified = False
        self._gavals = cfg.get_gavalnames()

        self._init_gui()

        self._populate_dates_list_info()
        self._dates_list_change_index(0)
        if not dt is None:
            i = 0
            for row in self._dates_list_info:
                if row[2] == dt:
                    self._dates_list.setCurrentIndex(i)
                    break
                i += 1

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        files = set()
        for url in e.mimeData().urls():
            files.add(url.toLocalFile())
        self._drawings_table.add_drawings(list(files))

    def _populate_dates_list_info(self):
        d = db.DB()
        self._dates_list_info = d.get_dates_by_code_id3(self._code_id)
        assert(len(self._dates_list_info))

        self._dates_list.clear()
        for row in self._dates_list_info:

            (code, descr, date_from_days, date_to_days,
                rid, ver, iter_) = row

            self._dates_list.addItem("%s .. %s"%(
                db.days_to_txt(date_from_days),
                db.days_to_txt(date_to_days)))

        self._dates_list_last_index = 0

    def _make_gval_widget(self, type_):
        class PairLEWidget(QWidget):
            def __init__(self, le, w, parent_=None):
                QWidget.__init__(self, parent=parent_)
                l = QHBoxLayout()
                l.addWidget(le)
                l.addWidget(w)
                l.setMargin(0)
                self.setLayout(l)
                self._le = le

            def text(self):
                return self._le.text()
            def setText(self, s):
                return self._le.setText(s)

        if type_ == "file":
            le = QLineEdit()
            b = QPushButton("...")
            class Do:
                def __init__(self, le, parent):
                    self._le = le
                    self._parent = parent
                def __call__(self):
                    (fn, _) = QFileDialog.getOpenFileName(self._parent,
                        "Select a file")
                    if fn != "":
                        self._le.setText(fn)
                        self._le.setModified(True)
            b.clicked.connect(Do(le, self))
            return PairLEWidget(le, b)
        elif type_.startswith("list:"):
            le = QLineEdit()
            b = QComboBox()
            values =type_[5:].split(";")
            b.addItem("...")
            for i in values:
                b.addItem(i)
            class Do:
                def __init__(self, le, l):
                    self._le = le
                    self._list = l[:]
                def __call__(self, i):
                    if i < 1 or i > len(self._list):
                        return
                    self._le.setText(self._list[i-1])
                    self._le.setModified(True)
            b.currentIndexChanged.connect(Do(le, values))
            return PairLEWidget(le, b)
        elif type_.startswith("clist:"):
            b = QComboBoxCList()
            values =type_[6:].split(";")
            for i in values:
                b.addItem(i)
            return b
        elif type_.startswith("readonly"):
            w = QLineEdit()
            w.setEnabled(False)
            return w
        else:
            return QLineEdit()

    def _init_gui(self):

        self._create_menu()

        g = QGridLayout()

        g.addWidget(QLabel("RID"), 10, 10)
        self._rid_w = QLineEdit()
        self._rid_w.setDisabled(True)
        g.addWidget(self._rid_w, 10, 11)

        g.addWidget(QLabel("ID"), 10, 12)
        self._id = QLineEdit()
        self._id.setDisabled(True)
        g.addWidget(self._id, 10, 13)


        g.addWidget(QLabel("Code"), 11, 10)
        self._code = QLineEdit()
        g.addWidget(self._code, 11, 11)
        self._code.setDisabled(True)

        g.addWidget(QLabel("Rev"), 11, 12)
        self._ver = QLineEdit()
        g.addWidget(self._ver, 11, 13)

        g.addWidget(QLabel("Iter"), 12, 10)
        self._iter = QLineEdit()
        self._iter.setDisabled(True)
        g.addWidget(self._iter, 12, 11)

        g.addWidget(QLabel("Default unit"), 12, 12)
        self._unit = QLineEdit()
        g.addWidget(self._unit, 12, 13)

        g.addWidget(QLabel("Description"), 13, 10)
        self._descr = QLineEdit()
        g.addWidget(self._descr, 13, 11, 1, 3)

        hl = QHBoxLayout()
        g.addLayout(hl, 15, 10, 1, 4)

        hl.addWidget(QLabel("From/to date"))
        self._dates_list = QComboBox()
        hl.addWidget(self._dates_list)
        self._dates_list.currentIndexChanged.connect(self._dates_list_change_index)

        b = QPushButton("...")
        b.clicked.connect(self._change_dates)
        hl.addWidget(b)


        # generic properties

        qgb = QGroupBox("Generic properties")
        g.addWidget(qgb, 18, 10, 1, 4)

        qgbg = QGridLayout()
        qgb.setLayout(qgbg)

        self._gvals = []
        gvalnames = cfg.get_gvalnames2()
        i = 0
        row = 0
        for (seq, idx, gvalname, caption, type_) in gvalnames:
            qgbg.addWidget(QLabel(caption), row / 2, 10 + (row % 2) * 2)
            le = self._make_gval_widget(type_)
            qgbg.addWidget(le, row / 2, 11 + (row % 2) * 2)
            self._gvals.append((gvalname, le, idx))
            row += 1

        # TODO: add the properties

        qtab = QTabWidget()
        self._qtab = qtab
        g.addWidget(qtab, 30, 10, 1, 4)
        g.setRowStretch(30, 100)

        # children
        self._children_table = QTableWidget()

        self._children_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._children_table.customContextMenuRequested.connect(
            self._children_menu)

        w = QWidget()
        l = QGridLayout()
        w.setLayout(l)
        b = QPushButton("Top")
        b.clicked.connect(lambda : self._children_move_row("top"))
        l.addWidget(b, 10, 10)
        b = QPushButton("Up")
        b.clicked.connect(lambda : self._children_move_row("up"))
        l.addWidget(b, 11, 10)
        b = QPushButton("Down")
        b.clicked.connect(lambda : self._children_move_row("down"))
        l.addWidget(b, 12, 10)
        b = QPushButton("Bottom")
        b.clicked.connect(lambda : self._children_move_row("bottom"))
        l.addWidget(b, 13, 10)
        l.addWidget(self._children_table, 10, 20, 5, 1)
        l.setRowStretch(14, 100)
        qtab.addTab(w, "Children")

        # drawing
        self._drawings_table = DrawingTable() #QTableWidget()
        self._drawings_table.rowChanged.connect(self._update_drawing_row)
        qtab.addTab(self._drawings_table, "Drawings")

        hl = QHBoxLayout()

        b = QPushButton("Close")
        b.clicked.connect(self.close)
        hl.addWidget(b)
        hl.addStretch()
        b= QPushButton("Save...")
        b.clicked.connect(self._save_changes)
        hl.addWidget(b)

        g.addLayout(hl , 100, 10, 1, 4)

        self.setWindowTitle("Edit code")

        w = QWidget()
        w.setLayout(g)
        self.setCentralWidget(w)
        self.resize(1024, 768)

    def _form_is_changed(self):
        if self._children_modified:
            return True
        if self._drawing_modified:
            return True

        for qle in self.findChildren(QLineEdit):
            if qle.isModified():
                return True

        for qcb in self.findChildren(QComboBoxCList):
            if qcb.isModified():
                return True

    def closeEvent(self, event):
        if self._form_is_changed():
            ret = QMessageBox.question(self, "BOMBrowser",
                "The form was changed; do you want to save before closing  ?",
                QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                event.ignore()
                return
            if ret == QMessageBox.Yes:
                ret = self._save_changes()
                if ret != "OK":
                    event.ignore()
                    return

        bbwindow.BBMainWindow.closeEvent(self, event)
        event.accept()

    def _dates_list_change_index(self, i):
        if self._dates_list_info is None:
            return

        # TODO: check if some data are changed

        (code, descr, date_from_days, date_to_days,
            rid, ver, iter_) = self._dates_list_info[i]

        if self._form_is_changed():
            if self._dates_list_last_index == i:
                return

            ret = QMessageBox.question(self, "BOMBrowser",
                "The form was changed; do you want to save before changing date  ?",
                QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                self._dates_list.setCurrentIndex(self._dates_list_last_index)
                return
            if ret == QMessageBox.Yes:
                ret = self._save_changes()
                if ret != "OK":
                    self._dates_list.setCurrentIndex(self._dates_list_last_index)
                    return

        self._populate_table(rid)
        self._dates_list_last_index = i

    def _create_menu(self):
        mainMenu = self.menuBar()

        m = mainMenu.addMenu("File")
        a = QAction("Reload config", self)
        a.triggered.connect(utils.reload_config_or_warn)
        m.addAction(a)
        m.addSeparator()
        a = QAction("Close", self)
        a.setShortcut("Ctrl+Q")
        a.triggered.connect(self.close)
        m.addAction(a)
        a = QAction("Exit", self)
        a.triggered.connect(self._exit_app)
        m.addAction(a)

        m = mainMenu.addMenu("Edit")
        a = QAction("Delete item revision...", self)
        a.triggered.connect(self._delete_revision)
        m.addAction(a)
        a = QAction("Delete code...", self)
        a.triggered.connect(self._delete_code)
        m.addAction(a)
        #a = QAction("Promote a prototype...", self)
        #m.triggered.connect(lambda x: True)
        #m.addAction(a)

        il = importer.get_importer_list() + customize.get_edit_window_importer_list()
        if len(il):
            m = mainMenu.addMenu("Import")
            for (name, descr, callable_) in il:
                a = QAction("Import as '%s'..."%(descr), self)
                a.triggered.connect(utils.Callable(
                    self._import_from, name, callable_))
                m.addAction(a)

        self._windowsMenu = self.build_windows_menu(mainMenu)

        m = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : self._show_about(db.connection))
        m.addAction(a)

    def _import_from(self, name, callable_):

        bom = callable_()

        if bom is None:
            QMessageBox.critical(self, "BOMBrowser",
                "Cannot import data")
            return

        if 0 in bom:
            root = 0
        else:
            data = []
            for k in bom:
                descr = "N/A"
                if "descr" in bom[k]:
                    descr = str(bom[k]["descr"])
                data.append((str(k), descr))
            w = SelectFromList(self, "Select a code for import",
                ["CODE", "DESCR"], data)
            w.exec_()

            ret = w.getIndex()
            if ret is None:
                return

            root = data[ret][0]

        children = [(bom[root]["deps"][k]["code"],
                bom[root]["deps"][k]["qty"], bom[root]["deps"][k]["each"],
                bom[root]["deps"][k]["unit"],
                bom[root]["deps"][k]["ref"]) for k in bom[root]["deps"]]

        self._children_table.setSortingEnabled(False)

        nrow = len(children)
        delta = nrow - self._children_table.rowCount()

        if delta > 0:
            while delta > 0:
                self._children_table.insertRow(0)
                delta -= 1
        elif delta < 0:
            while delta < 0:
                self._children_table.removeRow(0)
                delta += 1
        assert(nrow - self._children_table.rowCount() == 0)

        gavals = ["" for x in range(db.gavals_count)]
        for (row, (code, qty, each, unit, ref)) in enumerate(children):

            self._children_populate_row(row, "-", code, "-", qty,
                                each, unit, ref, gavals)

        self._children_table.setSortingEnabled(True)

        if "descr" in bom[root]:
            self._descr.setText(bom[root]["descr"])
        if "unit" in bom[root]:
            self._unit.setText(bom[root]["unit"])

        for i in range(db.gvals_count):
            gvn = "gval%d"%(i+1)
            if not gvn in bom[root]:
                continue
            v = bom[root][gvn]
            if v is None:
                continue
            self._gvals[i][1].setText(v)

        self._qtab.setTabText(0, "Children (%d)"%(self._children_table.rowCount()))

    def _delete_code(self):
        if self._form_is_changed():
            ret = QMessageBox.question(self, "BOMBrowser",
                "The form was changed; do you want to continue to remove this code  ?")
            if ret != QMessageBox.Yes:
                return

        reply = QMessageBox.question(self, "BOMBrowser",
                        "Are you sure to delete the code ?")

        if reply != QMessageBox.Yes:
            return

        d = db.DB()
        try:
            ret = d.delete_code(self._code_id)

        except:
            utils.show_exception(msg="Error during deletion of code id=%d\n"%(self._code_id))
            return

        if ret == "HASPARENTS":
            QMessageBox.critical(self, "BOMBrowser",
                "Cannot delete code id=%d: it has parent(s)"%(self._code_id))
            return
        elif ret != "":
            QMessageBox.critical(self, "BOMBrowser",
                "Unknown error '%s'; cannot delete code id=%d"%(
                    ret, self._code_id))
            return


        QMessageBox.information(self, "BOMBrowser",
            "Code id=%d has been deleted"%(self._code_id))

        self.close()

    def _delete_revision(self):
        if self._form_is_changed():
            ret = QMessageBox.question(self, "BOMBrowser",
                "The form was changed; do you want to continue deleting this revision  ?")
            if ret != QMessageBox.Yes:
                return

        reply = QMessageBox.question(self, "BOMBrowser",
                        "Are you sure to delete the current code revision?")

        if reply != QMessageBox.Yes:
            return

        d = db.DB()
        try:
            ret = d.delete_code_revision(self._rid)
        except:
            utils.show_exception(msg="Error during deletion of code revision rid=%d\n"%(self._rid))
            return

        if ret == "ISALONE":
            QMessageBox.critical(self, "BOMBrowser",
                "Cannot delete code revision rid=%d: "%(self._rid) +
                "it is the last one; delete the code instead")
            return
        elif ret == "ONLYPROTOTYPE":
            QMessageBox.critical(self, "BOMBrowser",
                "Cannot delete code revision rid=%d: "%(self._rid) +
                "cannot remain only the prototype.")
            return
        elif ret != "":
            QMessageBox.critical(self, "BOMBrowser",
                "Unknown error '%s'; cannot delete code id=%d"%(
                    ret, self._code_id))
            return

        QMessageBox.information(self, "BOMBrowser",
            "Code revision rid=%d has been deleted"%(self._rid))

        self._populate_dates_list_info()
        self._dates_list_change_index(0)

    def _exit_app(self):
        ret = QMessageBox.question(self, "BOMBrowser", "Do you want to exit from the application ?")
        if ret == QMessageBox.Yes:
            sys.exit(0)

    def _change_dates(self):
        d = EditDates(int(self._id.text()), self)
        d.exec_()

        self._refresh_date()

    def _refresh_date(self):
        d = db.DB()
        data = d.get_code_by_rid(self._rid)

        self.setWindowTitle("Edit code: %s @ %s"%(
            data["code"], data["date_from"]))

        self._from_date_days = data["date_from_days"]
        self._to_date_days = data["date_to_days"]

        dates = d.get_dates_by_code_id3(self._code_id)
        for i, row in enumerate(dates):
            code, descr, date_from_days, date_to_days = row[:4]
            self._dates_list.setItemText(i, "%s .. %s"%(
                    db.days_to_txt(date_from_days),
                    db.days_to_txt(date_to_days)))

    def _mangle_path(self, path):
        if not os.path.exists(path):
            return path
        if os.path.dirname(path) == '':
            return path

        default_dirs = cfg.config()["FILES_UPLOAD"].get("default_dirs", "")
        default_dirs = [ x.strip()
                         for x in default_dirs.split("\n")
                         if (len(x.strip()) > 0 and 
                             os.path.exists(x.strip()) and
                             os.path.isdir(x.strip())) ]

        for dd in default_dirs:
            if os.path.samefile(os.path.dirname(path), dd):
                return os.path.basename(path)
        return path

    def _save_changes_prepare_data(self):
        d = db.DB()

        # gvals values
        gvals = ["" for i in range(db.gvals_count)]
        for i in range(len(self._gvals)):
            gvals[self._gvals[i][2]-1] = self._gvals[i][1].text()

        # drawings
        drawings = []
        drawings_set = set()
        for i in range(self._drawings_table.rowCount()):
            name = self._drawings_table.item(i, 0).text()
            path = self._drawings_table.item(i, 1).text()
            if name in drawings_set:
                return ("Duplicate name in drawings: row=%d"%(i + 1),
                            None)
            if path in drawings_set:
                return ("Duplicate path in drawings: row='%s'"%(i + 1), None)
            drawings_set.add(name)
            drawings_set.add(path)
            path = self._mangle_path(path)
            drawings.append((name, path))

        # TBD: check for loop
        codes_set = set()
        children = []

        for i in range(self._children_table.rowCount()):
            code_id = self._children_table.item(i, 1).text().strip()
            code = self._children_table.item(i, 2).text().strip()
            qty = self._children_table.item(i, 4).text().strip()
            each = self._children_table.item(i, 5).text().strip()
            unit = self._children_table.item(i, 6).text().strip()
            ref = self._children_table.item(i, 7).text().strip()

            gavals_values = ["" for i in range(db.gavals_count)]
            for c, idx, gvalname, name, type_ in self._gavals:
                #gavals_values[idx-1] = self._children_table.item(i, 8+c).text().strip()
                gavals_values[idx-1] = self._children_table.cellWidget(i, 8+c).text().strip()

            try:
                qty = float(qty)
            except:
                return ("Incorrect value 'Q.ty' in row %d (%s)'"%(i + 1, qty),
                            None)
            try:
                each = float(each)
            except:
                return ("Incorrect value 'Each' in row %d (%s)'"%(i + 1, each),
                            None)

            codes = d.get_codes_by_code(code, case_sensitive=self._case_sens)

            if codes is None or len(codes) == 0:
                return ("Invalid code '%s' in row %d'"%(code, i + 1),
                            None)

            if code in codes_set:
                return ("Duplicated code '%s' in row %d'"%(code, i + 1),
                            None)

            dates = d.get_dates_by_code_id3(code_id)
            min_date_from_days = min([x[2] for x in dates])
            max_date_to_days = max([x[3] for x in dates])

            if (self._from_date_days < min_date_from_days or
                self._to_date_days > max_date_to_days):

                    return ("Children code '%s' in row %d' has shorter life date"%(code, i + 1),
                            None)

            codes_set.add(code)

            children.append((code_id, qty, each, unit, ref, gavals_values))

        return (None, (gvals, drawings, children))

    def _save_changes(self):

        (err, data) = self._save_changes_prepare_data()
        if err:
            QMessageBox.critical(self, "BOMBrowser",
                "Cannot insert data, the error is:\n"+err)
            return "ERROR"

        (gvals, drawings, children) = data

        descr = self._descr.text()
        if self._descr_force_uppercase:
            descr = descr.upper()

        d = db.DB()

        try:
            d.update_by_rid2(self._rid, descr.strip(),
                self._ver.text(), self._unit.text(),
                gvals, drawings, children
            )
        except:
            utils.show_exception(msg="Error during the data saving\n")
            return "ERROR"

        QMessageBox.information(self, "BOMBrowser",
                "Data saved")
        self._populate_table(self._rid)

        return "OK"

    def _children_populate_row(self, row, child_id, code, descr, qty,
                                each, unit, ref, gvls):
        i = QTableWidgetItem("%03d"%(row+1))
        i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        f = i.font()
        f.setItalic(True)
        i.setFont(f)
        self._children_table.setItem(row, 0, i)

        i = QTableWidgetItem(str(child_id))
        i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        i.setFont(f)
        self._children_table.setItem(row, 1, i)

        i = QTableWidgetItem(descr)
        i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        i.setFont(f)
        self._children_table.setItem(row, 3, i)

        self._children_table.setItem(row, 4, QTableWidgetItem(str(qty)))
        self._children_table.setItem(row, 5, QTableWidgetItem(str(each)))

        self._children_table.setItem(row, 7, QTableWidgetItem(ref))

        # after 1 and 3 because if we change 'code', 1 or 3 depends by code
        # and _children_cell_changed override these
        self._children_table.setItem(row, 2, QTableWidgetItem(code))

        if not unit is None and len(unit) > 0:
            # if unit is valid, override the code default one
            self._children_table.setItem(row, 6, QTableWidgetItem(unit))

        for c, idx, gvalname, name, type_ in self._gavals:
            txt = gvls[idx - 1]
            # TBD: set a more appropriate item
            #w = QTableWidgetItem()
            w = self._make_gval_widget(type_)
            w.setText(txt)
            self._children_table.setCellWidget(row, 8+c, w)

    def _populate_children(self, children):
        try:
            self._children_table.cellChanged.disconnect()
        except:
            pass

        labels = [
            "Seq",
            "Code id",
            "Code",
            "Description",
            "Q.ty", "Each", "Unit",
            "Ref"]
        labels.extend([
            name for c, idx, gvalname, name, value in self._gavals
        ])

        self._children_table.clear()
        self._children_table.setSortingEnabled(True)
        self._children_table.setSelectionBehavior(QTableView.SelectRows);
        self._children_table.setAlternatingRowColors(True)
        self._children_table.setSelectionMode(QTableView.ContiguousSelection)
        self._children_table.setColumnCount(len(labels))
        self._children_table.setRowCount(len(children))

        self._children_table.setHorizontalHeaderLabels(labels)
        self._children_table.setSortingEnabled(False)

        row = 0
        for (child_id, code, descr, qty, each, unit, ref, *gvls) in children:
            self._children_populate_row(row, child_id, code, descr, qty,
                                            each, unit, ref, gvls)
            row += 1

        self._children_table.setSortingEnabled(True)
        self._children_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        QApplication.instance().processEvents()
        self._children_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._children_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self._children_table.cellChanged.connect(self._children_cell_changed)


    def _populate_table(self, rid):
        self._rid = rid
        d = db.DB()

        data = d.get_code_by_rid(self._rid)

        self.setWindowTitle("Edit code: %s @ %s"%(
            data["code"], data["date_from"]))

        self._rid_w.setText(str(self._rid))
        self._id.setText(str(data["id"]))
        self._code.setText(data["code"])
        self._descr.setText(data["descr"])
        self._ver.setText(data["ver"])
        self._orig_revision = data["ver"]
        self._iter.setText(str(data["iter"]))
        self._unit.setText(data["unit"])
        self._from_date_days = data["date_from_days"]
        self._to_date_days = data["date_to_days"]

        # add the properties
        for i in range(len(self._gvals)):
            self._gvals[i][1].setText(data[self._gvals[i][0]])

        # children

        children = list(d.get_children_by_rid(self._rid))
        self._populate_children(children)
        # drawings

        drawings = list(d.get_drawings_by_rid(self._rid))
        self._drawings_table.clear()
        self._drawings_table.horizontalHeader().setStretchLastSection(True)
        self._drawings_table.setSortingEnabled(True)
        self._drawings_table.setSelectionBehavior(QTableView.SelectRows);
        self._drawings_table.setAlternatingRowColors(True)
        self._drawings_table.setColumnCount(2)
        self._drawings_table.setRowCount(len(drawings))
        self._drawings_table.setHorizontalHeaderLabels(["Name", "Path"])

        row = 0
        for (name, path) in drawings:
            path = utils.find_filename(path)
            i = QTableWidgetItem(name)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._drawings_table.setItem(row, 0, i)
            i = QTableWidgetItem(path)
            i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self._drawings_table.setItem(row, 1, i)
            row += 1
        self._drawings_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

        self._children_modified = False
        self._qtab.setTabText(0, "Children (%d)"%(self._children_table.rowCount()))
        self._update_drawing_row()
        self._drawing_modified = False

    def _children_cell_changed(self, row, col):
        self._children_modified = True
        table = self._children_table

        def table_set_text(c, v):
            i = table.item(row, c)
            if i is None:
                table.setItem(row, c, QTableWidgetItem(str(v)))
            else:
                i.setText(str(v))

        if col == 2:
            d = db.DB()
            i = table.item(row, 2)
            codes = d.get_codes_by_code(i.text(), case_sensitive=self._case_sens)

            if codes is None or len(codes) == 0:
                table.clearSelection()
                i.setBackground(QColor.fromRgb(255, 252, 187))
                return
            i.setBackground(table.item(row, 0).background())

            (id_, code, descr, ver, iter_, default_unit) = codes[0]
            table_set_text(1, id_)
            table_set_text(3, descr)
            table_set_text(6, default_unit)

            return
        elif col == 4 or col == 5:
            i = table.item(row, col)
            try:
                v = float(i.text())
                i.setBackground(table.item(row, 0).background())
            except:
                table.clearSelection()
                i.setBackground(QColor.fromRgb(255, 252, 187))
            return

    def _children_menu(self, point):
        contextMenu = QMenu(self)
        m = contextMenu.addAction("Insert row before")
        m.triggered.connect(self._children_insert_before)

        idxs = self._children_table.selectedIndexes()

        m = contextMenu.addAction("Insert row after")
        m.triggered.connect(self._children_insert_after)
        m.setEnabled(len(idxs) > 0)
        m = contextMenu.addAction("Delete row")
        m.triggered.connect(self._children_delete)
        m.setEnabled(len(idxs) > 0)
        contextMenu.addSeparator()
        m = contextMenu.addAction("Search code ...")
        m.triggered.connect(self._children_search_code)
        m.setEnabled(len(idxs) > 0)
        contextMenu.addSeparator()

        m = contextMenu.addAction("Copy lines")
        m.triggered.connect(self._children_copy)
        m.setEnabled(len(idxs) > 0)
        m = contextMenu.addAction("Paste lines")
        m.triggered.connect(self._children_paste)
        m.setEnabled(len(EditWindow._clipboard) >0)

        contextMenu.addSeparator()

        if len(idxs) > 0:
            row = idxs[0].row()
            code_id = None
            code = None
            try:
                code_id = int(self._children_table.item(row, 1).text())
                code = self._children_table.item(row, 2).text()
            except:
                pass

            if not code_id is None and not code is None:
                # sometime the code_id doesn't exist
                codecontextmenu.generate_codes_context_menu(code_id=code_id,
                    menu = contextMenu, parent=self)


        contextMenu.exec_(self._children_table.viewport().mapToGlobal(point))

    def _children_copy(self):
        idxs = self._children_table.selectedIndexes()
        selected_rows = list(set([idx.row() for idx in idxs]))
        selected_rows.sort()
        data = []
        for row in selected_rows:
            line = ['n/a']
            for c in range(1, self._children_table.columnCount()):
                    if c >= 8:
                        line.append(self._children_table.cellWidget(row, c).text())
                    else:
                        line.append(self._children_table.item(row, c).text())
            data.append(line)

        EditWindow._clipboard = data

    def _children_paste(self):

        if len(EditWindow._clipboard) < 1:
            return

        self._children_modified = True
        self._children_table.setSortingEnabled(False)

        try:
            self._children_table.cellChanged.disconnect()
        except:
            pass

        idxs = self._children_table.selectedIndexes()
        if len(idxs):
            row = idxs[0].row()
        else:
            row = 0

        gavals = ["" for x in range(db.gavals_count)]
        for line in EditWindow._clipboard:
            self._children_table.insertRow(row)
            self._children_populate_row(row, "", "", "", "1",
                                        "1", "NR", "", gavals)
            for c in range(1, self._children_table.columnCount()):
                    if c >= 8:
                        self._children_table.cellWidget(row, c).setText(line[c])
                    else:
                        self._children_table.item(row, c).setText(line[c])
            row += 1

        for row in range(self._children_table.rowCount()):
            self._children_table.item(row, 0).setText("%03d"%(row+1))

        self._children_table.setSortingEnabled(True)
        self._children_table.cellChanged.connect(self._children_cell_changed)

    def _children_move_row(self, where):

        idxs = self._children_table.selectedIndexes()
        if len(idxs) < 1:
            return
        self._children_modified = True

        nrow = self._children_table.rowCount()

        self._children_table.setSortingEnabled(False)

        try:
            self._children_table.cellChanged.disconnect()
        except:
            pass

        selected_rows = list(set([idx.row() for idx in idxs]))
        max_row = max(selected_rows)
        min_row = min(selected_rows)
        selected_rows_count = len(selected_rows)

        if where == "top":
            target_row = 0
        elif where == "bottom":
            target_row = nrow
        elif where == "up":
            target_row = min_row - 1
        elif where == "down":
            target_row = max_row + 2

        if target_row < 0:
            return

        data_after = []
        data_before = []
        data_moved = []
        for r in range(0, nrow):
            line = ['n/a']
            for c in range(1, self._children_table.columnCount()):
                    if c >= 8:
                        line.append(self._children_table.cellWidget(r, c).text())
                    else:
                        line.append(self._children_table.item(r, c).text())
            if r in selected_rows:
                data_moved.append(line)
            elif r < target_row:
                data_before.append(line)
            else:
                data_after.append(line)

        r = 0
        for r, line in enumerate(data_before + data_moved + data_after):
            for c in range(1, self._children_table.columnCount()):
                    if c >= 8:
                        self._children_table.cellWidget(r, c).setText(line[c])
                    else:
                        self._children_table.item(r, c).setText(line[c])

        for row in range(self._children_table.rowCount()):
            self._children_table.item(row, 0).setText("%03d"%(row+1))

        self._children_table.sortByColumn(0,Qt.AscendingOrder)

        self._children_table.setSortingEnabled(True)

        self._children_table.clearSelection()
        selectionModel = self._children_table.selectionModel()
        start_sel = len(data_before)
        end_sel = start_sel + len(data_moved) - 1
        index1 = self._children_table.model().index(start_sel, 0)
        index2 = self._children_table.model().index(end_sel, 2)
        itemSelection = QItemSelection(index1, index2)
        selectionModel.select(itemSelection,
                QItemSelectionModel.Rows | QItemSelectionModel.Select)

        self._children_table.scrollTo(index2)
        self._children_table.scrollTo(index1)

        self._children_table.cellChanged.connect(self._children_cell_changed)

    def _children_insert_before(self, offset=0):
        self._children_modified = True
        idxs = self._children_table.selectedIndexes()
        count = len(set([idx.row() for idx in idxs]))
        if count < 1:
            row = 0
            count = 1
        else:
            row = idxs[0].row()
            if offset > 0:
                row += count
        if row < 0:
            row = 0
        elif row >= self._children_table.rowCount():
            row = self._children_table.rowCount()
        self._children_table.setSortingEnabled(False)

        gavals = ["" for x in range(db.gavals_count)]
        while count > 0:
            self._children_table.insertRow(row)
            self._children_populate_row(row, "", "", "", "1",
                                        "1", "NR", "", gavals)
            count -= 1

        for row in range(self._children_table.rowCount()):
            self._children_table.item(row, 0).setText("%03d"%(row+1))
        self._children_table.sortByColumn(0,Qt.AscendingOrder)
        self._children_table.setSortingEnabled(True)

        self._qtab.setTabText(0, "Children (%d)"%(self._children_table.rowCount()))

    def _children_insert_after(self):
        self._children_modified = True
        self._children_insert_before(+1)

    def _children_delete(self):
        self._children_modified = True
        idxs = self._children_table.selectedIndexes()
        if len(idxs) < 1:
            return

        rows = list(set([idx.row() for idx in idxs]))
        rows.sort(reverse=True)

        self._children_table.setSortingEnabled(False)
        for row in rows:
            self._children_table.removeRow(row)

        for row in range(self._children_table.rowCount()):
            self._children_table.item(row, 0).setText("%03d"%(row+1))
        self._children_table.sortByColumn(0,Qt.AscendingOrder)
        self._children_table.setSortingEnabled(True)
        self._qtab.setTabText(0, "Children (%d)"%(self._children_table.rowCount()))

    def _children_search_code(self):
        idxs = self._children_table.selectedIndexes()
        if len(idxs) < 1:
            return

        d = SelectCode(self)
        if not d.exec_():
            return
        code = d.getCode()
        if code is None:
            return

        row = idxs[0].row()
        self._children_table.item(row, 2).setText(code)
        self._children_modified = True

    def _update_drawing_row(self):
        self._qtab.setTabText(1, "Drawings list (%d)"%(self._drawings_table.rowCount()))
        self._drawing_modified = True


def edit_code_by_code_id(code_id, dt=None):
    w = EditWindow(code_id, dt)
    w.show()
    return w

def test_edit():
    app = QApplication(sys.argv)
    w = EditWindow(code_id=2007) # top assembly
    w.show()
    sys.exit(app.exec_())

def test_edit_dates():
    app = QApplication(sys.argv)
    w = EditDates(6264, None) # top assembly
    w.exec_()

def test_select_list():
    app = QApplication(sys.argv)
    w = SelectFromList(None, "Prova", "Elenco1",
        ["a", "b", "c", "prova-d"])
    w.exec_()

    print(w.getIndex())

def test_select_list2():
    app = QApplication(sys.argv)
    w = SelectFromList(None, "Prova", ["Elenco1", "colb"],
        [["a", "b"], ["z", "prova-d"]])
    w.exec_()

    print(w.getIndex())

def test_upload_files():
    app = QApplication(sys.argv)
    d = CopyFilesDialog([
        ("Copy", "src-1", "dst-1"),
        ("Copy", "src-2", "dst-2"),
        ("Link", "src-2", ""),
    ])
    r = d.exec_()
    print(d.get_results())

if __name__ == "__main__":
    test_upload_files()
