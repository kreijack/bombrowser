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

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QAction
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox

def about(w):
    QMessageBox.about(w, "BOMBrowser - about",
        "BOMBrowser v0.2\n"+
        "Copyright 2020 G.Baroncelli\n")

def clean_menu(m):
        as_ = list(m.actions())
        for a in as_:
            m.removeAction(a)

def get_windows_list():

    codewindows = []
    bomwindows = []
    diffwindows = []
    for w in QApplication.topLevelWidgets():
        if not w.isWindow():
            continue
        t = w.windowTitle()
        if len(t) < 5:
            continue

        if t == "BOMBrowser - Diff dialog":
            continue

        if t.startswith("BOMBrowser - Diff window"):
            diffwindows.append((t, w))
        elif (t.startswith("BOMBrowser - Assembly") or
              t.startswith("BOMBrowser - Where used")):
            bomwindows.append((t, w))
        elif t.startswith("BOMBrowser - Codes list"):
            codewindows.append((t, w))

    return (codewindows, bomwindows, diffwindows)

def build_windows_menu(m, win, codes_list=True):
    clean_menu(m)
    c, b, d = get_windows_list()
    class ShowWindow():
        def __init__(self, w):
            self._w = w
        def __call__(self):
            self._w.raise_()
            self._w.setWindowState(Qt.WindowActive)
            self._w.showNormal()
            self._w.activateWindow()
            self._w.show()

    separator = False
    if codes_list:
        for (t, w) in c:

            a = QAction(t, win)
            if not separator:
                # add shortcut only for the first item
                a.setShortcut("Ctrl+L")
            a.triggered.connect(ShowWindow(w))
            m.addAction(a)
            separator = True

    if len(b):
        if separator:
            m.addSeparator()
        for t,w in b:
            a = QAction(t, win)
            a.triggered.connect(ShowWindow(w))
            m.addAction(a)

        separator = True

    if len(d):
        if separator:
            m.addSeparator()
        for t,w in d:
            a = QAction(t, win)
            a.triggered.connect(ShowWindow(w))
            m.addAction(a)

        separator = True

