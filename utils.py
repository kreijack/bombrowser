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

import sys, traceback

from PySide2.QtWidgets import QAction
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox, QMainWindow

from version import version
import asmgui, editcode, copycodegui, diffgui, db

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

def generate_codes_context_menu(code_id=None, rid=None, dt=None,
                                    menu=None, parent=None):

    def _edit_code(code_id, rid):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]

        editcode.edit_code_by_code_id(code_id)

    def _revise_code(code_id, rid, parent):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]

        copycodegui.revise_copy_code(code_id, parent)

    def _set_diff_from(scode_id, rid, parent):
        if not rid is None:
            diffgui.set_from_by_rid(rid)
            return

        diffgui.set_from(code_id, parent)

    def _set_diff_to(code_id, rid, parent):
        if not rid is None:
            diffgui.set_to_by_rid(rid)
            return

        diffgui.set_to(code_id, parent)

    def _show_assembly(code_id, rid, parent):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]

        asmgui.show_assembly(code_id, parent)

    def _show_this_assembly(code_id, date_from_days, rid):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]
            date_from_days = data["date_from_days"]

        asmgui.show_assembly_by_date(code_id, date_from_days)

    def _show_latest_assembly(code_id, rid):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]

        asmgui.show_latest_assembly(code_id)

    def _show_proto_assembly(code_id, rid):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]

        asmgui.show_proto_assembly(code_id)

    def _show_where_used(code_id, rid):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]

        asmgui.where_used(code_id)

    def _show_valid_where_used(code_id, rid):
        if code_id is None:
            d = db.DB()
            data = d.get_code_by_rid(rid)
            code_id = data["id"]

        asmgui.valid_where_used(code_id)


    menu.addAction("Show latest assembly").triggered.connect(
        lambda : _show_latest_assembly(code_id, rid))
    menu.addAction("Where used").triggered.connect(
        lambda : _show_where_used(code_id, rid))
    menu.addAction("Valid where used").triggered.connect(
        lambda : _show_valid_where_used(code_id, rid))
    menu.addAction("Show assembly by date").triggered.connect(
        lambda : _show_assembly(code_id, rid, parent))
    if (not code_id is None and not dt is None) or not rid is None:
        menu.addAction("Show this assembly").triggered.connect(
            lambda : _show_this_assembly(code_id, dt, rid))
    menu.addAction("Show prototype assembly").triggered.connect(
        lambda : _show_proto_assembly(code_id, rid))
    menu.addSeparator()
    menu.addAction("Copy/revise code ...").triggered.connect(
        lambda : _revise_code(code_id, rid, parent))
    menu.addAction("Edit code ...").triggered.connect(
        lambda : _edit_code(code_id, rid))
    menu.addSeparator()
    menu.addAction("Diff from...").triggered.connect(
        lambda : _set_diff_from(code_id, rid, parent))
    menu.addAction("Diff to...").triggered.connect(
        lambda : _set_diff_to(code_id, rid, parent))

    return menu

