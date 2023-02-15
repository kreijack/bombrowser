"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021,2022,2023 Goffredo Baroncelli <kreijack@inwind.it>

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

import sys, os

from PySide2.QtWidgets import  QScrollArea
from PySide2.QtWidgets import  QSplitter, QTableView, QLabel
from PySide2.QtWidgets import  QGridLayout, QApplication, QWidget
from PySide2.QtWidgets import  QLineEdit
from PySide2.QtWidgets import  QPushButton, QVBoxLayout
from PySide2.QtWidgets import  QHeaderView, QTableWidgetItem, QTableWidget
from PySide2.QtCore import  QPoint, Signal, Qt, QRegExp
from PySide2.QtGui import QRegExpValidator, QValidator, QColor, QBrush

import db, codegui, utils, time
import cfg, bbdate

class RevisionListWidget(QWidget):
    #tableCustomContextMenuRequested = Signal(QPoint)
    rightMenu = Signal(QPoint)
    doubleClicked = Signal()
    emitResult = Signal(float, int)

    def __init__(self, parent=None, bom=None):
        QWidget.__init__(self, parent)

        self._copy_info = None
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

        if bom is None:
            self._field_names += [("doc", "Document")]

        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            self._field_names.append((gvalname, caption))
        self._dates = dict()
        self._search_revision_cols = ["id", "rid", "Code","Description",
            "Rev", "Iteration", "Date from", "Date to"]

        if self._bom is None:
            self._search_revision_cols += ["Documents"]

        self._notgvalcols = len(self._search_revision_cols)

        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            self._search_revision_cols.append(caption)

        #assert(len(self._search_revision_cols) == len(self._field_names) )

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

                    # allow:
                    # =1224
                    # >1234
                    # 1234
                    # 1234;567
                    # >5000;<3000
                    myregexp = "^[!=<>]?[0-9]*(;[!=<>]?[0-9]*)*$"
                    w.textChanged.connect(bbdate.Validator(w,
                        QRegExpValidator(QRegExp(myregexp))))
                    w.setValidator(QRegExpValidator(QRegExp(myregexp)))
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

                if pk in ("rid", "id", "iter") or pk.startswith("date_"):
                    match = utils.bb_match(v[pk], pv, int)
                else:
                    match = utils.bb_match(v[pk], pv)
                if not match:
                    break

            if match:
                ret.append([v[kk] for kk in fns])

        return ret

    def _search_revisions_join_docs(self, **dd):
        d = db.DB()
        ret = d.search_revisions(**dd)

        prev_row = None
        for row in ret:
            if prev_row:
                # column 8 is document
                if prev_row[1] == row[1]:
                    prev_row[8] += ", " + os.path.basename(row[8])
                    continue

                yield prev_row

            prev_row = list(row)
            if prev_row[8] is None:
                prev_row[8] = ""
            else:
                prev_row[8] = os.path.basename(prev_row[8])

        if prev_row:
            yield prev_row

    def _apply_colors(self, color_filters, field_map, row, item):
        def match(k, v):
            if not k in field_map:
                return False

            field = str(row[field_map[k]])

            if v.startswith("!") and field != v[1:]:
                return True
            if field == v:
                return True

            return False

        def apply_actions(actions):
            for action in actions:
                if action.startswith("bg="):
                    item.setBackground(QColor(action[3:]))
                elif action.startswith("fg="):
                    item.setForeground(QColor(action[3:]))
                elif action.startswith("italic"):
                    f = item.font()
                    f.setItalic(True)
                    item.setFont(f)
                elif action.startswith("bold"):
                    f = item.font()
                    f.setBold(True)
                    item.setFont(f)
                else:
                    print("WARNING: unknown action '%s'"%(action))

        for (filters, actions) in color_filters:
            for f in filters:
                k,v = f.split("=")[:2]
                if not match(k, v):
                    break
            else:
                apply_actions(actions)

    def _search(self):
        time0 = time.time()
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

            self._last_search_params = dd
            if self._bom:
                ret = self._search_in_bom(dd)
            else:
                ret = list(self._search_revisions_join_docs(**dd))
        except:
            QApplication.beep()
            utils.show_exception(msg="Incorrect parameter for search")
            return

        if not ret or len(ret) == 0:
            QApplication.beep()
            self.emitResult.emit(0, 0)
            return

        self._table.setSortingEnabled(False)
        self._table.clear()

        self._table.setColumnCount(len(self._search_revision_cols))
        self._table.setHorizontalHeaderLabels(self._search_revision_cols)
        self._table.setRowCount(len(ret))

        r = 0
        limit = 1000
        self._dates = dict()

        # This dict maps the sql table column nr to the widget table column nr
        col_map = dict()
        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            col_map[self._notgvalcols + idx - 1] = seq + self._notgvalcols

        # This dict maps the sql table column id to the widget table column nr
        field_map = dict()
        for i, field in enumerate(self._field_names[:self._notgvalcols]):
            field_map[field[0]] = i
        for (seq, idx, gvalname, caption, type_) in cfg.get_gvalnames2():
            field_map[gvalname] = self._notgvalcols + idx - 1

        self._copy_info = ["\t".join(self._search_revision_cols)]
        revlistcolors = cfg.get_revlistolors()
        for row in ret:
            c = 0
            copy_row = ["" for x in self._search_revision_cols]
            items_list = []
            for c, v in enumerate(row):
                if c == 1:
                    rid = int(v)
                elif c == 6 or c == 7:
                    if c == 6:
                        self._dates[rid] = v
                    v = db.days_to_txt(v)

                # gval(s) are from column "self._notgvalcols" onwards.
                # Map it correctly
                if c >= self._notgvalcols:
                    if not c in col_map:
                        continue
                    c = col_map[c]
                i = QTableWidgetItem(str(v))
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                if len(revlistcolors) > 0:
                    self._apply_colors(revlistcolors, field_map, row, i)
                self._table.setItem(r, c, i)
                copy_row[c] = str(v)

            self._copy_info.append("\t".join(copy_row))
            r += 1
        self._copy_info = "\n".join(self._copy_info)

        self._table.setSortingEnabled(True)
        self._table.selectionModel().selectionChanged.connect(self._table_clicked)
        if len(ret) > 0:
            self._table.selectRow(0)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        QApplication.instance().processEvents()
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self._table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.emitResult.emit(time.time() - time0, len(ret))

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
