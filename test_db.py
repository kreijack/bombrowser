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

import db
import sys
import datetime
import pprint

def _test_insert_items(c):
    codes = [('code123', "descr456", 0), ('code124', "descr457", 0),
            ('code135', "descr468", 0), ('code136', "descr469", 0),
            ('code123', "descr456", 1)]
    map_code_id = {}
    for (code, descr, ver) in codes:


        if code in map_code_id:
            code_id = map_code_id[code]
        else:
            c.execute("""INSERT INTO items(code) VALUES (?)""",( code,))
            c.execute("""SELECT MAX (id) FROM items""")
            code_id = c.fetchone()[0]
            map_code_id[code] = code_id

        c.execute("""INSERT INTO item_revisions(
            descr, code_id, ver,
            iter, default_unit,
            gval1, gval2) VALUES (
            ?, ?, ?,
            ?, ?,
            ?, ?)""", (
                descr, code_id, "%d"%(ver),
                ver, "NR",
                "FOR1COD", "FOR1NAME"
            ))

_use_memory_sqlite=True

def _create_db():
    if _use_memory_sqlite:
        d = db.DBSQLite(":memory:")
        db._globaDBInstance = d
    else:
        d = db.DB() #_connection_string)
    d.create_db()
    cursor = d._conn.cursor()

    class MyCursor:
        def __init__(self, c, d):
            self._cursor = c
            self._db = d
        def execute(self, query, *args):
            q2=self._db._sql_translate(query)
            return self._cursor.execute(q2, *args)
        def fetchone(self):
            return self._cursor.fetchone()
        def fetchall(self):
            return self._cursor.fetchall()

    mc = MyCursor(cursor, d)
    return (d, mc)

def test_double_recreate_db():
    d, c = _create_db()
    assert("database_props" in d._get_tables_list())
    d, c = _create_db()

def test_get_code():
    d, c = _create_db()

    _test_insert_items(c)

    data = d.get_code(1, 0)
    assert(data["code"] == "code123")
    assert(data["descr"] == "descr456")

    data = d.get_codes_by_code("code124")
    assert(len(data) == 1)
    assert(data[0][1] == "code124")
    assert(data[0][2] == "descr457")


    data = d.get_codes_by_like_code("code12%")
    assert(len(data) == 2)
    data.sort(key = lambda x: x[1])
    assert(data[0][1] == "code123")
    assert(data[0][2] == "descr456")

    assert(data[1][1] == "code124")
    assert(data[1][2] == "descr457")

    data = d.get_codes_by_like_code_and_descr("code12%", "%7")
    assert(len(data) == 1)
    data.sort(key = lambda x: x[1])
    assert(data[0][1] == "code124")
    assert(data[0][2] == "descr457")


def test_get_code_by_rid():
    d, c = _create_db()

    _test_insert_items(c)

    data = d.get_code_from_rid(1)
    assert(data["code"] == "code123")
    assert(data["descr"] == "descr456")


def test_get_code_by_descr():
    d, c = _create_db()

    _test_insert_items(c)

    data = d.get_codes_by_like_descr("descr46%")
    assert(len(data) == 2)
    data.sort(key = lambda x: x[1])
    assert(data[0][1] == "code135")
    assert(data[0][2] == "descr468")

    assert(data[1][1] == "code136")
    assert(data[1][2] == "descr469")

def test_get_code_by_code_and_descr():
    d, c = _create_db()

    _test_insert_items(c)

    data = d.get_codes_by_like_code_and_descr("code13%", "descr%9")
    assert(len(data) == 1)
    data.sort(key = lambda x: x[0])

    assert(data[0][1] == "code136")
    assert(data[0][2] == "descr469")


