"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021,2022,2023,2024 Goffredo Baroncelli <kreijack@inwind.it>

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

import os

from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QGridLayout, QWidget
from PySide2.QtWidgets import QAction, QFrame
from PySide2.QtWidgets import QPushButton, QMessageBox
from PySide2.QtWidgets import QComboBox, QMenu

from PySide2.QtCore import Qt

import db, cfg, utils, customize

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class CodeWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._text_info = ""

        self._init_gui()

    def populate(self, id_, date_from_days, qty, each, unit, ref, gavals=dict()):

        d = db.get_db_instance()
        data = d.get_code(id_, date_from_days)

        if not data or len(data) < 1:
            QMessageBox.critical(self, "BOMBrowser",
                "The code id=%d at date %s seems to not exist"%(
                id_, db.days_to_txt(date_from_days)))
            return

        self._data = data
        self._qty = qty
        self._each = each
        if unit == "":
            self._unit = data["unit"]
        self._unit = unit
        self._ref = ref
        self._gavals = gavals
        self._gavalnames = []
        self._main_data = [
            ("Code", "code"),
            ("Revision", "ver"),
            ("Iteration", "iter"),
            ("Description", "descr"),
            ("Unit", "unit"),
        ]

        gvalnames = cfg.get_gvalnames2()
        for (seq, idx, gvalname, caption, type_) in gvalnames:
            self._main_data.append((caption, gvalname))

        gavalnames = cfg.get_gavalnames()
        for (seq, idx, gavalname, caption, type_) in gavalnames:
            self._gavalnames.append((caption, gavalname))

        self._drawings_and_urls = [(x[0], utils.find_filename(x[1]))
                for x in d.get_drawings_and_urls_by_rid(self._data["rid"])]

        self._update_widget()

    def _init_gui(self):
        self._grid = QGridLayout()
        self.setLayout(self._grid)

        b = QPushButton("Copy info...")
        self._grid.addWidget(b, 0, 0)
        b.clicked.connect(self._copy_info)
        self._mainWidget = QWidget()

        self._grid.addWidget(self._mainWidget, 10, 0, 1, 2)

        #self._update_widget(d)

    def addDatesListWidget(self, list_widget):
        self._grid.addWidget(list_widget, 0, 1)

    def _update_widget(self):
        # https://stackoverflow.com/questions/10416582/replacing-layout-on-a-qwidget-with-another-layout
        QWidget().setLayout(self._mainWidget.layout())

        grid = QGridLayout()
        self._mainWidget.setLayout(grid)

        class XLabel(QLabel):
            def __init__(self, *args, **kwargs):
                QLabel.__init__(self, *args, **kwargs)
                self.setTextInteractionFlags(Qt.TextSelectableByMouse)

        txt = ""
        row = 0

        row += 1
        grid.addWidget(XLabel("RID"), row, 0)
        grid.addWidget(XLabel(str(self._data["rid"])), row , 1)
        txt += "RID: %s\n"%(self._data["rid"])

        row += 1
        grid.addWidget(XLabel("ID"), row, 0)
        grid.addWidget(XLabel(str(self._data["id"])), row , 1)
        txt += "ID: %s\n"%(self._data["id"])

        row += 1
        keys = set(self._data.keys())
        for caption, key in self._main_data:
            grid.addWidget(XLabel(caption), row, 0)
            if key in self._data:
                grid.addWidget(XLabel(str(self._data[key])), row , 1)
                keys.discard(key)
                txt += "%s: %s\n"%(caption, self._data[key])
            else:
                txt += "%s:\n"%(caption)
            row += 1

        if self._ref != "":
            grid.addWidget(XLabel("Reference:"), row, 0)
            grid.addWidget(XLabel(str(self._ref)), row , 1)
            txt += "Reference: %s\n"%(self._ref)
            row += 1

        dt = db.days_to_txt(self._data["date_from_days"])
        grid.addWidget(XLabel("Date from:"), row, 0)
        grid.addWidget(XLabel(dt), row , 1)
        txt += "Date from: %s\n"%(dt)
        row += 1

        dt = db.days_to_txt(self._data["date_to_days"])
        grid.addWidget(XLabel("Date to:"), row, 0)
        grid.addWidget(XLabel(dt), row , 1)
        txt += "Date to: %s\n"%(dt)
        row += 1

        if self._qty != "":
            grid.addWidget(XLabel("Quantity"), row, 0)
            grid.addWidget(XLabel(str(self._qty)), row , 1)
            txt += "Quantity: %s\n"%(self._qty)
            row += 1

        if self._each != "":
            grid.addWidget(XLabel("   Each"), row, 0)
            grid.addWidget(XLabel(str(self._each)), row , 1)
            txt += "Each: %s\n"%(self._each)
            row += 1

        if self._qty != "" and len(self._gavals):
            # if qty != "" the items is inside an assy, and it does
            # make sense to print the gavals fields
            for caption, name in self._gavalnames:
                    grid.addWidget(XLabel(caption), row, 0)
                    grid.addWidget(XLabel(self._gavals[name]), row , 1)
                    txt += "%s: %s\n"%(caption, self._gavals[name])
                    row += 1

        grid.addWidget(QHLine(), row, 0, 1, 2)
        row += 1

        for k in self._data["properties"]:
            grid.addWidget(XLabel(k), row, 0)
            grid.addWidget(XLabel(str(self._data["properties"][k])), row , 1)
            txt += "%s: %s\n"%(k, str(self._data["properties"][k]))
            row += 1

        if len(self._data["properties"].keys()):
            grid.addWidget(QHLine(), row, 0, 1, 2)
            row += 1

        skip = not customize.has_drawing_button_be_enabled(self._data)
        maxlen = int(cfg.config()["BOMBROWSER"]["btnmaxlength"])
        for drw in self._drawings_and_urls:
            n = drw[0]
            if maxlen > 3 and len(n) > maxlen:
                n = n[:maxlen-3]+"..."
            b = QPushButton(n)
            grid.addWidget(b, row, 0, 1, 2)
            row += 1

            if skip:
                b.setEnabled(False)
                continue

            class Opener:
                def __init__(self, obj, *args):
                    self._obj = obj
                    self._args = args
                def __call__(self, *args0):
                    self._obj(*args0, *self._args)

            b.clicked.connect(Opener(utils.open_file_or_url, drw[1]))
            txt += "  Drawing: %s\n"%(drw[0])
            if utils.is_url(drw[1]):
                b.setToolTip("Description: %s\nURL: %s"%(
                    drw[0], drw[1]))
            else:
                b.setToolTip("File: %s\nFullpath: %s"%(
                    drw[0], drw[1]))

            b.setContextMenuPolicy(Qt.CustomContextMenu)
            b.customContextMenuRequested.connect(
                Opener(self._btn_context_menu, drw[0], drw[1], b)
            )

        if self._drawings_and_urls:
            grid.addWidget(QHLine(), row, 0, 1, 2)
            row += 1

        grid.addWidget(QLabel(""),row, 0, )
        grid.setRowStretch(row, 100)
        grid.setColumnStretch(1, 100)

        self._text_info = txt

    def _btn_context_menu(self, point, descr, url, btn):
        popMenu = QMenu(self)
        if utils.is_url(url):
            a = QAction('Copy description', self)
            a.triggered.connect(lambda : utils.copy_text_to_clipboard(descr))
            popMenu.addAction(a)
            a = QAction('Copy URL', self)
            a.triggered.connect(lambda : utils.copy_text_to_clipboard(url))
            popMenu.addAction(a)
        else:
            name = os.path.basename(url)
            dirname = os.path.dirname(url)
            a = QAction('Open dir', self)
            a.triggered.connect(lambda : utils.open_file_or_url(dirname))
            popMenu.addAction(a)
            a = QAction('Copy filename', self)
            a.triggered.connect(lambda : utils.copy_text_to_clipboard(name))
            popMenu.addAction(a)
            a = QAction('Copy dirname', self)
            a.triggered.connect(lambda : utils.copy_text_to_clipboard(dirname))
            popMenu.addAction(a)
            a = QAction('Copy full path', self)
            a.triggered.connect(lambda : utils.copy_text_to_clipboard(url))
            popMenu.addAction(a)
            a = QAction('Copy file', self)
            a.triggered.connect(lambda : utils.copy_file_to_clipboard(url))
            popMenu.addAction(a)

        popMenu.exec_(btn.mapToGlobal(point))

    def _copy_info(self):
        utils.copy_text_to_clipboard(self._text_info)


