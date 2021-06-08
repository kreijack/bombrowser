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

from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from PySide2.QtWidgets import QGridLayout, QPushButton
from PySide2.QtWidgets import QDialog, QHeaderView, QApplication
from PySide2.QtCore import Qt
import pprint

import db
import utils


class SelectDate(QDialog):
    def __init__(self, code_id, parent, only_data_code=False):
        QDialog.__init__(self, parent)
        self._code_id = code_id
        self._only_data_code = only_data_code
        self._return_values = None

        self._init_gui()
        self.show()
        self.setAttribute(Qt.WA_DeleteOnClose)

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._populate_table()
        QApplication.restoreOverrideCursor()

    def _init_gui(self):
        grid = QGridLayout()
        self.setWindowTitle("BOMBrowser - Select date")

        self._table = QTableWidget()
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QTableWidget.SelectRows);
        self._table.setAlternatingRowColors(True)

        grid.addWidget(self._table, 10, 0, 1, 2)

        b = QPushButton("Select")
        grid.addWidget(b, 20, 1)
        b.clicked.connect(self.accept)

        b = QPushButton("Cancel")
        b.clicked.connect(self.reject)
        grid.addWidget(b, 20, 0)

        self.setLayout(grid)

        self.resize(600,400)

    def _populate_table(self):
        d = db.DB()

               # code descr  rev   iter  date_from,            date_from_days
        data = [(r[0], r[1], r[5], r[6], db.days_to_txt(r[2]), r[2])
            for r in d.get_dates_by_code_id3(self._code_id)]
        sorted(data, reverse=True, key=lambda x : x[5])

        if not self._only_data_code:
            last = (data[-1][1], data[-1][2], data[-1][3])
            m = dict()
            for code, descr, rev, iter_, date_from, date_from_days in data:
                m[date_from_days] = (descr, rev, iter_)


            data2 = []

            data = d.get_bom_dates_by_code_id(self._code_id)
            assert(len(data))
            data.sort() # from lower to higher

            for date_from_days in data:
                if date_from_days in m:
                    last = m[date_from_days]
                data2.append((code, last[0], last[1], last[2],
                    db.days_to_txt(date_from_days), date_from_days))

            data2.sort(reverse=True, key=lambda x: x[5]) # from higher to lower
            data = data2


        assert(len(data))
        self._data = data

        self._table.clear()
        self._table.setColumnCount(5)
        self._table.selectionModel().selectionChanged.connect(self._table_clicked)
        self._table.doubleClicked.connect(self.accept)
        self._table.setSortingEnabled(False)
        self._table.setRowCount(len(data))
        #self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._table.setHorizontalHeaderLabels(["Code", "Description", "Rev", "Iter", "Date from"])

        for r in range(len(data)):
            row = data[r][:5] # ignore date_from_days
            for c in range(len(row)):
                i = QTableWidgetItem(str(row[c]))
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self._table.setItem(r, c, i)

        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        QApplication.instance().processEvents()
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self._table.selectRow(0)

    def _table_clicked(self, to, from_):

        if len(to.indexes()) < 1:
            return

        row = to.indexes()[0].row()
        self._return_values = (self._data[row][0], self._data[row][5])

    def get_code_and_date_from_days(self):
        return self._return_values


