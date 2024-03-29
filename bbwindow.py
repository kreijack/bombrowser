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

from PySide2.QtWidgets import QAction
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QMessageBox

from version import version
import listcodegui

window_title = "BOMBrowser " + version

_bbmainwindows_list = set()

class BBMainWindow(QMainWindow):
    def __init__(self, parent=None):
        global _bbmainwindows_list

        QMainWindow.__init__(self, parent)

        _bbmainwindows_list.add(self)

    def setWindowTitle(self, title):
        t = window_title + " - " + title
        QMainWindow.setWindowTitle(self, t)

    def closeEvent(self, event):
        global _bbmainwindows_list

        _bbmainwindows_list.remove(self)

        QMainWindow.closeEvent(self, event)

    def _get_windows_list(self):
        global _bbmainwindows_list

        windows = dict()
        for w in _bbmainwindows_list:

            if w is self:
                continue

            t = w.windowTitle()

            i1 = t.find(" - ")
            i2 = t.find(":", i1)
            wkey = t[i1+3:i2]
            if not wkey in windows:
                windows[wkey] = []
            windows[wkey].append((t, w))

        ret = []
        keys = list(windows.keys())
        keys.sort()
        for k in keys:
            ret.append(windows[k])
        return ret

    def build_windows_menu(self, main_menu, title="Windows", win=None):
        if win is None:
            win = self

        wm = main_menu.addMenu(title)
        # to install the shortcut key CTRL-L/CTRL-W
        self._build_windows_menu(wm, win)
        wm.aboutToShow.connect(
            lambda : self._build_windows_menu(wm, win))

    def _build_windows_menu(self, m, win):
        global _bbmainwindows_list

        for a in list(m.actions()):
            m.removeAction(a)

        class ShowWindow():
            def __init__(self, w):
                self._w = w
            def __call__(self):
                self._w.raise_()
                self._w.setWindowState(Qt.WindowActive)
                self._w.showNormal()
                self._w.activateWindow()
                self._w.show()

        def close_all_other_windows():
            ws = list(_bbmainwindows_list)
            for w in ws:
                if not w is self:
                    w.close()

        a = QAction("Close all other windows", win)
        a.setShortcut("Ctrl+W")
        m.addAction(a)
        a.triggered.connect(close_all_other_windows)

        a = QAction("New codes list window", win)
        a.setShortcut("Ctrl+L")
        m.addAction(a)
        a.triggered.connect(lambda : listcodegui.CodesWindow().show())

        separator = True

        for l in win._get_windows_list():
            if len(l):
                if separator:
                    m.addSeparator()
                for (t, w) in l:
                    a = QAction(t, win)
                    a.triggered.connect(ShowWindow(w))
                    m.addAction(a)

                separator = True


    def _show_about(self, connection=""):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("BOMBrowser - about");
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setText(window_title + "\n"
            "Copyright 2020,2021 G.Baroncelli<br>"
            "<br>"
            "<a href=https://gitlab.com/kreijack/bombrowser>"
            "https://gitlab.com/kreijack/bombrowser</a><br><br>" +
            connection)
        msgBox.exec_();
