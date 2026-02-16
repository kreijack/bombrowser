"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021,2022,2023,2024,2025,2026 Goffredo Baroncelli <kreijack@inwind.it>

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

import datetime
import os
import filelock
import socket
import gzip
import time

import db

class LogTransaction:
        def __init__(self, db, cfg):
                self._db = db
                self._cfg = cfg

                self._fname = cfg.config()["LOGGER"]["filename"]
                if len(self._fname) < 1:
                        self._fname = None

                self._compress = False
                if "compress" in cfg.config()["LOGGER"]:
                        c = cfg.config()["LOGGER"]["compress"].strip()
                        if c == "1":
                                self._compress = True

                self._logrotate = "0"
                if "logrotate" in cfg.config()["LOGGER"]:
                        c = cfg.config()["LOGGER"]["logrotate"].strip()
                        if c in ["0", "weekly", "monthly", "yearly"]:
                                self._logrotate = c

                self._delete_code_msg = None
                self._delete_rev_msg = None
                self._update_rev_msg  = None
                self._update_dates_msg = None

        def _revision_to_str(self, rev_id):
                [rev, children, drawings] = self._db.get_full_revision_by_rid(rev_id)
                msg=""
                gvalnames = dict()
                for (_, _, k, n, _) in self._cfg.get_gvalnames2():
                        gvalnames[k] = n
                gavalnames = dict()
                for (_, _, k, n, _) in self._cfg.get_gavalnames():
                        gavalnames[k] = n
                for k,v in rev.items():
                        if k.startswith("gval"):
                                kver=k
                        if k in gvalnames:
                                kver = gvalnames[k]
                                msg += "(%s)%s:\t%s\n"%(k, kver, str(v))
                        else:
                                msg += "%s:\t%s\n"%(k, str(v))

                msg += "Children:\n"
                msg += "\t#code_id\tcode\tdescr\tqty\teach\tunit\tref"
                for i in range(1, db.gavals_count+1):
                        k = "gaval%d"%(i)
                        if k in gavalnames:
                                name = "\t(%s)%s"%(k, gavalnames[k])
                        else:
                                name = "\t(%s)"%(k)
                        msg += name
                msg += "\n"
                for child in children:
                        msg += "\t" + "\t".join([str(x) for x in child]) + "\n"

                msg += "Drawings:\n"
                msg += "\t#file\tpath\n"
                for drawing in drawings:
                        msg += "\t"+ "\t".join(drawing) + "\n"

                return msg

        def _code_to_str(self, code_id):
                return "\n".join(
                        [self._revision_to_str(x[4])
                                for x in self._db.get_dates_by_code_id3(code_id)])

        def _append(self, msg):

                if self._logrotate == "weekly":
                        fn = "%s-%s"%(
                                self._fname,
                                time.strftime("%Y_%W", time.gmtime()))
                elif self._logrotate == "monthly":
                        fn = "%s-%s"%(
                                self._fname,
                                time.strftime("%Y-%m", time.gmtime()))
                elif self._logrotate == "yearly":
                        fn = "%s-%s"%(
                                self._fname,
                                time.strftime("%Y", time.gmtime()))
                else:
                        fn = self._fname

                if self._compress:
                        xopen = gzip.open
                        msg = msg.encode("utf-8")
                        fn = fn+".gz"
                else:
                        xopen = open

                with filelock.FileLock(self._fname+".lock"):
                        with xopen(fn, "a") as f:
                                f.write(msg)

        def _compare_msg(self, msg_old1, msg_new1):
                msg_old1 = msg_old1.split("\n")
                msg_new1 = msg_new1.split("\n")
                msg_old = []
                msg_new = []

                for line in msg_old1:
                        if line in msg_new1:
                                msg_old.append("  " + line)
                        else:
                                msg_old.append("- " + line)
                for line in msg_new1:
                        if line in msg_old1:
                                msg_new.append("  " + line)
                        else:
                                msg_new.append("+ " + line)

                return "\n".join(msg_old), "\n".join(msg_new)

        def _dates_to_str(self, code_id):
                dates = self._db.get_dates_by_code_id3(code_id)
                return "\n".join(
                        ["%s %s %s (%d) %s %s"%(
                                x[0], x[5], x[1], x[6],
                                db.days_to_iso(x[2]),
                                db.days_to_iso(x[3]))
                                        for x in dates])

        def _get_info(self):
                return "## timestamp: %s\n## username: %s\n## host: %s\n"%(
                        datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S %z"),
                        os.getlogin(),
                        socket.getfqdn())

        def delete_code_pre(self, code_id):
                self._delete_code_msg = None
                if self._fname is None:
                        return

                self._delete_code_msg = "## Delete code code_id=%d\n"%(code_id)
                self._delete_code_msg += self._get_info()
                self._delete_code_msg += "\n"
                self._delete_code_msg += self._code_to_str(code_id)
                self._delete_code_msg += "\n----\n"

        def delete_code_commit(self):
                if self._delete_code_msg is None:
                        return
                if self._fname is None:
                        return

                self._append(self._delete_code_msg)
                self._delete_code_msg = None

        def delete_rev_pre(self, rev_id):
                self._delete_rev_msg = None
                if self._fname is None:
                        return

                self._delete_rev_msg = "## Delete revision rev_id=%d\n"%(rev_id)
                self._delete_rev_msg += self._get_info()
                self._delete_rev_msg += "\n"
                self._delete_rev_msg += self._revision_to_str(rev_id)
                self._delete_rev_msg += "\n----\n"

        def delete_rev_commit(self):
                if self._delete_rev_msg is None:
                        return
                if self._fname is None:
                        return

                self._append(self._delete_rev_msg)
                self._delete_rev_msg = None

        def create_rev_commit(self, rev_id):
                if self._fname is None:
                        return

                msg = "## Create revision rev_id=%d\n"%(rev_id)
                msg += self._get_info()
                msg += "\n"
                msg += self._revision_to_str(rev_id)
                msg += "\n----\n"

                self._append(msg)

        def update_rev_pre(self, rev_id):
                self._update_rev_msg = None
                if self._fname is None:
                        return

                self._update_rev_id = rev_id
                self._update_rev_msg = self._revision_to_str(rev_id)

        def update_rev_commit(self):
                if self._update_rev_msg is None:
                        return
                if self._fname is None:
                        return

                current_msg = self._revision_to_str(self._update_rev_id)

                if current_msg == self._update_rev_msg:
                        msg = "## Update revision rev_id=%d\n"%(self._update_rev_id)
                        msg += self._get_info()
                        msg += "\n"
                        msg += "## the revisions are equal; the content will not logged\n"
                        msg += "\n----\n"
                else:
                        msg_old, msg_new = self._compare_msg(self._update_rev_msg,
                                                                current_msg)

                        msg = "## Update revision rev_id=%d\n"%(self._update_rev_id)
                        msg += self._get_info()
                        msg += "\n"
                        msg += "## Previous value\n"
                        msg += msg_old
                        msg += "\n"
                        msg += "## Current value\n"
                        msg += msg_new
                        msg += "\n----\n"

                self._append(msg)
                self._update_rev_msg = None

        def update_dates_pre(self, code_id):
                self._update_dates_msg = None
                if self._fname is None:
                        return

                self._update_dates_code_id = code_id
                self._update_dates_msg = self._dates_to_str(code_id)

        def update_dates_commit(self):
                if self._update_dates_msg is None:
                        return
                if self._fname is None:
                        return

                current_msg = self._dates_to_str(self._update_dates_code_id)

                if current_msg == self._update_dates_msg:
                        msg = "## Update dates code_id=%d\n"%(self._update_dates_code_id)
                        msg += self._get_info()
                        msg += "\n"
                        msg += "## the dates are equal; the content will not logged\n"
                        msg += "\n----\n"
                else:

                        msg_old, msg_new = self._compare_msg(self._update_dates_msg,
                                                        current_msg)

                        msg = "## Update dates code_id=%d\n"%(self._update_dates_code_id)
                        msg += self._get_info()
                        msg += "\n"
                        msg += "## Previous value\n"
                        msg += msg_old
                        msg += "\n"
                        msg += "## Current value\n"
                        msg += msg_new
                        msg += "\n----\n"

                self._append(msg)
                self._update_dates_msg = None


