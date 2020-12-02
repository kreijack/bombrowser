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
    sys.exit(app.exec_())
    
main(sys.argv)
