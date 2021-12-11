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

import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMessageBox

import cfg, db
import utils
import listcodegui

def main(args):

    if len(args) > 1 and args[1] == "--self-test":
        import exporter
        import importer
        import test_db

        for m in ["exporter", "importer", "test_db", "utils", "db"]:
            test_db.run_test(sys.argv[2:], sys.modules[m], m)
        return


    app = QApplication(sys.argv)

    sys.excepthook = utils._show_exception

    try:
        cfg.init()
    except:
        utils.show_exception(msg="Cannot load configuration: may be bombroser.ini is missing ?\nAbort\n")
        return

    fontscale = float(cfg.config()["BOMBROWSER"].get("scalefont", "1.0"))
    f = app.font()
    f.setPointSize(f.pointSize() * fontscale)
    app.setFont(f)

    try:
        d = db.DB()
        data = d.get_config()
    except:
        utils.show_exception(msg="Cannot connect to database\nAbort\n")
        return

    cfg.update_cfg(data)

    w = listcodegui.CodesWindow()
    w.show()

    i = 1
    while i < len(args):
        if args[i] == "--whereused":
            import asmgui
            i += 1
            asmgui.where_used(int(args[i]))
        elif args[i] == "--validwhereused":
            import asmgui
            i += 1
            asmgui.valid_where_used(int(args[i]))
        elif args[i] == "--showassembly":
            import asmgui
            i += 1
            asmgui.show_assembly(int(args[i]), None)
        elif args[i] == "--showlatestassembly":
            import asmgui
            i += 1
            asmgui.show_latest_assembly(int(args[i]))
        elif args[i] == "--editcode":
            import editcode
            i += 1
            editcode.edit_code_by_code_id(int(args[i]))
        elif args[i] == "--test-exception":
            _ = 1/0
        elif args[i] == "--manage-db":
            db.main("bombrowser --manage-db", args[i+1:])
            sys.exit()
        elif args[i] == "--help":
            import version
            print("bombrowser "+version.version)
            print()
            print("bombrowser --whereused <code>")
            print("bombrowser --validwhereused <code>")
            print("bombrowser --showassembly <code>")
            print("bombrowser --editcode <code>")
            print("bombrowser --manage-db <...>")
            print("bombrowser --self-test")
            sys.exit(0)

        else:
            print("Ignore command '%s'; quit."%(args[i]))
            sys.exit(0)

        i += 1


    sys.exit(app.exec_())

main(sys.argv)