class LogTransactionDeleteCode:
        def __init__(self, db, cfg, code_id):
                self._log_transaction = LogTransaction(db,cfg)
                self._code_id = code_id

        def __enter__(self):
                self._log_transaction.delete_code_pre(self._code_id)
                return self

        def abort(self):
                self._log_transaction = None

        def __exit__(self, exc_type, exc_val, exc_tb):
                if self._log_transaction:
                        self._log_transaction.delete_code_commit()


class LogTransactionDeleteRevision:
        def __init__(self, db, cfg, rev_id):
                self._log_transaction = LogTransaction(db,cfg)
                self._rev_id = rev_id

        def __enter__(self):
                self._log_transaction.delete_rev_pre(self._rev_id)
                return self

        def abort(self):
                self._log_transaction = None

        def __exit__(self, exc_type, exc_val, exc_tb):
                if self._log_transaction:
                        self._log_transaction.delete_rev_commit()


class LogTransactionUpdateRevision:
        def __init__(self, db, cfg, rev_id):
                self._log_transaction = LogTransaction(db,cfg)
                self._rev_id = rev_id

        def __enter__(self):
                self._log_transaction.update_rev_pre(self._rev_id)
                return self

        def abort(self):
                self._log_transaction = None

        def __exit__(self, exc_type, exc_val, exc_tb):
                if self._log_transaction:
                        self._log_transaction.update_rev_commit()


class LogTransactionUpdateDates:
        def __init__(self, db, cfg, code_id):
                self._log_transaction = LogTransaction(db,cfg)
                self._code_id = code_id

        def __enter__(self):
                self._log_transaction.update_dates_pre(self._code_id)
                return self

        def abort(self):
                self._log_transaction = None

        def __exit__(self, exc_type, exc_val, exc_tb):
                if self._log_transaction:
                        self._log_transaction.update_dates_commit()
