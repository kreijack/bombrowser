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

import sys, configparser, os, pprint, traceback

from PySide2.QtWidgets import QComboBox
from PySide2.QtWidgets import QSplitter, QTableView, QLabel, QTableWidgetItem
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication, QFileDialog
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QSplitter
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QDialog, QTabWidget
from PySide2.QtWidgets import QHeaderView, QMenu, QGroupBox, QTableWidget
from PySide2.QtGui import QColor, QDesktopServices

from PySide2.QtCore import Qt, QUrl

import db, asmgui, codegui, diffgui, utils, listcodegui, jdutil, cfg
import importer, copycodegui
from utils import catch_exception

class SelectCode(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self._init_gui()

    def _init_gui(self):
        grid = QGridLayout()

        self._search_widget = listcodegui.CodesWidget()
        self._search_widget.doubleClicked.connect(self.accept)
        grid.addWidget(self._search_widget, 10, 1, 1, 3)

        b = QPushButton("Cancel")
        b.clicked.connect(self.reject)
        grid.addWidget(b, 20, 1)

        b = QPushButton("OK")
        b.clicked.connect(self.accept)
        grid.addWidget(b, 20, 3)

        self.setLayout(grid)

        self.setWindowTitle(utils.window_title + " - Search code")
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
            date_from = self._table.item(row, 4).text().upper()
            date_to = self._table.item(row, 5).text()

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
        except:
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
        self._table.horizontalHeader().setStretchLastSection(True)
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

            i = QTableWidgetItem(db.days_to_txt(date_from_days))
            self._table.setItem(row, 4, i)

            i = QTableWidgetItem(db.days_to_txt(date_to_days))
            if row != 0:
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                i.setFont(f)
            self._table.setItem(row, 5, i)

            if date_from_days == db.prototype_date:
                # the row is prototype: we can't change anything
                #self._table.item(row, 4).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                #self._table.item(row, 4).setFont(f)
                self._table.item(row, 5).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self._table.item(row, 5).setFont(f)

            row += 1

        self.setWindowTitle(utils.window_title + " - Edit dates: %s"%(code))
        self._table.cellChanged.connect(self._cell_changed)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

    def _cell_changed(self, row, col):
        # check the date from column
        # and check the date to in row 0 cell
        if col != 4 and not (col == 5 and row == 0):
            return

        if row == 0 and col == 4:
            if self._table.item(0, 4).text().upper() == "PROTOTYPE":
            #if col == 5:
                # phantom change due to the rows below, ignore it
                #return

                self._table.item(0, 5).setText("")
                self._table.item(0, 5).setBackground(
                    self._table.item(row, 0).background())
                self._table.item(0, 5).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                if self._table.rowCount() > 1:
                    self._table.item(1, 5).setText("")
                    self._table.item(1, 5).setBackground(
                        self._table.item(row, 0).background())

                if row == 0 and col == 4:
                    self._table.item(row, col).setBackground(
                        self._table.item(row, 0).background())
                    return
            else:
                self._table.item(0, 5).setFlags(Qt.ItemIsSelectable |
                    Qt.ItemIsEnabled | Qt.ItemIsEditable)


        dt = self._table.item(row, col).text()
        err = False

        if row == 0 and col == 5:
            if dt != "":
                try:
                        from_date = db.iso_to_days(dt)
                except:
                    err = True
                if not err:
                    err = self._table.item(row, 4).text() > dt
        else:
            try:
                    from_date = db.iso_to_days(dt)
            except:
                err = True

            if not err:
                if row > 0 and (self._table.item(row -1 , col).text() < dt):
                    err = True
                if ((row < self._table.rowCount() - 1) and
                    (self._table.item(row +1 , col).text() > dt)):
                        err = True

        if err:
            self._table.clearSelection()
            self._table.item(row, col).setBackground(
                QColor.fromRgb(255, 252, 187))
            return

        self._table.item(row, col).setBackground(
            self._table.item(row, 0).background())

        if col == 4 and row < self._table.rowCount() - 1:
            to_date = from_date - 1
            to_date = db.days_to_iso(to_date)
            self._table.item(row+1, col+1).setText(to_date)


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


class EditWindow(utils.BBMainWindow):
    def __init__(self, code_id, dt=None, parent=None):
        utils.BBMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._code_id = code_id
        self._rid = None
        self._orig_revision = None
        self._descr_force_uppercase = cfg.config()["BOMBROWSER"].get("description_force_uppercase", "1")
        self._code_force_uppercase = cfg.config()["BOMBROWSER"].get("code_force_uppercase", "1")
        self._dates_list_info = None
        self._children_modified = False
        self._drawing_modified = False

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
        gvalnames = cfg.get_gvalnames()
        i = 0
        row = 0
        for name in gvalnames:
            t = cfg.get_gvalnames_type(name)
            le = QLineEdit()
            qgbg.addWidget(QLabel(name), row / 2, 10 + (row % 2) * 2)
            if t == "file":
                w = QHBoxLayout()
                w.addWidget(le)
                b = QPushButton("...")
                w.addWidget(b)
                class Do:
                    def __init__(self, le, parent):
                        self._le = le
                        self._parent = parent
                    def __call__(self):
                        (fn, _) = QFileDialog.getOpenFileName(self._parent,
                            "Select a file")
                        if fn != "":
                            self._le.setText(fn)
                b.clicked.connect(Do(le, self))
                qgbg.addLayout(w, row / 2, 11 + (row % 2) * 2)
            elif t.startswith("list:"):
                w = QHBoxLayout()
                w.addWidget(le)
                b = QComboBox()
                values =t[5:].split(";")
                b.addItem("...")
                for i in values:
                    b.addItem(i)
                class Do:
                    def __init__(self, le, l):
                        self._le = le
                        self._list = l[:]
                    def __call__(self, i):
                        if i < 1 or i >= len(self._list):
                            return
                        self._le.setText(self._list[i])
                b.currentIndexChanged.connect(Do(le, values))
                w.addWidget(b)
                qgbg.addLayout(w, row / 2, 11 + (row % 2) * 2)
            else:
                qgbg.addWidget(le, row / 2, 11 + (row % 2) * 2)


            self._gvals.append((name, le))
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
        self._drawings_table = QTableWidget()
        qtab.addTab(self._drawings_table, "Drawings")
        self._drawings_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._drawings_table.customContextMenuRequested.connect(
            self._drawing_menu)

        b = QPushButton("Close")
        b.clicked.connect(self._close)
        g.addWidget(b, 100, 10)

        self._update_btn = QPushButton("Save...")
        self._update_btn.clicked.connect(self._save_changes)
        g.addWidget(self._update_btn, 100, 13)

        self.setWindowTitle(utils.window_title + " - Edit code")

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

    def _close(self):
        if self._form_is_changed():
            ret = QMessageBox.question(self, "BOMBrowser",
                "The form was changed; do you want to close this window without saving  ?")
            if ret != QMessageBox.Yes:
                return
        self.close()

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
                "The form was changed; do you want to change date before saving data  ?")
            if ret != QMessageBox.Yes:
                self._dates_list.setCurrentIndex(self._dates_list_last_index)
                return

        self._populate_table(rid)
        self._dates_list_last_index = i

    def _create_menu(self):
        mainMenu = self.menuBar()

        m = mainMenu.addMenu("File")
        a = QAction("Close", self)
        a.setShortcut("Ctrl+Q")
        a.triggered.connect(self._close)
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

        il = importer.get_importer_list()
        if len(il):
            m = mainMenu.addMenu("Import")
            for (name, descr, callable_) in il:
                a = QAction("Import as '%s'..."%(descr), self)
                a.triggered.connect(utils.Callable(
                    self._import_from, name, callable_))
                m.addAction(a)

        self._windowsMenu = mainMenu.addMenu("Windows")
        self._windowsMenu.aboutToShow.connect(self._build_windows_menu)
        self._build_windows_menu()

        m = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : utils.about(self, db.connection))
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
            data = list([[k, bom[k]["descr"]] for k in bom])
            w = SelectFromList(self, "Select a code for import",
                ["CODE", "DESCR"], data)
            w.exec_()

            ret = w.getIndex()
            if ret is None:
                return

            root = data[ret][0]

        pprint.pprint(bom[root])

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

        for (row, (code, qty, each, unit, ref)) in enumerate(children):

            self._children_populate_row(row, "-", code, "-", qty,
                                each, unit, ref)

        self._children_table.setSortingEnabled(True)

        if root != 0:
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

    def _delete_code(self):
        if self._form_is_changed():
            ret = QMessageBox.question(self, "BOMBrowser",
                "The form was changed; do you want to continue without saving  ?")
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
                "The form was changed; do you want to continue without saving  ?")
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

    def _build_windows_menu(self):
        utils.build_windows_menu(self._windowsMenu, self)
        return

    def _change_dates(self):
        d = EditDates(int(self._id.text()), self)
        d.exec_()

        self._refresh_date()

    def _refresh_date(self):
        d = db.DB()
        data = d.get_code_by_rid(self._rid)

        self.setWindowTitle(utils.window_title + " - Edit code: %s @ %s"%(
            data["code"], data["date_from"]))

        self._from_date_days = data["date_from_days"]
        self._to_date_days = data["date_to_days"]

        dates = d.get_dates_by_code_id3(self._code_id)
        for i, row in enumerate(dates):
            code, descr, date_from_days, date_to_days = row[:4]
            self._dates_list.setItemText(i, "%s .. %s"%(
                    db.days_to_txt(date_from_days),
                    db.days_to_txt(date_to_days)))

    def _save_changes_prepare_data(self):
        d = db.DB()

        # gvals values
        gvals = ["" for i in range(db.gvals_count)]
        for i in range(len(self._gvals)):
            gvals[i] = self._gvals[i][1].text()

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
            drawings.append((name, path))

        # TBD: check for loop
        codes_set = set()
        children = []
        for i in range(self._children_table.rowCount()):
            code_id = self._children_table.item(i, 1).text()
            code = self._children_table.item(i, 2).text()
            qty = self._children_table.item(i, 4).text()
            each = self._children_table.item(i, 5).text()
            unit = self._children_table.item(i, 6).text()
            ref = self._children_table.item(i, 7).text()

            try:
                qty = float(qty)
            except:
                return ("Incorrect value 'Q.ty' in row %d (%s)'"%(i + 1, qty),
                            None)
            try:
                each = float(each)
            except:
                return ("Incorrect value 'Each' in row %d (%s)'"%(i + 1, qty),
                            None)

            codes = d.get_codes_by_code(code)

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

            children.append((code_id, qty, each, unit, ref))

        return (None, (gvals, drawings, children))

    def _save_changes(self):

        (err, data) = self._save_changes_prepare_data()
        if err:
            QMessageBox.critical(self, "BOMBrowser",
                "Cannot insert data, the error is:\n"+err)
            return "ERROR"

        (gvals, drawings, children) = data

        descr = self._descr.text()
        if self._descr_force_uppercase == "1":
            descr = descr.upper()

        d = db.DB()

        try:
            d.update_by_rid2(self._rid, descr
                , self._ver.text(), self._unit.text(),
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
                                each, unit, ref):
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
        self._children_table.setItem(row, 6, QTableWidgetItem(unit))
        self._children_table.setItem(row, 7, QTableWidgetItem(ref))

        # after 1,3  and 6 because if we change 'code', 1,3 or 6  may be changed
        self._children_table.setItem(row, 2, QTableWidgetItem(code))

    def _populate_children(self, children):
        try:
            self._children_table.cellChanged.disconnect()
        except:
            pass

        self._children_table.clear()
        self._children_table.horizontalHeader().setStretchLastSection(True)
        self._children_table.setSortingEnabled(True)
        self._children_table.setSelectionBehavior(QTableView.SelectRows);
        self._children_table.setAlternatingRowColors(True)
        self._children_table.setSelectionMode(self._drawings_table.SingleSelection)
        self._children_table.setColumnCount(8)
        self._children_table.setRowCount(len(children))
        self._children_table.setHorizontalHeaderLabels([
            "Seq",
            "Code id",
            "Code",
            "Description",
            "Q.ty", "Each", "Unit",
            "Ref"])
        self._children_table.setSortingEnabled(False)

        row = 0
        for (child_id, code, descr, qty, each, unit, ref) in children:
            self._children_populate_row(row, child_id, code, descr, qty,
                                            each, unit, ref)
            row += 1

        self._children_table.setSortingEnabled(True)
        self._children_table.cellChanged.connect(self._children_cell_changed)
        self._children_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

    def _populate_table(self, rid):
        self._rid = rid
        d = db.DB()

        data = d.get_code_by_rid(self._rid)

        self.setWindowTitle(utils.window_title + " - Edit code: %s @ %s"%(
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
            self._gvals[i][1].setText(data["gval%d"%(i+1)])

        # children

        children = list(d.get_children_by_rid(self._rid))
        self._populate_children(children)
        # drawings

        drawings = list(d.get_drawings_by_code_id(self._rid))
        self._drawings_table.clear()
        self._drawings_table.horizontalHeader().setStretchLastSection(True)
        self._drawings_table.setSortingEnabled(True)
        self._drawings_table.setSelectionBehavior(QTableView.SelectRows);
        self._drawings_table.setAlternatingRowColors(True)
        self._drawings_table.setSelectionMode(self._drawings_table.SingleSelection)
        self._drawings_table.setColumnCount(2)
        self._drawings_table.setRowCount(len(drawings))
        self._drawings_table.setHorizontalHeaderLabels(["Name", "Path"])

        row = 0
        for (name, path) in drawings:
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
        self._drawing_modified = False
        self._qtab.setTabText(0, "Children (%d)"%(self._children_table.rowCount()))
        self._qtab.setTabText(1, "Drawings list (%d)"%(self._drawings_table.rowCount()))

    def _children_cell_changed(self, row, col):
        self._children_modified = True
        table = self._children_table
        if col == 2:
            d = db.DB()
            i = table.item(row, 2)
            if self._code_force_uppercase == "1":
                i.setText(i.text().upper())
            codes = d.get_codes_by_code(i.text())

            if codes is None or len(codes) == 0:
                table.clearSelection()
                i.setBackground(QColor.fromRgb(255, 252, 187))
                return
            i.setBackground(table.item(row, 0).background())

            (id_, code, descr, ver, iter_, default_unit) = codes[0]
            table.item(row, 1).setText(str(id_))
            table.item(row, 3).setText(str(descr))
            table.item(row, 6).setText(str(default_unit))
            #code change
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
        m = contextMenu.addAction("Insert row after")
        m.triggered.connect(self._children_insert_after)
        m = contextMenu.addAction("Delete row")
        m.triggered.connect(self._children_delete)
        contextMenu.addSeparator()
        m = contextMenu.addAction("Search code ...")
        m.triggered.connect(self._children_search_code)
        contextMenu.addSeparator()
        m = contextMenu.addAction("Show latest assembly ...")
        m.triggered.connect(lambda : self._children_do("latest_assembly"))
        m = contextMenu.addAction("Where used...")
        m.triggered.connect(lambda : self._children_do("where_used"))
        m = contextMenu.addAction("Valid where used...")
        m.triggered.connect(lambda : self._children_do("valid_where_used"))
        m = contextMenu.addAction("Show assembly by date...")
        m.triggered.connect(lambda : self._children_do("by_date_assembly"))
        m = contextMenu.addAction("Show current assembly...")
        m.triggered.connect(lambda : self._children_do("current_assembly"))
        m = contextMenu.addAction("Show prototype assembly ...")
        m.triggered.connect(lambda : self._children_do("prototype_assembly"))
        contextMenu.addSeparator()
        m = contextMenu.addAction("Copy / revise code ...")
        m.triggered.connect(lambda : self._children_do("copy_revise"))
        m = contextMenu.addAction("Edit code ...")
        m.triggered.connect(lambda : self._children_do("edit"))

        contextMenu.exec_(self._children_table.viewport().mapToGlobal(point))
        pass

    def _children_do(self, cmd):

        idxs = self._children_table.selectedIndexes()
        if len(idxs) < 1:
            return
        row = idxs[0].row()

        code_id = int(self._children_table.item(row, 1).text())
        code = self._children_table.item(row, 2).text()

        if cmd == "edit":
            edit_code_by_code_id(code_id)
        elif cmd == "latest_assembly":
            asmgui.show_latest_assembly(code_id)
        elif cmd == "by_date_assembly":
            asmgui.show_assembly(code_id, self)
        elif cmd == "current_assembly":
            asmgui.show_assembly_by_date(code_id, self._from_date_days)
        elif cmd == "prototype_assembly":
            asmgui.show_proto_assembly(code_id)
        elif cmd == "where_used":
            asmgui.where_used(code_id)
        elif cmd == "valid_where_used":
            asmgui.valid_where_used(code_id)
        elif cmd == "copy_revise":
            copycodegui.revise_copy_code(code_id, self)

    def _children_move_row(self, where):

        idxs = self._children_table.selectedIndexes()
        if len(idxs) < 1:
            return
        self._children_modified = True

        nrow = self._children_table.rowCount()

        row = idxs[0].row()

        if where == "top":
            target_row = 0
        elif where == "bottom":
            target_row = nrow - 1
        elif where == "up":
            target_row = row - 1
        elif where == "down":
            target_row = row + 1

        if row == target_row or target_row < 0 or target_row >= nrow:
            return

        self._children_table.setSortingEnabled(False)

        try:
            self._children_table.cellChanged.disconnect()
        except:
            pass

        for c in range(1, self._children_table.columnCount()):
            tmp = self._children_table.item(row, c).text()
            self._children_table.item(row, c).setText(
                self._children_table.item(target_row, c).text())
            self._children_table.item(target_row, c).setText(tmp)

        for row in range(self._children_table.rowCount()):
            self._children_table.item(row, 0).setText("%03d"%(row+1))

        self._children_table.sortByColumn(0,Qt.AscendingOrder)

        self._children_table.setSortingEnabled(True)

        self._children_table.selectRow(target_row)
        self._children_table.cellChanged.connect(self._children_cell_changed)

    def _children_insert_before(self, offset=0):
        self._children_modified = True
        idxs = self._children_table.selectedIndexes()
        if len(idxs) < 1:
            row = 0
        else:
            row = idxs[0].row() + offset
        if row < 0:
            row = 0
        elif row >= self._children_table.rowCount():
            row = self._children_table.rowCount()
        self._children_table.setSortingEnabled(False)
        self._children_table.insertRow(row)

        self._children_populate_row(row, "", "", "", "1",
                                        "1", "NR", "")

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

        row = idxs[0].row()

        self._children_table.setSortingEnabled(False)
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

    def _drawing_menu(self, point):
        contextMenu = QMenu(self)
        viewDrawing = contextMenu.addAction("View drawing")
        viewDrawing.triggered.connect(self._view_drawing)
        deleteDrawing = contextMenu.addAction("Delete drawing")
        deleteDrawing.triggered.connect(self._delete_drawing)
        deleteDrawing = contextMenu.addAction("Add drawing ...")
        deleteDrawing.triggered.connect(self._add_drawing)

        contextMenu.exec_(self._drawings_table.viewport().mapToGlobal(point))

    def _view_drawing(self):
        idxs = self._drawings_table.selectedIndexes()
        if len(idxs) == 0:
            return

        for idx in idxs:
            r = idx.row()
            path = self._drawings_table.item(r, 1).text()
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _delete_drawing(self):
        idxs = self._drawings_table.selectedIndexes()
        if len(idxs) == 0:
            return
        self._drawing_modified = True

        rows = list(set([idx.row() for idx in idxs]))
        rows.sort(reverse=True)

        for row in rows:
            self._drawings_table.removeRow(row)

        self._qtab.setTabText(1, "Drawings list (%d)"%(self._drawings_table.rowCount()))

    def _add_drawing(self):
        (fn, _) = QFileDialog.getOpenFileName(self, "Select a file")
        if fn == "":
            return
        self._drawing_modified = True

        row = self._drawings_table.rowCount()
        self._drawings_table.setRowCount(row+1)
        self._drawings_table.setItem(row, 0, QTableWidgetItem(os.path.basename(fn)))
        self._drawings_table.setItem(row, 1, QTableWidgetItem(fn))
        self._qtab.setTabText(1, "Drawings list (%d)"%(self._drawings_table.rowCount()))

def edit_code_by_code_id(code_id, dt=None):
    w = EditWindow(code_id, dt)
    w.show()
    return w




def test_edit():
    app = QApplication(sys.argv)
    w = EditWindow(rid=2007) # top assembly
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

if __name__ == "__main__":
    test_select_list2()
