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
from PySide2.QtWidgets import QMenu, QTableView, QTextEdit
from PySide2.QtWidgets import QSplitter, QTreeView, QLabel, QLineEdit
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication, QPushButton
from PySide2.QtWidgets import QMessageBox, QAction, QDialog, QHeaderView
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import Qt, QItemSelectionModel, QAbstractTableModel
import pprint, traceback

import db, utils, selectdategui

class DiffWindow(QMainWindow):
    def __init__(self, id1, code1, date1, id2, code2, date2, parent=None):
        QMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._init_gui(id1, code1, date1, id2, code2, date2)
        self._create_menu()
        self._create_statusbar()
        self.resize(1024, 600)
        self.setWindowTitle("BOMBrowser - Diff window: %s @ %s <-> %s @ %s"%(
            code1, date1[:10], code2, date2[:10]))


    def _create_statusbar(self):
        self._my_statusbar = QStatusBar()
        #self._my_statusbar.showMessage("Status Bar Is Ready", 3000)
        self.setStatusBar(self._my_statusbar)

    def _init_gui(self, id1, code1, date1, id2, code2, date2):
        grid = QGridLayout()

        self._ql_id1 = QLineEdit(id1)
        self._ql_id2 = QLineEdit(id2)
        self._ql_code1 = QLineEdit(code1)
        self._ql_code2 = QLineEdit(code2)
        self._ql_date1 = QLineEdit(date1)
        self._ql_date2 = QLineEdit(date2)

        self._ql_id1.setReadOnly(True)
        self._ql_id2.setReadOnly(True)
        self._ql_code1.setReadOnly(True)
        self._ql_code2.setReadOnly(True)
        self._ql_date1.setReadOnly(True)
        self._ql_date2.setReadOnly(True)

        grid.addWidget(self._ql_id1, 1, 1)
        grid.addWidget(self._ql_code1, 1, 2)
        grid.addWidget(self._ql_date1, 1, 3)
        grid.addWidget(self._ql_id2, 1, 6)
        grid.addWidget(self._ql_code2, 1, 7)
        grid.addWidget(self._ql_date2, 1, 8)

        grid.addWidget(QLabel("From (-)"), 1, 0)
        grid.addWidget(QLabel("ID"), 0, 1)
        grid.addWidget(QLabel("Codes"), 0, 2)
        grid.addWidget(QLabel("Dates"), 0, 3)

        grid.addWidget(QLabel("To (+)"), 1, 5)
        grid.addWidget(QLabel("ID"), 0, 6)
        grid.addWidget(QLabel("Codes"), 0, 7)
        grid.addWidget(QLabel("Dates"), 0, 8)

        b = QPushButton("<->")
        b.clicked.connect(self._swap_diff)
        grid.addWidget(b, 1, 5)

        self._text = QTextEdit()
        self._text.setReadOnly(True)

        grid.addWidget(self._text, 4, 0, 1, 9)

        w = QWidget()
        w.setLayout(grid)

        self.setCentralWidget(w)

    def _swap_diff(self):
        tmp = self._ql_id1.text()
        self._ql_id1.setText(self._ql_id2.text())
        self._ql_id2.setText(tmp)

        tmp = self._ql_code1.text()
        self._ql_code1.setText(self._ql_code2.text())
        self._ql_code2.setText(tmp)

        tmp = self._ql_date1.text()
        self._ql_date1.setText(self._ql_date2.text())
        self._ql_date2.setText(tmp)

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

        self._windowsMenu = mainMenu.addMenu("Windows")
        self._windowsMenu.aboutToShow.connect(self._build_windows_menu)

        self._build_windows_menu()

        helpMenu = mainMenu.addMenu("Help")
        a = QAction("About ...", self)
        a.triggered.connect(lambda : utils.about(self))
        helpMenu.addAction(a)

    def _build_windows_menu(self):
        utils.build_windows_menu(self._windowsMenu, self)
        return

    def _exit_app(self):
        ret = QMessageBox.question(self, "BOMBrowser", "Do you want to exit from the application ?")
        if ret == QMessageBox.Yes:
            sys.exit(0)

    def do_diff(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self._do_diff()
        except:
            traceback.print_exc()
            QMessageBox.critical(self, "BOMBrowser", "Cannot perform the diff: check the date!")
        finally:
            QApplication.restoreOverrideCursor()

    def _do_diff(self):
        d = db.DB()
        code1, data1 = d.get_bom_by_code_id2(int(self._ql_id1.text()),
                                   self._ql_date1.text())
        code2, data2 = d.get_bom_by_code_id2(int(self._ql_id2.text()),
                                   self._ql_date2.text())

        # put the head of boms to the same ID to enshure to compare the "same" head
        if code1 != code2:
            code3 = max([max(data1.keys()), max(data2.keys())])+1
            data1[code3] = data1[code1]
            data1[code3]["id"] = code3
            data2[code3] = data2[code2]
            data2[code3]["id"] = code3
            data1.pop(code1)
            data2.pop(code2)

        keys = list(set(data1.keys()).union(data2.keys()))
        keys.sort()

        self._text.clear()

        txt = ""

        def is_children_equal(c1, c2):
            for k in ["qty", "each"]:
                if c1[k] != c2[k]:
                    return False

            return True

        def is_codes_equal(c1, c2):
            for k in ["code", "descr", "unit", "iter", "ver"]:
                if c1[k] != c2[k]:
                    return False

            if c1["deps"].keys() != c2["deps"].keys():
                return False

            for k in c1["deps"].keys():
                if not is_children_equal(c1["deps"][k], c2["deps"][k]):
                    return False

            return True

        for key in keys:
            if key in data1.keys() and key in data2.keys():
                if is_codes_equal(data1[key], data2[key]):
                        continue

                txt += "\n"
                # diff between the same code
                txt += " code: %s rev %s - %s\n"%(data1[key]["code"], data1[key]["ver"], data1[key]["descr"])
                for key2 in ["code", "descr", "unit", "ver"]:
                    if data1[key][key2] == data2[key][key2]:
                        continue

                    txt += "     -%s: %s\n"%(key2, data1[key][key2])
                    txt += "     +%s: %s\n"%(key2, data2[key][key2])

                child_ids = list(set(data1[key]["deps"].keys()).union(
                                     data2[key]["deps"].keys()))
                child_ids.sort()

                for child_id in child_ids:
                    if child_id in data1[key]["deps"].keys() and child_id in data2[key]["deps"].keys():
                        if is_children_equal(data1[key]["deps"][child_id], data2[key]["deps"][child_id]):
                            continue

                        child1 =data1[key]["deps"][child_id]
                        txt += "         -%f / %f: %s rev %s - %s\n"%(
                            child1["qty"], child1["each"],
                            data1[child_id]["code"],
                            data1[child_id]["ver"],
                            data1[child_id]["descr"])
                        child2 =data2[key]["deps"][child_id]
                        txt += "         +%f / %f: %s rev %s - %s\n"%(
                            child2["qty"], child2["each"],
                            data2[child_id]["code"],
                            data2[child_id]["ver"],
                            data2[child_id]["descr"])
                    elif child_id in data1[key]["deps"].keys():
                        child1 =data1[key]["deps"][child_id]
                        txt += "         -%f / %f: %s rev %s - %s\n"%(
                            child1["qty"], child1["each"],
                            data1[child_id]["code"],
                            data1[child_id]["ver"],
                            data1[child_id]["descr"])
                    else:
                        child2 =data2[key]["deps"][child_id]
                        txt += "         +%f / %f: %s rev %s - %s\n"%(
                            child2["qty"], child2["each"],
                            data2[child_id]["code"],
                            data2[child_id]["ver"],
                            data2[child_id]["descr"])

            elif  key in data1.keys():
                txt += "\n"
                txt += "-code: %s rev %s - %s\n"%(data1[key]["code"], data1[key]["ver"], data1[key]["descr"])
                txt += "     [....]\n"
            else:
                txt += "\n"
                txt += "+code: "+data2[key]["code"]+"\n"
                for key2 in  ["descr", "unit", "ver"]:
                    txt += "     +%s: %s\n"%(key2, data2[key][key2])

                child_ids = list(data2[key]["deps"].keys())
                child_ids.sort()
                for child_id in child_ids:
                    child2 =data2[key]["deps"][child_id]
                    txt += "         +%f / %f: %s rev %s - %s\n"%(
                            child2["qty"], child2["each"],
                            data2[child_id]["code"],
                            data2[child_id]["ver"],
                            data2[child_id]["descr"])

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

        self.setWindowTitle("BOMBrowser - Diff dialog")

        b=QPushButton("Hide")
        b.clicked.connect(self._do_hide)
        grid.addWidget(b,10, 2)

        self.setLayout(grid)

        self._id1 = ""
        self._id2 = ""
        self._code1 = ""
        self._code2 = ""
        self._date1 = ""
        self._date2 = ""

    def _do_diff(self):
        w = DiffWindow(self._id1, self._code1, self._date1,
                       self._id2, self._code2, self._date2,
                      parent=self)
        w.do_diff()
        w.show()
        self._do_hide()

    def _do_hide(self):
        self.hide()
        id_ = ""
        code = ""
        date = ""
        self._id1 = id_
        self._code1 = code
        self._date1 = date
        self._ql_id1.setText(id_)
        self._ql_code1.setText(code)
        self._ql_date1.setText(date)
        self._id2 = id_
        self._code2 = code
        self._date2 = date
        self._ql_id2.setText(id_)
        self._ql_code2.setText(code)
        self._ql_date2.setText(date)

    def set_from(self, code_id, code, date):
        self._id1 = code_id
        self._code1 = code
        self._date1 = date
        self._ql_id1.setText(code_id)
        self._ql_code1.setText(code)
        self._ql_date1.setText(date)

    def set_to(self, code_id, code, date):
        self._id2 = code_id
        self._code2 = code
        self._date2 = date
        self._ql_id2.setText(code_id)
        self._ql_code2.setText(code)
        self._ql_date2.setText(date)
        if self._code1 != "":
            self._do_diff()

_diffDialog = None

def set_from(code_id, parent):
    if not code_id:
        QApplication.beep()
        return

    d = db.DB()
    if not d.is_assembly(code_id):
        QApplication.beep()
        QMessageBox.critical(parent, "BOMBrowser", "The item is not an assembly")
        return

    dlg = selectdategui.SelectDate(code_id, parent)
    ret = dlg.exec_()
    if not ret:
        return

    (code, date_from, descr) = dlg.get_result()

    global _diffDialog
    if _diffDialog is None:
        _diffDialog = DiffDialog()
    _diffDialog.show()
    _diffDialog.set_from(str(code_id), code, date_from)

def set_to(code_id, parent):
    if not code_id:
        QApplication.beep()
        return

    d = db.DB()
    if not d.is_assembly(code_id):
        QApplication.beep()
        QMessageBox.critical(parent, "BOMBrowser", "The item is not an assembly")
        return

    dlg = selectdategui.SelectDate(code_id, parent)
    ret = dlg.exec_()
    if not ret:
        return

    (code, date_from, descr) = dlg.get_result()
    global _diffDialog
    if _diffDialog is None:
        _diffDialog = DiffDialog()
    _diffDialog.show()
    _diffDialog.set_to(str(code_id), code, date_from)

