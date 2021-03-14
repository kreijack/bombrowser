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

import sys, configparser, webbrowser, os

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar
from PySide2.QtWidgets import QSplitter, QTableView, QLabel, QTableWidgetItem
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication, QFileDialog
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QFrame, QSplitter
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QDialog
from PySide2.QtWidgets import QHeaderView, QMenu, QGroupBox, QTableWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem, QColor

from PySide2.QtCore import Qt, QAbstractTableModel, QEvent, QTimer

import db, asmgui, codegui, diffgui, utils, listcodegui, jdutil, cfg

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

        self.setWindowTitle("BOMBrowser - Search code")

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

    def _save(self):

        d = db.DB()

        dates = []
        row_cnt = self._table.rowCount()
        min_date_from_days = None
        max_date_to_days = None
        for row in range(row_cnt):
            rid = int(self._table.item(row, 0).text())
            date_from = self._table.item(row, 4).text()
            date_to = self._table.item(row, 5).text()

            try:
                date_from_days = db.iso_to_days(date_from)
                if date_to != '':
                    date_to_days = db.iso_to_days(date_to)
                else:
                    date_to_days = db.end_of_the_world
            except:
                QMessageBox.critical(self, "BOMBrowser",
                    "Error in date format row %d"%(row+1))
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

        try:
            d.update_dates(dates)
        except db.DBException as e:
            QMessageBox.critical(self, "BOMBrowser",
                    "Error during the data saving\n" +
                    e.args[0])
            return

        QMessageBox.information(self, "BOMBrowser",
                "Data saved")

        self.accept()

    def _cancel(self):
        self.reject()

    def _populate(self):

        d = db.DB()
        data = d.get_dates_by_code_id2(self._code_id)

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
            (code, descr, date_from, date_from_days, date_to, date_to_days,
                rid, rev, iter_) = line[:9]

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

            i = QTableWidgetItem(date_from)
            self._table.setItem(row, 4, i)

            i = QTableWidgetItem(date_to)
            if row != 0:
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                i.setFont(f)
            self._table.setItem(row, 5, i)

            row += 1

        self.setWindowTitle("BOMBrowser - Edit dates: %s"%(code))
        self._table.cellChanged.connect(self._cell_changed)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

    def _cell_changed(self, row, col):
        # check the date from column
        # and check the date to in row 0 cell
        if col != 4 and not (col == 5 and row == 0):
            return

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

