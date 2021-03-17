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

"""
Conversion date

Conversion table:
    date_{from,to}_days = 0 -> date_{from,to} = '2000-01-01'
    date_{from,to}_days = 999999 -> date_{from,to} = '4737-11-27'

SQL
    date_{from,to}_days = JULIANDAY(date_{from,to}) - JULIANDAY('2000-01-01')
    JULIANDAY('2000-01-01') = 2451544.5

PYTHON
    import jdutil
    jdutil.datetime('2000-01-01').to_jd() = 2451544.5

"""


import sys
import pprint
import datetime
import configparser
import time
import jdutil
import customize
import cfg
import traceback

def increase_date(d, inc=+1):
    return (datetime.date.fromisoformat(d) +
            datetime.timedelta(days=inc)).isoformat()

def iso_to_days(txt):
    return int(jdutil.datetime.fromisoformat(txt).to_jd() - 2451544.5)

def days_to_iso(n):
    return jdutil.jd_to_datetime(int(n) + 2451544.5).strftime("%Y-%m-%d")

def days_to_txt(n):
    if n is None:
        return ""
    if n == end_of_the_world:
        return ""
    elif n == prototype_date:
        return "PROTOTYPE"
    elif n == prototype_date - 1:
        return ""
    else:
        return jdutil.jd_to_datetime(int(n) + 2451544.5).strftime("%Y-%m-%d")

def now_to_days():
    return int(jdutil.datetime.now().to_jd() - 2451544.5)

_db_path = "database.sqlite"
# infinity date
end_of_the_world = 999999   # around 5000 ac
prototype_date = 999900
prototype_iter = 999999
gvals_count = 8
connection="Server: <UNDEF>"

class DBException(RuntimeError):
    pass

