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

from PySide2.QtWidgets import  QScrollArea
from PySide2.QtWidgets import  QSplitter, QTableView, QLabel
from PySide2.QtWidgets import  QGridLayout, QApplication, QWidget
from PySide2.QtWidgets import  QLineEdit
from PySide2.QtWidgets import  QPushButton, QVBoxLayout
from PySide2.QtWidgets import  QHeaderView, QTableWidgetItem, QTableWidget
from PySide2.QtCore import  QPoint, Signal, Qt, QRegExp
from PySide2.QtGui import QRegExpValidator, QValidator

import db, codegui, utils
import cfg, bbdate

class RevisionListWidget(QWidget):
    #tableCustomContextMenuRequested = Signal(QPoint)
    rightMenu = Signal(QPoint)
    doubleClicked = Signal()
    emitResult = Signal(int)

    def __init__(self, parent=None, bom=None):
        QWidget.__init__(self, parent)

        self._copy_info = ""
        self._code_id = None
        self._code = None
        self._rid = None
        self._bom = bom
        self._descr_force_uppercase = cfg.config()["BOMBROWSER"].get("description_force_uppercase", "1")
        self._code_force_uppercase = cfg.config()["BOMBROWSER"].get("code_force_uppercase", "1")
        self._data = dict()
        self._field_names = [
            ("code", "Code"), ("descr", "Description", 6),
            ("id", "id"), ("rid", "rid"),
            ("rev", "Rev"), ("iter_", "Iteration"),
            ("date_from_days", "Date from"),
            ("date_to_days", "Date to")]

        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            self._field_names.append((gvalname, caption))
        self._dates = dict()
        self._search_revision_cols = ["id", "rid", "Code","Description",
            "Rev", "Iteration", "Date from", "Date to"]
        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            self._search_revision_cols.append(caption)

        assert(len(self._search_revision_cols) == len(self._field_names))

        self._init_gui()

    def _init_gui(self):

        vb = QVBoxLayout()

        self._line_edit_widgets = dict()
        i = 0

        grid = QGridLayout()
        vb.addLayout(grid)
        row = 0
        for c in [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]:
            if i >= len(self._field_names):
                break
            col = 0
            while c > 0 and i < len(self._field_names):
                if len(self._field_names[i]) == 3:
                    key, descr, span = self._field_names[i]
                else:
                    key, descr = self._field_names[i]
                    span = 1
                l = QLabel(descr)
                l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(l, row, col)
                col += 1

                if "date_" in key:
                    w = bbdate.BBDatesLineEdit()
                elif key == 'id' or key == 'rid' or key == "iter_":
                    w = QLineEdit()
                    w.textChanged.connect(bbdate.Validator(w,
                        QRegExpValidator(QRegExp("^[!=<>]?[0-9]*$"))))
                    w.setValidator(QRegExpValidator(QRegExp("^[!=<>]?[0-9]*$")))
                else:
                    w = QLineEdit()

                self._line_edit_widgets[key] = w
                grid.addWidget(w, row, col, 1 , span)
                col += span
                w.returnPressed.connect(self._search)

                i += 1
                c -= 1

            row += 1

        b = QPushButton("Search")
        b.clicked.connect(self._search)
        b.setDefault(True)
        grid.addWidget(b, 0, 9)

        self._splitter = QSplitter()
        vb.addWidget(self._splitter)
        vb.setStretch(1, 100)

        self._table = QTableWidget()

        self._table.clear()
        self._table.setSortingEnabled(True)
        self._table.setSelectionBehavior(QTableView.SelectRows);
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionMode(self._table.SingleSelection)
        self._table.setColumnCount(len(self._search_revision_cols))
        self._table.setHorizontalHeaderLabels(self._search_revision_cols)
        self._splitter.addWidget(self._table)

        self._code_widget = codegui.CodeWidget()
        scrollarea = QScrollArea()
        scrollarea.setWidget(self._code_widget)
        scrollarea.setWidgetResizable(True)
        self._splitter.addWidget(scrollarea)

        self._splitter.setSizes([700, 1024-700])

        self.setLayout(vb)

        self._table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._tree_context_menu)
        self._table.doubleClicked.connect(self.doubleClicked)

    def _tree_context_menu(self, point):
        self.rightMenu.emit(self._table.viewport().mapToGlobal(point))

    def _search_in_bom(self, pattern):
        ret = []
        fns = ["id", "rid", "code","descr",
            "ver", "iter", "date_from_days", "date_to_days"]

        fns += ["" for x in cfg.get_gvalnames2()]
        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            fns[8 + idx -1] = gvalname

        for k, v in self._bom.items():
            match = True
            for pk, pv in pattern.items():
                if pk == 'iter_':
                    pk = 'iter'
                if not pk in v.keys():
                    print("WARNING: key '%s' not found"%(pk))
                    print("WARNING: pattern=", pattern)
                    print("WARNING: v=", v)
                    continue

                if len(pv) < 1:
                    continue

                if pv[0] in "=!<>":
                    mode = pv[0]
                    v1 = pv[1:]
                else:
                    mode = ""
                    v1 = pv

                if pk in ("rid", "id", "iter") or pk.startswith("date_"):
                    v1 = int(v1)

                if mode == '=':
                    if v1 != v[pk]:
                        match = False
                        break
                elif mode == '!':
                    if v1 == v[pk]:
                        match = False
                        break
                elif mode == '>':
                    if v1 >= v[pk]:
                        match = False
                        break
                elif mode == '<':
                    if v1 <= v[pk]:
                        match = False
                        break
                else:
                    if pk in ("rid", "id", "iter"):
                        # integer comparation
                        if v1 != v[pk]:
                            match = False
                            break
                    elif pk.startswith("date_"):
                        # integer comparation
                        if v1 != v[pk]:
                            match = False
                            break
                    else:
                        # string comparation
                        if not v1 in v[pk]:
                            match = False
        
            if match:
                ret.append([v[kk] for kk in fns])

        return ret

    def _search(self):

        try:
            dd = dict()
            for k in self._line_edit_widgets.keys():
                v = str(self._line_edit_widgets[k].text())
                if len(v) == 0:
                    continue
                if v in "=!<>" and len(v) < 1:
                    continue

                if k == "date_from_days" or k == "date_to_days":
                    if v[0] in "<>=!":
                        prefix = v[0]
                        v = v[1:]
                    else:
                        prefix = ""
                    if v.upper() == "PROTOTYPE":
                        v = str(db.prototype_date)
                    else:
                        v = str(db.iso_to_days(v))
                    v = prefix + v

                elif self._descr_force_uppercase == "1" and k == "descr":
                        v = v.upper()
                elif self._code_force_uppercase == "1" and k == "code":
                        v = v.upper()

                dd[k] = v

            if self._bom:
                ret = self._search_in_bom(dd)
            else:
                d = db.DB()
                ret = d.search_revisions(**dd)
        except:
            QApplication.beep()
            utils.show_exception(msg="Incorrect parameter for search")
            return

        if not ret or len(ret) == 0:
            QApplication.beep()
            self.emitResult.emit(0)
            return

        self._copy_info = "\t".join(self._search_revision_cols)
        self._copy_info += "\n"
        self._copy_info += "\n".join(["\t".join(map(str, row[:5])) for row in ret])

        self._table.setSortingEnabled(False)
        self._table.clear()

        self._table.setColumnCount(len(self._search_revision_cols))
        self._table.setHorizontalHeaderLabels(self._search_revision_cols)
        self._table.setRowCount(len(ret))

        r = 0
        limit = 1000
        self._dates = dict()


        col_map = dict()
        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            col_map[8 + idx - 1] = seq + 8
        for row in ret:
            c = 0
            for c, v in enumerate(row):
                if c == 1:
                    rid = int(v)
                elif c == 6 or c == 7:
                    if c == 6:
                        self._dates[rid] = v
                    v = db.days_to_txt(v)

                # gval(s) are from column 8 onwards. Map it correctly
                if c >= 8:
                    if not c in col_map:
                        continue
                    c = col_map[c]
                i = QTableWidgetItem(str(v))
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self._table.setItem(r, c, i)

            r += 1
        self._table.setSortingEnabled(True)
        self._table.selectionModel().selectionChanged.connect(self._table_clicked)
        if len(ret) > 0:
            self._table.selectRow(0)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        QApplication.instance().processEvents()
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.emitResult.emit(len(ret))

    def _table_clicked(self, to, from_):

        if len(to.indexes()) < 1:
            return

        row = to.indexes()[0].row()

        id_ = int(self._table.item(row, 0).text())
        rid = int(self._table.item(row, 1).text())
        code = self._table.item(row, 2).text()

        v = self._table.item(row, 6).text()
        self._date_from_days = self._dates[rid]

        self._code_id = id_
        self._code = code
        self._rid = rid

        self._code_widget.populate(id_, self._date_from_days,
            qty="", each="", ref="", unit="")

    def getCodeId(self):
        return self._code_id

    def getCode(self):
        return self._code

    def getRid(self):
        return self._rid

    def getDateFromDays(self):
        return self._date_from_days

    def getTableText(self):
        return self._copy_info

if __name__ == "__main__":
    cfg.init()
    app = QApplication(sys.argv)
    w = RevisionListWidget()
    w.show()
    sys.exit(app.exec_())
