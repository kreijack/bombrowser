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

from PySide2.QtWidgets import QPushButton, QMainWindow, QTextEdit
from PySide2.QtWidgets import QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import Qt

import customize, bbwindow, utils

class ShowResult(bbwindow.BBMainWindow):
    def __init__(self, txt='', bom_descr = '', parent=None):
        bbwindow.BBMainWindow.__init__(self, parent=parent)

        l = QVBoxLayout()
        self._edit = QTextEdit()
        self._edit.setReadOnly(True)
        l.addWidget(self._edit)

        b = QPushButton("Close")
        b.clicked.connect(self.close)
        l.addWidget(b)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)
        self.resize(800, 600)
        self.setWindowTitle('BOM Checker: ' + bom_descr)

        self.setHtml(txt)

    def setHtml(self, txt):
        self._edit.setHtml(txt)


def loop_check(root, data):

    local = { "path": [],
             "res": "" }

    def iterate(n):

        if n in local["path"]:
            local["res"] += "<font color=red>ERROR</font color=red>"
            local["res"] += "&nbsp;Loop detect:&nbsp;"

            i = local["path"].index(n)
            local["res"] += ",&nbsp;".join([data[k]["code"] for k in local["path"][i:] + [n]])
            local["res"] += "<br>\n"
            return
        local["path"].append(n)
        for child in data[n]["deps"]:
            iterate(child)
        local["path"] = local["path"][:-1]

    iterate(root)

    return local["res"]


def run_bom_tests(root, data, bom_descr):

    with utils.OverrideCursor():
        res = ""
        checkers = [loop_check] + customize.get_bom_checker_list()
        for check in checkers:
            res += check(root, data)

    if res == '':
        res = "<font color=green><H1>Success</H1></font><br><\n>"
        res += "No problem detect"
    else:
        res = "<font color=red><H1>Error</H1></font><br><\n><hr>\n" + res

    w = ShowResult(bom_descr = bom_descr)
    w.setHtml(res)
    w.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    d = ShowResult()
    d.setHtml("""
        <h1>Test</h1><br>
        <font color=red>Red test </font>
    """)
    d.show()
    sys.exit(app.exec_())
