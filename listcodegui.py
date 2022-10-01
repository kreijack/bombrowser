"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021 Goffredo Baroncelli <kreijack@inwind.it>

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

from PySide2.QtWidgets import QScrollArea, QStatusBar, QActionGroup
from PySide2.QtWidgets import QSplitter, QTableView, QLabel
from PySide2.QtWidgets import QWidget, QApplication, QStackedWidget
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QHeaderView, QMenu, QTableWidget, QTableWidgetItem

from PySide2.QtCore import Qt, Signal, QPoint

import db, codegui, bbwindow
import cfg, searchrevisiongui, codecontextmenu

class CodesListWidget(QWidget):
    #tableCustomContextMenuRequested = Signal(QPoint)
    rightMenu = Signal(QPoint)
    doubleClicked = Signal()
    emitResult = Signal(int)

    def __init__(self, parent=None, bom=None):
        QWidget.__init__(self, parent)

        self._bom = bom
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
        #self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QTableView.SelectRows);
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionMode(self._table.SingleSelection)
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["id", "Code", "Description", "Rev", "Iter"])
        self._splitter.addWidget(self._table)

        self._codes_widget = codegui.CodesWidget()
        scrollarea = QScrollArea()
        scrollarea.setWidget(self._codes_widget)
        scrollarea.setWidgetResizable(True)
        self._splitter.addWidget(scrollarea)

        self._splitter.setSizes([700, 1024-700])

        self.setLayout(vb)

        self._table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._tree_context_menu)
        self._table.doubleClicked.connect(self.doubleClicked)

    def _tree_context_menu(self, point):
        self.rightMenu.emit(self._table.viewport().mapToGlobal(point))

    def _search(self):
        cs = self._code_search.text()
        ds = self._descr_search.text()
        if self._descr_force_uppercase == "1":
                ds = ds.upper()
        if self._code_force_uppercase == "1":
                cs = cs.upper()

        if self._bom:
                ret = []
                for k, v in self._bom.items():
                    if ((cs == "" or cs in v["code"]) and
                        (ds == "" or ds in v["descr"])):
                            ret.append((v["id"], v["code"], v["descr"], v["ver"], v["iter"]))
        else:
                d = db.DB()
                ret = d.get_codes_by_like_code_and_descr(cs, ds)

        if not ret or len(ret) == 0:
            QApplication.beep()
            self.emitResult.emit(0)
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
        QApplication.instance().processEvents()
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.emitResult.emit(len(ret))

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

        self._codes_widget.populate(id_)

    def getCodeId(self):
        return self._code_id

    def getCode(self):
        return self._code

    def getTableText(self):
        return self._copy_info

class CodesWindow(bbwindow.BBMainWindow):
    def __init__(self, parent=None, bom=None, bomdesc=''):
        bbwindow.BBMainWindow.__init__(self, parent)
        self._bom = bom

        if bom is None:
                self.setWindowTitle("Codes list")
        else:
                self.setWindowTitle("Search in bom: "+bomdesc)

        self._init_gui()
        self.resize(1024, 600)

    def _create_statusbar(self):
        self._my_statusbar = QStatusBar()
        self._my_statusbar.showMessage("Status Bar Is Ready", 3000)
        self.setStatusBar(self._my_statusbar)

    def _create_menu(self):
        mainMenu = self.menuBar()

        m = mainMenu.addMenu("File")
        a = QAction("Close", self)
        a.setShortcut("Ctrl+Q")
        a.triggered.connect(self.close)
        m.addAction(a)
        a = QAction("Exit", self)
        a.triggered.connect(self._exit_app)
        m.addAction(a)

        m = mainMenu.addMenu("Edit")
        a = QAction("Copy table values", self)
        a.triggered.connect(self._copy_info_action)
        m.addAction(a)

        m = mainMenu.addMenu("Search mode")
        ag = QActionGroup(self)
        ag.setExclusive(True)

        a = QAction("Simple", self)
        a.setCheckable(True)
        a.triggered.connect(lambda : self._stacked_widget.setCurrentIndex(0))
        ag.addAction(a)
        a.setChecked(True)
        m.addAction(a)

        a = QAction("Advanced", self)
        a.setCheckable(True)
        m.addAction(a)
        a.triggered.connect(lambda : self._stacked_widget.setCurrentIndex(1))
        ag.addAction(a)

        self._windowsMenu = self.build_windows_menu(mainMenu)

        m = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : self._show_about(db.connection))
        m.addAction(a)

    def _exit_app(self):
        ret = QMessageBox.question(self, "BOMBrowser", "Do you want to exit from the application ?")
        if ret == QMessageBox.Yes:
            sys.exit(0)

    def _copy_info_action(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(self._stacked_widget.currentWidget().getTableText(),
            mode=cb.Clipboard)

    def _init_gui(self):

        self._create_statusbar()

        self._codes_widget = CodesListWidget(self, bom=self._bom)
        self._revisions_widget = searchrevisiongui.RevisionListWidget(self, bom=self._bom)
        self._stacked_widget = QStackedWidget()
        self._stacked_widget.addWidget(self._codes_widget)
        self._stacked_widget.addWidget(self._revisions_widget)

        self.setCentralWidget(self._stacked_widget)

        self._codes_widget.rightMenu.connect(self._codes_widget_context_menu)
        self._revisions_widget.rightMenu.connect(self._revisions_widget_context_menu)

        self._codes_widget.emitResult.connect(self._show_results)
        self._revisions_widget.emitResult.connect(self._show_results)
        self._create_menu()
        # create toolbar

    def _show_results(self, n):
        if n > 0:
            self._my_statusbar.showMessage("Last search result %s"%(str(n)))
        else:
            self._my_statusbar.showMessage("Last search returned 0 result !!!")

    def _codes_widget_context_menu(self, point):
        if not self._codes_widget.getCodeId():
            QApplication.beep()
            return
        contextMenu = QMenu(self)

        codecontextmenu.generate_codes_context_menu(
            code_id = self._codes_widget.getCodeId(),
            menu = contextMenu,
            parent = self)

        contextMenu.exec_(point)

    def _revisions_widget_context_menu(self, point):

        if not self._revisions_widget.getCodeId():
            QApplication.beep()
            return

        contextMenu = QMenu(self)

        codecontextmenu.generate_codes_context_menu(
            rid = self._revisions_widget.getRid(),
            menu = contextMenu,
            parent = self)

        contextMenu.exec_(point)