def _test_insert_assembly(c):
    """
          10/01        15/01        20/01         25/01

            O            O            O            O
            |            |            |            |
            A            A            A            A
           / \          / \          / \          / \
          B   C        B   C        B   C        B   M
         / \ / \      / \ / \      / \ / \      / \ / \
        D  E F  G    H  E I  G    D  E I  L    D  E I  L

    """
    ass = {
        "O": ( ("2020-01-10", "",           ("A",)), ),

        "A": ( ("2020-01-10", "2020-01-24", ("B", "C")),
               ("2020-01-25", "",           ("B", "M")), ),

        "B": ( ("2020-01-10", "2020-01-14", ("D", "E")),
               ("2020-01-15", "2020-01-19", ("H", "E")),
               ("2020-01-20", "",           ("D", "C")), ),

        "C": ( ("2020-01-10", "2020-01-14", ("F", "G")),
               ("2020-01-15", "2020-01-19", ("I", "G")),
               ("2020-01-20", "",           ("I", "L")), ),

        "D": ( ("2020-01-10", "",           ()), ),

        "E": ( ("2020-01-10", "",           ()), ),

        "F": ( ("2020-01-10", "",           ()), ),

        "G": ( ("2020-01-10", "",           ()), ),

        "H": ( ("2020-01-15", "",           ()), ),

        "I": ( ("2020-01-15", "",           ()), ),

        "L": ( ("2020-01-20", "",           ()), ),

        "M": ( ("2020-01-25", "",           ("I", "L")), ),
    }


    map_code_id = {}
    iter_ = dict()
    for code in ass:

        c.execute("""INSERT INTO items(code) VALUES (?)""", (code,))
        c.execute("""SELECT MAX (id) FROM items""")
        code_id = c.fetchone()[0]

        map_code_id[code] = code_id
        iter_[code] = 0

     # insert the assy by date order

    for code in ass:
        code_id = map_code_id[code]


        for (date_from, date_to, children) in ass[code]:

            if date_to == "":
                dts = db.end_of_the_world
            else:
                dts = db.iso_to_days(date_to)

            c.execute("""INSERT INTO item_revisions(
                descr, code_id, ver,
                iter, default_unit,
                date_from_days, date_from,
                date_to_days, date_to,
                gval1, gval2) VALUES (
                ?, ?, ?,
                ?, ?,

                ?, ?,
                ?, ?,

                ?, ?)""", (
                    "Items '%s'"%(i), code_id, "1",
                    iter_[code], "NR",

                    db.iso_to_days(date_from), date_from,
                    dts, date_to,

                    "FOR1COD", "FOR1NAME"
            ))
            iter_[code] += 1

            for child in children:
                c.execute("""SELECT MAX (id) FROM item_revisions""")
                rid = c.fetchone()[0]
                c.execute("""INSERT INTO assemblies (
                        unit,
                        child_id, revision_id,
                        qty,
                        each,
                        ref
                    ) VALUES (
                        ?,
                        ?, ?,
                        ?,
                        ?,
                        ?
                    )""", (
                            "NR",
                            map_code_id[child], rid,
                            1,
                            1,
                            '//')
                    )

def test_get_parent_dates_range_by_code_id():
    d, c = _create_db()

    _test_insert_assembly(c)

    c.execute("SELECT id FROM items WHERE code=?", ("I",))
    i_id = c.fetchone()[0]

    data = d.get_parent_dates_range_by_code_id(i_id)

    c.execute("SELECT id FROM items WHERE code=?", ("M",))
    m_id = c.fetchone()[0]
    c.execute("SELECT id FROM items WHERE code=?", ("C",))
    c_id = c.fetchone()[0]

    for row in data:
        if row[0] == m_id:
            break

    assert(row[0] == m_id)
    assert(row[1] == db.iso_to_days("2020-01-25"))
    assert(row[2] == db.end_of_the_world)

    for row in data:
        if row[0] == c_id:
            break

    assert(row[0] == c_id)
    assert(row[1] == db.iso_to_days("2020-01-15"))
    assert(row[2] == db.end_of_the_world)