class _BaseServer:

    def __init__(self, path):
        self._open(path)


        if "database_props" in self._get_tables_list():
            c = self._conn.cursor()
            self._sqlex(c, """SELECT value FROM database_props WHERE "key"='ver'""")
            self._ver = c.fetchone()[0]

            # for now v0.3 and v0.4 are equal
            assert(self._ver == "0.4" or self._ver == "0.3")

        else:
            self._ver = "empty"

    def _sqlex(self, c, query, *args, **kwargs):
        c.execute(query, *args, **kwargs)

    def _sqlexm(self, c, query, *args, **kwargs):
        c.executemany(query, *args, **kwargs)

    def _commit(self, c):
        c.commit()

    def _rollback(self, c):
        c.rollback()

    def _begin(self, c):
        c.begin()

    def _sql_translate(self, s):
        return s

    def _open(self, connection_string):
        raise DBException("Cannot implemented")

    def _get_tables_list(self):
        cursor = self._conn.cursor()
        return [row.table_name for row in cursor.tables()]

    def _get_db_v0_4(self):
        stms = """
            --
            -- ver 0.4
            --
            DROP INDEX IF EXISTS items.item_code_idx;
            DROP INDEX IF EXISTS items.item_code_ver_idx;
            DROP INDEX IF EXISTS items.item_code_ver_iter;
            DROP INDEX IF EXISTS drawings.drawing_idx;
            DROP INDEX IF EXISTS drawings.assemblies_child_idx;
            DROP INDEX IF EXISTS drawings.assemblies_parent_idx;

            DROP TABLE IF EXISTS assemblies;
            DROP TABLE IF EXISTS item_properties;
            DROP TABLE IF EXISTS database_props;
            DROP TABLE IF EXISTS drawings;
            DROP TABLE IF EXISTS item_revisions;
            DROP TABLE IF EXISTS items;

            CREATE TABLE    items (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) UNIQUE NOT NULL
            );

            CREATE INDEX item_code_idx             ON items(code);

            CREATE TABLE item_revisions (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code_id         INTEGER,
                date_from       VARCHAR(10) NOT NULL DEFAULT '2000-01-01',
                date_to         VARCHAR(10) DEFAULT '',
                date_from_days  INTEGER DEFAULT 0,          -- 2000-01-01
                date_to_days    INTEGER DEFAULT 999999,
                ver             VARCHAR(10) NOT NULL,
                iter            INTEGER,
                type            VARCHAR(255),
                note            VARCHAR(255),
                descr           VARCHAR(255) NOT NULL,
                default_unit    VARCHAR(10) NOT NULL,
                gval1           VARCHAR(255) DEFAULT '',
                gval2           VARCHAR(255) DEFAULT '',
                gval3           VARCHAR(255) DEFAULT '',
                gval4           VARCHAR(255) DEFAULT '',
                gval5           VARCHAR(255) DEFAULT '',
                gval6           VARCHAR(255) DEFAULT '',
                gval7           VARCHAR(255) DEFAULT '',
                gval8           VARCHAR(255) DEFAULT '',

                FOREIGN KEY (code_id) REFERENCES items(id)
            );

            CREATE INDEX revision_code_id ON item_revisions(code_id);
            CREATE INDEX revision_code_id_date ON
                item_revisions(code_id, date_from_days);
            CREATE INDEX revision_date_from ON item_revisions(date_from);
            CREATE INDEX revision_date_from_days ON item_revisions(date_from_days);
            CREATE INDEX revision_date_to ON item_revisions(date_to);
            CREATE INDEX revision_date_to_days ON item_revisions(date_to_days);
            CREATE UNIQUE INDEX revision_code_iter
                ON item_revisions(code_id, iter);

            CREATE TABLE item_properties (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                descr       VARCHAR(255),
                value       VARCHAR(1024),
                revision_id     INTEGER,

                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );
            CREATE UNIQUE INDEX item_prop_descr_rid ON item_properties(revision_id, descr);

            CREATE TABLE assemblies (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                unit            VARCHAR(10),
                child_id        INTEGER,
                revision_id     INTEGER,
                qty             FLOAT,
                each            FLOAT DEFAULT 1.0,
                ref             VARCHAR(600) DEFAULT '',

                FOREIGN KEY (child_id) REFERENCES items(id),
                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );

            CREATE INDEX assemblies_child_idx ON assemblies(child_id);
            CREATE INDEX assemblies_revision_idx ON assemblies(revision_id);

            CREATE TABLE database_props (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                "key"       VARCHAR(255),
                value       VARCHAR(500)
            );

            INSERT INTO database_props ("key", value) VALUES ('ver', '0.4');

            CREATE TABLE drawings (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) DEFAULT '',
                revision_id INTEGER,
                filename    VARCHAR(255) NOT NULL,
                fullpath    VARCHAR(255) NOT NULL,

                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );

        """

        stms = self._sql_translate(stms)

        return stms

    def create_db(self):

        stms = self._get_db_v0_4()
        c = self._conn.cursor()
        for s in stms.split(";"):
            s = s.strip()
            if len(s) == 0:
                continue
            self._sqlex(c, s)

        self._conn.commit()

    def get_code(self, id_code, date_from_days):
        return self._get_code(self._conn.cursor(), id_code, date_from_days)

    def _get_code(self, c, id_code, date_from_days):

        self._sqlex(c, """
            SELECT i.code, r.descr, r.ver, r.iter, r.default_unit,
                r.gval1, r.gval2, r.gval3, r.gval4, r.gval5, r.gval6,
                r.date_from, r.date_from_days, r.date_to, r.date_to_days, r.id,
                r.gval7, r.gval8
            FROM item_revisions AS r
            LEFT JOIN items AS i
                 ON r.code_id = i.id
            WHERE r.code_id=?
              AND r.date_from_days = ?
            """, (id_code, date_from_days))
        res = c.fetchone()
        if not res:
            return None

        data = dict()
        data["code"] = res[0]
        data["descr"] = res[1]
        data["ver"] = res[2]
        data["iter"] = res[3]
        data["unit"] = res[4]

        data["gval1"] = res[5]
        data["gval2"] = res[6]
        data["gval4"] = res[8]
        data["gval3"] = res[7]
        data["gval5"] = res[9]
        data["gval6"] = res[10]
        data["gval7"] = res[16]
        data["gval8"] = res[17]

        data["date_from"] = days_to_txt(res[12])
        data["date_from_days"] = res[12]
        data["date_to"] = days_to_txt(res[14])
        data["date_to_days"] = res[14]

        data["rid"] = res[15]
        data["id"] = id_code

        data["properties"] = dict()

        self._sqlex(c, """
            SELECT descr, value
            FROM item_properties
            WHERE revision_id=?
            """, (res[15], ))

        res = c.fetchall()
        if res:
            for k,v in res:
                data["properties"][k] = v

        return data

    def get_code_from_rid(self, rid):
        return self._get_code_from_rid(self._conn.cursor(), rid)

    def _get_code_from_rid(self, c, rid):

        self._sqlex(c, """
            SELECT i.code, r.descr, r.ver, r.iter, r.default_unit,
                r.gval1, r.gval2, r.gval3, r.gval4, r.gval5, r.gval6,
                r.date_from, r.date_from_days, r.date_to, r.date_to_days,
                i.id, r.gval7, r.gval8
            FROM item_revisions AS r
            LEFT JOIN items AS i
                 ON r.code_id = i.id
            WHERE r.id = ?
            """, (rid, ))
        res = c.fetchone()
        if not res:
            return None

        data = dict()
        data["code"] = res[0]
        data["descr"] = res[1]
        data["ver"] = res[2]
        data["iter"] = res[3]
        data["unit"] = res[4]

        data["gval1"] = res[5]
        data["gval2"] = res[6]
        data["gval3"] = res[7]
        data["gval4"] = res[8]
        data["gval5"] = res[9]
        data["gval6"] = res[10]
        data["gval7"] = res[16]
        data["gval8"] = res[17]

        data["date_from"] = days_to_txt(res[12])
        data["date_from_days"] = res[12]
        data["date_to"] = days_to_txt(res[14])
        data["date_to_days"] = res[14]

        data["id"] = res[15]
        data["rid"] = rid


        data["properties"] = dict()

        #self._sqlex(c, """
        #    SELECT descr, value
        #    FROM item_properties
        #    WHERE item_id=?
        #    """, (id_code, ))
        #
        #res = c.fetchall()
        #if res:
        #    for k,v in res:
        #        data["properties"][k] = v

        return data

    def get_codes_by_code(self, code):
        c = self._conn.cursor()

        self._sqlex(c, """
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM (
                    SELECT i.id, MAX(iter) AS iter
                    FROM items AS i
                    LEFT JOIN item_revisions AS r
                        ON r.code_id = i.id
                    WHERE i.code = ?
                    GROUP BY i.id
            ) AS r2
            LEFT JOIN item_revisions AS r
                ON r.code_id = r2.id AND r.iter = r2.iter
            LEFT JOIN items AS i
                ON r.code_id = i.id
            ORDER BY r.iter DESC
            """, (code,))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_code(self, code):
        c = self._conn.cursor()
        self._sqlex(c, """
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM (
                    SELECT i.id, MAX(iter) AS iter
                    FROM items AS i
                    LEFT JOIN item_revisions AS r
                        ON r.code_id = i.id
                    WHERE i.code LIKE ?
                    GROUP BY i.id
            ) AS r2
            LEFT JOIN item_revisions AS r
                ON r.code_id = r2.id AND r.iter = r2.iter
            LEFT JOIN items AS i
                ON r.code_id = i.id
            ORDER BY i.code, r.iter DESC
            """, (code,))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_descr(self, descr):
        c = self._conn.cursor()
        self._sqlex(c, """
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM (
                    SELECT i.id, MAX(iter) AS iter
                    FROM item_revisions AS r
                    LEFT JOIN items AS i
                        ON r.code_id = i.id
                    WHERE r.descr LIKE ?
                    GROUP BY i.id
            ) AS r2
            LEFT JOIN item_revisions AS r
                ON r.code_id = r2.id AND r.iter = r2.iter
            LEFT JOIN items AS i
                ON r.code_id = i.id
            ORDER BY i.code, r.iter DESC

            """, (descr, ))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_code_and_descr(self, code, descr):
        c = self._conn.cursor()
        self._sqlex(c, """
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM (
                    SELECT i.id, MAX(iter) AS iter
                    FROM item_revisions AS r
                    LEFT JOIN items AS i
                        ON r.code_id = i.id
                    WHERE i.code LIKE ? AND r.descr LIKE ?
                    GROUP BY i.id
            ) AS r2
            LEFT JOIN item_revisions AS r
                ON r.code_id = r2.id AND r.iter = r2.iter
            LEFT JOIN items AS i
                ON r.code_id = i.id
            ORDER BY i.code, r.iter DESC
            """, (code, descr))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_dates_by_code_id2(self, id_code):
        c = self._conn.cursor()
        self._sqlex(c, """SELECT DISTINCT i.code, r.descr,
                                     r.date_from, r.date_from_days, r.date_to,
                                     r.date_to_days, r.id, r.ver, r.iter
                     FROM  item_revisions AS r
                     LEFT JOIN items AS i ON r.code_id = i.id
                     WHERE           r.code_id = ?
                     ORDER BY        r.date_from DESC
                  """, (id_code, ))

        return list(c.fetchall())

    def get_parent_dates_range_by_code_id(self, id_code):
        c = self._conn.cursor()
        self._sqlex(c, """
                SELECT r.code_id AS pid,
                       MIN(r.date_from_days) AS dfrom,
                       MAX(r.date_to_days) AS dto
                FROM assemblies AS a
                LEFT JOIN item_revisions AS r
                    ON a.revision_id = r.id
                WHERE a.child_id = ?
                GROUP BY r.code_id
                  """, (id_code, ))

        return list(c.fetchall())

    def get_children_dates_range_by_rid(self, rid):
        c = self._conn.cursor()
        self._sqlex(c, """
                SELECT a.child_id AS c_id,
                       MIN(r.date_from_days) AS dfrom,
                       MAX(r.date_to_days) AS dto
                FROM assemblies AS a
                LEFT JOIN item_revisions AS r
                    ON a.child_id = r.code_id
                WHERE a.revision_id = ?
                GROUP BY a.child_id
                  """, (rid, ))

        return list(c.fetchall())

    def is_assembly(self, id_code):
        c = self._conn.cursor()
        self._sqlex(c, """SELECT COUNT(*)
                     FROM assemblies AS a
                     LEFT JOIN item_revisions AS r
                       ON r.id = a.revision_id
                     WHERE  r.code_id = ?
                  """, (id_code, ))

        return c.fetchone()[0] > 0

    def get_bom_by_code_id2(self, code_id0, date_from):

        date_from_days_ref = iso_to_days(date_from)

        data = dict()

        c = self._conn.cursor()

        self._sqlex(c, """SELECT i.code, r.date_from_days, r.date_to_days, r.id
                         FROM item_revisions AS r
                         LEFT JOIN items AS i
                           ON i.id = r.code_id
                         WHERE  r.code_id = ?
                           AND  r.date_from_days <= ?
                           AND   ? <= r.date_to_days
                         ORDER BY r.date_from_days DESC
                     """,
                     (code_id0, date_from_days_ref, date_from_days_ref) )

        data2 = list(c.fetchall())

        (code0, date_from_days, date_to_days, rid) = data2[0]
        date_from_days0 = date_from_days
        todo = [rid]
        done = []

        while len(todo):
            rid = todo.pop()

            done.append(rid)
            d2 = self._get_code_from_rid(c, rid)
            d = d2["properties"]
            d2.pop("properties")
            d.update(d2)
            d["deps"] = dict()

            self._sqlex(c, """
                SELECT a.unit, a.qty, a.each, rc.date_from, rc.date_to,
                        rc.iter, a.child_id, rc.code_id, rc.date_from_days,
                        rc.date_to_days, a.ref, rc.id
                FROM assemblies AS a
                LEFT JOIN item_revisions AS rc
                  ON a.child_id = rc.code_id
                WHERE   a.revision_id = ?
                  AND   rc.date_from_days <= ?
                  AND   ? <= rc.date_to_days
                ORDER BY a.child_id
                """, (rid, date_from_days_ref, date_from_days_ref))

            children = c.fetchall()

            if children is None or len(children) == 0:
                data[d["id"]] = d
                continue

            for (unit, qty, each, date_from_, date_to_, it, child_id,
                 parent_id, date_from_days_, date_to_days_, ref, crid) in children:
                d["deps"][child_id] = {
                    "code_id": child_id,
                    "unit": unit,
                    "qty": qty,
                    "each": each,
                    "iter": it,
                    "ref": ref,
                }

                if not crid in done:
                    todo.append(crid)

            data[d["id"]] = d

        #mindt = "N/A"
        #for k in data[code_id0]["deps"]:
        #    cid = data[code_id0]["deps"][k]["code_id"]
        #    if mindt == "N/A" or mindt > data[cid]["date_to"]:
        #        mindt = data[cid]["date_to"]
        #data[code_id0]["date_to"] = mindt

        return (code_id0, data)

    def _get_parents(self, c, id_code, date_from_days, date_to_days):
        self._sqlex(c, """
            SELECT a.unit, c.code, r.default_unit, a.qty, a.each,
                    r.iter, r.code_id, r.date_from, r.date_to, r.date_from_days,
                    r.date_to_days
            FROM assemblies AS a
            LEFT JOIN item_revisions AS r
                ON a.revision_id = r.id
            LEFT JOIN items AS c
                ON r.code_id = c.id

            WHERE a.child_id = ?
              AND NOT (
                   r.date_from_days > ?
                OR r.date_to_days < ?
              )
            ORDER BY c.code, r.date_from_days DESC
            """, (id_code, date_to_days, date_from_days))

        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def _get_valid_parents(self, c, id_code):
        self._sqlex(c, """
            SELECT a.unit, c.code, r.default_unit, a.qty, a.each,
                    r.iter, r.code_id, r.date_from, r.date_to, r.date_from_days,
                    r.date_to_days
            FROM assemblies AS a
            LEFT JOIN item_revisions AS r
                ON a.revision_id = r.id
            LEFT JOIN items AS c
                ON r.code_id = c.id

            WHERE a.child_id = ?
              AND r.date_to_days = ?
            ORDER BY c.code, r.date_from_days DESC
            """, (id_code, end_of_the_world))

        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_where_used_from_id_code(self, id_code, valid=False):
        c = self._conn.cursor()

        self._sqlex(c, """
            SELECT code FROM items WHERE id=?
        """, (id_code,))
        code0 = c.fetchone()[0]

        self._sqlex(c, """
            SELECT MIN(date_from_days)
            FROM item_revisions
            WHERE code_id = ?
        """, (id_code, ))
        (xdate_from_days0, ) = c.fetchone()

        self._sqlex(c, """
            SELECT MAX(date_to_days)
            FROM item_revisions
            WHERE code_id = ?
        """, (id_code,))
        (xdate_to_days0, ) = c.fetchone()

        todo = [(id_code, xdate_from_days0, xdate_to_days0 )]
        data = dict()
        done = set()

        while len(todo):
            (id_, xdate_from_days, xdate_to_days) = todo.pop()
            done.add((id_, xdate_from_days))

            d2 = self._get_code(c, id_, xdate_from_days)
            d = d2["properties"]
            d2.pop("properties")
            d.update(d2)
            d["deps"] = dict()

            if valid:
                parents = self._get_valid_parents(c, id_)
            else:
                parents = self._get_parents(c, id_, xdate_from_days, xdate_to_days)
            if parents is None or len(parents) == 0:
                data[(d["code"], xdate_from_days)] = d
                continue

            for (unit, cc, def_unit, qty, each, it,
                    parent_id, date_from_, date_to_, date_from_days_,
                    date_to_days_) in parents:
                if cc == code0:
                    continue
                if unit is None:
                   unit = def_unit
                d["deps"][(cc, date_from_days_)] = {
                    "code": cc,
                    "unit": unit,
                    "qty": qty,
                    "each": each,
                    "iter": it,
                    "ref": "",
                }

                if not (parent_id, date_from_days_) in done:
                    todo.append((parent_id, date_from_days_, date_to_days_))

            data[(d["code"], xdate_from_days)] = d

        top = (code0, xdate_from_days0)
        return (top, data)

    def get_drawings_by_code_id(self, rev_id):
        c = self._conn.cursor()
        self._sqlex(c, """
            SELECT filename, fullpath
            FROM drawings
            WHERE revision_id = ?
            """, (rev_id,))

        res = c.fetchall()
        if not res:
            return []
        else:
            return res

    def get_bom_dates_by_code_id(self, code_id):
        sdates = set()
        dates = []
        done = set()
        todo = [code_id]

        c = self._conn.cursor()

        self._sqlex(c, """
            SELECT MIN(date_from_days)
            FROM item_revisions
            WHERE code_id = ?
            """, (code_id,))

        date_from_min = c.fetchone()[0]
        while len(todo):

            cid = todo.pop()
            done.add(cid)
            self._sqlex(c, """
                    SELECT r.date_from, r.date_from_days
                    FROM item_revisions AS r
                    WHERE r.code_id = ?
                """, (cid,))

            for (date_from, date_from_days) in c.fetchall():
                if date_from_days < date_from_min:
                    continue
                if not date_from_days in sdates:
                    sdates.add(date_from_days)
                    dates.append((date_from, date_from_days))

            self._sqlex(c, """
                    SELECT DISTINCT a.child_id
                    FROM assemblies AS a
                    LEFT JOIN item_revisions AS r
                      ON a.revision_id = r.id
                    WHERE r.code_id = ?
                """, (cid,))

            l = set([x[0] for x in c.fetchall()])
            l = l.difference(done)
            todo += list(l)
        return dates

    def copy_code(self, new_code, rid, descr, rev, copy_props=True,
                  copy_docs=True, new_date_from_days=None):
        c = self._conn.cursor()
        self._begin(c)
        try:

            try:
                self._sqlex(c, """
                        INSERT INTO items(code) VALUES (?)
                    """, (new_code, ))
            except:
                raise DBException("The code already exists")

            self._sqlex(c, """SELECT MAX(id) FROM items""")
            new_code_id = c.fetchone()[0]

            if new_date_from_days is None:
                new_date_from_days = now_to_days()
            new_date_from = days_to_iso(new_date_from_days)

            self._sqlex(c, """
                INSERT INTO item_revisions(
                    code_id,
                    date_from,
                    date_from_days,
                    date_to,
                    ver,
                    iter,
                    note,
                    descr,
                    default_unit,
                    gval1, gval2, gval3, gval4, gval5, gval6, gval7, gval8
                ) SELECT
                    ?,
                    ?,
                    ?,
                    '',
                    ?,
                    0,
                    note,
                    ? ,
                    default_unit,
                    gval1, gval2, gval3, gval4, gval5, gval6, gval7, gval8
                FROM item_revisions
                WHERE id = ?
            """, (new_code_id, new_date_from, new_date_from_days, rev, descr, rid))

            self._sqlex(c, """SELECT MAX(id) FROM item_revisions""")
            new_rid = c.fetchone()[0]

            self._revise_code_copy_others(c, new_rid, rid, copy_docs, copy_props)

        except:
            self._rollback(c)
            raise

        self._commit(c)

        return new_rid

    def revise_code(self, rid, descr, rev, copy_props=True, copy_docs=True,
                    new_date_from_days=None):
        c = self._conn.cursor()
        self._begin(c)
        try:
            self._sqlex(c, """
                SELECT r2.id, r2.date_from_days, r2.iter
                FROM (
                    SELECT r.code_id, MAX(r.iter) AS iter
                    FROM item_revisions AS r
                    WHERE r.code_id = (
                        SELECT DISTINCT code_id
                        FROM item_revisions
                        WHERE id = ?
                    )
                    GROUP BY r.code_id
                ) AS r
                LEFT JOIN item_revisions AS r2
                    ON r.code_id=r2.code_id AND r.iter=r2.iter
                """, (rid, ))


            (latest_rid, old_date_from_days, old_iter) = c.fetchone()

            if new_date_from_days is None:
                new_date_from_days = now_to_days()
            new_date_from = days_to_iso(new_date_from_days)

            if new_date_from_days <= old_date_from_days:
                raise DBException("A revision already occurred this day")


            if new_date_from_days == prototype_date:
                new_iter = prototype_iter
            else:
                new_iter = old_iter + 1

            self._sqlex(c, """
                INSERT INTO item_revisions(
                    code_id,
                    date_from,
                    date_from_days,
                    date_to,
                    ver,
                    iter,
                    note,
                    descr,
                    default_unit,
                    gval1, gval2, gval3, gval4, gval5, gval6, gval7, gval8
                ) SELECT
                    code_id,
                    ?,
                    ?,
                    '',
                    ?,
                    ?,
                    note,
                    ? ,
                    default_unit,
                    gval1, gval2, gval3, gval4, gval5, gval6, gval7, gval8
                FROM item_revisions
                WHERE id = ?
            """, (new_date_from, new_date_from_days, rev, new_iter, descr, rid))

            self._sqlex(c, """SELECT MAX(id) FROM item_revisions""")
            new_rid = c.fetchone()[0]


            old_date_to_days = new_date_from_days - 1
            self._sqlex(c, """
                UPDATE item_revisions
                SET date_to = ?, date_to_days = ?
                WHERE id = ?
            """, (days_to_iso(old_date_to_days),
                old_date_to_days, latest_rid))

            self._revise_code_copy_others(c, new_rid, rid, copy_docs, copy_props)

        except:
            self._rollback(c)
            raise

        self._commit(c)

        return new_rid

    def _revise_code_copy_others(self, c, new_rid, old_rid, copy_docs, copy_props):

            self._sqlex(c, """
                INSERT INTO assemblies (
                    unit,
                    child_id,
                    revision_id,
                    qty,
                    each,
                    ref
                ) SELECT
                    unit,
                    child_id,
                    ?,
                    qty,
                    each,
                    ref
                FROM assemblies
                WHERE revision_id = ?
            """, (new_rid, old_rid))

            if copy_docs:
                self._sqlex(c, """
                    INSERT INTO drawings (
                        code,
                        revision_id,
                        filename,
                        fullpath
                    ) SELECT
                        code,
                        ?,
                        filename,
                        fullpath
                    FROM drawings
                    WHERE revision_id = ?
                """, (new_rid, old_rid))

            if copy_props:
                self._sqlex(c, """
                    INSERT INTO item_properties (
                        descr,
                        value,
                        revision_id
                    ) SELECT
                        descr,
                        value,
                        ?
                    FROM item_properties
                    WHERE revision_id = ?
                """, (new_rid, old_rid))

    def get_children_by_rid(self, rid):
        c = self._conn.cursor()
        self._sqlex(c, """
            SELECT a.child_id, i.code, r2.descr, a.qty, a.each, a.unit,
                   a.ref
            FROM assemblies AS a
            LEFT JOIN (
                SELECT code_id, MAX(iter) AS iter
                FROM item_revisions
                GROUP BY code_id
            ) AS r
              ON r.code_id = a.child_id
            LEFT JOIN items AS i
              ON a.child_id = i.id
            LEFT JOIN item_revisions AS r2
              ON r2.code_id = a.child_id AND r2.iter = r.iter
            WHERE a.revision_id = ?
            ORDER BY a.id
        """, (rid,))

        return c.fetchall()

    def update_by_rid(self, rid, descr, ver, default_unit,
            gval1, gval2, gval3, gval4, gval5, gval6, gval7, gval8,
            drawings=[], children=[]):

        c = self._conn.cursor()
        self._begin(c)
        try:
            self._sqlex(c, """
                UPDATE item_revisions SET
                    descr=?, ver=?, default_unit=?,
                    gval1=?, gval2=?, gval3=?, gval4=?, gval5=?,
                    gval6=?, gval7=?, gval8=?
                WHERE id=?
                """,(descr, ver, default_unit,
                     gval1, gval2, gval3, gval4, gval5,
                     gval6, gval7, gval8,
                     rid))

            self._sqlex(c, """
                DELETE FROM drawings
                WHERE revision_id = ?
            """, (rid, ))

            if len(drawings) > 0:

                self._sqlexm(c, """
                        INSERT INTO drawings(revision_id, filename, fullpath)
                        VALUES (?, ?, ?)
                    """, [(rid, name, path) for (name, path) in drawings])

            self._sqlex(c, """
                DELETE FROM assemblies
                WHERE revision_id = ?
            """, (rid, ))

            if len(children) > 0:
                # (code_id, qty, each, unit)
                self._sqlexm(c, """
                        INSERT INTO assemblies(
                            revision_id, child_id, qty, each, ref, unit)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, [(rid, code_id, qty, each, ref, unit)
                        for (code_id, qty, each, unit, ref) in children])


        except:
            self._rollback(c)
            raise

        self._commit(c)


    def update_dates(self, dates):
        # dates.append((rid, date_from, date_from_days, date_to, date_to_days))
        c = self._conn.cursor()
        self._begin(c)
        try:
            for (rid, date_from, date_from_days, date_to, date_to_days) in dates:
                self._sqlex(c, """
                    UPDATE item_revisions SET
                        date_from=?, date_from_days=?,
                        date_to=?, date_to_days=?
                    WHERE id = ?
                """, (date_from, date_from_days, date_to, date_to_days, rid))
        except:
            self._rollback()
            raise

        self._commit(c)

    def get_config(self):
        ret = dict()
        c = self._conn.cursor()
        self._sqlex(c, """
            SELECT "key", value FROM database_props
        """)
        for (key, value) in c.fetchall():
            if not key.startswith("cfg."):
                continue
            key = key[4:] # skip cfg.
            key1,key2 = key.split(".")

            if not key1 in ret:
                ret[key1] = dict()

            ret[key1][key2] = value

        return ret


import sqlite3
import traceback

class DBSQLServer(_BaseServer):
    def __init__(self, path=None):
        _BaseServer.__init__(self, path)

    def _begin(self, c):
        pass

    def _sqlex(self, c, query, *args, **kwargs):
        try:
            _BaseServer._sqlex(self, c, query, *args, **kwargs)
        except self._mod.Error as er:
            errmsg = 'ODBC error: %s' % (' '.join(er.args)) + "\n"
            errmsg += "ODBC query:\n"
            errmsg += "-"*30+"\n"
            errmsg += query + "\n"
            errmsg += "-"*30+"\n"
            errmsg += "Exception class is: " + str(er.__class__) + "\n"
            errmsg += 'ODBC traceback: \n'
            exc_type, exc_value, exc_tb = sys.exc_info()
            errmsg += '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb))

            print(errmsg)

            raise DBException(errmsg)

    def _sqlexm(self, c, query, *args, **kwargs):
        try:
            _BaseServer._sqlexm(self, c, query, *args, **kwargs)
        except self._mod.Error as er:
            errmsg = 'ODBC error: %s' % (' '.join(er.args)) + "\n"
            errmsg += "ODBC query:\n"
            errmsg += "-"*30+"\n"
            errmsg += query + "\n"
            errmsg += "-"*30+"\n"
            errmsg += "Exception class is: " + str(er.__class__) + "\n"
            errmsg += 'ODBC traceback: \n'
            exc_type, exc_value, exc_tb = sys.exc_info()
            errmsg += '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb))

            print(errmsg)

            raise DBException(errmsg)

    def _sql_translate(self, s):
        def process(l):
            if " RENAME TO " in l:
                l = l.replace("ALTER TABLE ", "EXEC sp_rename '")
                l = l.replace(" RENAME TO ", "', '")
                l = l.replace(";", "';")
            if "VARCHAR" in l:
                l = l.replace("VARCHAR", "NVARCHAR")
            return l
        s = '\n'.join([process(line) for line in s.split("\n")])
        return s

    def _open(self, connection_string):
        import pyodbc
        self._mod = pyodbc
        self._conn = pyodbc.connect(connection_string)


class DBSQLite(_BaseServer):
    def __init__(self, path=None):
        _BaseServer.__init__(self, path)

    def _open(self, path):
        if path != "":
            self._db_path = path
        else:
            self._db_path = _db_path

        self._conn = sqlite3.connect(self._db_path)

    def _commit(self, c):
        self._conn.commit()

    def _rollback(self, c):
        self._conn.rollback()

    def _begin(self, c):
        c.execute("BEGIN")

    def _sqlex(self, c, query, *args, **kwargs):
        try:
            _BaseServer._sqlex(self, c, query, *args, **kwargs)
        except sqlite3.Error as er:
            errmsg = 'SQLite error: %s' % (' '.join(er.args)) + "\n"
            errmsg += "SQLite query:\n"
            errmsg += "-"*30+"\n"
            errmsg += query + "\n"
            errmsg += "-"*30+"\n"
            errmsg += "Exception class is: " + str(er.__class__) + "\n"
            errmsg += 'SQLite traceback: \n'
            errmsg += traceback.format_exc()
            #exc_type, exc_value, exc_tb = sys.exc_info()
            #errmsg += '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb))
            #print("e=",er)


            print(errmsg)

            raise DBException(errmsg)

    def _sqlexm(self, c, query, *args, **kwargs):
        try:
            _BaseServer._sqlexm(self, c, query, *args, **kwargs)
        except sqlite3.Error as er:
            errmsg = 'SQLite error: %s' % (' '.join(er.args)) + "\n"
            errmsg += "SQLite query:\n"
            errmsg += "-"*30+"\n"
            errmsg += query + "\n"
            errmsg += "-"*30+"\n"
            errmsg += "Exception class is: " + str(er.__class__) + "\n"
            errmsg += 'SQLite traceback: \n'
            exc_type, exc_value, exc_tb = sys.exc_info()
            errmsg += '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb))

            print(errmsg)

            raise DBException(errmsg)

    def _sql_translate(self, stms):
        stms = stms.replace(" IDENTITY", "")
        stms = stms.replace(" ON items;", ";")
        stms = stms.replace(" ON drawings;", ";")
        stms = stms.replace(" ON assemblies;", ";")

        return stms

    def _get_tables_list(self):
        c = self._conn.cursor()
        self._sqlex(c, "SELECT name FROM sqlite_master WHERE type='table';")
        return [x[0] for x in c.fetchall()]


class DBPG(_BaseServer):
    def __init__(self, path=None):
        import psycopg2
        self._mod = psycopg2
        _BaseServer.__init__(self, path)

    def _commit(self, c):
        self._conn.commit()

    def _rollback(self, c):
        self._conn.rollback()

    def _begin(self, c):
        c.execute("BEGIN")

    def _sqlex(self, c, query, *args, **kwargs):
        query = self._sql_translate(query)
        try:
            _BaseServer._sqlex(self, c, query, *args, **kwargs)
        except self._mod.Error as e:
            errmsg = "PGError: %s\n"%(e.pgerror)        # error number
            errmsg = "PGCode: %s\n"%(e.pgcode)        # error number
            errmsg += "-"*30+"\n"
            errmsg += query + "\n"
            errmsg += "-"*30+"\n"
            errmsg += 'Traceback: \n'
            exc_type, exc_value, exc_tb = sys.exc_info()
            errmsg += '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb))

            print(errmsg)

            raise DBException(errmsg)

    def _sqlexm(self, c, query, *args, **kwargs):
        query = self._sql_translate(query)
        try:
            _BaseServer._sqlexm(self, c, query, *args, **kwargs)
        except self._mod.Error as e:
            errmsg = "PGError: %s\n"%(e.pgerror)        # error number
            errmsg = "PGCode: %s\n"%(e.pgcode)        # error number
            errmsg += "-"*30+"\n"
            errmsg += query + "\n"
            errmsg += "-"*30+"\n"
            errmsg += 'Traceback: \n'
            exc_type, exc_value, exc_tb = sys.exc_info()
            errmsg += '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb))

            print(errmsg)

            raise DBException(errmsg)


    def _sql_translate(self, s):
        def process(l):
            if "?" in l:
                l = l.replace("?", "%s")
            if "INTEGER NOT NULL IDENTITY PRIMARY KEY" in l:
                l = l.replace("INTEGER NOT NULL IDENTITY PRIMARY KEY",
                    "SERIAL PRIMARY KEY")
            return l
        s = '\n'.join([process(line) for line in s.split("\n")])
        return s

    def _open(self, path):

        self._conn = self.psycopg2.connect(path)

    def _get_tables_list(self):
        c = self._conn.cursor()
        self._sqlex(c, """
            SELECT tablename
                FROM pg_catalog.pg_tables
                WHERE schemaname != 'pg_catalog' AND
                    schemaname != 'information_schema';
            """)

        return [x[0] for x in c.fetchall()]


_globaDBInstance = None
def DB(path=None):
    global _globaDBInstance
    global connection

    if _globaDBInstance:
        return _globaDBInstance

    if not path is None:
        if path.upper().startswith("SQLITE:"):
            _globaDBInstance = DBSQLite(path[7:])
            return _globaDBInstance
        elif path.upper().startswith("SQLSERVER:"):
            _globaDBInstance = DBSQLServer(path[10:])
            return _globaDBInstance

        assert (False)

    dbtype = cfg.config().get("BOMBROWSER", "db")
    if dbtype == "sqlite":
        path = cfg.config().get("SQLITE", "path")
        _globaDBInstance = DBSQLite(path)
        connection="Server: SQLITE:"+path[-30:]
        return _globaDBInstance
    elif dbtype == "sqlserver":
        connection_string = cfg.config().get("SQLSERVER", "conn")
        _globaDBInstance = DBSQLServer(connection_string)
        connection="Server: SQLSERVER"
        return _globaDBInstance
    elif dbtype == "postgresql":
        d = {
            "server": cfg.config().get("POSTGRESQL", "server"),
            "database": cfg.config().get("POSTGRESQL", "database"),
            "username": cfg.config().get("POSTGRESQL", "username"),
            "password": cfg.config().get("POSTGRESQL", "password"),
        }
        d["password"] = customize.database_password(d["password"])
        connection_string = "host={server} dbname={database} user={username} password={password}".format(**d)
        connection="Server: PostgreSQL:"+d["username"]+"@"+d["server"]+":"+d["database"]
        _globaDBInstance = DBPG(connection_string)
        return _globaDBInstance

    assert(False)