class CodesWidget(CodeWidget):

    def __init__(self):
        CodeWidget.__init__(self)
        self._list = QComboBox()
        self.addDatesListWidget(self._list)
        self._code_id = None
        self._list.currentIndexChanged.connect(self._list_change_index)
        self._ignore = True

    def populate(self, code_id):
        self._code_id = code_id

        d = db.get_db_instance()
        dates = d.get_dates_by_code_id3(self._code_id)
        if not dates or len(dates) < 1:
            QMessageBox.critical(self, "BOMBrowser",
                "The code id=%d seems to not exist"%(
                code_id))
            return

        self._ignore = True
        self._list.clear()
        self._dates = dates

        for data2 in self._dates:
            (icode, idescr, idate_from_days, idate_to_days, rid) = data2[:5]

            self._list.addItem("%s .. %s"%(
                db.days_to_txt(idate_from_days),
                db.days_to_txt(idate_to_days)))

        self._date_from = db.days_to_txt(self._dates[0][2])
        self._date_from_days = self._dates[0][2]
        self._date_to = db.days_to_txt(self._dates[0][3])
        self._date_to_days = self._dates[0][3]
        self._rid = self._dates[0][4]
        self._ignore = False

        self._list_change_index(0)

    def _list_change_index(self, i):
        if self._code_id is None:
            return
        if self._ignore:
            return
        self._date_from_days = self._dates[i][2]
        CodeWidget.populate(self, self._code_id, self._date_from_days,
            "", "", "", "")

