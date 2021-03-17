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
import pprint, os

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar
from PySide2.QtWidgets import QSplitter, QTableView, QLabel, QDialog
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QFrame
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QHeaderView, QComboBox, QMenu
from PySide2.QtGui import QStandardItemModel, QStandardItem, QDesktopServices

from PySide2.QtCore import Qt, QAbstractTableModel, QEvent, QMimeData, QUrl
from PySide2.QtCore import QByteArray

import db, asmgui, cfg

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class CodeWidget(QWidget):

    def __init__(self, id_, winParent, date_from_days=None, unit=None, qty=None,
                 each=None, date_from=None, date_to=None,
                 parent = None, ref=None, rid=None):
        QWidget.__init__(self, parent)

        if ref is None or ref == "None":
            ref = ""
        if date_from is None or date_from == "None":
            date_from = ""
        if date_to is None or date_to == "None":
            date_to = ""

        self._code_id = id_
        self._rid = rid
        self._qty = qty
        self._each = each
        self._date_from = db.days_to_txt(date_from_days)
        self._date_from_days = date_from_days
        self._date_to = date_to
        self._winParent = winParent
        self._unit = unit
        self._ref = ref
        self._main_data = [
            ("Code", "code"),
            ("Revision", "ver"),
            ("Iteration", "iter"),
            ("Description", "descr"),
            ("Unit", "unit"),
        ]

        gvalnames = cfg.config().get("BOMBROWSER", "gvalnames").split(",")
        i = 0
        for i in range(len(gvalnames)):
            self._main_data.append((gvalnames[i], "gval%d"%(i+1)))
        self._init_gui()

    def _init_gui(self):
        self._grid = QGridLayout()
        self.setLayout(self._grid)

        #self._grid.clear()
        d = db.DB()

        if self._date_from_days is None:

            self._dates = d.get_dates_by_code_id3(self._code_id)
            self._list = QComboBox()
            for data2 in self._dates:
                (icode, idescr, idate_from_days, idate_to_days, rid) = data2[:5]

                self._list.addItem("%s .. %s"%(
                    db.days_to_txt(idate_from_days),
                    db.days_to_txt(idate_to_days)))

            self._grid.addWidget(self._list, 0, 1)
            self._date_from = db.days_to_txt(self._dates[0][2])
            self._date_from_days = self._dates[0][2]
            self._date_to = db.days_to_txt(self._dates[0][3])
            self._date_to_days = self._dates[0][3]
            self._rid = self._dates[0][4]
            self._list.currentIndexChanged.connect(self._list_change_index)

        b = QPushButton("Copy info...")
        self._grid.addWidget(b, 0, 0)
        b.clicked.connect(self._copy_info)
        self._mainWidget = QWidget()

        self._grid.addWidget(self._mainWidget, 10, 0, 1, 2)

        self._update_widget(d)

    def _list_change_index(self, i):
        self._date_from = db.days_to_txt(self._dates[i][2])
        self._date_from_days = self._dates[i][2]
        self._date_to = db.days_to_txt(self._dates[i][3])
        self._date_to_days = self._dates[i][3]

        self._update_widget(db.DB())

    def _update_widget(self, d):
        # https://stackoverflow.com/questions/10416582/replacing-layout-on-a-qwidget-with-another-layout
        QWidget().setLayout(self._mainWidget.layout())

        grid = QGridLayout()
        self._mainWidget.setLayout(grid)

        class XLabel(QLabel):
            def __init__(self, *args, **kwargs):
                QLabel.__init__(self, *args, **kwargs)
                self.setTextInteractionFlags(Qt.TextSelectableByMouse)

        data = d.get_code(self._code_id, self._date_from_days)
        if self._unit:
            data["unit"] = self._unit

        self._rid = data["rid"]

        txt = ""
        row = 0

        row += 1
        grid.addWidget(XLabel("RID"), row, 0)
        grid.addWidget(XLabel(str(self._rid)), row , 1)
        txt += "RID: %s\n"%(str(self._rid))

        row += 1
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

        drawings = d.get_drawings_by_code_id(self._rid)
        for drw in drawings:
            b = QPushButton(drw[0])
            class Opener:
                def __init__(self, obj, *args):
                    self._obj = obj
                    self._args = args
                def __call__(self, *args0):
                    self._obj(*args0, *self._args)

            b.clicked.connect(Opener(self._open_file, drw[1]))
            txt += "  Drawing: %s\n"%(drw[0])
            b.setToolTip("File: %s\nFullpath: %s"%(
                drw[0], drw[1]))

            b.setContextMenuPolicy(Qt.CustomContextMenu)
            b.customContextMenuRequested.connect(
                Opener(self._btn_context_menu, drw[1], b)
            )
            grid.addWidget(b, row, 0, 1, 2)
            row += 1

        if drawings:
            grid.addWidget(QHLine(), row, 0, 1, 2)
            row += 1

        grid.addWidget(QLabel(""),row, 0, )
        grid.setRowStretch(row, 100)
        grid.setColumnStretch(1, 100)

        self._text_info = txt

    def _btn_context_menu(self, point, fullpath, btn):
        name = os.path.basename(fullpath)
        dirname = os.path.dirname(fullpath)
        popMenu = QMenu(self)
        a = QAction('Open dir', self)
        a.triggered.connect(lambda : self._open_file(dirname))
        popMenu.addAction(a)
        a = QAction('Copy filename', self)
        a.triggered.connect(lambda : self._copy_str(name))
        popMenu.addAction(a)
        a = QAction('Copy dirname', self)
        a.triggered.connect(lambda : self._copy_str(dirname))
        popMenu.addAction(a)
        a = QAction('Copy full path', self)
        a.triggered.connect(lambda : self._copy_str(fullpath))
        popMenu.addAction(a)
        a = QAction('Copy file', self)
        a.triggered.connect(lambda : self._copy_file(fullpath))
        popMenu.addAction(a)

        popMenu.exec_(btn.mapToGlobal(point))

    def _copy_str(self, s):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(s, mode=cb.Clipboard)

    def _copy_file(self, fn):
        md = QMimeData()
        md.setUrls([QUrl.fromLocalFile(fn)])
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setMimeData(md)

    def _copy_info(self):
        self._copy(self._text_info)

    def _open_file(self, nf):
        QDesktopServices.openUrl(nf)

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

