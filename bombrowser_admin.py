"""
BOM Browser - tool to browse a bom
Copyright (C) 2024 Goffredo Baroncelli <kreijack@inwind.it>

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
import zipfile
import os
from datetime import datetime

from PySide2.QtWidgets import QPushButton, QMainWindow, QSpinBox, QLabel
from PySide2.QtWidgets import QTextEdit, QFileDialog, QMessageBox
from PySide2.QtWidgets import QGridLayout, QApplication, QGroupBox, QWidget

import db, utils, cfg, version

class AdminWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self._init_gui()

        if self._is_db_empty():
            for x in self._non_init_db_gb:
                x.setEnabled(False)
        else:
            self._refresh_columns_number()

        self._log_append("Connection: %s\n"%(db.connection))

        self.setWindowTitle("BOMBrowser database admin")

    def _is_db_empty(self):
        d = db.get_db_instance()
        with db.ROCursor(d) as c:
            return not "database_props" in d._get_tables_list(c)

    def _init_gui(self):

        g = QGridLayout()

        g.addWidget(QLabel("Number of gval columns"), 10, 10)
        self._gval_count = QSpinBox()
        self._gval_count.setMinimum(0)
        g.addWidget(self._gval_count, 10, 12)

        g.addWidget(QLabel("Number of gaval columns"), 20, 10)
        self._gaval_count = QSpinBox()
        self._gaval_count.setMinimum(0)
        g.addWidget(self._gaval_count, 20, 12)

        b =QPushButton("Change gval/gaval number of columns...")
        b.clicked.connect(self._change_columns)
        g.addWidget(b, 30, 10, 1, 3)

        g.setColumnStretch(10, 100)

        gb1 = QGroupBox("gval/gaval columns")
        gb1.setLayout(g)

        g = QGridLayout()
        b =QPushButton("Backup database")
        b.clicked.connect(self._backup_database)
        g.addWidget(b, 30, 10)

        b =QPushButton("Restore database")
        b.clicked.connect(self._restore_database)
        g.addWidget(b, 40, 10)

        b =QPushButton("Automatic database backup")
        b.clicked.connect(self._automatic_backup_2)
        g.addWidget(b, 50, 10)


        gb2 = QGroupBox("Backup/Restore database")
        gb2.setLayout(g)

        g = QGridLayout()
        b =QPushButton("Init database")
        b.clicked.connect(self._init_database)
        g.addWidget(b, 40, 10)

        gb3 = QGroupBox("Init database")
        gb3.setLayout(g)


        g = QGridLayout()
        b =QPushButton("Info database")
        b.clicked.connect(self._info_database)
        g.addWidget(b, 40, 10)

        b =QPushButton("Info exported database")
        b.clicked.connect(self._info_database_export)
        g.addWidget(b, 50, 10)

        gb4 = QGroupBox("Info database")
        gb4.setLayout(g)


        g = QGridLayout()
        g.addWidget(gb1, 10, 1, 1, 5)
        g.addWidget(gb2, 20, 1, 1, 5)
        g.addWidget(gb3, 30, 1, 1, 5)
        g.addWidget(gb4, 40, 1, 1, 5)

        self._non_init_db_gb = [gb1, gb2, gb4]

        self._log = QTextEdit()
        g.addWidget(self._log, 100, 1, 1, 5)
        g.setRowStretch(100, 100)

        b =QPushButton("Close")
        b.clicked.connect(self.close)
        g.addWidget(b, 120, 5)

        w = QWidget()
        w.setLayout(g)
        self.setCentralWidget(w)

    def _init_database(self):
        reply = QMessageBox.question(self,"Confirm the init of database",
                    "Do you want to init the database ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Init db aborted !!!\n")
            return
        reply = QMessageBox.question(self,"Confirm the init of database",
                    "Are you really convinced to init the database ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Init db aborted !!!\n")
            return

        with utils.OverrideCursor():
            self._log_append("Init database:")
            self._log_append("----------------------------")

            if not self._is_db_empty():
                self._automatic_backup()

            db.new_db(db.get_db_instance())

        for x in self._non_init_db_gb:
            x.setEnabled(True)

        self._refresh_columns_number()
        self._log_append("The database was initialized\n")

    def _info_database(self):
        tables = db.get_db_instance().list_main_tables()
        with db.ROCursor(db.get_db_instance()) as c:
            stat = dict()
            for i in tables:
                c.execute("SELECT count(*) FROM %s"%(i))
                r = c.fetchone()[0]
                stat[i] = r

            c.execute("SELECT MAX(date_from) FROM item_revisions WHERE iter < ?",
                      (db.prototype_iter,))
            max_date_from = c.fetchone()[0]
            c.execute("SELECT MIN(date_from) FROM item_revisions")
            min_date_from = c.fetchone()[0]

        self._log_append("Info database:")
        self._log_append("----------------------------")
        for i in tables:
            self._log_append("Table %s: %d rows"%(i, stat[i]))
        self._log_append("Last revision: %s"%(max_date_from))
        self._log_append("First revision: %s"%(min_date_from))
        self._log_append("gval columns count: %d"%(db.gvals_count))
        self._log_append("gaval columns count: %d"%(db.gavals_count))
        self._log_append("")

    def _info_database_export(self):
        tables = db.get_db_instance().list_main_tables()
        nf = QFileDialog.getOpenFileName(self, "Restore backup",
                                    filter="Zip file format (*.zip);; All files (*.*)",
                                    selectedFilter="Zip file format (*.zip)")
        if nf[0] == "":
            return

        nf = nf[0]
        stat = dict()


        self._log_append("Info exported database:")
        self._log_append("----------------------------")
        self._log_append(self._get_info_exported_database(nf))

    def _get_info_exported_database(self, nf):

        ret = "File: %s\n"%(nf)

        with zipfile.ZipFile(nf) as z:
            for zfn in z.namelist():
                cnt = 0;
                for line in z.open(zfn).readlines():
                    cnt += 1
                ret += "File %s: %d rows\n"%(zfn, cnt-1)

        gval, gaval = self._count_gval_gaval(nf)
        ret += "gval columns count: %d\n"%(gval)
        ret += "gaval columns count: %d\n"%(gaval)

        return ret

    def _log_append(self, s):
        self._log.setText(self._log.toPlainText() + s + "\n")
        self._log.verticalScrollBar().setValue(
           self._log.verticalScrollBar().maximum()
        )

    def _add_column(self, t, tname, colname):
        t.execute("""
            ALTER TABLE %s
            ADD %s VARCHAR(255) DEFAULT ''
                    """%(tname, colname)
        )

    def _drop_column(self, t, tname, colname):
        try:
            t.execute("""
                ALTER TABLE %s
                DROP COLUMN %s
                        """%(tname, colname)
            )
        except Exception as e:
            #
            # SQL Server need to remove the constraint (DEFAULT ....)
            # before deleting tyhe column
            #
            se = str(e)
            i1 = se.find("SQL Server")
            i2 = se.find("The object '")
            i3 = se.find("' is dependent on column")
            if i1 < 0 or i2 < 0 or i3 < 0:
                raise e

            constraintname = se[i2:i3].split("'")[1]
            t.execute("""
                ALTER TABLE %s
                DROP CONSTRAINT %s
                        """%(tname, constraintname)
            )
            t.execute("""
                ALTER TABLE %s
                DROP COLUMN %s
                        """%(tname, colname)
            )

    def _change_columns(self):

        if (db.gvals_count == self._gval_count.value() and
            db.gavals_count == self._gaval_count.value()):
                return

        self._log_append("Change columns count:")
        self._log_append("----------------------------")

        self._automatic_backup()

        with db.Transaction(db.get_db_instance()) as t:
            self._change_gval_column(t)
            self._change_gaval_column(t)

        self._refresh_columns_number()
        self._log_append("")

    def _change_gval_column(self, t):
        if db.gvals_count == self._gval_count.value():
            return

        reply = QMessageBox.question(self,"Confirm the change of column",
                    "Found %d gvals columns, will be set to %d :\n"%(
                        db.gvals_count, self._gval_count.value()) +
                    "Do you want to continue ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Change number of gval aborted !!!\n")
            return

        reply = QMessageBox.question(self,"Confirm the change of column",
                    "Are you really convinced to change the column gval ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Change number of gval aborted !!!\n")
            return

        if db.gvals_count > self._gval_count.value():
            for i in range(self._gval_count.value() + 1, db.gvals_count + 1):
                self._drop_column(t, "item_revisions", "gval%d"%(i))
        else: # drop columns
            for i in range(db.gvals_count + 1 , self._gval_count.value() + 1):
                self._add_column(t, "item_revisions", "gval%d"%(i))

        self._log_append("Change number of gval from %d to %d"%(
                        db.gvals_count, self._gval_count.value()))


    def _change_gaval_column(self, t):
        if db.gavals_count == self._gaval_count.value():
            return

        reply = QMessageBox.question(self,"Confirm the change of column",
                    "Found %d gavals columns, will be set to %d :\n"%(
                        db.gavals_count, self._gaval_count.value()) +
                    "Do you want to continue ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Change number of gaval aborted !!!\n")
            return

        reply = QMessageBox.question(self,"Confirm the change of column",
                    "Are you really convinced to change the column gaval ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Change number of gaval aborted !!!\n")
            return

        if db.gavals_count > self._gaval_count.value():
            # drop columns
            for i in range(self._gaval_count.value() + 1, db.gavals_count + 1):
                self._drop_column(t, "assemblies", "gaval%d"%(i))
        else: # drop columns
            for i in range(db.gavals_count + 1 , self._gaval_count.value() + 1):
                self._add_column(t, "assemblies", "gaval%d"%(i))

        self._log_append("Change number of gaval from %d to %d"%(
                        db.gavals_count, self._gaval_count.value()))


    def _backup_database(self):
        nf = QFileDialog.getSaveFileName(self, "Export backup",
                                    filter="Zip file format (*.zip);; All files (*.*)",
                                    selectedFilter="Zip file format (*.zip)")
        if nf[0] == "":
            return

        with utils.OverrideCursor():
            db.dump_tables(nf[0], db.get_db_instance(), quiet=True)

        self._log_append("Backup database:")
        self._log_append("----------------------------")
        self._log_append("Saved db to " + nf[0] + "\n")

    def _count_gval_gaval(self, nf):
        gval = 0
        gaval = 0
        with zipfile.ZipFile(nf) as z:
            with z.open("item_revisions.csv") as f:
                line = f.readline().decode('utf-8')
                for i in line.split("\t"):
                    if i.startswith("gval"):
                        gval = int(i[4:])

            with z.open("assemblies.csv") as f:
                line = f.readline().decode('utf-8')
                for i in line.split("\t"):
                    if i.startswith("gaval"):
                        gaval = int(i[5:])


        return gval, gaval

    def _restore_database(self):
        nf = QFileDialog.getOpenFileName(self, "Restore backup",
                                    filter="Zip file format (*.zip);; All files (*.*)",
                                    selectedFilter="Zip file format (*.zip)")
        if nf[0] == "":
            return

        info = self._get_info_exported_database(nf[0])
        reply = QMessageBox.question(self,"Confirm the restore",
                    "-"*20 + "\n" +
                    info +
                    "-"*20 + "\n" +
                    "Do you want to continue to restore ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Restored db aborted !!!\n")
            return
        reply = QMessageBox.question(self,"Confirm the restore",
                    "Are you really convinced to restore the database ?",
                                QMessageBox.Yes, QMessageBox.No);
        if reply != QMessageBox.Yes:
            self._log_append("Restored db aborted !!!\n")
            return
        with utils.OverrideCursor():
            gval, gaval = self._count_gval_gaval(nf[0])
            db.gvals_count = gval
            db.gavals_count = gaval

            self._log_append("Restore database:")
            self._log_append("----------------------------")

            self._automatic_backup()

            db.restore_tables(nf[0], db.get_db_instance(), quiet=True)

            self._log_append("Restored db from '" + nf[0] + "'\n")

        self._refresh_columns_number()

    def _refresh_columns_number(self):
        db.get_db_instance().update_gavals_gvals_count_by_db()
        self._gval_count.setValue(db.gvals_count)
        self._gaval_count.setValue(db.gavals_count)

    def _automatic_backup_2(self):
        self._log_append("Automatic backup database:")
        self._log_append("----------------------------")
        self._automatic_backup()

    def _automatic_backup(self):
        if not os.path.exists("backup-db/"):
            os.mkdir("backup-db/")
        backupfile="backup-db/bombrowser-%s.bkp.zip"%(datetime.now().strftime("%Y%m%d%H%M%S"))
        self._log_append("Start backup to %s ..."%(backupfile))
        db.dump_tables(backupfile, db.get_db_instance(), quiet=True)
        self._log_append("Backup ended")


def bombrowser_init():
    app = QApplication(sys.argv)

    sys.excepthook = utils._show_exception

    try:
        cfg.init()
    except Exception as e:
        QMessageBox.critical(None, "BOMBrowser - %s"%(version.version),
            "Cannot load configuration: may be bombrowser.ini is missing ?\nAbort\n")
        print(e)
        return

    ret = cfg.check_cfg()
    if len(ret) != 1 or ret[0][0] != "OK":
        message = "ERROR in bombrowser.ini\n"
        for type_, msg in ret:
            if type_ == "MORE":
                message += "WARNING: " + msg + "\n"
            else:
                message += "CRITICAL: " + msg + "\n"
        message += "Abort\n"
        QMessageBox.critical(None, "BOMBrowser - %s"%(version.version),
            message)
        return

    fontscale = float(cfg.config()["BOMBROWSER"].get("scalefont", "1.0"))
    f = app.font()
    f.setPointSize(f.pointSize() * fontscale)
    app.setFont(f)

    try:
        dbtype = cfg.config()["BOMBROWSER"]["db"]
        c = cfg.config()[dbtype.upper()]
        db.init(dbtype, dict(c))
    except:
        utils.show_exception(msg="Cannot connect to database\nAbort\n")
        return

    return app

def main():

    app = bombrowser_init()

    w = AdminWindow()
    w.show()

    sys.exit(app.exec_())

main()