def test_get_children_dates_range_by_rid():
    d, c = _create_db()

    _test_insert_assembly(c)

    c.execute("""
        SELECT MAX(r.id)
        FROM item_revisions AS r
        LEFT JOIN items AS i
          ON r.code_id = i.id
        WHERE i.code=?""", ("A",))
    a_rid = c.fetchone()[0]

    data = d.get_children_dates_range_by_rid(a_rid)

    assert(len(data) == 2)

    c.execute("SELECT id FROM items WHERE code=?", ("B",))
    b_id = c.fetchone()[0]
    c.execute("SELECT id FROM items WHERE code=?", ("M",))
    m_id = c.fetchone()[0]

    for row in data:
        if row[0] == b_id:
            break

    assert(row[0] == b_id)
    assert(row[1] == db.iso_to_days("2020-01-10"))
    assert(row[2] == db.end_of_the_world)

    for row in data:
        if row[0] == m_id:
            break

    assert(row[0] == m_id)
    assert(row[1] == db.iso_to_days("2020-01-25"))
    assert(row[2] == db.end_of_the_world)

def test_is_assembly():
    d, c = _create_db()

    _test_insert_assembly(c)

    assert(d.is_assembly(d.get_codes_by_code("A")[0][0]))
    assert(not d.is_assembly(d.get_codes_by_code("L")[0][0]))

def test_get_dates():
    d, c = _create_db()

    _test_insert_assembly(c)

    id_ = d.get_codes_by_code("A")[0][0]

    dates = [ db.days_to_iso(x[2]) for x in d.get_dates_by_code_id3(id_)]
    assert(len(dates) == 2)
    assert("2020-01-10" in dates)
    assert("2020-01-25" in dates)

def test_get_bom():
    d, c = _create_db()

    _test_insert_assembly(c)

    id_ = d.get_codes_by_code("O")[0][0]

    def find_in_bom(code):
        for k in bom:
            if code == bom[k]["code"]:
                return True
        else:
            return False

    (root, bom) = d.get_bom_by_code_id3(id_, db.iso_to_days("2020-01-25"))

    assert(find_in_bom("L"))
    assert(not find_in_bom("H"))
    assert(find_in_bom("O"))

    (root, bom) = d.get_bom_by_code_id3(id_, db.iso_to_days("2020-01-15"))

    assert(not find_in_bom("L"))
    assert(find_in_bom("H"))
    assert(find_in_bom("O"))

def test_get_bom_dates_by_code_id():
    d, c = _create_db()

    _test_insert_assembly(c)

    id_ = d.get_codes_by_code("O")[0][0]

    dates = d.get_bom_dates_by_code_id(id_)
    assert(len(dates) == 4)

    assert("2020-01-10" in [db.days_to_iso(x) for x in dates])
    assert("2020-01-25" in [db.days_to_iso(x) for x in dates])

    id_ = d.get_codes_by_code("H")[0][0]

    dates = d.get_bom_dates_by_code_id(id_)

    assert(len(dates) == 1)

    assert("2020-01-15" in [db.days_to_iso(x) for x in dates])

    id_ = d.get_codes_by_code("B")[0][0]

    dates = d.get_bom_dates_by_code_id(id_)

    assert(len(dates) == 3)

    assert("2020-01-10" in [db.days_to_iso(x) for x in dates])
    assert(not "2020-01-25" in [db.days_to_iso(x) for x in dates])

def test_get_children_by_rid():
    d, c = _create_db()

    _test_insert_assembly(c)

    id_ = d.get_codes_by_code("A")[0][0]
    rid = d.get_code(id_, db.iso_to_days("2020-01-10"))["rid"]
    children = d.get_children_by_rid(rid)
    assert(len(children) == 2)

    assert("B" in [x[1] for x in children])
    assert(not "M" in [x[1] for x in children])

    id_ = d.get_codes_by_code("E")[0][0]
    rid = d.get_code(id_, db.iso_to_days("2020-01-10"))["rid"]
    children = d.get_children_by_rid(rid)
    assert(len(children) == 0)

    id_ = d.get_codes_by_code("C")[0][0]
    rid = d.get_code(id_, db.iso_to_days("2020-01-10"))["rid"]
    children = d.get_children_by_rid(rid)
    assert(len(children) == 2)
    assert("F" in [x[1] for x in children])
    assert("G" in [x[1] for x in children])

    id_ = d.get_codes_by_code("C")[0][0]
    rid = d.get_code(id_, db.iso_to_days("2020-01-20"))["rid"]
    children = d.get_children_by_rid(rid)
    assert(len(children) == 2)
    assert("I" in [x[1] for x in children])
    assert("L" in [x[1] for x in children])