class EditWindow(QMainWindow):
    def __init__(self, rid, parent=None):
        QMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._rid = rid
        self._orig_revision = None
        self._descr_force_uppercase = cfg.config()["BOMBROWSER"].get("description_force_uppercase", "1")
        self._code_force_uppercase = cfg.config()["BOMBROWSER"].get("code_force_uppercase", "1")

        self._init_gui()

        self._populate_table()

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

        hl.addWidget(QLabel("From date"))
        self._from_date = QLineEdit()
        self._from_date.setDisabled(True)
        hl.addWidget(self._from_date)

        hl.addWidget(QLabel("To date"))
        self._to_date = QLineEdit()
        self._to_date.setDisabled(True)
        hl.addWidget(self._to_date)

        b = QPushButton("...")
        b.clicked.connect(self._change_dates)
        hl.addWidget(b)


        # generic properties

        qgb = QGroupBox("Generic properties")
        g.addWidget(qgb, 18, 10, 1, 4)

        qgbg = QGridLayout()
        qgb.setLayout(qgbg)

        self._gvals = []
        gvalnames = cfg.config().get("BOMBROWSER", "gvalnames").split(",")
        i = 0
        row = 0
        for i in range(len(gvalnames)):
            name = gvalnames[i]
            le = QLineEdit()
            qgbg.addWidget(QLabel(name), row / 2, 10 + (row % 2) * 2)
            qgbg.addWidget(le, row / 2, 11 + (row % 2) * 2)
            self._gvals.append((name, le))
            row += 1


        # TODO: add the properties

        splitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)
        g.addWidget(splitter, 30, 10, 1, 4)
        g.setRowStretch(30, 100)
        # children

        qgb = QGroupBox("Children")
        splitter.addWidget(qgb)

        qgbg = QGridLayout()
        qgb.setLayout(qgbg)

        self._children_table = QTableWidget()
        qgbg.addWidget(self._children_table, 1, 10, 1, 2)
        self._children_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._children_table.customContextMenuRequested.connect(
            self._children_menu)

        # drawing

        qgb = QGroupBox("Drawings list")
        splitter.addWidget(qgb)

        qgbg = QGridLayout()
        qgb.setLayout(qgbg)

        self._drawings_table = QTableWidget()
        qgbg.addWidget(self._drawings_table, 1, 10, 1, 2)
        self._drawings_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._drawings_table.customContextMenuRequested.connect(
            self._drawing_menu)


        b = QPushButton("Close")
        b.clicked.connect(self.close)
        g.addWidget(b, 100, 10)

        self._update_btn = QPushButton("Save...")
        self._update_btn.clicked.connect(self._save_changes)
        g.addWidget(self._update_btn, 100, 13)

        self.setWindowTitle("BOMBrowser - Edit code")

        w = QWidget()
        w.setLayout(g)
        self.setCentralWidget(w)
        self.resize(1024, 768)

    def _create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        self._windowsMenu = mainMenu.addMenu("Windows")

        self._windowsMenu.aboutToShow.connect(self._build_windows_menu)

        closeAction = QAction("Close", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.triggered.connect(self.close)
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self._exit_app)

        fileMenu.addAction(closeAction)
        fileMenu.addAction(exitAction)

        self._build_windows_menu()

        helpMenu = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : utils.about(self))
        helpMenu.addAction(a)

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

        d = db.DB()
        data = d.get_code_from_rid(self._rid)

        self.setWindowTitle("BOMBrowser - Edit code: %s @ %s"%(
            data["code"], data["date_from"]))

        self._from_date.setText(data["date_from"])
        self._to_date.setText(data["date_to"])
        self._from_date_days = data["date_from_days"]
        self._to_date_days = data["date_to_days"]

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


            dates = d.get_dates_by_code_id2(code_id)
            min_date_from_days = min([x[3] for x in dates])
            max_date_to_days = max([x[5] for x in dates])

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
            return

        (gvals, drawings, children) = data

        descr = self._descr.text()
        if self._descr_force_uppercase == "1":
            descr = descr.upper()

        d = db.DB()

        try:
            d.update_by_rid(self._rid, descr
                , self._ver.text(), self._unit.text(),
                *gvals, drawings, children
            )
        except db.DBException as e:
            QMessageBox.critical(self, "BOMBrowser",
                    "Error during the data saving\n" +
                    e.args[0])
            return

        QMessageBox.information(self, "BOMBrowser",
                "Data saved")

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

        self._children_table.setItem(row, 2, QTableWidgetItem(code))

        i = QTableWidgetItem(descr)
        i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        i.setFont(f)
        self._children_table.setItem(row, 3, i)

        self._children_table.setItem(row, 4, QTableWidgetItem(str(qty)))
        self._children_table.setItem(row, 5, QTableWidgetItem(str(each)))
        self._children_table.setItem(row, 6, QTableWidgetItem(unit))
        self._children_table.setItem(row, 7, QTableWidgetItem(ref))

    def _populate_table(self):
        d = db.DB()

        data = d.get_code_from_rid(self._rid)

        self.setWindowTitle("BOMBrowser - Edit code: %s @ %s"%(
            data["code"], data["date_from"]))

        self._rid_w.setText(str(self._rid))
        self._id.setText(str(data["id"]))
        self._code.setText(data["code"])
        self._descr.setText(data["descr"])
        self._ver.setText(data["ver"])
        self._orig_revision = data["ver"]
        self._iter.setText(str(data["iter"]))
        self._unit.setText(data["unit"])
        self._from_date.setText(data["date_from"])
        self._to_date.setText(data["date_to"])
        self._from_date_days = data["date_from_days"]
        self._to_date_days = data["date_to_days"]

        # add the properties
        for i in range(len(self._gvals)):
            self._gvals[i][1].setText(data["gval%d"%(i+1)])

        # children

        try:
            self._children_table.cellChanged.disconnect()
        except:
            pass

        children = list(d.get_children_by_rid(self._rid))
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

    def _children_cell_changed(self, row, col):
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
        insertAfter = contextMenu.addAction("Insert row after")
        insertAfter.triggered.connect(self._children_insert_after)
        insertBefore = contextMenu.addAction("Insert row before")
        insertBefore.triggered.connect(self._children_insert_before)
        delete = contextMenu.addAction("Delete row")
        delete.triggered.connect(self._children_delete)
        searchCode = contextMenu.addAction("Search code ...")
        searchCode.triggered.connect(self._children_search_code)

        contextMenu.exec_(self._children_table.viewport().mapToGlobal(point))
        pass

    def _children_insert_before(self, offset=0):
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

    def _children_insert_after(self):
        self._children_insert_before(+1)

    def _children_delete(self):
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
            webbrowser.open(path)

    def _delete_drawing(self):
        idxs = self._drawings_table.selectedIndexes()
        if len(idxs) == 0:
            return

        rows = list(set([idx.row() for idx in idxs]))
        rows.sort(reverse=True)

        for row in rows:
            self._drawings_table.removeRow(row)

    def _add_drawing(self):
        (fn, _) = QFileDialog.getOpenFileName(self, "Select a file")
        if fn == "":
            return
        row = self._drawings_table.rowCount()
        self._drawings_table.setRowCount(row+1)
        self._drawings_table.setItem(row, 0, QTableWidgetItem(os.path.basename(fn)))
        self._drawings_table.setItem(row, 1, QTableWidgetItem(fn))


def edit_code_by_code_id(code_id):
    d = db.DB()
    dates = d.get_dates_by_code_id2(code_id)
    assert(len(dates))
    (code, descr, date_from, date_from_days, date_to, date_to_days,
        rid, ver, iter_) = dates[0][:9]

    w = EditWindow(rid =rid)
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

if __name__ == "__main__":
    test_edit()
