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



"""
- create a new code
- edit a code (parameters, properties, drawings)

- edit an assembly (date and child)

- revise a code (copy all properties to a new code)
- revise an assembly (copy all properties to a new code)

- update all tree with the new code
"""

import sys

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar
from PySide2.QtWidgets import QSplitter, QTableView, QLabel
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QFrame
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QHeaderView, QMenu
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PySide2.QtCore import Qt, QAbstractTableModel, QEvent, QTimer

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

        b = QPushButton("OK")
        b.clicked.connect(self.close)
        g.addWidget(b, 20, 10)

        self.setWindowTitle("BOMBrowser: create new code")

        w = QWidget()
        w.setLayout(g)
        self.setCentralWidget(w)

        self._timer = QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self._timeout)


    def _timeout(self):
            pass



_newCodeWindow = None
def newCodeWindow():
    global _newCodeWindow

    if not _newCodeWindow:
        _newCodeWindow = NewCodeWindow()

    _newCodeWindow.show()


class EditWindow(QMainWindow):
    def __init__(self, id_ = None, date=None):
        QMainWindow.__init__(self)

        self._the_id = id_
        self._date = date
        self._orig_revision = None

        self._init_gui()

        if not self._the_id is None:
            self._populate_table()

        self._ver_changed()

    def _init_gui(self):
        g = QGridLayout()

        """
            CREATE TABLE    items (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                descr       VARCHAR(255) NOT NULL,
                code        VARCHAR(255) NOT NULL,
                ver         VARCHAR(10) NOT NULL,
                iter        INTEGER,
                default_unit VARCHAR(255) NOT NULL,
                for1cod     VARCHAR(255) DEFAULT '',
                for1id      VARCHAR(255) DEFAULT '',
                for1name    VARCHAR(255) DEFAULT '',
                prod1cod    VARCHAR(255) DEFAULT '',
                prod1name   VARCHAR(255) DEFAULT '',
                prod2cod    VARCHAR(255) DEFAULT '',
                prod2name   VARCHAR(255) DEFAULT ''
            );
        """

        g.addWidget(QLabel("Id"), 10, 10)
        self._id = QLineEdit()
        self._id.setDisabled(True)
        g.addWidget(self._id, 10, 11, 1, 1)

        g.addWidget(QLabel("Code"), 11, 10)
        self._code = QLineEdit()
        g.addWidget(self._code, 11, 11, 1, 2)

        b = QPushButton("...")
        b.clicked.connect(self._complete_code)

        if self._the_id:
            self._code.setDisabled(True)
        else:
            g.addWidget(b, 11, 13)


        g.addWidget(QLabel("Description"), 12, 10)
        self._descr = QLineEdit()
        g.addWidget(self._descr, 12, 11, 1, 3)

        g.addWidget(QLabel("Version"), 13, 10)
        self._ver = QLineEdit()
        self._ver.textChanged.connect(self._ver_changed)
        g.addWidget(self._ver, 13, 11, 1, 1)

        g.addWidget(QLabel("Iter"), 14, 10)
        self._iter = QLineEdit()
        self._iter.setDisabled(True)
        g.addWidget(self._iter, 14, 11, 1, 1)

        g.addWidget(QLabel("Default unit"), 15, 10)
        self._unit = QLineEdit()
        g.addWidget(self._unit, 15, 11, 1, 1)

        g.addWidget(QLabel("Supplier #1 name"), 16, 10)
        self._supp1name = QLineEdit()
        g.addWidget(self._supp1name, 16, 11, 1, 3)

        g.addWidget(QLabel("Supplier #1 code"), 17, 10)
        self._supp1cod = QLineEdit()
        g.addWidget(self._supp1cod, 17, 11, 1, 1)

        g.addWidget(QLabel("Supplier #2 name"), 18, 10)
        self._supp2name = QLineEdit()
        g.addWidget(self._supp2name, 18, 11, 1, 3)

        g.addWidget(QLabel("Supplier #2 code"), 19, 10)
        self._supp2cod = QLineEdit()
        g.addWidget(self._supp2cod, 19, 11, 1, 1)

        g.addWidget(QLabel("Supplier #3 name"), 20, 10)
        self._supp3name = QLineEdit()
        g.addWidget(self._supp3name, 20, 11, 1, 3)

        g.addWidget(QLabel("Supplier #3 code"), 21, 10)
        self._supp3cod = QLineEdit()
        g.addWidget(self._supp3cod, 21, 11, 1, 1)

        # TODO: add the properties


        b = QPushButton("Cancel")
        b.clicked.connect(self.close)
        g.addWidget(b, 30, 13)

        self._update_btn = QPushButton("Update code")
        self._update_btn.clicked.connect(self.close)
        g.addWidget(self._update_btn, 30, 10)

        self._revise_btn = QPushButton("Revise code")
        self._revise_btn.clicked.connect(self.close)
        g.addWidget(self._revise_btn, 30, 11)

        self.setWindowTitle("BOMBrowser: create new code")

        w = QWidget()
        w.setLayout(g)
        self.setCentralWidget(w)

    def _ver_changed(self):
        if self._ver.text() == self._orig_revision:
            self._update_btn.setEnabled(True)
            self._revise_btn.setEnabled(False)
        else:
            self._update_btn.setEnabled(False)
            self._revise_btn.setEnabled(True)

    def _complete_code(self):
        print("TBD")

    def _populate_table(self):
        d = db.DB()

        data = d.get_code(self._the_id)

        """
        data["code"] = res[0]
        data["descr"] = res[1]
        data["ver"] = res[2]
        data["iter"] = res[3]
        data["unit"] = res[4]

        data["for1name"] = res[6]
        data["for1cod"] = res[5]
        data["prod1name"] = res[8]
        data["prod1cod"] = res[7]
        data["prod2name"] = res[10]
        data["prod2cod"] = res[9]
        """

        self._id.setText(str(self._the_id))
        self._code.setText(data["code"])
        self._descr.setText(data["descr"])
        self._ver.setText(data["ver"])
        self._orig_revision = data["ver"]
        self._iter.setText(str(data["iter"]))
        self._unit.setText(data["unit"])
        self._supp1name.setText(data["for1name"])
        self._supp1cod.setText(data["for1cod"])
        self._supp2name.setText(data["prod1name"])
        self._supp2cod.setText(data["prod1cod"])
        self._supp3name.setText(data["prod2name"])
        self._supp3cod.setText(data["prod2cod"])

        # TODO: add the properties

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #w = EditWindow(id_=2) # resistor
    w = EditWindow(id_=2007) # top assembly
    w.show()
    sys.exit(app.exec_())
