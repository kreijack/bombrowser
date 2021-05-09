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

import sys, html

from PySide2.QtWidgets import QStatusBar
from PySide2.QtWidgets import QTextEdit, QHBoxLayout, QCheckBox
from PySide2.QtWidgets import QLabel, QLineEdit
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication, QPushButton
from PySide2.QtWidgets import QMessageBox, QAction, QDialog
from PySide2.QtCore import Qt, Signal
import pprint, traceback

import db, utils, selectdategui, bbwindow, cfg

class CodeDate(QWidget):

    refreshBom = Signal()

    def __init__(self, id_, code, date_days, parent=None):
        QWidget.__init__(self, parent)
        date = db.days_to_txt(date_days)
        self._code = code
        self._id = id_
        self._date = date
        self._date_days = date_days
        self._ret_code = None
        self._ret_data = None

        g = QGridLayout()

        g.addWidget(QLabel("Code"), 10, 10)
        le = QLineEdit()
        le.setText(code)
        le.setReadOnly(True)
        g.addWidget(le, 11, 10)

        g.addWidget(QLabel("Date"), 10, 15)
        le = QLineEdit()
        le.setText(date)
        le.setReadOnly(True)
        g.addWidget(le, 11, 15)

        b = QPushButton("Refresh")
        b.clicked.connect(self._do_refresh)
        g.addWidget(b, 10, 20, 2, 1)

        self.setLayout(g)

    def _get_bom(self):
        d = db.DB()
        return d.get_bom_by_code_id3(self._id, self._date_days)

    def _do_refresh(self):
        self._ret_code, self._ret_data = self._get_bom()
        self.refreshBom.emit()

    def getData(self):
        return (self._id, self._code, self._date, self._date_days)

    def getBom(self):
        if self._ret_code is None:
            self._ret_code, self._ret_data = self._get_bom()
        return (self._ret_code, self._ret_data)

    def getCaption(self):
        return "%s @ %s"%(self._code, self._date)

