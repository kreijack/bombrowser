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

import sys, traceback

from PySide2.QtWidgets import QAction
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox, QMainWindow

version = "v0.4.2b3"

def __show_exception(exc_type, exc_value, exc_traceback,
        title, msg):

    exc_info = (exc_type, exc_value, exc_traceback)
    excs = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                                 '{0}: {1}'.format(exc_type.__name__, exc_value)])
    msg = msg + "\n" + "-" * 30 + "\n" + excs + "\n" + "-" * 30 + "\n"

    QMessageBox.critical(None, title, msg)

def _show_exception(exc_type, exc_value, exc_traceback):
    __show_exception(exc_type, exc_value, exc_traceback,
        "BOMBrowser - %s"%(version),
        "Catch 'uncautch' exception:")

def show_exception(title = "BOMBrowser - %s"%(version),
                   msg = "BOMBrowser - got exception"):
    __show_exception(*sys.exc_info(), title, msg)

_bbmainwindows_list = []
_bbmainwindows_list_cnt = 0


window_title = "BOMBrowser " + version

class BBMainWindow(QMainWindow):
    def __init__(self, parent=None):
        global _bbmainwindows_list_cnt
        global _bbmainwindows_list

        QMainWindow.__init__(self, parent)
        self.__bbmainwindow_list_cnt = _bbmainwindows_list_cnt
        _bbmainwindows_list_cnt += 1

        _bbmainwindows_list.append([self.__bbmainwindow_list_cnt,
            self, ""])

    def setWindowTitle(self, title):
        global _bbmainwindows_list_cnt
        global _bbmainwindows_list

        QMainWindow.setWindowTitle(self, title)

        for i in _bbmainwindows_list:
            if i[0] == self.__bbmainwindow_list_cnt:
                i[2] = title
                break

    def closeEvent(self, event):
        global _bbmainwindows_list_cnt
        global _bbmainwindows_list

        for i in range(len(_bbmainwindows_list)):
            if _bbmainwindows_list[i][0] == self.__bbmainwindow_list_cnt:
                _bbmainwindows_list.pop(i)
                break

        QMainWindow.closeEvent(self, event)

    def _get_windows_list(self):
        global _bbmainwindows_list_cnt
        global _bbmainwindows_list

        codewindows = []
        bomwindows = []
        diffwindows = []
        editwindows = []
        for (id_, w, t) in _bbmainwindows_list:

            if id_ == self.__bbmainwindow_list_cnt:
                continue

            if t.startswith(window_title + " - Diff window"):
                diffwindows.append((t, id_))
            elif t.startswith(window_title + " - Edit code"):
                editwindows.append((t, id_))
            elif (t.startswith(window_title + " - Assembly") or
                  t.startswith(window_title + " - Valid where used") or
                  t.startswith(window_title + " - Where used")):
                bomwindows.append((t, id_))
            elif t.startswith(window_title + " - Codes list"):
                codewindows.append((t, id_))

        return (codewindows, bomwindows, diffwindows, editwindows)

    def build_windows_menu(self, main_menu, title="Windows", win=None):
        if win is None:
            win = self

        wm = main_menu.addMenu(title)
        self._build_windows_menu(wm, win)
        wm.aboutToShow.connect(
            lambda : self._build_windows_menu(wm, win))

    def _build_windows_menu(self, m, win):

        global _bbmainwindows_list_cnt
        global _bbmainwindows_list

        for a in list(m.actions()):
            m.removeAction(a)

        c, b, d, e = win._get_windows_list()

        class ShowWindow():
            def __init__(self, id_):
                self._id = id_
            def __call__(self):
                for (id_, w, t) in _bbmainwindows_list:
                    if id_ == self._id:
                        w.raise_()
                        w.setWindowState(Qt.WindowActive)
                        w.showNormal()
                        w.activateWindow()
                        w.show()
                        break

        separator = False

        for (t, w) in c:
            a = QAction(t, win)
            # add the CTRL-L short cut only for the first window
            if not separator:
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

        if len(e):
            if separator:
                m.addSeparator()
            for t,w in e:
                a = QAction(t, win)
                a.triggered.connect(ShowWindow(w))
                m.addAction(a)

            separator = True

class BBMainWindowNotClose(BBMainWindow):
    def __init__(self, parent=None):
        BBMainWindow.__init__(self, parent)

    def closeEvent(self, event):
        if len(_bbmainwindows_list) == 1:
            BBMainWindow.closeEvent(self, event)
        else:
            QMainWindow.closeEvent(self, event)


def about(w, connection=""):
    msgBox = QMessageBox(w)
    msgBox.setWindowTitle("BOMBrowser - about");
    msgBox.setTextFormat(Qt.RichText)
    msgBox.setText(window_title + "\n"
        "Copyright 2020,2021 G.Baroncelli<br>"
        "<br>"
        "<a href=https://gitlab.com/kreijack/bombrowser>"
        "https://gitlab.com/kreijack/bombrowser</a><br><br>" +
        connection)
    msgBox.exec_();

class Callable:
    def __init__(self, f, *args, **kwargs):
        self._f = f
        self._args = args
        self._kwargs = kwargs
    def __call__(self):
        return self._f(*self._args, **self._kwargs)

def catch_exception(f):
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            QMessageBox.critical(None, "BOMBrowser",
                "During call of function '%r' an exception occurred:"%(f) +
                "-"*30 + "\n" +
                '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb)) +
                "-"*30 + "\n")

            print('\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
            raise

    return wrapper
