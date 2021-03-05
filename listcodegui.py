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

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar
from PySide2.QtWidgets import QSplitter, QTableView, QLabel
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QFrame
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QHeaderView, QMenu
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PySide2.QtCore import Qt, QAbstractTableModel, QEvent

import db, asmgui, codegui, diffgui, utils, editcode
import copycodegui, selectdategui



class CodesWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("BOMBrowser - Codes list")
        self._main_data = [
            ("Code", "code"),
            ("Version", "ver"),
            ("Iteration", "iter"),
            ("Description", "descr"),
            ("Unit", "unit"),
        ]

        self._copy_info = ""
        self._code_id = None

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

        closeAction = QAction("Close", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.triggered.connect(self.close)
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+X")
        exitAction.triggered.connect(self._exit_app)
        fileMenu.addAction(closeAction)
        fileMenu.addAction(exitAction)

        editMenu = mainMenu.addMenu("Edit")
        copyAction = QAction("Copy", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self._copy_info_action)
        editMenu.addAction(copyAction)

        self._windowsMenu = mainMenu.addMenu("Window")
        self._windowsMenu.aboutToShow.connect(self._build_windows_menu)

        self._build_windows_menu()

        helpMenu = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : utils.about(self))
        helpMenu.addAction(a)

    def _new_code(self):
        editcode.newCodeWindow()

    def _build_windows_menu(self):
        utils.build_windows_menu(self._windowsMenu, self, codes_list = False)
        return

    def _exit_app(self):
        ret = QMessageBox.question(self, "BOMBrowser", "Do you want to exit from the application ?")
        if ret == QMessageBox.Yes:
            sys.exit(0)

    def _copy_info_action(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(self._copy_info, mode=cb.Clipboard)

    def _init_gui(self):
        self._create_menu()
        # create toolbar
        self._create_statusbar()


        vb = QVBoxLayout()
        hr = QHBoxLayout()

        hr.addWidget(QLabel("Code:"))
        self._code_search = QLineEdit()
        self._code_search.returnPressed.connect(self._search)
        hr.addWidget(self._code_search)

        hr.addWidget(QLabel("Description:"))
        self._descr_search = QLineEdit()
        self._descr_search.returnPressed.connect(self._search)
        hr.addWidget(self._descr_search)


        b = QPushButton("Search")
        b.clicked.connect(self._search)
        b.setDefault(True)
        hr.addWidget(b)

        vb.addLayout(hr)
        self._splitter = QSplitter()
        vb.addWidget(self._splitter)
        vb.setStretch(1, 100)

        self._table = QTableView()
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QTableView.SelectRows);
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionMode(self._table.SingleSelection)
        #self._table.clicked.connect(self._table_clicked)
        model = self.TableModel([], ["id", "Code", "Version", "Iteration", "Description"])
        self._table.setModel(model)
        self._splitter.addWidget(self._table)
        self._splitter.addWidget(QWidget())
        self._splitter.setSizes([700, 1024-700])

        w = QWidget()
        w.setLayout(vb)
        self.setCentralWidget(w)

        self._table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._tree_context_menu)

    def _tree_context_menu(self, point):
        contextMenu = QMenu(self)
        showAssembly = contextMenu.addAction("Show assembly ...")
        showAssembly.triggered.connect(self._show_assembly)
        whereUsed = contextMenu.addAction("Where used ...")
        whereUsed.triggered.connect(self._show_where_used)
        validWhereUsed = contextMenu.addAction("Valid where used ...")
        validWhereUsed.triggered.connect(self._show_valid_where_used)
        contextMenu.addSeparator()
        reviseCode = contextMenu.addAction("Revise/copy code ...")
        reviseCode.triggered.connect(self._revise_code)
        contextMenu.addSeparator()
        doDiff1 = contextMenu.addAction("Diff from")
        doDiff1.triggered.connect(self._set_diff_from)
        doDiff2 = contextMenu.addAction("Diff to")
        doDiff2.triggered.connect(self._set_diff_to)

        contextMenu.exec_(self._table.viewport().mapToGlobal(point))

    def _get_code_and_date(self):
        w = selectdategui.SelectDate(self._code_id, self)
        ret = w.exec_()
        if not ret:
            return (0, 0, 0, 0)

        (code, date_from, date_to) = w.get_result()
        return(self._code_id, code, date_from, date_to)

    def _set_diff_from(self):
        if not self._code_id:
            QApplication.beep()

        d = db.DB()
        if not d.is_assembly(self._code_id):
            QApplication.beep()
            QMessageBox.critical(self, "BOMBrowser", "The item is not an assembly")
            return

        code_id, code, date_from, date_to = self._get_code_and_date()
        if code == 0:
            return

        diffgui.set_from(code_id, code, date_from)

    def _set_diff_to(self):
        if not self._code_id:
            QApplication.beep()

        d = db.DB()
        if not d.is_assembly(self._code_id):
            QApplication.beep()
            QMessageBox.critical(self, "BOMBrowser", "The item is not an assembly")
            return

        code_id, code, date_from, date_to = self._get_code_and_date()
        if code == 0:
            return

        diffgui.set_to(code_id, code, date_from)

    def _show_assembly(self):
        if not self._code_id:
            QApplication.beep()

        d = db.DB()
        if not d.is_assembly(self._code_id):
            QApplication.beep()
            QMessageBox.critical(self, "BOMBrowser", "The item is not an assembly")
            return

        code_id, code, date_from, descr = self._get_code_and_date()
        if code == 0:
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        w = asmgui.AssemblyWindow(None) #self)
        w.show()
        data = d.get_bom_by_code_id2(self._code_id, date_from)
        w.populate(*data)
        QApplication.restoreOverrideCursor()

    def _revise_code(self):
        if not self._code_id:
            QApplication.beep()

        copycodegui.revise_copy_code(self._code_id, self)

    def _show_where_used(self):
        if not self._code_id:
            QApplication.beep()
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        d = db.DB()
        data = d.get_where_used_from_id_code(self._code_id)
        #pprint.pprint(data)
        if len(data[1]) == 1:
            QApplication.restoreOverrideCursor()
            QApplication.beep()
            QMessageBox.critical(self, "BOMBrowser", "The item is not in an assembly")
            return

        #w = asmgui.WhereUsedWindow(self)
        w = asmgui.WhereUsedWindow(None)
        w.show()
        w.populate(*data)
        QApplication.restoreOverrideCursor()

    def _show_valid_where_used(self):
        asmgui.valid_where_used(self._code_id, self)

    class TableModel(QAbstractTableModel):
        def __init__(self, data, header):
            QAbstractTableModel.__init__(self)
            self._data = data
            self._header = header
            self._swap_matrix = {
                0:0,
                1:1,
                2:3,
                3:4,
                4:2
            }

        def data(self, index, role):
            if role == Qt.DisplayRole:
                # See below for the nested-list data structure.
                # .row() indexes into the outer list,
                # .column() indexes into the sub-list
                c = self._swap_matrix[index.column()]
                return self._data[index.row()][c]

        def sort(self, col, direction):
            self.layoutAboutToBeChanged.emit()
            self._data.sort(key=lambda row : row[col],
                reverse = direction == Qt.SortOrder.AscendingOrder)
            self.layoutChanged.emit()

        def rowCount(self, index):
            # The length of the outer list.
            return len(self._data)

        def columnCount(self, index):
            # The following takes the first sub-list, and returns
            # the length (only works if all rows are an equal length)
            return len(self._header)

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self._header[col]

    def _search(self):
        d = db.DB()
        if self._code_search.text() != "" and self._descr_search.text():
            ret = d.get_codes_by_like_code_and_descr(
                self._code_search.text(), self._descr_search.text())
        elif self._code_search.text() == "":
            ret = d.get_codes_by_like_descr(self._descr_search.text())
        else:
            ret = d.get_codes_by_like_code(self._code_search.text())

        if not ret or len(ret) == 0:
            self._my_statusbar.showMessage("0 results", 3000)
            QApplication.beep()
            return

        self._copy_info = "\t".join(["id", "Code", "Version", "Iteration", "Description"])
        self._copy_info += "\n"
        self._copy_info += "\n".join(["\t".join(map(str, row[:5])) for row in ret])
        model = self.TableModel(
        	ret,
        	["id", "Code", "Version", "Iteration", "Description"])
        self._table.setModel(model)
        self._table.selectionModel().selectionChanged.connect(self._table_clicked)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


    def _table_clicked(self, to, from_):

        if len(to.indexes()) < 1:
            return

        row = to.indexes()[0].row()

        class IDX:
            def row(self):
                return self._r
            def column(self):
                return self._c
            def __init__(self, r, c):
                self._r = r
                self._c = c
        idx = IDX(row, 0)
        id_ = self._table.model().data(idx, Qt.DisplayRole)

        self._update_metadata(id_)

    def _update_metadata(self, id_):

        self._code_id = id_

        scrollarea = QScrollArea()
        scrollarea.setWidget(codegui.CodeWidget(id_, self))
        #scrollarea.setWidgetResizable(False)
        self._splitter.replaceWidget(1, scrollarea)
        self._grid_widget = scrollarea



