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
import jdutil

def increase_date(d, inc=+1):
    return (datetime.date.fromisoformat(d) +
            datetime.timedelta(days=inc)).isoformat()

def iso_to_days(txt):
    return jdutil.datetime.fromisoformat(txt).to_jd() - 2451544.5

_db_path = "database.sqlite"
# infinity date
end_of_the_world = 999999

class DBSQLServer:

    def __init__(self, path):
        self._open(path)


        #print("table list=", list(self._get_tables_list()))
        if "database_props" in self._get_tables_list():
        #try:
            c = self._conn.cursor()
            c.execute("""SELECT value FROM database_props WHERE "key"='ver'""")
            self._ver = c.fetchone()[0]

            self._check_for_db_update(c)
        #except:
            #print("WARN: table database_props might not exist")
            #print("ver=", self._ver)
        else:
            self._ver = "empty"

    def _sql_translate(self, s):
        return s

    def _open(self, connection_string):
        import pyodbc
        self._conn = pyodbc.connect(connection_string)

    def _get_tables_list(self):
        cursor = self._conn.cursor()
        return [row.table_name for row in cursor.tables()]

    def _check_for_db_update(self, c):
        #print("self._ver =", self._ver)
        if self._ver == "0.1":
            smts = """
                -- ver 0.1 -> ver 0.2
                ALTER TABLE assemblies
                ADD COLUMN date_from_days  INTEGER DEFAULT 0;

                ALTER TABLE assemblies
                ADD COLUMN date_to_days  INTEGER DEFAULT 999999;

                UPDATE assemblies SET date_from = SUBSTR(date_from,1, 10);

                UPDATE assemblies SET date_to = SUBSTR(date_to,1, 10);

                UPDATE assemblies SET
                    date_from_days = CAST(
                        (JULIANDAY(date_from) - JULIANDAY('2000-01-01')) AS
                        INTEGER);

                UPDATE assemblies SET
                    date_to_days = CAST(
                        (JULIANDAY(date_to) - JULIANDAY('2000-01-01')) AS
                        INTEGER);

                UPDATE assemblies
                SET date_to_days = 999999
                WHERE date_to_sec = 9999999999;

                UPDATE database_props
                SET value = '0.2'
                WHERE key == 'ver';
            """

            for s in smts.split(";"):
                c.execute(s)
            self._conn.commit()
            self._ver = "0.2"

        if self._ver == "0.2":
            smts = """
                -- ver 0.2 -> ver 0.3

                DROP TABLE IF EXISTS item_revisions;

                CREATE TABLE item_revisions (
                    id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                    code_id         INTEGER,
                    date_from       VARCHAR(255) NOT NULL DEFAULT '2000-01-01',
                    date_to         VARCHAR(255) DEFAULT '4737-11-27',
                    date_from_days  INTEGER DEFAULT 0,
                    date_to_days    INTEGER DEFAULT 999999,
                    ver             VARCHAR(10) NOT NULL,
                    iter            INTEGER,
                    note            VARCHAR(255),
                    descr           VARCHAR(255) NOT NULL,
                    default_unit    VARCHAR(255) NOT NULL,
                    for1cod         VARCHAR(255) DEFAULT '',
                    for1name        VARCHAR(255) DEFAULT '',
                    prod1cod        VARCHAR(255) DEFAULT '',
                    prod1name       VARCHAR(255) DEFAULT '',
                    prod2cod        VARCHAR(255) DEFAULT '',
                    prod2name       VARCHAR(255) DEFAULT '',

                    FOREIGN KEY (code_id) REFERENCES items(id)
                );

                ALTER TABLE assemblies
                RENAME TO old_assemblies;

                CREATE TABLE assemblies (
                    id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                    unit            VARCHAR(255),
                    child_id        INTEGER,
                    revision_id     INTEGER,
                    qty             FLOAT,
                    each            FLOAT DEFAULT 1.0,
                    ref             VARCHAR(255) DEFAULT '',

                    FOREIGN KEY (child_id) REFERENCES items(id),
                    FOREIGN KEY (revision_id) REFERENCES item_revision(id)
                );

                DROP INDEX IF EXISTS assemblies_child_idx;
                DROP INDEX IF EXISTS assemblies_parent_idx;

                CREATE INDEX assemblies_child_idx ON assemblies(child_id);
                CREATE INDEX assemblies_revision_idx ON assemblies(revision_id);

                INSERT INTO item_revisions(
                    code_id,
                    date_from, date_to, date_from_days, date_to_days,
                    ver, iter,
                    note,
                    descr, default_unit,
                    for1cod, for1name, prod1cod, prod1name,
                    prod2cod, prod2name
                ) SELECT DISTINCT
                    a.parent_id,
                    a.date_from, a.date_to, a.date_from_days, a.date_to_days,
                    i.ver, i.iter,
                    '',
                    i.descr, i.default_unit,
                    i.for1cod, i.for1name, i.prod1cod, i.prod1name,
                    i.prod2cod, i.prod2name
                FROM old_assemblies AS a
                LEFT JOIN items AS i ON a.parent_id = i.id;

                INSERT INTO item_revisions(
                    code_id,
                    -- date are got from default
                    ver, iter,
                    note,
                    descr, default_unit,
                    for1cod, for1name, prod1cod, prod1name,
                    prod2cod, prod2name
                ) SELECT
                    id,
                    0, 0,
                    '',
                    descr, default_unit,
                    for1cod, for1name, prod1cod, prod1name,
                    prod2cod, prod2name
                FROM items
                WHERE NOT id IN (SELECT DISTINCT parent_id FROM old_assemblies);

                INSERT INTO assemblies (
                    unit,
                    child_id,
                    revision_id,
                    qty,
                    each,
                    ref
                ) SELECT
                    a.unit,
                    a.child_id,
                    r.id,
                    a.qty,
                    a.each,
                    a.ref
                FROM old_assemblies AS a
                LEFT JOIN item_revisions AS r
                   ON r.code_id = a.parent_id AND
                    r.date_from_days = a.date_from_days AND
                    r.date_to_days = a.date_to_days;

                CREATE INDEX revision_code_id ON item_revisions(code_id);
                CREATE INDEX revision_date_from ON item_revisions(date_from);
                CREATE INDEX revision_date_from_days ON item_revisions(date_from_days);
                CREATE INDEX revision_date_to ON item_revisions(date_to);
                CREATE INDEX revision_date_to_days ON item_revisions(date_to_days);
                CREATE INDEX revision_code_id_date ON
                    item_revisions(code_id, date_from_days);

                -- rename column instead fo dropping
                ALTER TABLE items
                RENAME COLUMN ver TO old_ver;

                ALTER TABLE items
                RENAME COLUMN iter TO old_iter;

                ALTER TABLE items
                RENAME COLUMN descr TO old_descr;

                ALTER TABLE items
                RENAME COLUMN default_unit TO old_default_unit;

                ALTER TABLE items
                RENAME COLUMN for1cod TO old_for1cod;

                ALTER TABLE items
                RENAME COLUMN for1name TO old_for1name;

                ALTER TABLE items
                RENAME COLUMN prod1cod TO old_prod1cod;

                ALTER TABLE items
                RENAME COLUMN prod1name TO old_prod1name;

                ALTER TABLE items
                RENAME COLUMN for1id TO old_for1id;

                ALTER TABLE items
                RENAME COLUMN prod2cod TO old_prod2cod;

                ALTER TABLE items
                RENAME COLUMN prod2name TO old_prod2name;

                UPDATE database_props
                SET value = '0.3'
                WHERE key == 'ver';
            """

            smts = self._sql_translate(smts)
            for s in smts.split(";"):
                print("smt=",s)
                c.execute(s)
            self._conn.commit()
            self._ver = "0.3"

        if self._ver == "0.3":
            return

        print("Unknown database version: abort")
        sys.exit(100)

    def create_db(self):
        stms = """
            --
            -- ver 0.3
            --
            DROP INDEX IF EXISTS item_code_idx ON items;
            DROP INDEX IF EXISTS item_code_ver_idx ON items;
            DROP INDEX IF EXISTS item_code_ver_iter ON items;
            DROP INDEX IF EXISTS drawing_idx ON drawings;
            DROP INDEX IF EXISTS assemblies_child_idx ON assemblies;
            DROP INDEX IF EXISTS assemblies_parent_idx ON assemblies;

            DROP TABLE IF EXISTS assemblies;
            DROP TABLE IF EXISTS item_properties;
            DROP TABLE IF EXISTS database_props;
            DROP TABLE IF EXISTS drawings;
            DROP TABLE IF EXISTS items;

            CREATE TABLE    items (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) NOT NULL,
            );

            CREATE INDEX item_code_idx             ON items(code);
            CREATE INDEX item_code_ver_idx         ON items(code, ver);
            CREATE UNIQUE INDEX item_code_ver_iter ON items(code, ver, iter);

            CREATE TABLE item_revisions (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code_id         INTEGER,
                date_from       VARCHAR(255) NOT NULL DEFAULT '0000-00-00',
                date_to         VARCHAR(255) DEFAULT NULL,
                date_from_days  INTEGER DEFAULT 0,
                date_to_days    INTEGER DEFAULT 999999,
                ver             VARCHAR(10) NOT NULL,
                iter            INTEGER,
                note            VARCHAR(255),
                descr           VARCHAR(255) NOT NULL,
                ver             VARCHAR(10) NOT NULL,
                iter            INTEGER,
                default_unit    VARCHAR(255) NOT NULL,
                for1cod         VARCHAR(255) DEFAULT '',
                for1id          VARCHAR(255) DEFAULT '',
                for1name        VARCHAR(255) DEFAULT '',
                prod1cod        VARCHAR(255) DEFAULT '',
                prod1name       VARCHAR(255) DEFAULT '',
                prod2cod        VARCHAR(255) DEFAULT '',
                prod2name       VARCHAR(255) DEFAULT '',

                FOREIGN KEY (code_id) REFERENCES items(id)
            );

            CREATE INDEX revision_code_id ON item_revisions(code_id);
            CREATE INDEX revision_code_id_date ON
                item_revisions(code_id, date_from_days);
            CREATE INDEX revision_date_from ON item_revisions(date_from);
            CREATE INDEX revision_date_from_days ON item_revisions(date_from_days);
            CREATE INDEX revision_date_to ON item_revisions(date_to);
            CREATE INDEX revision_date_to_days ON item_revisions(date_to_days);


            CREATE TABLE item_properties (
                id          INTEGER NOT NULL PRIMARY KEY,
                descr       VARCHAR(255),
                value       VARCHAR(255),
                revision_id     INTEGER,

                FOREIGN KEY (item_id) REFERENCES item_revisions(id)
            );
            CREATE UNIQUE INDEX item_prop_descr_iid ON item_properties(item_id, descr);

            CREATE TABLE assemblies (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                unit            VARCHAR(255),
                child_id        INTEGER,
                revision_id     INTEGER,
                qty             FLOAT,
                each            FLOAT DEFAULT 1.0,

                FOREIGN KEY (child_id) REFERENCES items(id),
                FOREIGN KEY (revision_id) REFERENCES item_revision(id)
            );

            CREATE INDEX assemblies_child_idx ON assemblies(child_id);
            CREATE INDEX assemblies_revision_idx ON assemblies(revision_id);

            CREATE TABLE database_props (
                id          INTEGER NOT NULL IDENTITY PRIMARY  KEY,
                "key"       VARCHAR(255),
                value       VARCHAR(255)
            );

            INSERT INTO database_props ("key", value) VALUES ('ver', '0.2');

            CREATE TABLE drawings (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) DEFAULT '',
                item_id     INTEGER,
                filename    VARCHAR(255) NOT NULL,
                fullpath    VARCHAR(255) NOT NULL,

                FOREIGN KEY (item_id) REFERENCES items(id)
            );

        """

        stms = self._sql_translate(stms)
        c = self._conn.cursor()
        for s in stms.split(";"):
            #print("Executing '%s'"%(s))
            c.execute(s)
        self._conn.commit()

    def get_code(self, id_code, date_from):
        return self._get_code(self._conn.cursor(), id_code, date_from)

    def _get_code(self, c, id_code, date_from_days):

        c.execute("""
            SELECT i.code, r.descr, r.ver, r.iter, r.default_unit,
                r.for1cod, r.for1name,
                r.prod1cod, r.prod1name, r.prod2cod, r.prod2name,
                r.date_from, r.date_from_days, r.date_to, r.date_to_days, r.id
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

        data["for1name"] = res[6]
        data["for1cod"] = res[5]
        data["prod1name"] = res[8]
        data["prod1cod"] = res[7]
        data["prod2cod"] = res[9]
        data["prod2name"] = res[10]

        data["date_from"] = res[11]
        data["date_from_days"] = res[12]
        data["date_to"] = res[13]
        data["date_to_days"] = res[14]

        data["rid"] = res[15]
        data["id"] = id_code

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

    def _get_code_from_rid(self, c, rid):

        c.execute("""
            SELECT i.code, r.descr, r.ver, r.iter, r.default_unit,
                r.for1cod, r.for1name,
                r.prod1cod, r.prod1name, r.prod2cod, r.prod2name,
                r.date_from, r.date_from_days, r.date_to, r.date_to_days,
                i.id
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

        data["for1name"] = res[6]
        data["for1cod"] = res[5]
        data["prod1name"] = res[8]
        data["prod1cod"] = res[7]
        data["prod2cod"] = res[9]
        data["prod2name"] = res[10]

        data["date_from"] = res[11]
        data["date_from_days"] = res[12]
        data["date_to"] = res[13]
        data["date_to_days"] = res[14]

        data["id"] = res[15]
        data["rid"] = rid


        data["properties"] = dict()

        #c.execute("""
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
        c.execute("""
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM items AS i
            LEFT JOIN  (
                SELECT descr, ver, iter, default_unit, code_id, MAX(date_from_days)
                FROM item_revisions
                GROUP BY code_id
            ) AS r
                ON r.code_id = i.id
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
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM items AS i
            LEFT JOIN (
                SELECT descr, ver, iter, default_unit, code_id, MAX(date_from_days)
                FROM item_revisions
                GROUP BY code_id
            ) AS r
                ON r.code_id = i.id
            WHERE i.code LIKE ?
            ORDER BY i.id
            """, (code, ))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_descr(self, descr):
        c = self._conn.cursor()
        c.execute("""
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM items AS i
            LEFT JOIN  (
                SELECT descr, ver, iter, default_unit, code_id, MAX(date_from_days)
                FROM item_revisions
                GROUP BY code_id
            ) AS r
                ON r.code_id = i.id
            WHERE r.descr = ?
            ORDER BY i.id
            """, (descr, ))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_codes_by_like_code_and_descr(self, code, descr):
        c = self._conn.cursor()
        c.execute("""
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM items AS i
            LEFT JOIN  (
                SELECT descr, ver, iter, default_unit, code_id, MAX(date_from_days)
                FROM item_revisions
                GROUP BY code_id
            ) AS r
                ON r.code_id = i.id
            WHERE r.descr like ? and i.code like ?
            ORDER BY i.id
            """, (descr, code))
        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_dates_by_code_id2(self, id_code):
        c = self._conn.cursor()
        c.execute("""SELECT DISTINCT i.code, r.descr,
                                     r.date_from, r.date_from_days,
                                     r.date_to, r.date_to_days
                     FROM  item_revisions AS r
                     LEFT JOIN items AS i ON r.code_id = i.id
                     WHERE           r.code_id = ?
                     ORDER BY        r.date_from DESC
                  """, (id_code, ))

        return list(c.fetchall())

    def get_dates_by_code_id(self, id_code):
        c = self._conn.cursor()
        c.execute("""SELECT DISTINCT i.code, r.date_from, r.date_to
                     FROM            item_revisions AS r
                     LEFT JOIN items AS i ON r.code_id = i.id
                     WHERE           r.code_id = ?
                     ORDER BY        r.date_from ASC
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
                     FROM item_revisions
                     WHERE  code_id = ?
                  """, (id_code, ))

        return c.fetchone()[0] > 0

    def get_bom_by_code_id2(self, code_id0, date_from):

        date_from_days_ref = iso_to_days(date_from)

        data = dict()

        c = self._conn.cursor()

        c.execute("""SELECT i.code, r.date_from_days, r.date_to_days, r.id
                     FROM item_revisions AS r
                     LEFT JOIN items AS i
                       ON i.id = r.code_id
                     WHERE  r.code_id = ?
                       AND  r.date_from_days <= ?
                       AND   ? < r.date_to_days """,
                     (code_id0, date_from_days_ref, date_from_days_ref) )

        (code0, date_from_days, date_to_days, rid) = c.fetchall()[0]
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

            c.execute("""
                SELECT a.unit, a.qty, a.each, rc.date_from, rc.date_to,
                        rc.iter, a.child_id, rc.code_id, rc.date_from_days,
                        rc.date_to_days, a.ref, rc.id
                FROM assemblies AS a
                LEFT JOIN item_revisions AS rc
                  ON a.child_id = rc.code_id
                WHERE   a.revision_id = ?
                  AND   rc.date_from_days <= ?
                  AND   ? < rc.date_to_days
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
        c.execute("""
            SELECT a.unit, c.code, r.default_unit, a.qty, a.each, r.date_from, r.date_to,
                    r.iter, r.code_id, r.date_from, r.date_to, r.date_from_days,
                    r.date_to_days
            FROM assemblies AS a
            LEFT JOIN item_revisions AS r
                ON a.revision_id = r.id
            LEFT JOIN items AS c
                ON r.code_id = c.id

            WHERE child_id = ?
              AND r.date_from_days >= ?
              AND r.date_to_days <= ?
            ORDER BY c.code, r.date_from_days DESC
            """, (id_code, date_from_days, date_to_days))

        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    # TODO FIX ME
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
        c = self._conn.cursor()

        c.execute("""
            SELECT code FROM items WHERE id=?
        """, (id_code,))
        code0 = c.fetchone()[0]

        c.execute("""
            SELECT MIN(date_from_days)
            FROM item_revisions
            WHERE code_id = ? AND date_from_days >= ?
        """, (id_code, xdate_from))
        xdate_from0 = c.fetchone()[0]

        c.execute("""
            SELECT MIN(date_to_days)
            FROM item_revisions
            WHERE code_id = ? AND date_to_days >= ?
        """, (id_code, xdate_to))
        xdate_to0 = c.fetchone()[0]

        todo = [(id_code, xdate_from0, xdate_to0)]
        data = dict()
        done = []

        while len(todo):
            id_, xdate_from, xdate_to = todo.pop()
            done.append((id_, xdate_from, xdate_to))

            d2 = self._get_code(c, id_, xdate_from)
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

            d.update(d2)
            parents = self._get_parents(c, id_, xdate_from, xdate_to)
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

        return ((code0, xdate_from0, xdate_to0), data)

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

class DBSQLite(DBSQLServer):
    def __init__(self, path=None):
        DBSQLServer.__init__(self, path)

    def _open(self, path):
        if path != "":
            self._db_path = path
        else:
            self._db_path = _db_path

        import sqlite3
        self._conn = sqlite3.connect(self._db_path)

    def _sql_translate(self, stms):
        stms = stms.replace(" IDENTITY", "")
        stms = stms.replace(" ON items;", ";")
        stms = stms.replace(" ON drawings;", ";")
        stms = stms.replace(" ON assemblies;", ";")

        return stms

    def _get_tables_list(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [x[0] for x in cursor.fetchall()]


_globaDBInstance = None
def DB(path=None):
    global _globaDBInstance

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

    cfg = configparser.ConfigParser()
    cfg.read_file(open("bombrowser.ini"))
    dbtype = cfg.get("BOMBROWSER", "db")
    if dbtype == "sqlite":
        path = cfg.get("SQLITE", "path")
        _globaDBInstance = DBSQLite(path)
        return _globaDBInstance
    elif dbtype == "sqlserver":
        d = {
            "driver": cfg.get("SQLSERVER", "driver"),
            "server": cfg.get("SQLSERVER", "server"),
            "database": cfg.get("SQLSERVER", "database"),
            "username": cfg.get("SQLSERVER", "username"),
            "password": cfg.get("SQLSERVER", "password"),
        }
        connection_string = "DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}".format(**d)
        _globaDBInstance = DBSQLServer(connection_string)
        return _globaDBInstance
    assert(False)

