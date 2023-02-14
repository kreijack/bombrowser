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

import sys

from PySide2.QtWidgets import  QWidget, QCalendarWidget
from PySide2.QtWidgets import  QPushButton
from PySide2.QtWidgets import  QGridLayout
from PySide2.QtWidgets import  QLineEdit, QHBoxLayout, QDialog
from PySide2.QtCore import  Qt, QRegExp, Signal
from PySide2.QtGui import QRegExpValidator, QValidator

import db, codegui, utils
import cfg

class BBDateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QGridLayout()
        
        self._dt = QCalendarWidget()
        self._dt.activated.connect(self.accept)
        l.addWidget(self._dt, 1, 1, 1, 2)
        
        b = QPushButton("Ok")
        b.clicked.connect(self.accept)
        l.addWidget(b, 10, 1)

        b = QPushButton("Cancel")
        b.clicked.connect(self.reject)
        l.addWidget(b, 10, 2)

        self.setLayout(l)

    def selectedDate(self):
        return self._dt.selectedDate().toString(Qt.ISODate)

class _DateValidator(QValidator):
    def __init__(self, parent=None, allow_prototype=True,
                    allow_cmp=True):
        super().__init__()
        self._intermediate = QRegExp("^\d{0,4}-?\d{0,2}-?\d{0,2}$")
        self._ok = QRegExp("^\d{4,4}-\d{2,2}-\d{2,2}$")
        self._allow_prototype=allow_prototype
        self._allow_cmp=allow_cmp

    def validate(self, input_, pos):
        if len(input_) == 0:
            return (QValidator.Acceptable, input_, pos)

        if (not (input_[0] in "!=<>") and 
            not input_[0].isdigit()
            and not (self._allow_prototype and 
                 input_.upper() == "PROTOTYPE"[:len(input_)])
            ):
                return (QValidator.Invalid, input_, pos)

        s = input_
        if self._allow_cmp:
            if input_[0] in "!=<>":
                s = input_[1:]

        if self._allow_prototype and s.upper() == "PROTOTYPE":
            return (QValidator.Acceptable, input_, pos)

        if s.upper() == "PROTOTYPE"[:len(s)]:
            return (QValidator.Intermediate, input_, pos)

        if len(s) == 0:
            return (QValidator.Intermediate, input_, pos)

        if self._intermediate.indexIn(s) == -1:
            return (QValidator.Invalid, input_, pos)

        if self._ok.indexIn(s) == -1:
            return (QValidator.Intermediate, input_, pos)

        try:
            db.iso_to_days(s)
        except:
            return (QValidator.Intermediate, input_, pos)

        return (QValidator.Acceptable, input_, pos)

class Validator:
    def __init__(self, w, v):
        self._validator = v
        self._widget = w

    def __call__(self, s):
        if s == "":
            self._widget.setStyleSheet('background:')
            return

        r, _, _ = self._validator.validate(s, len(s))
        if r == QValidator.Invalid:
            colour = 'orange'
        elif r == QValidator.Intermediate:
            colour = 'lightyellow'
        else:
            colour = '' #lightgreen'
        self._widget.setStyleSheet('background:%s' % colour)

class BBDatesLineEdit(QWidget):
    textChanged = Signal(str)
    def __init__(self, text='', parent=None, 
                 allow_prototype=True, allow_cmp=True):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._le = QLineEdit()
        self.setText(text)
        self._le.setValidator(_DateValidator(
                                allow_prototype=allow_prototype,
                                allow_cmp=allow_cmp))
        self._le.textChanged.connect(Validator(self._le, _DateValidator()))
        self._le.textChanged.connect(self.textChanged)

        layout.addWidget(self._le)

        if allow_prototype:
            b = QPushButton("P")
            width = b.fontMetrics().boundingRect("P").width() + 7
            b.setMaximumWidth(width)
            b.clicked.connect(self._set_prototype)
            layout.addWidget(b)

        b = QPushButton("...")
        width = b.fontMetrics().boundingRect("...").width() + 7
        b.setMaximumWidth(width)
        b.clicked.connect(self._show_calendar)
        layout.addWidget(b)

        self.returnPressed = self._le.returnPressed

    def _set_prototype(self):
        s = self._le.text()
        if len(s) and s[0] in "=!<>":
            s = s[0]
        else:
            s = ""
        self._le.setText(s + "PROTOTYPE")

    def text(self):
        s = self._le.text()
        return s
    
    def setText(self, t):
        self._le.setText(t)

    def _show_calendar(self):
        d = BBDateDialog(self)
        if d.exec_() == d.Rejected:
            return
        s = self._le.text()
        if len(s) and s[0] in "=!<>":
            s = s[0]
        else:
            s = ""
        self._le.setText(s + d.selectedDate())
        
    def setReadOnly(self, v):
        self._le.setReadOnly(v)
        

if __name__ == '__main__':
    from PySide2.QtWidgets import  QApplication
    app = QApplication(sys.argv)
    bb = BBDatesLineEdit(allow_prototype=False, allow_cmp=False)
    bb.show()
    sys.exit(app.exec_())

        
