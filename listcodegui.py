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

import sys, configparser

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar
from PySide2.QtWidgets import QSplitter, QTableView, QLabel
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QFrame
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QHeaderView, QMenu, QTableWidget, QTableWidgetItem
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PySide2.QtCore import Qt, QAbstractTableModel, QEvent, Signal, QPoint

import db, asmgui, codegui, diffgui, utils, editcode
import copycodegui, selectdategui, cfg

class CodesWidget(QWidget):
    #tableCustomContextMenuRequested = Signal(QPoint)
    rightMenu = Signal(QPoint)
    doubleClicked = Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._copy_info = ""
        self._code_id = None
        self._code = None
        self._descr_force_uppercase = cfg.config()["BOMBROWSER"].get("description_force_uppercase", "1")
        self._code_force_uppercase = cfg.config()["BOMBROWSER"].get("code_force_uppercase", "1")
        self._data = dict()

        self._init_gui()

    def _init_gui(self):

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

        self._table = QTableWidget()

        self._table.clear()
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QTableView.SelectRows);
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionMode(self._table.SingleSelection)
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["id", "Code", "Description", "Rev", "Iter"])
        self._splitter.addWidget(self._table)
        self._splitter.addWidget(QWidget())
        self._splitter.setSizes([700, 1024-700])

        self.setLayout(vb)

        self._table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._tree_context_menu)
        self._table.doubleClicked.connect(self.doubleClicked)

    def _tree_context_menu(self, point):
        self.rightMenu.emit(self._table.viewport().mapToGlobal(point))

    def _search(self):
        d = db.DB()
        cs = self._code_search.text()
        ds = self._descr_search.text()
        if self._descr_force_uppercase == "1":
                ds = ds.upper()
        if self._code_force_uppercase == "1":
                cs = cs.upper()

        if cs != "" and ds:
            ret = d.get_codes_by_like_code_and_descr(cs, ds)
        elif cs == "":
            ret = d.get_codes_by_like_descr(ds)
        else:
            ret = d.get_codes_by_like_code(cs)

        if not ret or len(ret) == 0:
            QApplication.beep()
            return

        self._copy_info = "\t".join(["id", "Code", "Rev", "Iteration", "Description"])
        self._copy_info += "\n"
        self._copy_info += "\n".join(["\t".join(map(str, row[:5])) for row in ret])

        self._table.setSortingEnabled(False)
        self._table.clear()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["id", "Code", "Description", "Rev", "Iter"])
        self._table.setRowCount(len(ret))
        row = 0
        for data in ret:
            (id_, code, ver, iter_, descr) = data[:5]
            c = 0
            for txt in (id_, code, ver, iter_, descr):
                i = QTableWidgetItem(str(txt))
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self._table.setItem(row, c, i)
                c += 1
            row += 1
        self._table.setSortingEnabled(True)
        self._table.selectionModel().selectionChanged.connect(self._table_clicked)
        if len(ret) > 0:
            self._table.selectRow(0)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def _table_clicked(self, to, from_):

        if len(to.indexes()) < 1:
            return

        row = to.indexes()[0].row()

        id_ = int(self._table.item(row, 0).text())
        code = self._table.item(row, 1).text()

        self._update_metadata(id_, code)

    def _update_metadata(self, id_, code):

        self._code_id = id_
        self._code = code

        scrollarea = QScrollArea()
        scrollarea.setWidget(codegui.CodeWidget(id_, self))

        # this to avoid unexpected crash
        w = self._splitter.widget(1)

        self._splitter.replaceWidget(1, scrollarea)
        self._grid_widget = scrollarea

    def getCodeId(self):
        return self._code_id

    def getCode(self):
        return self._code

    def getTableText(self):
        return self._copy_info

class CodesWindow(utils.BBMainWindowNotClose):
    def __init__(self, parent=None):
        utils.BBMainWindowNotClose.__init__(self, parent)
        self.setWindowTitle(utils.window_title + " - Codes list")

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
        exitAction.triggered.connect(self._exit_app)
        fileMenu.addAction(closeAction)
        fileMenu.addAction(exitAction)

        editMenu = mainMenu.addMenu("Edit")
        copyAction = QAction("Copy table values", self)
        copyAction.triggered.connect(self._copy_info_action)
        editMenu.addAction(copyAction)

        self._windowsMenu = mainMenu.addMenu("Windows")
        self._windowsMenu.aboutToShow.connect(self._build_windows_menu)

        self._build_windows_menu()

        helpMenu = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : utils.about(self))
        helpMenu.addAction(a)

    def _build_windows_menu(self):
        utils.build_windows_menu(self._windowsMenu, self)
        return

    def _exit_app(self):
        ret = QMessageBox.question(self, "BOMBrowser", "Do you want to exit from the application ?")
        if ret == QMessageBox.Yes:
            sys.exit(0)

    def _copy_info_action(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(self._codes_widget.getTableText(), mode=cb.Clipboard)

    def _init_gui(self):
        self._create_menu()
        # create toolbar
        self._create_statusbar()

        self._codes_widget = CodesWidget(self)

        self.setCentralWidget(self._codes_widget)

        self._codes_widget.rightMenu.connect(self._tree_context_menu)

    def _tree_context_menu(self, point):
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
        doDiff1 = contextMenu.addAction("Diff from")
        doDiff1.triggered.connect(self._set_diff_from)
        doDiff2 = contextMenu.addAction("Diff to")
        doDiff2.triggered.connect(self._set_diff_to)

        contextMenu.exec_(point)

    def _get_code_and_date(self):
        w = selectdategui.SelectDate(self._codes_widget.getCodeId(), self)
        ret = w.exec_()
        if not ret:
            return (0, 0, 0, 0)

        (code, date_from, date_to) = w.get_result()
        return(self._codes_widget.getCodeId(), code, date_from, date_to)

    def _set_diff_from(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        diffgui.set_from(self._codes_widget.getCodeId(), self)

    def _set_diff_to(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        diffgui.set_to(self._codes_widget.getCodeId(), self)

    def _show_latest_assembly(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        asmgui.show_latest_assembly(self._codes_widget.getCodeId())

    def _show_assembly(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        asmgui.show_assembly(self._codes_widget.getCodeId(), self)

    def _revise_code(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        copycodegui.revise_copy_code(self._codes_widget.getCodeId(), self)

    def _edit_code(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        editcode.edit_code_by_code_id(self._codes_widget.getCodeId())

    def _show_where_used(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        asmgui.where_used(self._codes_widget.getCodeId(), self)

    def _show_valid_where_used(self):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        asmgui.valid_where_used(self._codes_widget.getCodeId(), self)

