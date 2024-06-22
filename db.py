"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021,2022,2023,2024 Goffredo Baroncelli <kreijack@inwind.it>

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
import datetime
import time
import traceback

import jdutil
from utils import xescape, xunescape

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
gvals_count = 20
gavals_count = 3
connection="Server: <UNDEF>"
_globaDBInstance = None
_nested_transaction = 0

class DBException(RuntimeError):
    pass


class DBExceptionWithTraceback(DBException):
    def __init__(self, arg):
        DBException.__init__(self, arg)


class Transaction:
    def __init__(self, d):
        self._db = d
        self._cursor = None
        self._inside_context = False

    def begin(self):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        if self._cursor:
            return

        self._cursor = self._db._get_cursor()
        self._db._begin(self._cursor)

    def execute(self, query, *args):
        self.begin()

        r = self._db._execute(self._cursor, query, *args)
        self.description = self._cursor.description
        return r

    def executemany(self, query, *args):
        self.begin()

        r = self._db._executemany(self._cursor, query, *args)
        self.description = self._cursor.description
        return r

    def fetchone(self):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        return self._db._translate_fetchone_(
            self._cursor,
            self._cursor.fetchone())

    def fetchall(self):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        return self._db._translate_fetchall_(
            self._cursor,
            self._cursor.fetchall())

    def commit(self):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        r = self._db._commit()
        self._cursor = None

        return r

    def rollback(self):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        r = self._db._rollback()

        self._cursor = None

        return r

    def __enter__(self):
        global _nested_transaction
        if _nested_transaction != 0:
            raise DBException("ENESTEDTRANSACTION")
        _nested_transaction += 1

        self._inside_context = True
        return self

    def __exit__(self, type_, value, traceback):
        if self._cursor:
            if value is None:
                self.commit()
            else:
                self.rollback()
        self._cursor = None
        self._inside_context = False
        self._db = None

        global _nested_transaction
        if _nested_transaction != 1:
            raise DBException("ENESTEDTRANSACTION")
        _nested_transaction -= 1


class ROCursor:
    def __init__(self, d):
        self._db = d
        self._cursor = None
        self._inside_context = False

    def _check_query(self, query):
        for w in ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE"]:
            if w in query:
                raise DBException("NOTALLOWEDQUERY: It is not allowed to use %s"%(w))

    def execute(self, query, *args):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        if not self._cursor:
            self._cursor = self._db._get_cursor()

        self._check_query(query)
        r = self._db._execute(self._cursor, query, *args)
        self.description = self._cursor.description
        return r

    def fetchone(self):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        return self._db._translate_fetchone_(
            self._cursor,
            self._cursor.fetchone())

    def fetchall(self):
        if not self._inside_context:
            raise DBException("NOTINCONTEXT")

        return self._db._translate_fetchall_(
            self._cursor,
            self._cursor.fetchall())

    def __enter__(self):
        self._inside_context = True
        return self

    def __exit__(self, type_, value, traceback):
        # do a rollback otherwise postgresql screws
        if isinstance(self._db, DBPG):
            self._db._rollback()
        self._db = None
        self._cursor = None
        self._inside_context = False