def test_where_used():
    d, c = _create_db()

    _test_insert_assembly(c)

    def find_in_bom(code):
        for k in bom:
            if code == bom[k]["code"]:
                return True
        else:
            return False

    id_ = d.get_codes_by_code("B")[0][0]
    (root, bom) = d.get_where_used_from_id_code(id_)

    assert(find_in_bom("A"))
    assert(not find_in_bom("H"))
    assert(find_in_bom("O"))

    id_ = d.get_codes_by_code("H")[0][0]
    (root, bom) = d.get_where_used_from_id_code(id_)

    assert(not find_in_bom("L"))
    assert(find_in_bom("H"))
    assert(find_in_bom("O"))

def test_valid_where_used():
    d, c = _create_db()

    _test_insert_assembly(c)

    def find_in_bom(code):
        for k in bom:
            if code == bom[k]["code"]:
                return True
        else:
            return False

    id_ = d.get_codes_by_code("D")[0][0]
    (root, bom) = d.get_where_used_from_id_code(id_)
    assert(len(bom) == 6) # 5 fathers,grand... + the root node = 6

    assert(find_in_bom("A"))
    assert(not find_in_bom("H"))
    assert(find_in_bom("O"))

    id_ = d.get_codes_by_code("H")[0][0]
    (root, bom) = d.get_where_used_from_id_code(id_)

    assert(not find_in_bom("L"))
    assert(find_in_bom("H"))
    assert(find_in_bom("O"))


def test_get_config():
    d, c = _create_db()

    import cfg

    c.execute("""
        INSERT INTO database_props("key", value)
        VALUES ('cfg.test_sect.test_key', 'test-value')
    """)

    cfg.init()
    ret = d.get_config()
    cfg.update_cfg(ret)

    assert(cfg.config()["test_sect"]["test_key"] == 'test-value')

def _create_code_revision(c, code, nr=10):

    c.execute("""INSERT INTO items(code) VALUES (?)""",( code,))
    c.execute("""SELECT MAX (id) FROM items""")
    code_id = c.fetchone()[0]

    dates = ["%04d-06-10"%(2001+i) for i in range(nr+1, 0, -1)]

    i = len(dates)
    to_date_days = db.end_of_the_world
    to_date = ""
    for dt in dates:
        c.execute("""INSERT INTO item_revisions(
            date_from, date_from_days,
            date_to, date_to_days,
            descr, code_id, ver,
            iter, default_unit,
            gval1, gval2) VALUES (
            ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?,
            ?, ?)""", (
                dt, db.iso_to_days(dt),
                to_date, to_date_days,
                "CODE %s"%(code), code_id, "0",
                i, "NR",
                "FOR1COD", "FOR1NAME"
            ))

        to_date_days = db.iso_to_days(dt)-1
        to_date = db.days_to_iso(to_date_days)
        i -= 1

    return code_id