class DiffWindow(bbwindow.BBMainWindow):
    def __init__(self, bom1, bom2, parent=None):
        bbwindow.BBMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._bom1 = bom1
        self._bom2 = bom2
        self._init_gui()
        self._create_menu()
        self._create_statusbar()
        self.resize(1024, 600)
        self.setWindowTitle("Diff window: %s <-> %s"%(
                        bom1.getCaption(), bom2.getCaption()))


    def _create_statusbar(self):
        self._my_statusbar = QStatusBar()
        #self._my_statusbar.showMessage("Status Bar Is Ready", 3000)
        self.setStatusBar(self._my_statusbar)

    def _init_gui(self):
        grid = QGridLayout()
        self._grid = grid

        hl = QHBoxLayout()
        grid.addLayout(hl, 5, 0, 1, 10)

        self._cb_only_top_code = QCheckBox("Diff only top code")
        self._cb_only_top_code.clicked.connect(self.do_diff)
        hl.addWidget(self._cb_only_top_code)
        self._cb_minimal = QCheckBox("Diff only main attributes")
        self._cb_minimal.clicked.connect(self.do_diff)
        hl.addWidget(self._cb_minimal)
        hl.addStretch()

        grid.addWidget(self._bom1, 10, 1)
        grid.addWidget(self._bom2, 10, 7)
        self._bom2.refreshBom.connect(self.do_diff)
        self._bom1.refreshBom.connect(self.do_diff)
        grid.addWidget(QLabel("<font color=red>From (-)</>"), 10, 0)
        grid.addWidget(QLabel("<font color=green>To (+)</>"), 10, 6)

        b = QPushButton("<->")
        b.clicked.connect(self._swap_diff)
        grid.addWidget(b, 10, 5)

        self._text = QTextEdit()
        self._text.setReadOnly(True)

        grid.addWidget(self._text, 20, 0, 1, 10)

        w = QWidget()
        w.setLayout(grid)

        self.setCentralWidget(w)

    def _swap_diff(self):
        tmp = self._bom1
        self._bom1 = self._bom2
        self._bom2 = tmp
        self._grid.addWidget(self._bom1, 10, 1)
        self._grid.addWidget(self._bom2, 10, 7)
        self.do_diff()

    def _create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        closeAction = QAction("Close", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.triggered.connect(self.close)
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+X")
        exitAction.triggered.connect(self._exit_app)

        fileMenu.addAction(closeAction)
        fileMenu.addAction(exitAction)

        self._windowsMenu = self.build_windows_menu(mainMenu)

        helpMenu = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : self._show_about(db.connection))
        helpMenu.addAction(a)

    def _exit_app(self):
        ret = QMessageBox.question(self, "BOMBrowser", "Do you want to exit from the application ?")
        if ret == QMessageBox.Yes:
            sys.exit(0)

    def do_diff(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self._do_diff()
        except:
            utils.show_exception(msg="Cannot perform the diff: check the date!")
        finally:
            QApplication.restoreOverrideCursor()

    def _do_diff(self):
        code1, data1 = self._bom1.getBom()
        code2, data2 = self._bom2.getBom()

        # put the head of boms to the same ID to ensure to compare the "same" head
        if code1 != code2:
            data1 = data1.copy()
            data2 = data2.copy()
            code3 = max([max(data1.keys()), max(data2.keys())])+1
            data1[code3] = data1[code1]
            data1[code3]["id"] = code3
            data2[code3] = data2[code2]
            data2[code3]["id"] = code3
            data1.pop(code1)
            data2.pop(code2)
        else:
            code3 = code1

        gvals = cfg.get_gvalnames2()

        if self._cb_only_top_code.isChecked():
            keys = [code1]
        else:
            keys = list(set(data1.keys()).union(data2.keys()))
            keys.sort()

        if self._cb_minimal.isChecked():
            allowed_keys = [
                "qty", "descr", "code"
            ]
        else:
            allowed_keys = None


        self._text.clear()

        txt = ""

        item_props_blacklist = set(["id", "rid", "deps",
            "date_from_days", "date_to_days"])

        def is_children_equal(c1, c2):
            for k in ["qty", "each", "unit", "ref"]:
                if allowed_keys and not k in allowed_keys:
                    continue
                if c1[k] != c2[k]:
                    return False

            return True

        def is_codes_equal(c1, c2):
            k1 = set(c1.keys())
            k2 = set(c2.keys())
            if allowed_keys:
                k1 = k1.intersection(allowed_keys)
                k2 = k2.intersection(allowed_keys)
            if k1 != k2:
                return False

            k1.difference_update(item_props_blacklist)
            for k in k1:
                if c1[k] != c2[k]:
                    return False

            if c1["deps"].keys() != c2["deps"].keys():
                return False

            for k in c1["deps"].keys():
                if not is_children_equal(c1["deps"][k], c2["deps"][k]):
                    return False

            return True

        def makeRed(s):
            s = html.escape(s)
            s = "<font color=red>"+s+"</font><br>"
            return s
        def makeGreen(s):
            s = html.escape(s)
            s = "<font color=green>"+s+"</font><br>"
            return s
        def pretty_float(f):
            s="%f"%(f)
            while len(s) > 1 and s[-1] in "0.":
                s = s[:-1]
            return s
        def dump_child(child_dep, child_data):
            s = "%s / %s %s: %s"%(
                    pretty_float(child_dep["qty"]),
                    pretty_float(child_dep["each"]),
                    child_dep["unit"],
                    child_data["code"])
            if ((not allowed_keys or "ver" in allowed_keys) and
                    "ver" in child_data):
                s += " rev %s"%(child_data["ver"])
            if ((not allowed_keys or "descr" in allowed_keys) and
                    "descr" in child_data):
                s += " - %s"%(child_data["descr"])
            if ((not allowed_keys or "ref" in allowed_keys) and
                    "ref" in child_data):
                s += ";- %s"%(child_dep["ref"])
            return s
        def dump_code(c):
            s = " code: %s"%(c["code"])
            if ((not allowed_keys or "ver" in allowed_keys) and
                    "ver" in c):
                s += " rev %s"%(c["ver"])
            if ((not allowed_keys or "descr" in allowed_keys) and
                    "descr" in c):
                s += " - %s"%(c["descr"])
            return s

        for key in keys:
            if key in data1.keys() and key in data2.keys():
                if is_codes_equal(data1[key], data2[key]):
                        continue

                txt += "<br>\n"
                # diff between the same code
                txt += html.escape(dump_code(data1[key])) + "<br>"

                keys = set(data1[key].keys()).union(data2[key].keys())
                keys.difference_update(item_props_blacklist)
                keys = list(keys)
                keys.sort()
                keys = [x for x in keys if not x.startswith("gval")]
                keys = keys + [gvalname for (seq, idx, gvalname, caption, type_) in gvals]
                if allowed_keys:
                    keys = [ x for x in keys if x in allowed_keys]

                for key2 in keys:
                    if (key2 in data1[key] and key2 in data2[key] and
                            data1[key][key2] == data2[key][key2]):
                        continue
                    name = key2
                    if name.startswith("gval"):
                        for (seq, idx, gvalname, caption, type_) in gvals:
                            if gvalname == name:
                                name = caption
                                break

                    if key2 in data1[key]:
                        txt += "&nbsp;" * 5 + makeRed(
                                "-%s: %s\n"%(name, data1[key][key2]))
                    if key2 in data2[key]:
                        txt += "&nbsp;" * 5 + makeGreen(
                            "+%s: %s\n"%(name, data2[key][key2]))

                child_ids = list(set(data1[key]["deps"].keys()).union(
                                     data2[key]["deps"].keys()))
                child_ids.sort()

                for child_id in child_ids:
                    if child_id in data1[key]["deps"].keys() and child_id in data2[key]["deps"].keys():
                        if is_children_equal(data1[key]["deps"][child_id], data2[key]["deps"][child_id]):
                            continue

                    if child_id in data1[key]["deps"].keys():
                        child =data1[key]["deps"][child_id]
                        txt += "&nbsp;" * 9 + makeRed("-" +
                            dump_child(child, data1[child_id]))
                    if child_id in data2[key]["deps"].keys():
                        child =data2[key]["deps"][child_id]
                        txt += "&nbsp;" * 9 + makeGreen("+" +
                            dump_child(child, data2[child_id]))

            elif  key in data1.keys():
                txt += "<br>\n"
                txt += makeRed("-" + dump_code(data1[key])) + "\n"
                txt += "&nbsp;" * 5 + "[....]<br>\n"
            else:
                txt += "<br>\n"
                txt += makeGreen("+" + dump_code(data2[key])) + "\n"

                keys = set(data2[key].keys())
                keys.difference_update(item_props_blacklist)
                keys = list(keys)
                keys.sort()
                keys = [x for x in keys if not x.startswith("gval")]
                keys = keys + [gvalname for (seq, idx, gvalname, caption, type_) in gvals]
                if allowed_keys:
                    keys = [ x for x in keys if x in allowed_keys]

                for key2 in  keys:
                    name = key2
                    if name.startswith("gval"):
                        for (seq, idx, gvalname, caption, type_) in gvals:
                            if gvalname == name:
                                name = caption
                                break
                    if key2 in data2[key]:
                        txt += "&nbsp;" * 5 + makeGreen(
                            "+%s: %s\n"%(name, data2[key][key2]))

                child_ids = list(data2[key]["deps"].keys())
                child_ids.sort()
                for child_id in child_ids:
                    child =data2[key]["deps"][child_id]
                    txt += "&nbsp;" * 9 + makeGreen("+" +
                        dump_child(child, data2[child_id]))

        self._text.setText(txt)

class DiffDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        grid = QGridLayout()

        self._ql_id1 = QLineEdit(" "*10)
        self._ql_id2 = QLineEdit(" "*10)
        self._ql_code1 = QLineEdit(" "*10)
        self._ql_code2 = QLineEdit(" "*10)
        self._ql_date1 = QLineEdit(" "*10)
        self._ql_date2 = QLineEdit(" "*10)

        self._ql_id1.setReadOnly(True)
        self._ql_id2.setReadOnly(True)
        self._ql_code1.setReadOnly(True)
        self._ql_code2.setReadOnly(True)
        self._ql_date1.setReadOnly(True)
        self._ql_date2.setReadOnly(True)


        grid.addWidget(self._ql_id1, 1, 1)
        grid.addWidget(self._ql_id2, 2, 1)
        grid.addWidget(self._ql_code1, 1, 2)
        grid.addWidget(self._ql_code2, 2, 2)
        grid.addWidget(self._ql_date1, 1, 3)
        grid.addWidget(self._ql_date2, 2, 3)

        grid.addWidget(QLabel("From (-)"), 1, 0)
        grid.addWidget(QLabel("To (+)"), 2, 0)
        grid.addWidget(QLabel("ID"), 0, 1)
        grid.addWidget(QLabel("Codes"), 0, 2)
        grid.addWidget(QLabel("Dates"), 0, 3)

        self.setWindowTitle("Diff dialog")

        b=QPushButton("Hide")
        b.clicked.connect(self._do_hide)
        grid.addWidget(b,10, 2)

        self.setLayout(grid)

        self._id1 = -1
        self._id2 = -1
        self._code1 = ""
        self._code2 = ""
        self._date1 = ""
        self._date2 = ""

    def _do_diff(self):
        print(self._id1 + self._id2 + 0)
        bom1 = CodeDate(self._id1, self._code1,
                       self._date_from_days1)
        bom2 = CodeDate(self._id2, self._code2,
                       self._date_from_days2)
        w = DiffWindow(bom1, bom2)
        w.do_diff()
        w.show()
        self._do_hide()

    def _do_hide(self):
        self.hide()
        id_ = -1
        code = ""
        date = ""
        self._id1 = id_
        self._code1 = code
        self._date1 = date
        self._ql_id1.setText("")
        self._ql_code1.setText(code)
        self._ql_date1.setText(date)
        self._id2 = id_
        self._code2 = code
        self._date2 = date
        self._ql_id2.setText("")
        self._ql_code2.setText(code)
        self._ql_date2.setText(date)

    def set_from(self, code_id, code, date, date_from_days):
        self._id1 = code_id
        self._code1 = code
        self._date1 = date
        self._ql_id1.setText(str(code_id))
        self._ql_code1.setText(code)
        self._ql_date1.setText(date)
        self._date_from_days1 = date_from_days

    def set_to(self, code_id, code, date, date_from_days):
        self._id2 = code_id
        self._code2 = code
        self._date2 = date
        self._ql_id2.setText(str(code_id))
        self._ql_code2.setText(code)
        self._ql_date2.setText(date)
        self._date_from_days2 = date_from_days

        if self._code1 != "":
            self._do_diff()

_diffDialog = None

def set_from(code_id, parent):
    if not code_id:
        QApplication.beep()
        return

    #d = db.DB()
    #if not d.is_assembly(code_id):
    #    QApplication.beep()
    #    QMessageBox.critical(parent, "BOMBrowser", "The item is not an assembly")
    #    return

    dlg = selectdategui.SelectDate(code_id, parent)
    ret = dlg.exec_()
    if not ret:
        return

    (code, date_from_days) = dlg.get_code_and_date_from_days()
    date_from = db.days_to_txt(date_from_days)

    global _diffDialog
    if _diffDialog is None:
        _diffDialog = DiffDialog()
    _diffDialog.show()
    _diffDialog.set_from(code_id, code, date_from, date_from_days)

def set_to(code_id, parent):
    if not code_id:
        QApplication.beep()
        return

    #d = db.DB()
    #if not d.is_assembly(code_id):
    #    QApplication.beep()
    #    QMessageBox.critical(parent, "BOMBrowser", "The item is not an assembly")
    #    return

    dlg = selectdategui.SelectDate(code_id, parent)
    ret = dlg.exec_()
    if not ret:
        return

    (code, date_from_days) = dlg.get_code_and_date_from_days()
    date_from = db.days_to_txt(date_from_days)

    global _diffDialog
    if _diffDialog is None:
        _diffDialog = DiffDialog()
    _diffDialog.show()
    _diffDialog.set_to(code_id, code, date_from, date_from_days)

def set_to_by_rid(rid):

    d = db.DB()
    data = d.get_code_by_rid(rid)
    code_id = data["id"]
    date_from_days = data["date_from_days"]
    date_from = db.days_to_txt(data["date_from_days"])
    code = data["code"]

    #if not d.is_assembly(code_id):
    #    QApplication.beep()
    #    QMessageBox.critical(None, "BOMBrowser", "The item is not an assembly")
    #    return

    global _diffDialog
    if _diffDialog is None:
        _diffDialog = DiffDialog()
    _diffDialog.show()
    _diffDialog.set_to(code_id, code, date_from, date_from_days)

def set_from_by_rid(rid):

    d = db.DB()
    data = d.get_code_by_rid(rid)
    code_id = data["id"]
    date_from_days = data["date_from_days"]
    date_from = db.days_to_txt(data["date_from_days"])
    code = data["code"]

    #if not d.is_assembly(code_id):
    #    QApplication.beep()
    #    QMessageBox.critical(None, "BOMBrowser", "The item is not an assembly")
    #    return

    global _diffDialog
    if _diffDialog is None:
        _diffDialog = DiffDialog()
    _diffDialog.show()
    _diffDialog.set_from(code_id, code, date_from, date_from_days)