class _BaseServer:

    def __init__(self, path):
        self._path = path
        self._conn = None
        self._read_only = None

        self._ver = "empty"

    def get_db_ver(self):
        if self._ver == "empty":
            self._ver = self._fetch_rev()
        return self._ver

    def _fetch_db_rev(self):
        with ROCursor(self) as c:
            if not "database_props" in self._get_tables_list(c):
                return "empty"
            try:
                c.execute("SELECT value FROM database_props WHERE name='ver' ")
                v = c.fetchone()[0]
            except:
                return "empty"
        # for now v0.3 and v0.4 are equal
        assert(v == "0.4" or v == "0.3")
        return v

    def update_gavals_gvals_count_by_db(self):
        global gvals_count, gavals_count
        with ROCursor(self) as c:
            c.execute("SELECT * FROM item_revisions WHERE id=0")
            descr = [str(x[0]).upper() for x in c.description]

        n = -1
        for d in descr:
            if d.startswith("GVAL"):
                n = max(int(d[4:]), n)
        assert(n>0)
        gvals_count = n

        with ROCursor(self) as c:
            c.execute("SELECT * FROM assemblies WHERE id=0")
            descr = [str(x[0]).upper() for x in c.description]

        n = -1
        for d in descr:
            if d.startswith("GAVAL"):
                n = max(int(d[5:]), n)
        assert(n>0)
        gavals_count = n

    # these two methods can be overrided to tweak the data returned by
    # fetchone/fetchall
    def _translate_fetchone_(self, c, x):
        return x

    def _translate_fetchall_(self, c, x):
        return x

    def _get_cursor(self):
        if self._conn is None:
            self._open(self._path)
        try:
            c = self._conn.cursor()
        except:
            try:
                if self._conn:
                    self._conn.close()
            except:
                pass
            finally:
                self._conn = None
            raise

        return c

    def _execute_gen(self, method, query, *args, **kwargs):
        query = self._sql_translate(query)
        try:
            method(query, *args, **kwargs)
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            stack = traceback.extract_stack()
            e._orig_exc_type = exc_type
            e._orig_exc_value = exc_value
            e._orig_exc_tb = exc_tb
            tb = 'Traceback: \n' + "".join(
                traceback.format_list(stack[:-1] +
                traceback.extract_tb(exc_tb)) +
                traceback.format_exception_only(exc_type, exc_value)
            )
            e._orig_traceback = tb
            e._orig_query = query

            self._exception_handler(exc_value)

            raise e

    def _exception_handler(self, exc_value):
        pass

    def _execute(self, c, query, *args, **kwargs):
        self._execute_gen(c.execute, query, *args, **kwargs)

    def _executemany(self, c, query, *args, **kwargs):
        self._execute_gen(c.executemany, query, *args, **kwargs)

    def _commit(self):
        self._conn.commit()

    def _rollback(self):
        self._conn.rollback()

    def _begin(self, c):
        c.execute("BEGIN")

    def _sql_translate(self, s):
        return s

    def _open(self, connection_string):
        raise DBException("Cannot implemented")

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

            -- remember to sync the list_main_tables() method
            DROP TABLE IF EXISTS assemblies;
            DROP TABLE IF EXISTS item_properties;
            DROP TABLE IF EXISTS database_props;
            DROP TABLE IF EXISTS drawings;
            DROP TABLE IF EXISTS item_revisions;
            DROP TABLE IF EXISTS items;

            CREATE TABLE    items (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) NOT NULL
            );

            CREATE UNIQUE INDEX item_code_idx             ON items(code);

            CREATE TABLE item_revisions (
                id              INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code_id         INTEGER,
                date_from       VARCHAR(10) DEFAULT '2000-01-01' NOT NULL ,
                date_to         VARCHAR(10) DEFAULT '',
                date_from_days  INTEGER DEFAULT 0,          -- 2000-01-01
                date_to_days    INTEGER DEFAULT 999999,
                ver             VARCHAR(10) NOT NULL,
                iter            INTEGER,
                type            VARCHAR(255),
                note            VARCHAR(255),
                descr           VARCHAR(255) NOT NULL,
                default_unit    VARCHAR(10) NOT NULL,

                -- the line below will be expanded on the basis of
                -- the global module variable 'gvals_count'
                -- sync the size with the one in bombrowser_admin.py
                gval1           VARCHAR(255) DEFAULT '',

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

                -- the line below will be expanded on the basis of
                -- the global module variable 'gavals_count'
                -- sync the size with the one in bombrowser_admin.py
                gaval1          VARCHAR(255) DEFAULT '',

                FOREIGN KEY (child_id) REFERENCES items(id),
                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );

            CREATE INDEX assemblies_child_idx ON assemblies(child_id);
            CREATE INDEX assemblies_revision_idx ON assemblies(revision_id);
            CREATE UNIQUE INDEX assemblies_child_revision_unique ON assemblies(revision_id, child_id);

            CREATE TABLE database_props (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                name        VARCHAR(255),
                value       VARCHAR(500)
            );

            INSERT INTO database_props (name, value) VALUES ('ver', '0.4');

            CREATE TABLE drawings (
                id          INTEGER NOT NULL IDENTITY PRIMARY KEY,
                code        VARCHAR(255) DEFAULT '',
                revision_id INTEGER,
                filename    VARCHAR(255) NOT NULL,
                fullpath    VARCHAR(255) NOT NULL,

                FOREIGN KEY (revision_id) REFERENCES item_revisions(id)
            );

        """

        t = stms.split("\n")
        s = "gval1           VARCHAR(255) DEFAULT '',"
        for i in range(len(t)):
            if s in t[i]:
                break
        else:
            assert(False and "we need to find 's'")

        k = t[i]
        stms = '\n'.join(t[:i])
        stms += '\n'
        stms += '\n'.join([
            k.replace('1', "%d"%(i)) for i in range(1, gvals_count+1)
        ])
        stms += '\n'
        stms += '\n'.join(t[i+1:])

        t = stms.split("\n")
        s = "gaval1          VARCHAR(255) DEFAULT '',"
        for i in range(len(t)):
            if s in t[i]:
                break
        else:
            assert(False and "we need to find 's'")

        k = t[i]
        stms = '\n'.join(t[:i])
        stms += '\n'
        stms += '\n'.join([
            k.replace('1', "%d"%(i)) for i in range(1, gavals_count+1)
        ])
        stms += '\n'
        stms += '\n'.join(t[i+1:])

        return stms

    def is_db_read_only(self):
        if self._read_only is None:
            read_only = False
            try:
                with Transaction(self) as c:
                    c.execute("""INSERT INTO database_props(name, value)
                                 VALUES ('test_ro', 'test_ro')""")
                    # we want only check if this is possible
                    c.rollback()
            except:
                read_only = True

            self._read_only = read_only

        return self._read_only

    def create_db(self):
        stms = self._get_db_v0_4()
        with Transaction(self) as c:
            for s in stms.split(";"):
                s = s.strip()
                if len(s) == 0:
                    continue
                c.execute(s)

    def dump_table(self, tname):
        with ROCursor(self) as c:
            c.execute("SELECT * FROM "+ tname)
            colnames = [desc[0] for desc in c.description]
            return (colnames, c.fetchall())

    def _insert_table(self, tname, columns, data):
        with Transaction(self) as c:
            self._insert_table_(c, tname, columns, data)

    def _insert_table_(self, c, tname, columns, data):
        c.execute("DELETE FROM " + tname)
        c.execute("SELECT * FROM "+ tname)
        real_colnames = [desc[0].upper() for desc in c.description]
        columns = [x.upper() for x in columns]
        c.fetchall()
        # handle the case where the columns from the backup are
        # differents to the databases ones (i.e. different gaval values)
        final_colnames = []
        final_colnames_idx = []
        for col in real_colnames:
            if not col in columns:
                continue
            i = columns.index(col)
            assert(i >= 0)
            final_colnames.append(col)
            final_colnames_idx.append(i)

        for row in data:
            row2 = []
            for idx in  final_colnames_idx:
                row2.append(row[idx])
            c.execute(("INSERT INTO " + tname +
                " (" + ",".join(final_colnames) + ") VALUES " +
                " (" + ",".join(["?" for i in final_colnames]) + ")"),
                row2)

    def list_main_tables(self):
        # maintain in the correct order by dependecies/foreign keys
        return ["items", "item_revisions", "assemblies",
            "item_properties", "drawings",
            "database_props"]

    def dump_tables(self):
        return [(i, *self.dump_table(i))
            for i in self.list_main_tables()]

    def get_code(self, id_code, date_from_days):
        with ROCursor(self) as c:
            return self._get_code(c, id_code, date_from_days)

    def _get_code(self, c, id_code, date_from_days):
        gval_query = ", ".join(["r.gval%d"%(i+1) for i in range(gvals_count)])

        c.execute("""
            SELECT i.code, r.descr, r.ver, r.iter, r.default_unit,
                   r.date_from_days, r.date_to_days, r.id,
                   """ + gval_query + """
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

        data["date_from"] = days_to_txt(res[5])
        data["date_from_days"] = res[5]
        data["date_to"] = days_to_txt(res[6])
        data["date_to_days"] = res[6]

        data["rid"] = res[7]

        for i in range(gvals_count):
            data["gval%d"%(i+1)] = res[8+i]

        data["id"] = id_code

        data["properties"] = dict()

        c.execute("""
            SELECT descr, value
            FROM item_properties
            WHERE revision_id=?
            """, (data["rid"], ))

        res = c.fetchall()
        if res:
            for k,v in res:
                data["properties"][k] = v

        return data

    def get_full_revision_by_rid(self, rid):
        with ROCursor(self) as cur:
            r = self._get_code_by_rid(cur, rid)
            c = self._get_children_by_rid(cur, rid)
            d = self._get_drawings_by_rid(cur, rid)
        return (r, c, d)

    def get_code_by_rid(self, rid):
        with ROCursor(self) as c:
            return self._get_code_by_rid(c, rid)

    def _get_code_by_rid(self, c, rid):

        gval_query = ", ".join(["r.gval%d"%(i+1) for i in range(gvals_count)])

        c.execute("""
            SELECT i.code, r.descr, r.ver, r.iter, r.default_unit,
                r.date_from_days, r.date_to_days, i.id,
                """ + gval_query + """
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

        data["date_from"] = days_to_txt(res[5])
        data["date_from_days"] = res[5]
        data["date_to"] = days_to_txt(res[6])
        data["date_to_days"] = res[6]

        data["id"] = res[7]

        for i in range(gvals_count):
            data["gval%d"%(i+1)] = res[8+i]

        data["rid"] = rid

        data["properties"] = dict()

        c.execute("""
            SELECT descr, value
            FROM item_properties
            WHERE revision_id=?
            """, (rid, ))

        res = c.fetchall()
        if res:
            for k,v in res:
                data["properties"][k] = v

        return data

    # case sensitive search
    def get_codes_by_code(self, code, case_sensitive=True):
        icode = "i.code"
        if not case_sensitive:
            code = code.upper()
            icode = "UPPER(%s)"%(icode)
        with ROCursor(self) as c:
            c.execute("""
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM (
                    SELECT i.id, MAX(iter) AS iter
                    FROM items AS i
                    LEFT JOIN item_revisions AS r
                        ON r.code_id = i.id
                    WHERE %s = ?
                    GROUP BY i.id
            ) AS r2
            LEFT JOIN item_revisions AS r
                ON r.code_id = r2.id AND r.iter = r2.iter
            LEFT JOIN items AS i
                ON r.code_id = i.id
            ORDER BY r.iter DESC
            """%(icode), (code,))
            res = c.fetchall()
            if not res:
                return None
            else:
                return res

    def _expand_search_str_clauses(self, req, case_sensitive):
        # split query joined by ';'
        req2 = []

        for row in req:
            if len(row) == 2:
                row = list(row)
                row.append(None)

            field, value, func = row
            if len(value) > 0 and value[0] == "=":
                req2.append((field, (value,), func))
                continue

            vs = value.split(";")
            req2.append((field, vs, func))

        q2 = []
        args = []
        for (field, values, func) in req2:
            q = []
            if func is None:
                f = lambda x: x
            else:
                f = func
            for value in values:
                if len(value) > 0 and value[0] in "<=>":
                    op = value[0]
                    arg = f(value[1:])
                elif len(value) > 0 and value[0] == "!":
                    op = "<>"
                    arg = f(value[1:])
                elif "%" in value or "_" in value or "[" in value or "]" in value:
                    op = "LIKE"
                    arg = f(value)
                elif len(value) > 0 and func is None:
                    op = "LIKE"
                    arg = "%" + value + "%"
                elif len(value) > 0 :
                    op = "="
                    arg = f(value)
                else:
                    # if we are here, the field is empty and any <=>! are specified
                    continue

                if not case_sensitive and isinstance(arg, str):
                    arg = arg.upper()
                    q.append("UPPER(%s) %s ?"%(field, op))
                else:
                    q.append("%s %s ?"%(field, op))
                args.append(arg)

            if len(q) > 0:
                if len(q) > 1:
                    q2.append("(" + " OR ".join(q) + ")")
                else:
                    q2.append(q[0])

        qry = " AND ".join(q2)

        return (" " + qry + " ", args)

    # case sensitive search
    def get_codes_by_like_code_and_descr(self, code, descr, case_sensitive=True):
        if code == "" and descr == "":
            return []

        with ROCursor(self) as c:
            q = """
            SELECT i.id, i.code, r.descr, r.ver, r.iter, r.default_unit
            FROM (
                    SELECT i.id, MAX(iter) AS iter
                    FROM item_revisions AS r
                    LEFT JOIN items AS i
                        ON r.code_id = i.id
                    WHERE
            """

            q2, args = self._expand_search_str_clauses((
                ("i.code", code, None),
                ("r.descr", descr, None)
            ), case_sensitive)

            q += """
                        """ + q2
            q += """
                    GROUP BY i.id
            ) AS r2
            LEFT JOIN item_revisions AS r
                ON r.code_id = r2.id AND r.iter = r2.iter
            LEFT JOIN items AS i
                ON r.code_id = i.id
            ORDER BY i.code, r.iter DESC
            """

            c.execute(q, args)
            res = c.fetchall()
            if not res:
                return None
            else:
                return res

    def get_dates_by_code_id3(self, id_code):
        with ROCursor(self) as c:
            c.execute("""SELECT DISTINCT i.code, r.descr,
                                     r.date_from_days, r.date_to_days,
                                     r.id, r.ver, r.iter
                     FROM  item_revisions AS r
                     LEFT JOIN items AS i ON r.code_id = i.id
                     WHERE           r.code_id = ?
                     ORDER BY        r.date_from_days DESC
                  """, (id_code, ))

            return list(c.fetchall())

    def get_parent_dates_range_by_code_id(self, id_code):
        with ROCursor(self) as c:
            return self._get_parent_dates_range_by_code_id(c, id_code)

    def _get_parent_dates_range_by_code_id(self, c, id_code):
        c.execute("""
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
        with ROCursor(self) as c:
            return self._get_children_dates_range_by_rid(c, rid)

    def _get_children_dates_range_by_rid(self, c, rid):
        c.execute("""
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

    def get_bom_by_code_id3(self, code_id0, date_from_days_ref):

        data = dict()

        with ROCursor(self) as c:
            c.execute("""SELECT i.code, r.date_from_days, r.date_to_days, r.id
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
                d2 = self._get_code_by_rid(c, rid)
                d = d2["properties"]
                d2.pop("properties")
                d.update(d2)
                d["deps"] = dict()

                gavals = ""
                for i in range(gavals_count):
                    gavals += ", a.gaval%d"%(i+1)
                c.execute("""
                    SELECT a.unit, a.qty, a.each,
                            rc.iter, a.child_id, rc.code_id, rc.date_from_days,
                            rc.date_to_days, a.ref,
                            rc.id %s
                    FROM assemblies AS a
                    LEFT JOIN item_revisions AS rc
                      ON a.child_id = rc.code_id
                    WHERE   a.revision_id = ?
                      AND   rc.date_from_days <= ?
                      AND   ? <= rc.date_to_days
                    ORDER BY a.id
                    """%(gavals), (rid, date_from_days_ref, date_from_days_ref))

                children = c.fetchall()

                if children is None or len(children) == 0:
                    data[d["id"]] = d
                    continue

                for line in children:
                    (unit, qty, each, it, child_id,parent_id,
                     date_from_days_, date_to_days_, ref, crid) = line[:10]
                    gavalues = line[10:]
                    d["deps"][child_id] = {
                        "code_id": child_id,
                        "unit": unit,
                        "qty": qty,
                        "each": each,
                        "iter": it,
                        "ref": ref,
                    }
                    for i in range(gavals_count):
                        d["deps"][child_id]["gaval%d"%(i+1)] = gavalues[i]

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
            SELECT a.unit, c.code, r.default_unit, a.qty, a.each,
                    r.iter, r.code_id, r.date_from_days, r.date_to_days
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
        c.execute("""
            SELECT a.unit, c.code, r.default_unit, a.qty, a.each,
                    r.iter, r.code_id, r.date_from_days, r.date_to_days
            FROM assemblies AS a
            LEFT JOIN item_revisions AS r
                ON a.revision_id = r.id
            LEFT JOIN items AS c
                ON r.code_id = c.id

            WHERE a.child_id = ?
              AND r.date_to_days >= ?
              AND r.date_from_days < ?
            ORDER BY c.code, r.date_from_days DESC
            """, (id_code, prototype_date - 1, prototype_date))

        res = c.fetchall()
        if not res:
            return None
        else:
            return res

    def get_where_used_from_id_code(self, id_code, valid=False):
        with ROCursor(self) as c:
            c.execute("""
                SELECT code FROM items WHERE id=?
            """, (id_code,))
            code0 = c.fetchone()[0]

            c.execute("""
                SELECT MIN(date_from_days)
                FROM item_revisions
                WHERE code_id = ?
            """, (id_code, ))
            (xdate_from_days0, ) = c.fetchone()

            c.execute("""
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
                        parent_id, date_from_days_, date_to_days_) in parents:
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

    def get_drawings_and_urls_by_rid(self, rev_id):
        with ROCursor(self) as c:
            ret = self._get_drawings_by_rid(c, rev_id)
        return ret

    def _get_drawings_by_rid(self, c, rev_id):
        c.execute("""
            SELECT filename, fullpath
            FROM drawings
            WHERE revision_id = ?
            ORDER BY id
            """, (rev_id,))

        res = c.fetchall()
        if not res:
            return []
        else:
            return res

    def get_bom_dates_by_code_id(self, code_id):
        sdates = set()
        done = set()
        todo = [code_id]

        with ROCursor(self) as c:
            c.execute("""
                SELECT MIN(date_from_days)
                FROM item_revisions
                WHERE code_id = ?
                """, (code_id,))

            date_from_min = c.fetchone()[0]
            while len(todo):

                cid = todo.pop()
                done.add(cid)
                c.execute("""
                        SELECT r.date_from_days
                        FROM item_revisions AS r
                        WHERE r.code_id = ?
                          AND date_from_days >= ?
                    """, (cid, date_from_min))

                for (date_from_days,) in c.fetchall():
                    if not date_from_days in sdates:
                        sdates.add(date_from_days)

                c.execute("""
                        SELECT DISTINCT child_id
                        FROM assemblies
                        WHERE revision_id IN (
                            SELECT id
                            FROM item_revisions
                            WHERE code_id = ?
                        )
                    """, (cid,))

                l = set([x[0] for x in c.fetchall()])
                l = l.difference(done)
                todo += list(l)

            dates = list(sdates)
            dates.sort(reverse=True)
            return dates

    def copy_code(self, new_code, rid, descr, rev, copy_props=True,
                  copy_docs=True, new_date_from_days=None,
                  new_date_to_days=end_of_the_world):

        if new_date_from_days is None:
            new_date_from_days = now_to_days()

        with Transaction(self) as c:
            c.execute("""
                SELECT COUNT(*)
                FROM items
                WHERE code = ?
            """,(new_code,))
            if c.fetchone()[0] != 0:
                raise DBException("The code already exists")

            dates = self._get_children_dates_range_by_rid(c, rid)

            for (cid, cdate_from_days, cdate_to_days) in dates:
                if cdate_from_days > new_date_from_days:
                    raise DBException("Children %d is later than new code"%(cid))
                if cdate_to_days < new_date_to_days:
                    raise DBException("Children %d is earlier than new code"%(cid))

            c.execute("""
                INSERT INTO items(code) VALUES (?)
            """, (new_code, ))

            c.execute("""SELECT MAX(id) FROM items""")
            new_code_id = c.fetchone()[0]

            if new_date_from_days == prototype_date:
                new_iter = prototype_iter
            else:
                new_iter = 0

            new_rid = self._copy_revision(c, new_code_id,
                new_date_from_days, new_date_to_days,
                rev, new_iter, descr, rid, copy_docs, copy_props)

        return new_rid

    def revise_code(self, rid, descr, rev, copy_props=True, copy_docs=True,
                    new_date_from_days=None):

        if new_date_from_days is None:
            new_date_from_days = now_to_days()
        new_date_to_days = end_of_the_world

        with Transaction(self) as c:
            c.execute("""
                    SELECT id, date_from_days, iter, code_id
                    FROM item_revisions AS r
                    WHERE r.code_id = (
                            SELECT DISTINCT code_id
                            FROM item_revisions
                            WHERE id = ?
                        )
                    ORDER BY iter DESC
                """, (rid, ))

            item_revisions = c.fetchall()

            if len(item_revisions) == 0:
                raise DBException("Cannot find the old revision")

            code_id = item_revisions[0][3]

            # there are the following cases
            # 1) revise a code w/o prototype
            #       - the new iteration is the last one +1
            #       - check the date against the last one
            # 2) revise a code w/ prototype
            #       - the new iteration is the last one +1 < prototype_iter
            #       - check the date against the last one < prototype one
            # 3) revise a prototype code (w/o other revision)
            #       - the new iteration is 0
            #       - don't check the date

            if item_revisions[0][1] == prototype_date:
                if new_date_from_days == prototype_date:
                    raise DBException("Cannot create a 2nd revision")

                new_date_to_days = prototype_date -1
                if len(item_revisions) == 1:
                    # case 3
                    new_iter = 0
                    latest_rid = -1
                else:
                    # case #2
                    new_iter = item_revisions[1][2] + 1
                    latest_rid = item_revisions[1][0]
                    if new_date_from_days <= item_revisions[1][1]:
                        raise DBException("The new revision date is previous to the last revision")

            else:
                # case 1
                new_iter = item_revisions[0][2] + 1
                latest_rid = item_revisions[0][0]
                if new_date_from_days == prototype_date:
                    new_iter = prototype_iter
                else:
                    new_iter = item_revisions[0][2] + 1
                if new_date_from_days <= item_revisions[0][1]:
                    raise DBException("The new revision date is previous to the last revision")

            new_rid = self._copy_revision(c, code_id,
                new_date_from_days, new_date_to_days,
                rev, new_iter, descr, rid, copy_docs, copy_props)

            if latest_rid >= 0:
                old_date_to_days = new_date_from_days - 1
                c.execute("""
                    UPDATE item_revisions
                    SET date_to = ?, date_to_days = ?
                    WHERE id = ?
                """, (days_to_iso(old_date_to_days),
                    old_date_to_days, latest_rid))

        return new_rid

    def _copy_revision(self, c, new_code_id, new_date_from_days, new_date_to_days,
                rev, new_iter, descr, old_rid, copy_docs, copy_props):

        gval_query = ", ".join(["gval%d"%(i+1) for i in range(gvals_count)])

        c.execute("""
            INSERT INTO item_revisions(
                code_id,
                date_from, date_from_days,
                date_to, date_to_days,
                ver,
                iter,
                note,
                descr,
                default_unit,
                """ + gval_query + """
            ) SELECT
                ?,
                ?, ?,
                ?, ?,
                ?,
                ?,
                note,
                ? ,
                default_unit,
                """ + gval_query + """
            FROM item_revisions
            WHERE id = ?
        """, (new_code_id,
                days_to_iso(new_date_from_days), new_date_from_days,
                days_to_iso(new_date_to_days), new_date_to_days,
            rev, new_iter,
            descr, old_rid))

        c.execute("""SELECT MAX(id) FROM item_revisions""")
        new_rid = c.fetchone()[0]

        # ORACLE DB complains (constraint violation) if we put this in
        # a single query like:
        #     INSERT ... SELECT ... FROM .. ORDER BY
        # It doesn't like ORDER BY. So split it in two query
        gaval_query = " ".join([",gaval%d"%(i+1) for i in range(gavals_count)])
        q = """SELECT
                unit,
                child_id,
                ?,
                qty,
                each,
                ref
                %s
            FROM assemblies
            WHERE revision_id = ?
            ORDER BY id
        """%(gaval_query)
        c.execute(q, (new_rid, old_rid))
        res = c.fetchall()
        if len(res) > 0:
            q = """
                INSERT INTO assemblies (
                    unit,
                    child_id,
                    revision_id,
                    qty,
                    each,
                    ref
                    %s
                ) VALUES (?, ?, ?, ?, ?, ? %s)
            """%(gaval_query, ",? " * gavals_count)
            c.executemany(q, res)

        if copy_docs:
            c.execute("""
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
            c.execute("""
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

        return new_rid

    def get_children_by_rid(self, rid):
        with ROCursor(self) as c:
            r = self._get_children_by_rid(c, rid)
        return r

    def _get_children_by_rid(self, c, rid):
        gval_query = "".join([",a.gaval%d"%(i+1) for i in range(gavals_count)])
        c.execute("""
            SELECT a.child_id, i.code, r2.descr, a.qty, a.each, a.unit,
                   a.ref %s
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
        """%(gval_query), (rid,))

        return c.fetchall()

    def update_by_rid2(self, rid, descr, ver, default_unit,
            gvals, drawings=[], children=[], prev_values = None):

        with Transaction(self) as c:
            if prev_values:
                data_, children_, drawings_ = prev_values
                if data_ != self._get_code_by_rid(c, rid):
                    return "DATACHANGED"
                if children_ != self._get_children_by_rid(c, rid):
                    return "DATACHANGED"
                if drawings_ != self._get_drawings_by_rid(c, rid):
                    return "DATACHANGED"

            gval_query = ", ".join(["gval%d = ?"%(i+1) for i in range(gvals_count)])
            c.execute("""
                UPDATE item_revisions SET
                    descr=?, ver=?, default_unit=?,
                    """ + gval_query + """
                WHERE id=?
                """,(descr, ver, default_unit,
                     *gvals, rid))

            c.execute("""
                DELETE FROM drawings
                WHERE revision_id = ?
            """, (rid, ))

            if len(drawings) > 0:

                c.executemany("""
                        INSERT INTO drawings(revision_id, filename, fullpath)
                        VALUES (?, ?, ?)
                    """, [(rid, name, path) for (name, path) in drawings])

            c.execute("""
                DELETE FROM assemblies
                WHERE revision_id = ?
            """, (rid, ))

            if len(children) > 0:
                q = """
                        INSERT INTO assemblies(
                            revision_id, child_id, qty, each, ref, unit %s)
                        VALUES (?, ?, ?, ?, ?, ? %s)
                """%( "".join([",gaval%d "%(x+1) for x in range(gavals_count)]),
                    "".join([",? " for x in range(gavals_count)]),
                )
                args = [(rid, code_id, qty, each, ref, unit, *gvs)
                        for (code_id, qty, each, unit, ref, *gvs) in children]
                c.executemany(q, args)

        return "OK"

    def update_dates(self, dates):
        # dates[] = [
        #     (rid, date_from, date_from_days, date_to, date_to_days),
        #     [...]
        # ]
        # check that the date_from are in order
        l = [x[2] for x in dates]
        l1 = l[:]
        l1.sort(reverse=True)
        if l != l1:
            raise DBException("DATEERROR: date_from are not sorted")

        will_be_proto = max(l1) == prototype_date
        if max(l1) > prototype_date:
            raise DBException("DATEERROR: date_from > prototype date")
        l = [x[4] for x in dates]
        if max(l) > end_of_the_world:
            raise DBException("DATEERROR: date_to > end_of_the_world date")

        # check that the date_to are in order
        l = [x[4] for x in dates]
        l1 = l[:]
        l1.sort(reverse=True)
        if l != l1:
            raise DBException("DATEERROR: date_to are not sorted")

        # check that date_from(n) > date_to(n+1)
        for i in range(len(dates)-1):
            if dates[i][2] != dates[i+1][4] + 1:
                raise DBException("DATEERROR: date_from[n] != date_to[n+1]+1")

        # check that date_from <= date_to
        for row in dates:
            if row[2] > row[4]:
                raise DBException("DATEERROR: date_from > date_to")

        with Transaction(self) as c:

            c.execute("""
                SELECT code_id
                FROM item_revisions
                WHERE id = ?
            """,(dates[0][0],))
            code_id = c.fetchone()[0]

            c.execute("""
                SELECT id, iter
                FROM item_revisions
                WHERE code_id = ?
                ORDER BY date_from DESC
            """,(code_id,))
            res = c.fetchall()[:]
            l = [x[1] for x in res]
            l1 = l[:]
            l1.sort(reverse=True)
            if l1 != l:
                raise DBException("DATEERROR: iter in db are not sorted")

            was_proto = max(l) == prototype_iter

            l = [x[0] for x in res]
            l1 = [x[0] for x in dates]
            assert(l1 == l)

            min_date_from_days = None
            max_date_to_days = None
            for (rid, _1, date_from_days, _2, date_to_days) in dates:

                if min_date_from_days is None or min_date_from_days > date_from_days:
                    min_date_from_days = date_from_days
                if max_date_to_days is None or max_date_to_days < date_to_days:
                     max_date_to_days = date_to_days

                for (cid, cdate_from_days, cdate_to_days) in self._get_children_dates_range_by_rid(c, rid):
                    if cdate_from_days > date_from_days:
                        raise DBException("DATEERROR: children date_from > parent date_from")
                    assert(cdate_from_days <= date_from_days)
                    if cdate_to_days < date_to_days:
                        raise DBException("DATEERROR: children date_to < parent date_to")
                    assert(cdate_to_days >= date_to_days)

            # check that the date range has a wider life than
            # any parents
            for (pid, pdate_from_days, pdate_to_days) in self._get_parent_dates_range_by_code_id(c, code_id):
                if pdate_from_days < min_date_from_days:
                    raise DBException("DATEERROR: parent date_from < min children date_from")
                assert(pdate_from_days >= min_date_from_days)
                if pdate_to_days > max_date_to_days:
                    raise DBException("DATEERROR: parent date_from < min children date_from")
                assert(pdate_to_days <= max_date_to_days)

            # ok insert the data
            for (rid, date_from, date_from_days, date_to, date_to_days) in dates:
                c.execute("""
                    UPDATE item_revisions SET
                        date_from=?, date_from_days=?,
                        date_to=?, date_to_days=?
                    WHERE id = ?
                """, (date_from,
                    date_from_days,
                    date_to,
                    date_to_days, rid))

            #  reset the iter
            if was_proto:
                c.execute("""
                    SELECT MAX(iter)
                    FROM item_revisions
                    WHERE code_id = ?
                      AND iter < ?
                """, (code_id, prototype_iter))

                ret = c.fetchone()
                if ret is None or ret[0] is None:
                    new_iter = 0
                else:
                    new_iter = ret[0] + 1

                c.execute("""
                    UPDATE item_revisions
                    SET iter = ?
                    WHERE iter = ?
                      AND code_id = ?
                """, (new_iter, prototype_iter, code_id))

            # update the iter if there is a prototype
            if will_be_proto:
                c.execute("""
                    UPDATE item_revisions
                    SET iter = ?
                    WHERE date_from_days = ?
                      AND code_id = ?
                """, (prototype_iter, prototype_date, code_id))

    def delete_code(self, code_id):
        with Transaction(self) as c:
            c.execute("""
                SELECT COUNT(*)
                FROM assemblies
                WHERE child_id = ?
            """, (code_id,))
            cnt = c.fetchone()[0]

            if cnt > 0:
                c.rollback()
                return "HASPARENTS"

            c.execute("""
                DELETE FROM drawings
                WHERE revision_id IN
                (SELECT id
                 FROM item_revisions
                 WHERE code_id = ?
                )
                """, (code_id,))

            c.execute("""
                DELETE FROM assemblies
                WHERE revision_id IN
                (SELECT id
                 FROM item_revisions
                 WHERE code_id = ?
                )
                """, (code_id,))

            c.execute("""
                DELETE FROM item_properties
                WHERE revision_id IN
                (SELECT id
                 FROM item_revisions
                 WHERE code_id = ?
                )
                """, (code_id,))

            c.execute("""
                DELETE FROM item_revisions
                WHERE code_id = ?
                """, (code_id,))

            c.execute("""
                DELETE FROM items
                WHERE id = ?
                """, (code_id,))

        return ""

    def delete_code_revision(self, rid):
        with Transaction(self) as c:
            c.execute("""
                SELECT COUNT(*)
                FROM item_revisions
                WHERE code_id = (
                    SELECT code_id
                    FROM item_revisions
                    WHERE id = ?
                )
            """, (rid,))
            cnt = c.fetchone()[0]

            if cnt < 2:
                c.rollback()
                return "ISALONE"

            c.execute("""
                SELECT code_id, iter
                FROM item_revisions
                WHERE id = ?
            """, (rid,))
            code_id, iter_ = c.fetchone()

            c.execute("""
                SELECT COUNT(*)
                FROM item_revisions
                WHERE code_id = ?
                  AND iter < ?
            """, (code_id, iter_))

            cnt = c.fetchone()[0]

            # adjust the date of the adiajenct item_revision
            if cnt > 0:
                c.execute("""
                    SELECT MAX(iter)
                    FROM item_revisions
                    WHERE code_id = ?
                      AND iter < ?
                """, (code_id, iter_))
                prev_iter = c.fetchone()[0]

                c.execute("""
                    SELECT date_to, date_to_days
                    FROM item_revisions
                    WHERE id = ?
                """, (rid,))
                date_to, date_to_days = c.fetchone()

                c.execute("""
                    UPDATE item_revisions
                    SET date_to = ?, date_to_days = ?
                    WHERE code_id = ?
                      AND iter = ?
                """, (date_to, date_to_days, code_id, prev_iter))
            else:
                c.execute("""
                    SELECT MIN(iter)
                    FROM item_revisions
                    WHERE code_id = ?
                      AND iter > ?
                """, (code_id, iter_))
                next_iter = c.fetchone()[0]

                if next_iter == prototype_iter:
                    c.rollback()
                    return "ONLYPROTOTYPE"

                c.execute("""
                    SELECT date_from, date_from_days
                    FROM item_revisions
                    WHERE id = ?
                """, (rid,))
                date_from, date_from_days = c.fetchone()

                c.execute("""
                    UPDATE item_revisions
                    SET date_from = ?, date_from_days = ?
                    WHERE code_id = ?
                      AND iter = ?
                """, (date_from, date_from_days, code_id, next_iter))

            # drop all the children

            c.execute("""
                DELETE FROM drawings
                WHERE revision_id = ?
                """, (rid,))

            c.execute("""
                DELETE FROM assemblies
                WHERE revision_id = ?
                """, (rid,))

            c.execute("""
                DELETE FROM item_properties
                WHERE revision_id = ?
                """, (rid,))

            c.execute("""
                DELETE FROM item_revisions
                WHERE id = ?
                """, (rid,))

        return ""

    # case sensitive search
    def search_revisions(self, case_sensitive=True, **kwargs):
        gval_query = ", ".join(["r.gval%d"%(i+1) for i in range(gvals_count)])

        query = """
            SELECT DISTINCT i.id, r.id, i.code, r.descr, r.ver, r.iter,
                r.date_from_days, r.date_to_days, d.fullpath,
                """ + gval_query + """
            FROM item_revisions AS r
            LEFT JOIN items AS i
              ON r.code_id = i.id
            LEFT JOIN drawings AS d
              ON d.revision_id = r.id
        """

        where = []

        args = []
        arg_names = ["id", "rid", "code", "rev", "iter_", "descr",
                     "date_from_days", "date_to_days", "doc"]
        arg_names += ["gval%d"%(i+1) for i in range(gvals_count)]

        # check that nobody is passing not supported argument
        if len(set(kwargs.keys()).difference(set(arg_names))) != 0:
            raise DBException("ARGUMENTERROR: unknow arguments: %r"%(kwargs.keys()))
        assert(len(set(kwargs.keys()).difference(set(arg_names))) == 0)

        for k in kwargs:
            assert(k in arg_names)
            arg = str(kwargs[k]).strip()
            assert(len(arg) > 0)

            table = "r"
            if k in ["code", "id"]:
                table = "i"
            elif k == 'doc':
                table = "d"
                k = "fullpath"
            elif k == "rid":
                k = "id"
            elif k == "rev":
                k = "ver"
            elif k == "iter_":
                k = "iter"

            if k in ["id", "iter", "date_from_days", "date_to_days"]:
                where.append(("%s.%s"%(table, k), arg, int))
            else:
                where.append(("%s.%s"%(table, k), arg, None))

        if len(where):
            query += "            WHERE\n"
            q, args = self._expand_search_str_clauses(where, case_sensitive)
            query += "                " + q

        query += """
                ORDER BY i.code ASC, r.iter ASC
        """

        #print("query=", query)
        #print("args=", args)
        with ROCursor(self) as c:
            c.execute(query, args)

            return c.fetchall()

    def create_first_code(self):
        date_from = days_to_iso(0)
        date_to = days_to_iso(end_of_the_world)
        with Transaction(self) as c:
            c.execute("INSERT INTO items(code) VALUES (?)", (
                '000000000000', )
            )
            c.execute("SELECT MAX(id) FROM items")
            mid = c.fetchone()[0]

            c.execute("""INSERT INTO item_revisions(
                descr, code_id, ver,
                iter, default_unit,
                date_from, date_from_days,
                date_to, date_to_days) VALUES (
                ?, ?, ?,
                ?, ?,
                ?, ?,
                ?, ?)""",
                ('FIRST CODE', mid, '0', 0, 'NR',
                 date_from, iso_to_days(date_from),
                 date_to, iso_to_days(date_to))
            )


class DBSQLServer(_BaseServer):
    def __init__(self, path=None):
        _BaseServer.__init__(self, path)

    def _insert_table(self, tname, columns, data):
        cs = columns[:]
        while "key" in cs:
            i = cs.index("key")
            cs[i] = "[key]"

        with Transaction(self) as c:
            c.execute("SET IDENTITY_INSERT " + tname +" ON" )
            self._insert_table_(c, tname, cs, data)
            c.execute("SET IDENTITY_INSERT " + tname +" OFF" )

    # SQLServer doesn't like BEGIN; it is 'autobegin'
    def _begin(self, c):
        pass

    def _exception_handler(self, exc_value):
        msg = str(exc_value)
        if ("Attempt to use a closed connection" in msg or
            "08S01" in msg):
                try:
                    self._conn.close()
                except:
                    pass
                finally:
                    self._conn = None

    def _sql_translate(self, s):
        def process(l):
            #if " RENAME TO " in l:
            #    l = l.replace("ALTER TABLE ", "EXEC sp_rename '")
            #    l = l.replace(" RENAME TO ", "', '")
            #    l = l.replace(";", "';")
            if " VARCHAR" in l:
                l = l.replace(" VARCHAR", " NVARCHAR")
            return l
        s = '\n'.join([process(line) for line in s.split("\n")])
        return s

    def _open(self, connection_string):
        import pyodbc
        self._mod = pyodbc
        self._conn = pyodbc.connect(connection_string)

    def _get_tables_list(self, c):
        return [row.table_name for row in self._get_cursor().tables()]


class DBOracleServer(_BaseServer):
    def __init__(self, path=None):
        _BaseServer.__init__(self, path)

    # oracle doesn't like 'BEGIN'
    def _begin(self, c):
        pass

    def _exception_handler(self, exc_value):
        msg = str(exc_value)
        if ("DPI-1080:" in msg or
            "DPI-1010:" in msg):
                try:
                    self._conn.close()
                except:
                    pass
                finally:
                    self._conn = None

    def _sql_translate(self, s):
        def process(l):
            if "DROP INDEX IF EXISTS " in l:
                i = l.find("DROP INDEX IF EXISTS ")
                i += 21
                iname = l[i:]
                l = """
                    DECLARE
                       index_not_exists EXCEPTION;
                       PRAGMA EXCEPTION_INIT (index_not_exists, -1418);
                    BEGIN
                       EXECUTE IMMEDIATE 'DROP INDEX %s';
                    EXCEPTION
                       WHEN index_not_exists THEN NULL;
                    END;
                """%(iname)
            if "DROP TABLE IF EXISTS " in l:
                i = l.find("DROP TABLE IF EXISTS ")
                i += 21
                iname = l[i:]
                l = """
                    DECLARE
                       table_does_not_exist EXCEPTION;
                       PRAGMA EXCEPTION_INIT (table_does_not_exist, -942);
                    BEGIN
                       EXECUTE IMMEDIATE 'DROP TABLE %s';
                    EXCEPTION
                       WHEN table_does_not_exist THEN NULL;
                    END;
                """%(iname)

            if " VARCHAR" in l:
                l = l.replace(" VARCHAR", " NVARCHAR2")
            if " NOT NULL IDENTITY " in l:
                l = l.replace(" NOT NULL IDENTITY ",
                    " GENERATED BY DEFAULT AS IDENTITY NOT NULL ")
            return l

        s = ';'.join([process(line) for line in s.split(";")])
        cnt = 1
        while "?" in s:
            i = s.find("?")
            s = s[:i] + ":%d"%(cnt) + s[i+1:]
            cnt += 1

        i = 0
        while True:
            i = s.find(" AS ", i)
            if i < 0:
                break
            if not s[i:].startswith(" AS IDENTITY "):
               s = s[:i+1] + s[i+4:]
            else:
                i += 5

        return s

    def create_db(self):

        stms = self._get_db_v0_4()

        # due to the expansion of DROP TABLE IF EXISTS,
        # we need to do the _sql_translate at this level
        stms = self._sql_translate(stms)

        with Transaction(self) as c:

            while len(stms):
                stms = stms.strip()
                if stms.upper().startswith("DECLARE"):
                    i = stms.upper().find("END")
                    s = stms[:i+3] + ";"
                    stms = stms[i+3:]
                    c.execute(s)
                elif stms.upper().startswith(";"):
                    stms = stms[1:]
                    continue
                else:
                    i = stms.find(";")
                    if i >= 0:
                        s = stms[:i]
                        stms = stms[i+1:]
                    else:
                        s = stms
                        stms = ""
                    c.execute(s)

    def _open(self, connection_string):
        import cx_Oracle
        self._mod = cx_Oracle
        user = None
        pwd = None
        host = None

        for c in connection_string.split(";"):
            k, v = map(lambda x: x.strip(), c.split("="))
            if k == "user":
                user = v
            elif k == "pw":
                pwd = v
            elif k == "host":
                host = v
            else:
                raise DBException("Oracle: incorrect connection string (%s)"%(
                    connection_string))

        self._conn = cx_Oracle.connect(user, pwd, host)

    def _get_tables_list(self, c):
        c.execute("""
                SELECT table_name
                FROM user_tables
            """)

        return [x[0].lower() for x in c.fetchall()]

    def _translate_fetchone_(self, c, row):
        # if the query refers to a non existent column,
        # the query return None
        if row is None:
            return None
        return self._translate_fetchall_(c, [row])[0]

    def _translate_fetchall_(self, c, rows):
        tr = [("VARCHAR" in str(x[1])) for x in c.description]

        def f(y, i):
            if tr[i] and y is None:
                return ''
            return y

        return [list([f(x, i) for (i, x) in enumerate(row)]) for row in rows]


class DBSQLite(_BaseServer):
    def __init__(self, path=None, ignore_case_during_search=True):
        if path == "" or path is None:
            path = _db_path
        self._ignore_case_during_search = ignore_case_during_search
        _BaseServer.__init__(self, path)

    def _open(self, path):
        import sqlite3
        self._conn = sqlite3.connect(path)
        self._conn.execute("PRAGMA foreign_keys = ON")
        if not self._ignore_case_during_search:
            self._conn.execute("PRAGMA case_sensitive_like = 1")
        self._mod = sqlite3

    def _sql_translate(self, stms):
        stms = stms.replace(" IDENTITY", "")
        #stms = stms.replace(" ON items;", ";")
        #stms = stms.replace(" ON drawings;", ";")
        #stms = stms.replace(" ON assemblies;", ";")

        return stms

    def _get_tables_list(self, c):
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [x[0] for x in c.fetchall()]


class DBPG(_BaseServer):
    def __init__(self, path=None):
        import psycopg2
        _BaseServer.__init__(self, path)

    def _insert_table(self, tname, columns, data):
        with Transaction(self) as c:
            self._insert_table_(c, tname, columns, data)

            c.execute("SELECT COUNT(*) FROM " + tname)
            n = c.fetchone()[0]
            if n > 0:
                c.execute("SELECT MAX(id) FROM " + tname)
                n = c.fetchone()[0] + 10
            else:
                n = 100
            c.execute("ALTER SEQUENCE " + tname + "_id_seq RESTART WITH %d"%(n) )

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
        import psycopg2
        self._mod = psycopg2
        self._conn = psycopg2.connect(path)
        self._conn.set_client_encoding("UNICODE")

    def _get_tables_list(self, c):
        c.execute("""
        SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname != 'pg_catalog' AND
                schemaname != 'information_schema';
        """)

        return [x[0] for x in c.fetchall()]

    def get_bom_dates_by_code_id(self, code_id):
        sdates = set()
        done = set()
        todo = [code_id]

        with ROCursor(self) as c:

            c.execute("""
                SELECT MIN(date_from_days)
                FROM item_revisions
                WHERE code_id = ?
                """, (code_id,))

            date_from_min = c.fetchone()[0]

            c.execute("""

                SELECT DISTINCT r.date_from_days
                FROM item_revisions AS r
                WHERE r.code_id IN (

                    WITH RECURSIVE child_of(child_id) AS (
                        SELECT  ?
                        UNION
                        SELECT a.child_id
                        FROM child_of AS co
                        LEFT JOIN item_revisions AS r
                           ON r.code_id = co.child_id
                        LEFT JOIN assemblies AS a
                           ON a.revision_id = r.id
                    )
                    SELECT  child_id
                    FROM child_of
                )  AND date_from_days >= ?

            """,(code_id, date_from_min))

            dates = [x[0] for x in c.fetchall()]

            return dates


class DBMySQL(_BaseServer):
    def __init__(self, path=None):
        _BaseServer.__init__(self, path)

    def _insert_table(self, tname, columns, data):
        with Transaction(self) as c:
            self._insert_table_(c, tname, columns, data)

    def _sql_translate(self, s):
        def process(l):
            if "DROP INDEX IF EXISTS" in l:
                i = l.find(".")
                j = l.rfind(" ", 0, i)
                k = l.find(";")
                if k < 0:
                    k = len(l)+ 10
                tbname = l[j+1:i]
                l = l[:j] + " " + l[i+1:k] + " ON " + tbname + l[k:]
            if " IDENTITY " in l:
                i = l.find(" IDENTITY ")
                l = l[:i] + " AUTO_INCREMENT " + l[i+10:]
            if "each" in l:
                l = l.replace("each", "`each`")
            if "?" in l:
                l = l.replace("?", "%s")
            #print(l)
            return l
        s = '\n'.join([process(line) for line in s.split("\n")])
        return s

    def _translate_fetchall_(self, c, rows):
        # MySQL return tuple, sometime we need list
        return list(_BaseServer._translate_fetchall_(self, c, rows))

    def _open(self, path):
        import MySQLdb
        self._mod = MySQLdb
        self._conn = MySQLdb.connect(*path.split(";"))
        #self._conn.set_client_encoding("UNICODE")

    def _get_tables_list(self, c):
        c.execute("""SHOW TABLES""")
        return [x[0] for x in c.fetchall()]

    def get_bom_dates_by_code_id(self, code_id):
        sdates = set()
        done = set()
        todo = [code_id]

        with ROCursor(self) as c:

            c.execute("""
                SELECT MIN(date_from_days)
                FROM item_revisions
                WHERE code_id = ?
                """, (code_id,))

            date_from_min = c.fetchone()[0]

            c.execute("""

                SELECT DISTINCT r.date_from_days
                FROM item_revisions AS r
                WHERE r.code_id IN (

                    WITH RECURSIVE child_of(child_id) AS (
                        SELECT  ?
                        UNION
                        SELECT a.child_id
                        FROM child_of AS co
                        LEFT JOIN item_revisions AS r
                           ON r.code_id = co.child_id
                        LEFT JOIN assemblies AS a
                           ON a.revision_id = r.id
                    )
                    SELECT  child_id
                    FROM child_of
                )  AND date_from_days >= ?

            """,(code_id, date_from_min))

            dates = [x[0] for x in c.fetchall()]

            return dates


def get_db_instance():

    global _globaDBInstance

    assert(_globaDBInstance)
    return _globaDBInstance

def init(dbtype, cfg):
    global _globaDBInstance
    global connection

    connection, _globaDBInstance = _create_db(dbtype, cfg)
    return _globaDBInstance

def _create_db(dbtype, cfg):

    if dbtype == "sqlite":
        path = cfg["path"]
        ignore_case_during_search = cfg["ignore_case_during_search"] != "0"
        instance = DBSQLite(path, ignore_case_during_search)
        connection="Server: SQLITE/"+path[-30:]

    elif dbtype == "oracle":
        connection_string = cfg["conn"]
        instance = DBOracleServer(connection_string)
        connection = "Server: ORACLE/" + connection_string

    elif dbtype == "sqlserver":
        connection_string = cfg["conn"]
        instance = DBSQLServer(connection_string)
        connection="Server: SQLSERVER/"+connection_string

    elif dbtype == "postgresql":
        import customize
        cfg["password"] = customize.database_password(cfg["password"])
        connection_string = "host={server} dbname={database} user={username} password={password}".format(**cfg)
        connection="Server: PostgreSQL/" + connection_string
        instance = DBPG(connection_string)

    elif dbtype == "mysql":
        import customize
        cfg["password"] = customize.database_password(cfg["password"])
        connection_string = ";".join([cfg["server"], cfg["username"],
            cfg["password"], cfg["database"]])
        connection="Server: MySQL/" + connection_string
        instance = DBMySQL(connection_string)

    elif dbtype == "bbserver":
        import customize

        host = cfg["host"]
        port = int(cfg["port"])
        username = cfg["username"]
        password = cfg["password"]
        password = customize.database_password(password)

        import bbserver
        instance = bbserver.RemoteSQLClient(host, port)
        connection="Server: RemoteBBServer:%s@%d"%(host, port)
        instance.remote_server_do_auth(username, password)

    return connection,instance

def restore_tables(nf, d, quiet=False):
    import zipfile
    with zipfile.ZipFile(nf) as z:
        fntables = [i[:-4] for i in z.namelist() if i.endswith(".csv")]
        fntables.sort()
        l = d.list_main_tables()
        l.sort()
        assert(l==fntables)

        gval = 0
        gaval = 0

        with z.open("item_revisions.csv") as f:
            line = f.readline().decode('utf-8').rstrip("\n\r")
            for i in line.split("\t"):
                if i.lower().startswith("gval"):
                    gval = int(i[4:])

        with z.open("assemblies.csv") as f:
            line = f.readline().decode('utf-8').rstrip("\n\r")
            for i in line.split("\t"):
                if i.lower().startswith("gaval"):
                    gaval = int(i[5:])

        global gvals_count, gavals_count

        print

        if gaval > gavals_count:
            gavals_count = gaval
        if gval > gvals_count:
            gvals_count = gval

        d.create_db()

        if not quiet:
            print()
        for table in d.list_main_tables():
            tablefn = table+".csv"
            with z.open(tablefn) as f:
                columns = f.readline().decode("utf-8").rstrip("\n\r").split("\t")
                d._insert_table(table, columns,
                    [list(map(xunescape,
                              x[:-1].decode("utf-8").rstrip("\n\r").split("\t")))
                     for x in f.readlines()]
                )
                if not quiet:
                     print("\r%s                                 "%(table), end="")
        if not quiet:
            print("\rDone                          ")

def dump_tables(nf, d, quiet=False):
        import zipfile
        import tempfile
        import os

        z=zipfile.ZipFile(nf, "w", compression=zipfile.ZIP_DEFLATED)
        tmpfilename = tempfile.NamedTemporaryFile(delete=False).name
        try:
            for (tname, columns, data) in d.dump_tables():

                with open(tmpfilename, "w", encoding='utf-8') as f:
                    f.write("\t".join(columns)+"\n")
                    cnt = 0
                    for row in data:
                        f.write("\t".join(map(xescape, row))+"\n")
                        if not quiet:
                            print("%s: %d                                 \r"%(tname, cnt), end="")
                        cnt += 1

                z.write(tmpfilename, arcname="%s.csv"%(tname))
        finally:
            if os.path.exists(tmpfilename):
                os.unlink(tmpfilename)

def new_db(d):
    d.create_db()
    d.create_first_code()

def main(prgname, args):
    import cfg

    cfg.init()
    dbtype = cfg.config()["BOMBROWSER"]["db"]
    conf = cfg.config()[dbtype.upper()]

    if len(args) == 2 and args[0] == "--dump-tables":
        init(dbtype, dict(conf))
        d = get_db_instance()
        dump_tables(args[1], d)
        print("DB dumped")

    elif len(args) >= 1 and args[0] == "--new-db":
        if len(args) == 2:
            if args[1] == "--yes-really-i-know-what-i-want":
                pass
            else:
                print("ERROR: exit")
                return
        else:
            print("Enter 'yes-really-i-know-what-i-want' > ", end='')
            s = input()
            if s != 'yes-really-i-know-what-i-want':
                print("ERROR: exit")
                return

        init(dbtype, dict(conf))
        d = get_db_instance()
        new_db(d)
        print("DB created")

    elif len(args) >= 2 and args[0] == "--restore-tables":
        if len(args) == 3:
            if args[1] == "--yes-really-i-know-what-i-want":
                args=[args[0], args[2]]
            else:
                print("ERROR: exit")
                return
        else:
            print("Enter 'yes-really-i-know-what-i-want' > ", end='')
            s = input()
            if s != 'yes-really-i-know-what-i-want':
                print("ERROR: exit")
                return

        init(dbtype, dict(conf))
        d = get_db_instance()
        restore_tables(args[1], d)
        print("DB restored")

    else:
        print("usage: %s --dump-tables <file.zip>"%(prgname))
        print("usage: %s --new-db"%(prgname))
        print("usage: %s --restore-tables <file.zip>"%(prgname))
        sys.exit(0)

