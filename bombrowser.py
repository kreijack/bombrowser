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

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMessageBox

import db, listcodegui, cfg

def main(args):
    app = QApplication(sys.argv)

    try:
        cfg.init()
    except:
        QMessageBox.critical(None, "BOMBrowser", "Cannot load configuration: may be bombroser.ini missing ?\nAbort")
        raise


    try:
        d = db.DB()
        data = d.get_config()
    except Exception as e:
        QMessageBox.critical(None, "BOMBrowser",
            "Cannot connect to database\nAbort\n" +
            "Exception:\n" +
            "-"*30 + "\n" +
            str(e) + "\n" +
            "-"*30
        )
        raise

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

        else:
            print("Ignore command '%s'"%(args[i]))

        i += 1


    sys.exit(app.exec_())

main(sys.argv)
