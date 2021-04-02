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

import sys, configparser

from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QLabel, QLineEdit, QCheckBox
from PySide2.QtWidgets import QGridLayout, QWidget, QPushButton
from PySide2.QtWidgets import QMessageBox, QDialog
from PySide2.QtCore import Qt
import pprint

import db, codegui, diffgui, editcode
import exporter, utils, selectdategui, cfg

class CopyCode(QDialog):
    def __init__(self, rev_id, parent):
        QDialog.__init__(self, parent)
        self._rid = rev_id
        self._results = None
        self._new_code = None
        self._new_rid = None
        self._start_editor = None

        self._db = db.DB()
        data = self._db.get_code_by_rid(self._rid)

        self._old_code = data["code"]
        self._old_descr = data["descr"]
        self._old_ver = data["ver"]
        self._old_iter = data["iter"]
        self._date_from = data["date_from"]
        self._date_from_days = data["date_from_days"]
        self._date_to = data["date_to"]
        self._date_to_days = data["date_to_days"]
        self._code_id = data["id"]

        data = self._db.get_dates_by_code_id3(self._code_id)

        i = 0
        while i < len(data) - 1 and data[i][2] == db.prototype_date:
            i += 1
        self._last_date = db.days_to_txt(data[i][2])
        self._last_date_days = data[i][2]
        self._last_iter = data[i][6]
        self._last_ver = data[i][5]
        self._last_revid = data[i][4]

        self._proto_exists = data[0][2] == db.prototype_date

        self._descr_force_uppercase = cfg.config()["BOMBROWSER"].get("description_force_uppercase", "1")
        self._code_force_uppercase = cfg.config()["BOMBROWSER"].get("code_force_uppercase", "1")

        self._init_gui()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def _init_gui(self):
        grid = QGridLayout()
        self.setWindowTitle("BOMBrowser - Copy / Revise code")
        #w = QWidget()
        #w.setLayout(grid)
        #self.setCentralWidget(w)

        gold = QGroupBox("Old")
        gnew = QGroupBox("New")
        gdescr = QGroupBox("")

        grid.addWidget(QLabel("Old"), 9, 1)
        grid.addWidget(QLabel("New"), 9, 2)

        grid.addWidget(QLabel("Code:"), 10, 0)
        self._l_old_code = QLabel(self._old_code)
        grid.addWidget(self._l_old_code, 10, 1)
        self._l_new_code = QLineEdit(self._old_code)
        grid.addWidget(self._l_new_code, 10, 2)

        grid.addWidget(QLabel("Iter:"), 11, 0)
        self._l_old_revision = QLabel("%d"%(self._old_iter))
        grid.addWidget(self._l_old_revision, 11, 1)
        self._l_new_iter = QLabel()
        grid.addWidget(self._l_new_iter, 11, 2)

        grid.addWidget(QLabel("Rev:"), 12, 0)
        self._l_old_rev = QLabel(self._old_ver)
        grid.addWidget(self._l_old_rev, 12, 1)
        self._l_new_rev = QLineEdit(self._old_ver)
        grid.addWidget(self._l_new_rev, 12, 2)

        grid.addWidget(QLabel("Date from:"), 13, 0)
        self._l_old_date_from = QLabel(self._date_from)
        grid.addWidget(self._l_old_date_from, 13, 1)
        self._l_new_date_from = QLineEdit(
            db.days_to_iso(db.now_to_days())
        )
        grid.addWidget(self._l_new_date_from, 13, 2)


        grid.addWidget(QLabel("Old Description:"), 17, 0)
        self._l_old_descr = QLabel(self._old_descr)
        grid.addWidget(self._l_old_descr, 17, 1, 1, 2)
        grid.addWidget(QLabel("New Description:"), 18, 0)
        self._l_new_descr = QLineEdit(self._old_descr)
        grid.addWidget(self._l_new_descr, 18, 1, 1, 2)

        self._cb_copy_rev = QCheckBox("Copy")
        self._cb_copy_rev.stateChanged.connect(self._change_copy_btn)
        self._cb_copy_rev.setCheckState(Qt.CheckState.Unchecked)
        grid.addWidget(self._cb_copy_rev, 20, 0)

        self._cb_copy_docs = QCheckBox("Copy documents")
        self._cb_copy_docs.setCheckState(Qt.CheckState.Checked)
        grid.addWidget(self._cb_copy_docs, 20, 1)

        self._cb_copy_props = QCheckBox("Copy properties")
        self._cb_copy_props.setCheckState(Qt.CheckState.Checked)
        grid.addWidget(self._cb_copy_props, 20, 2)

        self._cb_start_edit = QCheckBox("Start edit dialog after the copy/revision")
        self._cb_start_edit.setCheckState(Qt.CheckState.Checked)
        grid.addWidget(self._cb_start_edit, 21, 0, 1, 2)

        self._cb_proto = QCheckBox("Prototype")
        self._cb_proto.stateChanged.connect(self._change_proto_btn)
        self._cb_proto.setCheckState(Qt.CheckState.Unchecked)
        grid.addWidget(self._cb_proto, 21, 2)


        pb = QPushButton("Cancel")
        pb.clicked.connect(self._close)
        grid.addWidget(pb, 30, 0)

        pb = QPushButton("Copy/Revise")
        pb.clicked.connect(self._do)
        grid.addWidget(pb, 30, 2)

        self.setLayout(grid)

        self._change_copy_btn()
        self._change_proto_btn()

    def _check_values(self):
        if self._cb_proto.checkState() == Qt.CheckState.Checked:
            newdate = db.prototype_date

            if (self._proto_exists and
                self._cb_copy_rev.checkState() == Qt.CheckState.Unchecked):
                    QMessageBox.critical(self,
                        "BOMBrowser - error",
                        "A prototype of this already exists")
                    return False
        else:
            try:
                newdate = db.iso_to_days(self._l_new_date_from.text())
            except:
                QMessageBox.critical(self,
                    "BOMBrowser - error",
                    "The new 'From date' field format is incorrect")
                return False

        if self._cb_copy_rev.checkState() == Qt.CheckState.Unchecked:
            if (newdate <= self._last_date_days and
                self._last_date_days != db.prototype_date):
                    QMessageBox.critical(self,
                        "BOMBrowser - error",
                        "The new 'From date' is earlier than the previous ones")
                    return False

        if self._cb_copy_rev.checkState() == Qt.CheckState.Checked:
            d = db.DB()
            data = d.get_codes_by_code(self._l_new_code.text())
            if not data is None and len(data) != 0:
                QMessageBox.critical(self,
                    "BOMBrowser - error",
                    "The new Code already exists")
                return False

        return True

    def _do(self):
        self._start_editor = self._cb_start_edit.checkState() == Qt.CheckState.Checked

        if not self._check_values():
            return

        reply = QMessageBox.question(self, "Copy/revise confirmation",
                                "Do you want to copy/revise the code ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply == QMessageBox.No:
            return

        d = db.DB()

        code = self._l_new_code.text()
        descr = self._l_new_descr.text()
        if self._descr_force_uppercase == "1":
                descr = descr.upper()
        if self._code_force_uppercase == "1":
                code = code.upper()

        try:
            if self._cb_proto.checkState() == Qt.CheckState.Checked:
                newdate = db.prototype_date
            else:
                newdate = db.iso_to_days(self._l_new_date_from.text())
            if self._cb_copy_rev.checkState() == Qt.CheckState.Checked:
                new_rid = d.copy_code(code,
                    self._rid,
                    descr,
                    self._l_new_rev.text(),
                    self._cb_copy_props.checkState() == Qt.CheckState.Checked,
                    self._cb_copy_docs.checkState() == Qt.CheckState.Checked,
                    new_date_from_days=newdate)
                self._new_code = code
                self._new_rid = new_rid
            else:
                new_rid = d.revise_code(self._rid,
                    descr,
                    self._l_new_rev.text(),
                    self._cb_copy_props.checkState() == Qt.CheckState.Checked,
                    self._cb_copy_docs.checkState() == Qt.CheckState.Checked,
                    new_date_from_days=newdate)

            self._new_code = code
            self._new_rid = new_rid
        except db.DBException as e:
            QMessageBox.critical(self,
                "BOMBrowser - error",
                "Cannot copy/revise the code " + self._l_old_code.text() + "\n" +
                "The error is: " + "\n" + "-" * 20 + "\n" + e.args[0] +
                "\n" + "-" * 20)
            return
        except:
            utils.show_exception(msg="Cannot copy/revise the code " +
                self._l_old_code.text())
            return

        self.accept()

    def getNewCode(self):
        return self._new_code

    def getNewRId(self):
        return self._new_rid

    def _close(self):
        reply = QMessageBox.question(self, "Exit dialog", "Close dialog",
                                QMessageBox.Yes, QMessageBox.No);
        self._start_editor = self._cb_start_edit.checkState() == Qt.CheckState.Checked
        if reply == QMessageBox.Yes:
            self.reject()

    def _change_proto_btn(self):
        if self._cb_proto.checkState() == Qt.CheckState.Checked:
            self._l_new_date_from.setReadOnly(True)
            self._l_new_date_from.setEnabled(False)
            self._l_new_date_from.setText("PROTOTYPE")
        else:
            self._l_new_date_from.setReadOnly(False)
            self._l_new_date_from.setEnabled(True)
            self._l_new_date_from.setText(
                db.days_to_iso(db.now_to_days())
            )
        self._update_new_iter()

    def _change_copy_btn(self):
        if self._cb_copy_rev.checkState() == Qt.CheckState.Checked:
            self._l_new_code.setReadOnly(False)
            self._l_new_code.setEnabled(True)
            self._l_new_rev.setText("0")
        else:
            self._l_new_code.setText(self._l_old_code.text())
            self._l_new_code.setReadOnly(True)
            self._l_new_code.setEnabled(False)
            new_rev = self._l_old_rev.text()
            try:
                if new_rev == '':
                    new_rev = '0'
                else:
                    lastchar = new_rev[-1]
                    if new_rev == '0':
                        new_rev = 'A'
                    elif lastchar >= '0' and lastchar <= '9':
                        try:
                            new_rev = str(int(new_rev)+1)
                        except:
                            new_rev = new_rev +"_bis"
                    elif lastchar >= 'A' and lastchar <= 'Y':
                        new_rev = new_rev[:-1]+chr(ord(lastchar)+1)
                    else:
                        new_rev = new_rev +"_bis"
            except:
                raise
                new_rev = new_rev +"_bis"

            self._l_new_rev.setText(new_rev)
        self._update_new_iter()

    def _update_new_iter(self):
        if self._cb_proto.checkState() == Qt.CheckState.Checked:
            self._l_new_iter.setText(str(db.prototype_iter))
        elif self._cb_copy_rev.checkState() == Qt.CheckState.Checked:
            self._l_new_iter.setText("0")
        else:
            self._l_new_iter.setText("%d"%(self._last_iter+1))

    def shouldStartEditor(self):
        return self._start_editor


def revise_copy_code(code_id, parent):
        d = db.DB()

        assert(parent)
        w = selectdategui.SelectDate(code_id, parent, only_data_code=True)
        ret = w.exec_()
        if not ret:
            return None

        (code, date_from_days) = w.get_code_and_date_from_days()
        if code == 0:
            return None

        data = d.get_code(code_id, date_from_days)
        rid = data["rid"]

        revise_copy_code_by_rid(rid)

def revise_copy_code_by_rid(rid):
        w = CopyCode(rid, None)
        if not w.exec_():
            return None

        if w.getNewCode() is None:
            return None

        if not w.shouldStartEditor():
            QMessageBox.information(parent, "BOMBrowser",
                "Success: you created a new code/revision")
            return None

        d = db.DB()
        codes = d.get_codes_by_code(w.getNewCode())
        if len(codes):
            w2 = editcode.EditWindow(codes[0][0])
            w2.show()
