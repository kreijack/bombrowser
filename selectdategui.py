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
from PySide2.QtWidgets import QMenu, QTableView, QFileDialog, QAbstractItemView
from PySide2.QtWidgets import QSplitter, QTreeView, QLabel, QLineEdit
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication, QPushButton
from PySide2.QtWidgets import QMessageBox, QAction, QDialog, QHeaderView
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import Qt, QItemSelectionModel, QAbstractTableModel
import pprint

import db, codegui, diffgui
import exporter, utils


class SelectDate(QDialog):
    def __init__(self, code_id, parent, only_data_code=False):
        QDialog.__init__(self, parent)
        self._code_id = code_id
        self._only_data_code = only_data_code

        self._init_gui()
        self._populate_table()

    class TableModel(QAbstractTableModel):
        def __init__(self, data, header):
            QAbstractTableModel.__init__(self)
            self._data = data
            self._header = header

        def data(self, index, role):
            if role == Qt.DisplayRole:
                # See below for the nested-list data structure.
                # .row() indexes into the outer list,
                # .column() indexes into the sub-list
                return self._data[index.row()][index.column()]

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

    def _init_gui(self):
        grid = QGridLayout()
        self.setWindowTitle("BOMBrowser: Select date")

        self._table = QTableView()
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QTableView.SelectRows);
        self._table.setAlternatingRowColors(True)
        #self._table.clicked.connect(self._table_clicked)
        #model = self.TableModel([], ["id", "Code", "Date from", "Date to"])
        #self._table.setModel(model)


        grid.addWidget(self._table, 10, 0, 1, 2)

        b = QPushButton("Select")
        grid.addWidget(b, 20, 0)
        b.clicked.connect(self.accept)

        b = QPushButton("Cancel")
        b.clicked.connect(self.reject)
        grid.addWidget(b, 20, 1)

        self.setLayout(grid)

        self.resize(600,400)

    def _populate_table(self):
        d = db.DB()
               # code descr  date_from rev iter
        data = [(r[0], r[1], r[7], r[8], r[2])
            for r in d.get_dates_by_code_id2(self._code_id)]
        sorted(data, reverse=True, key=lambda x : x[2])


        if not self._only_data_code:
            last = (data[0][1], data[0][3], data[0][4])
            m = dict()
            for code, descr, rev, iter_, date_from in data:
                m[date_from] = (descr, rev, iter_)

            data = d.get_bom_dates_by_code_id(self._code_id)
            data.sort(reverse=True)
            assert(len(data))

            data2 = []
            for r in data:
                if r[0] in m:
                    last = m[r[0]]
                data2.append((code, last[0], last[1], last[2], r[0]))

            data = data2

        assert(len(data))

        model = self.TableModel(data, ["Code", "Description", "Rev", "Iter", "Date from"])
        self._table.setModel(model)
        self._table.selectionModel().selectionChanged.connect(self._table_clicked)
        self._table.doubleClicked.connect(self.accept)
        self._table.selectRow(0)
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

        self._return_id = (
            self._table.model().data(IDX(row, 0), Qt.DisplayRole),
            self._table.model().data(IDX(row, 4), Qt.DisplayRole),
            self._table.model().data(IDX(row, 1), Qt.DisplayRole)
        )

    def get_result(self):
        return self._return_id


