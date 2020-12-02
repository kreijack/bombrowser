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
import webbrowser

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar
from PySide2.QtWidgets import QSplitter, QTableView, QLabel, QDialog
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QFrame
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QHeaderView
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PySide2.QtCore import Qt, QAbstractTableModel, QEvent
import pprint

import db, asmgui

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class CodeWidget(QWidget):

    def __init__(self, id_, winParent, unit=None, qty=None, each=None,
                 date_from=None, date_to=None, parent = None, ref=None):
        QWidget.__init__(self, parent)

        if ref is None or ref == "None":
            ref = ""
        if date_from is None or date_from == "None":
            date_from = ""
        if date_to is None or date_to == "None":
            date_to = ""

        self._code_id = id_
        self._qty = qty
        self._each = each
        self._date_from = date_from
        self._date_to = date_to
        self._winParent = winParent
        self._unit = unit
        self._ref = ref
        self._main_data = [
            ("Code", "code"),
            ("Version", "ver"),
            ("Iteration", "iter"),
            ("Description", "descr"),
            ("Unit", "unit"),
            ("Fornitore", "for1name"),
            ("  P/N", "for1cod"),
            ("Produttore", "prod1name"),
            ("  P/N", "prod1cod"),
            ("Produttore", "prod2name"),
            ("  P/N", "prod2cod"),
        ]
        self._init_gui()

    def _init_gui(self):

        class XLabel(QLabel):
            def __init__(self, *args, **kwargs):
                QLabel.__init__(self, *args, **kwargs)
                self.setTextInteractionFlags(Qt.TextSelectableByMouse)

        grid = QGridLayout()
        self.setLayout(grid)

        #self._grid.clear()
        d = db.DB()
        data = d.get_code(self._code_id)
        if self._unit:
            data["unit"] = self._unit

        #subg = QGridLayout()
        #grid.addLayout(subg, 0, 0, 1, 2)

        #b = QPushButton("Change code...")
        #subg.addWidget(b, 0, 0)
        #b.clicked.connect(self._change_code)
        #b = QPushButton("Change assembly...")
        #subg.addWidget(b, 0, 1)
        #b.clicked.connect(self._change_assembly)
        #b = QPushButton("Show assembly...")
        #subg.addWidget(b, 0, 0)
        #b.clicked.connect(self._show_assembly)
        #b = QPushButton("Where used...")
        #subg.addWidget(b, 0, 1)
        #b.clicked.connect(self._where_used)

        b = QPushButton("Copy info...")
        grid.addWidget(b, 0, 0)
        b.clicked.connect(self._copy_info)

        txt = ""
        row = 1
        grid.addWidget(XLabel("ID"), row, 0)
        grid.addWidget(XLabel(str(self._code_id)), row , 1)
        txt += "ID: %s\n"%(str(self._code_id))

        row += 1
        keys = set(data.keys())
        for caption, key in self._main_data:
            grid.addWidget(XLabel(caption), row, 0)
            if key in data:
                grid.addWidget(XLabel(str(data[key])), row , 1)
                keys.discard(key)
                txt += "%s: %s\n"%(caption, data[key])
            else:
                txt += "%s:\n"%(caption)
            row += 1

        if not self._date_from is None:
            grid.addWidget(XLabel("Reference:"), row, 0)
            grid.addWidget(XLabel(str(self._ref)), row , 1)
            txt += "Reference: %s\n"%(self._ref)
            row += 1

        if not self._date_from is None:
            grid.addWidget(XLabel("Date from:"), row, 0)
            grid.addWidget(XLabel(str(self._date_from)), row , 1)
            txt += "Date from: %s\n"%(self._date_from)
            row += 1

        if not self._date_to is None:
            grid.addWidget(XLabel("Date to:"), row, 0)
            grid.addWidget(XLabel(str(self._date_to)), row , 1)
            txt += "Date to: %s\n"%(self._date_to)
            row += 1


        if not self._qty is None:
            grid.addWidget(XLabel("Quantity"), row, 0)
            grid.addWidget(XLabel(str(self._qty)), row , 1)
            txt += "Quantity: %s\n"%(self._qty)
            row += 1

        if not self._each is None:
            grid.addWidget(XLabel("   Each"), row, 0)
            grid.addWidget(XLabel(str(self._each)), row , 1)
            txt += "Each: %s\n"%(self._each)
            row += 1

        grid.addWidget(QHLine(), row, 0, 1, 2)
        row += 1

        for k in data["properties"]:
            grid.addWidget(XLabel(k), row, 0)
            grid.addWidget(XLabel(str(data["properties"][k])), row , 1)
            txt += "%s: %s\n"%(k, str(data["properties"][k]))
            row += 1

        if len(data["properties"].keys()):
            grid.addWidget(QHLine(), row, 0, 1, 2)
            row += 1

        drawings = d.get_drawings_by_code_id(self._code_id)
        for drw in drawings:
            b = QPushButton(drw[0])
            class Opener:
                def __init__(self, obj, fullpath):
                    self._obj = obj
                    self._fullpath = fullpath+""
                def __call__(self):
                    self._obj(self._fullpath)

            b.clicked.connect(Opener(self._open_file, drw[1]))
            txt += "  Drawing: %s\n"%(drw[0])

            grid.addWidget(b, row, 0, 1, 2)
            row += 1

        if drawings:
            grid.addWidget(QHLine(), row, 0, 1, 2)
            row += 1

        grid.addWidget(QLabel(""),row, 0, )
        grid.setRowStretch(row, 100)
        grid.setColumnStretch(1, 100)

        self._text_info = txt

    def _copy_info(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(self._text_info, mode=cb.Clipboard)

    def _open_file(self, nf):
        webbrowser.open(nf)

    def _change_code(self):
        if not self._code_id:
            QApplication.beep()
            return

        #self._my_statusbar.showMessage("Not implemented", 3000)

    def _where_used(self):
        if not self._code_id:
            QApplication.beep()
            return
        asmgui.where_used(self._code_id, self._winParent)

    def _show_assembly(self):
        if not self._code_id:
            QApplication.beep()
            return
        asmgui.show_assembly(self._code_id, self._winParent)
