import sys

from PySide2.QtWidgets import QMainWindow, QScrollArea, QStatusBar
from PySide2.QtWidgets import QSplitter, QTableView, QLabel
from PySide2.QtWidgets import QGridLayout, QWidget, QApplication
from PySide2.QtWidgets import QMessageBox, QAction, QLineEdit, QFrame
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PySide2.QtCore import Qt, QAbstractTableModel, QEvent

import db, listcodegui

def main(args):
    app = QApplication(sys.argv)
    w = listcodegui.CodesWindow()
    w.show()

    i = 0
    while i < len(args):
        if args[i] == "--whereused":
            import asmgui
            i += 1
            asmgui.where_used(int(args[i]), None)
        elif args[i] == "--validwhereused":
            import asmgui
            i += 1
            asmgui.valid_where_used(int(args[i]), None)
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
