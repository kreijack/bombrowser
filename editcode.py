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

import db, asmgui, codegui, diffgui, utils


class NewCodeWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        g = QGridLayout()
        g.addWidget(QLabel("Code"), 10, 10)
        self._code = QLineEdit()
        g.addWidget(self._code, 10, 11, 1, 3)

        b = QPushButton("Cancel")
        b.clicked.connect(self.close)
        g.addWidget(b, 20, 13)

        b = QPushButton("Create and edit code")
        b.clicked.connect(self.close)
        g.addWidget(b, 20, 10)

        self.setWindowTitle("BOMBrowser: create new code")

        w = QWidget()
        w.setLayout(g)
        self.setCentralWidget(w)


_newCodeWindow = None
def newCodeWindow():
    global _newCodeWindow

    if not _newCodeWindow:
        _newCodeWindow = NewCodeWindow()

    _newCodeWindow.show()