def test_update_dates():
    d, c = _create_db()

    code = "TEST-CODE"
    code_id = _create_code_revision(c, code)
    d._commit(c)

    c.execute("""
        SELECT id, date_from, date_from_days, date_to, date_to_days
        FROM item_revisions
        WHERE code_id = ?
        ORDER BY iter DESC
    """, (code_id, ))
    dates_good = [list(x) for x in c.fetchall()]
    assert(len(dates_good))

    dates = [ x[:] for x in dates_good]

    d.update_dates(dates)

    c.execute("""
        SELECT COUNT(*)
        FROM item_revisions
        WHERE code_id = ?
          AND date_from_days = ?
    """, (code_id, db.prototype_date))
    assert(c.fetchone()[0] == 0)

    c.execute("""
        SELECT COUNT(*)
        FROM item_revisions
        WHERE code_id = ?
          AND iter= ?
    """, (code_id, db.prototype_iter))
    assert(c.fetchone()[0] == 0)

    # insert a prototype
    dates = [ x[:] for x in dates_good]
    
    dates[0][1] = db.days_to_iso(db.prototype_date)
    dates[0][2] = db.prototype_date
    dates[0][3] = ""
    dates[0][4] = db.end_of_the_world

    dates[1][3] = ""
    dates[1][4] = db.prototype_date - 1
    
    d.update_dates(dates)

    c.execute("""
        SELECT COUNT(*)
        FROM item_revisions
        WHERE code_id = ?
          AND date_from_days = ?
    """, (code_id, db.prototype_date))
    assert(c.fetchone()[0] == 1)

    c.execute("""
        SELECT COUNT(*)
        FROM item_revisions
        WHERE code_id = ?
          AND iter= ?
    """, (code_id, db.prototype_iter))
    assert(c.fetchone()[0] == 1)

    dates = [ x[:] for x in dates_good]
    d.update_dates(dates)

    c.execute("""
        SELECT COUNT(*)
        FROM item_revisions
        WHERE code_id = ?
          AND iter= ?
    """, (code_id, db.prototype_iter))
    assert(c.fetchone()[0] == 0)

def test_update_dates_fail():
    d, c = _create_db()

    code = "TEST-CODE"
    code_id = _create_code_revision(c, code)
    d._commit(c)

    c.execute("""
        SELECT id, date_from, date_from_days, date_to, date_to_days
        FROM item_revisions
        WHERE code_id = ?
        ORDER BY iter DESC
    """, (code_id, ))
    dates_good = [list(x) for x in c.fetchall()]
    assert(len(dates_good))
    
    dates = [ x[:] for x in dates_good]
    # _to < _from
    dates[0][4] = dates[0][2] - 1
    
    failed = False
    try:
        d.update_dates(dates)
    except:
        failed = True
    assert(failed)
    
    
    dates = [ x[:] for x in dates_good]
    # swap two rows
    tmp = dates[1][2]
    dates[1][2] = dates[0][2]
    dates[0][2] = tmp
    
    failed = False
    try:
        d.update_dates(dates)
    except:
        failed = True
    assert(failed)
    
    
    dates = [ x[:] for x in dates_good]
    # two row equals
    dates[1][2] = dates[0][2]
    
    failed = False
    try:
        d.update_dates(dates)
    except:
        failed = True
    assert(failed)

    
    dates = [ x[:] for x in dates_good]
    # _to(n+1) >= _from(n)
    dates[1][4] = dates[0][2]
    
    failed = False
    try:
        d.update_dates(dates)
    except:
        failed = True
    assert(failed)


    dates = [ x[:] for x in dates_good]
    # from > prototype date
    dates[0][2] = db.prototype_date + 1
    
    failed = False
    try:
        d.update_dates(dates)
    except:
        failed = True
    assert(failed)


    dates = [ x[:] for x in dates_good]
    # to > end_of_the_worlf
    dates[0][4] = db.end_of_the_world + 1
    
    failed = False
    try:
        d.update_dates(dates)
    except:
        failed = True
    assert(failed)


#------

def run_test(filters):
    import inspect
    from inspect import getmembers, isfunction

    for (name, obj) in inspect.getmembers(sys.modules[__name__]):
        if not inspect.isfunction(obj):
            continue
        if not name.startswith("test_"):
            continue

        skip = len(filters) > 0
        for f in filters:
            if f in name:
                skip = False
                break

        if skip:
            continue

        print(name, end="...")
        sys.stdout.flush()
        obj()
        print("OK")


if __name__ == "__main__":
    #global _connection_string
    for i in range(1, len(sys.argv[1:])):
        if sys.argv[i] == "--create":
            d = getdb.DB()
            d.create_db()
            sys.exit()
        elif sys.argv[i] == "--use-ini-config":
            _use_memory_sqlite=False
        elif sys.argv[i] == "--test":
            run_test(sys.argv[i+1:])

