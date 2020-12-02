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

import sqlite3
import sys
import pprint
import datetime

def increase_date(d, inc=+1):
    return (datetime.date.fromisoformat(d) +
            datetime.timedelta(days=inc)).isoformat()

_db_path = "database.sqlite"
# infinity date
end_of_the_world = 999999

class DB:

    def __init__(self, path=None):
        if path:
            self._db_path = path
        else:
            self._db_path = _db_path
        self._conn = sqlite3.connect(_db_path)
        c = self._conn.cursor()
        c.execute("SELECT value FROM database_props WHERE key='ver'")
        self._ver = c.fetchone()[0]

        self._check_for_db_update()

    def _check_for_db_update(self):
        #print("self._ver =", self._ver)
        if self._ver == "0.1":
            c = self._conn.cursor()
            c.execute("""
                ALTER TABLE assemblies
                ADD COLUMN date_from_days  INTEGER DEFAULT 0
            """)
            c.execute("""
                ALTER TABLE assemblies
                ADD COLUMN date_to_days  INTEGER DEFAULT 999999
            """)
            c.execute("""
                UPDATE assemblies SET
                    date_from = SUBSTR(date_from,1, 10)
            """)
            c.execute("""
                UPDATE assemblies SET
                    date_to = SUBSTR(date_to,1, 10)
            """)
            c.execute("""
                UPDATE assemblies SET
                    date_from_days = CAST(
                        (JULIANDAY(date_from) - JULIANDAY('0000-12-31')) AS
                        INTEGER)
            """)
            c.execute("""
                UPDATE assemblies SET
                    date_to_days = CAST(
                        (JULIANDAY(date_to) - JULIANDAY('0000-12-31')) AS
                        INTEGER)
            """)
            c.execute("""
                UPDATE assemblies
                SET date_to_days = 999999
                WHERE date_to_sec = 9999999999
            """)
            c.execute("""
                UPDATE database_props
                SET value = '0.2'
                WHERE key == 'ver'
            """)
            self._conn.commit()
            self._ver = "0.2"

        if self._ver == "0.2":
            return

        print("Unknown database version: abort")
        sys.exit(100)


    @staticmethod
    def create_db(path=None):
        if not path:
            path = _db_path
        stmts = """
            DROP INDEX IF EXISTS item_code_idx;
            DROP INDEX IF EXISTS item_code_ver_idx;
            DROP INDEX IF EXISTS item_code_ver_iter;
            DROP INDEX IF EXISTS drawing_idx;
            DROP INDEX IF EXISTS assemblies_child_idx;
            DROP INDEX IF EXISTS assemblies_parent_idx;

            DROP TABLE IF EXISTS assemblies;
            DROP TABLE IF EXISTS item_properties;
            DROP TABLE IF EXISTS database_props;
            DROP TABLE IF EXISTS drawings;
            DROP TABLE IF EXISTS items;

            CREATE TABLE    items (
                id          INTEGER NOT NULL PRIMARY KEY,
                descr       TEXT NOT NULL,
                code        TEXT NOT NULL,
                ver         TEXT NOT NULL,
                iter        INTEGER,
                default_unit TEXT NOT NULL,
                for1cod     TEXT DEFAILT "",
                for1id      TEXT DEFAILT "",
                for1name    TEXT DEFAILT "",
                prod1cod    TEXT DEFAILT "",
                prod1name   TEXT DEFAILT "",
                prod2cod    TEXT DEFAILT "",
                prod2name   TEXT DEFAILT ""
            );
            CREATE INDEX item_code_idx             ON items(code);
            CREATE INDEX item_code_ver_idx         ON items(code, ver);
            CREATE UNIQUE INDEX item_code_ver_iter ON items(code, ver, iter);

            CREATE TABLE item_properties (
                id          INTEGER NOT NULL PRIMARY KEY,
                descr       TEXT,
                value       TEXT,
                item_id     INTEGER,

                FOREIGN KEY (item_id) REFERENCES items(id)
            );
            CREATE UNIQUE INDEX item_prop_descr_iid ON item_properties(item_id, descr);

            CREATE TABLE assemblies (
                id              INTEGER NOT NULL PRIMARY KEY,
                unit            TEXT,
                child_id        INTEGER,
                parent_id       INTEGER,
                qty             FLOAT,
                each            FLOAT DEFAULT 1.0,
                date_from       TEXT NOT NULL DEFAULT '0000-00-00',
                date_to         TEXT DEFAULT NULL,
                date_from_days  INTEGER DEFAULT 0,
                date_to_days    INTEGER DEFAULT 999999,
                iter            INTEGER,
                ref             TEXT DEFAULT "",

                FOREIGN KEY (child_id) REFERENCES items(id),
                FOREIGN KEY (parent_id) REFERENCES items(id)
            );

            CREATE INDEX assemblies_child_idx ON assemblies(child_id);
            CREATE INDEX assemblies_parent_idx ON assemblies(parent_id);

            CREATE TABLE database_props (
                id          INTEGER NOT NULL PRIMARY KEY,
                key         TEXT,
                value       TEXT
            );

            INSERT INTO database_props (key, value) VALUES ('ver', '0.2');

            CREATE TABLE drawings (
                id          INTEGER NOT NULL PRIMARY KEY,
                code        TEXT NOT NULL,
                item_id     INTEGER,
                filename    TEXT NOT NULL,
                fullpath    TEXT NOT NULL,

                FOREIGN KEY (item_id) REFERENCES items(id)
            );

        """

        conn = sqlite3.connect(path)
        c = conn.cursor()
        for s in stmts.split(";"):
            c.execute(s)
        conn.commit()

    def get_code(self, id_code):
        c = self._conn.cursor()
        c.execute("""
            SELECT code, descr, ver, iter, default_unit,
                for1cod, for1name,
                prod1cod, prod1name, prod2cod, prod2cod
            FROM items
            WHERE id=?
            """, (id_code, ))
        res = c.fetchone()
        if not res:
            return None

        data = dict()
        data["code"] = res[0]
        data["descr"] = res[1]
        data["ver"] = res[2]
        data["iter"] = res[3]
        data["unit"] = res[4]

        data["for1name"] = res[6]
        data["for1cod"] = res[5]
        data["prod1name"] = res[8]
        data["prod1cod"] = res[7]
        data["prod2name"] = res[10]
        data["prod2cod"] = res[9]

        data["properties"] = dict()

        c.execute("""
            SELECT descr, value
            FROM item_properties
            WHERE item_id=?
            """, (id_code, ))

        res = c.fetchall()
        if res:
            for k,v in res:
                data["properties"][k] = v

        return data

    def get_codes_by_code(self, code):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, code, descr, ver, iter, default_unit
            FROM items
            WHERE code=?
            ORDER BY id
            """, (code, ))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_code(self, code):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, code, descr, ver, iter, default_unit
            FROM items
            WHERE code like ?
            ORDER BY id
            """, (code, ))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_descr(self, descr):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, code, descr, ver, iter, default_unit
            FROM items
            WHERE descr like ?
            ORDER BY id
            """, (descr, ))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_code_and_descr(self, code, descr):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, code, descr, ver, iter, default_unit
            FROM items
            WHERE descr like ? and code like ?
            ORDER BY id
            """, (descr, code))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_dates_by_code_id(self, id_code):
        c = self._conn.cursor()
        c.execute("""SELECT DISTINCT i.code, a.date_from, a.date_to
                     FROM            assemblies AS a
                     LEFT JOIN items AS i ON a.parent_id = i.id
                     WHERE           a.parent_id = ?
                     ORDER BY        a.date_from DESC
                  """, (id_code, ))

        l =  [list(x) for x in c.fetchall()]
        dtmax = ""
        for i in l:
            if i[2] == "":
                dtmax = ""
                break
            if dtmax < i[2]:
                dtmax = i[2]
        l.sort(key= lambda x: x[1])

        i = 0
        while i < len(l) -1:
            if l[i][1] == l[i+1][1]:
                l.pop(i)
                continue
            i += 1

        for i in range(len(l)-1):
            l[i][2] = increase_date(l[i+1][1], -1)

        l[-1][2] = dtmax

        return l

    def is_assembly(self, id_code):
        c = self._conn.cursor()
        c.execute("""SELECT COUNT(*)
                     FROM   assemblies
                     WHERE  parent_id = ?
                  """, (id_code, ))

        return c.fetchone()[0] > 0

    def get_bom_by_code_id2(self, code_id0, date_from):
        data = dict()

        c = self._conn.cursor()

        c.execute("""SELECT i.code, a.date_from_days, a.date_to_days
                     FROM items AS i
                     LEFT JOIN assemblies AS a
                       ON a.parent_id = i.id
                     WHERE
                        i.id = ?
                       AND
                        a.date_from = ?""",
                     (code_id0, date_from) )

        (code0, date_from_days, date_to_days) = c.fetchone()
        todo = [(code_id0, date_from, "N/A")]
        #todo = [code_id0]
        done = []

        while len(todo):
            (code_id, date_from, date_to) = todo.pop()
            done.append(code_id)
            d2 = self.get_code(code_id)
            d2["id"] = code_id
            d = d2["properties"]
            d2.pop("properties")
            d["date_from"] = date_from
            d["date_to"] = date_to
            d.update(d2)
            d["deps"] = dict()


            c.execute("""
                SELECT a.unit, a.qty, a.each, a.date_from, a.date_to,
                        a.iter, a.child_id, a.parent_id, a.date_from_days, a.date_to_days, ref
                FROM assemblies AS a
                WHERE
                    a.parent_id = ?
                  AND
                    a.date_from_days <= ?
                  AND
                    ? < a.date_to_days
                ORDER BY a.id
                """, (code_id, date_from_days, date_from_days))

            children = c.fetchall()

            if children is None or len(children) == 0:
                data[d["id"]] = d
                continue

            for (unit, qty, each, date_from_, date_to_, it, child_id,
                 parent_id, date_from_days_, date_to_days_, ref) in children:
                d["deps"][child_id] = {
                    "code_id": child_id,
                    "unit": unit,
                    "qty": qty,
                    "each": each,
                    "iter": it,
                    "ref": ref,
                }

                if not child_id in done:
                    todo.append((child_id, date_from_, date_to_))

            data[d["id"]] = d

        mindt = "N/A"
        for k in data[code_id0]["deps"]:
            cid = data[code_id0]["deps"][k]["code_id"]
            if mindt == "N/A" or mindt > data[cid]["date_to"]:
                mindt = data[cid]["date_to"]
        data[code_id0]["date_to"] = mindt

        return (code_id0, data)


    def _get_parents(self, id_code, date_from_days, date_to_days):
        c = self._conn.cursor()
        c.execute("""
            SELECT a.unit, c.code, c.default_unit, a.qty, a.each, a.date_from, a.date_to,
                    a.iter, a.parent_id, a.date_from, a.date_to, a.date_from_days,
                    a.date_to_days
            FROM assemblies AS a
            LEFT JOIN items AS c
                ON a.parent_id = c.id
            WHERE child_id = ?
              AND a.date_from_days >= ?
              AND a.date_to_days <= ?
            ORDER BY c.code, a.date_from_days DESC
            """, (id_code, date_from_days, date_to_days))

        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def _join_data(self, data):
        #return
        keys = list(data.keys())
        keys.sort(reverse=True)
        pprint.pprint(keys)

        i = 0
        while i < len(keys)-1:
            (code1, date_from1, date_to1) = keys[i]
            (code2, date_from2, date_to2) = keys[i+1]

            if code1 != code2:
                i += 1
                continue

            v1 = data[keys[i]]
            v2 = data[keys[i+1]]

            #assert(date_from2 > date_to1)

            #date1to = datetime.date.fromisoformat(v1["date_to"]).toordinal()
            #date2from = datetime.date.fromisoformat(v2["date_from"]).toordinal()
            if (date_from2 - date_to1) > 1:
                i += 1
                continue

            equal = True
            for k in v1.keys():
                if k == "date_from" or k == "date_to":
                    continue
                if v1[k] != v2[k]:
                    equal = False
                    break

            if not equal:
                i += 1
                continue

            data[keys[i]]["date_to"] = data[keys[i+1]]["date_to"]
            data.pop(keys[i+1])
            keys.pop(i+1)

    def get_where_used_from_id_code(self, id_code, xdate_from=0, xdate_to=end_of_the_world):
        code0 = self.get_code(id_code)
        code0 = code0["code"] # code

        data = dict()
        todo = [(id_code, xdate_from, xdate_to)]
        done = []

        while len(todo):
            id_, xdate_from, xdate_to = todo.pop()
            done.append((id_, xdate_from, xdate_to))

            d2 = self.get_code(id_)
            d2["id"] = id_
            d = d2["properties"]
            d2.pop("properties")
            if xdate_from > 0:
                d["date_from"] = datetime.date.fromordinal(xdate_from).isoformat()
            else:
                d["date_from"] = ""
            if xdate_to < end_of_the_world:
                d["date_to"] = datetime.date.fromordinal(xdate_to).isoformat()
            else:
                d["date_to"] = ""
            if d2["code"] == '100001':
                print('100001', d["date_from"], d["date_to"])
            d.update(d2)
            parents = self._get_parents(id_, xdate_from, xdate_to)
            d["deps"] = dict()
            if parents is None or len(parents) == 0:
                data[(d["code"], xdate_from, xdate_to)] = d
                continue

            for (unit, cc, def_unit, qty, each, date_from, date_to, it,
                    parent_id, date_from_, date_to_, date_from_days,
                    date_to_days) in parents:
                if unit is None:
                   unit = def_unit
                d["deps"][(cc, date_from_days, date_to_days)] = {
                    "code": cc,
                    "unit": unit,
                    "qty": qty,
                    "each": each,
                    "iter": it,
                    "ref": "",
                    #"date_from": date_from_,
                    #"date_to": date_to_,
                }

                #print(date_from_days, xdate_from)
                assert(date_from_days >= xdate_from)

                if not (parent_id, date_from_days, date_to_days) in done:
                    todo.append((parent_id, date_from_days, date_to_days))



            data[(d["code"], xdate_from, xdate_to)] = d
            #pprint.pprint(data)
            #pprint.pprint(todo)
            #print("todo=", todo)

        #self._join_data(data)

        return ((code0, 0, end_of_the_world), data)

    def get_drawings_by_code_id(self, code_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT filename, fullpath
            FROM drawings
            WHERE item_id = ?
            """, (code_id,))

        res = c.fetchall()
        if not res:
            return []
        else:
            return res



