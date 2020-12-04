import db
import sys
import datetime

def _test_insert_items(c):
    codes = [('code123', "descr456", 0), ('code124', "descr457", 0),
            ('code135', "descr468", 0), ('code136', "descr469", 0),
            ('code123', "descr456", 1)]
    for (code, descr, ver) in codes:

        c.execute("""INSERT INTO items(
            descr, code, ver,
            iter, default_unit,
            for1cod, for1name) VALUES (
            ?, ?, ?,
            ?, ?,
            ?, ?)""", (
                descr, code, "%d"%(ver),
                ver, "NR",
                "FOR1COD", "FOR1NAME"
            ))

_connection_string="SQLITE::memory:"

def _create_db():
    d = db.DB(_connection_string)
    d.create_db()
    return (d, d._conn.cursor())

def test_double_recreate_db():
    d, c = _create_db()
    assert("database_props" in d._get_tables_list())
    d, c = _create_db()

def test_get_code():
    d, c = _create_db()

    _test_insert_items(c)

    data = d.get_code(1)
    assert(data["code"] == "code123")
    assert(data["descr"] == "descr456")

    data = d.get_codes_by_code("code124")
    assert(len(data) == 1)
    assert(data[0][1] == "code124")
    assert(data[0][2] == "descr457")


    data = d.get_codes_by_like_code("code12%")
    assert(len(data) == 3)
    data.sort(key = lambda x: x[1])
    assert(data[0][1] == "code123")
    assert(data[0][2] == "descr456")

    assert(data[2][1] == "code124")
    assert(data[2][2] == "descr457")

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
        "O": [ ("A", "2020-01-10", "2020-01-14"),
               ("A", "2020-01-15", "2020-01-19"),
               ("A", "2020-01-20", "2020-01-24"),
               ("A", "2020-01-25", ""), ],

        "A": [ ("B", "2020-01-10", "2020-01-14"),
               ("B", "2020-01-15", "2020-01-19"),
               ("B", "2020-01-20", ""),

               ("C", "2020-01-10", "2020-01-14"),
               ("C", "2020-01-15", "2020-01-19"),
               ("C", "2020-01-20", "2020-01-24"),

               ("M", "2020-01-25", ""), ],

        "B": [ ("D", "2020-01-10", "2020-01-14"),
               ("D", "2020-01-20", ""),

               ("H", "2020-01-15", "2020-01-19"),

               ("E", "2020-01-10", ""), ],

        "C": [ ("F", "2020-01-10", "2020-01-14"),

               ("G", "2020-01-10", "2020-01-19"),

               ("I", "2020-01-15", ""),

               ("L", "2020-01-20", ""), ],

        "M": [ ("I", "2020-01-25", ""),

               ("L", "2020-01-25", ""), ],

    }


    items = set(ass.keys())
    items2=list(items)
    for k in items2:
        for i,from_, to in ass[k]:
            items.add(i)

    map_code_id = {}
    for i in items:
        c.execute("""INSERT INTO items(
            descr, code, ver,
            iter, default_unit,
            for1cod, for1name) VALUES (
            ?, ?, ?,
            ?, ?,
            ?, ?)""", (
                "Items '%s'"%(i), i, "1",
                1, "NR",
                "FOR1COD", "FOR1NAME"
        ))
        c.execute("""SELECT MAX(id) FROM items""")
        id_ = c.fetchone()[0]
        map_code_id[i] = id_

    # insert the assy by date order

    dates = []
    for parent in ass:
        for child, from_, to_ in ass[parent]:
            if not from_ in dates:
                dates.append(from_)

    dates.sort()

    while len(dates):
        the_date = dates[0]
        dates = dates[1:]

        for parent in ass:
            for child, from_, to_ in ass[parent]:
                if from_ != the_date:
                    continue

                if to_ == "":
                    ts = db.end_of_the_world
                else:
                    ts = datetime.date.fromisoformat(to_).toordinal()
                #print("map_code_id[child]=", map_code_id[child])
                c.execute("""INSERT INTO assemblies (
                    unit,
                    child_id, parent_id,
                    qty,
                    each,
                    date_from, date_to,
                    date_from_days,
                    date_to_days,
                    iter, ref) VALUES (
                    ?,
                    ?, ?,
                    ?,
                    ?,
                    ?, ?,
                    ?, ?,
                    ?, ? )""", (
                        "NR",
                        map_code_id[child], map_code_id[parent],
                        1,
                        1,
                        from_, to_,
                        datetime.date.fromisoformat(from_).toordinal(),
                        ts,
                        0, '//')
                )

def test_is_assembly():
    d, c = _create_db()

    _test_insert_assembly(c)

    assert(d.is_assembly(d.get_codes_by_code("A")[0][0]))
    assert(not d.is_assembly(d.get_codes_by_code("L")[0][0]))

def test_get_dates():
    d, c = _create_db()

    _test_insert_assembly(c)

    id_ = d.get_codes_by_code("A")[0][0]

    dates = [ x[1] for x in d.get_dates_by_code_id(id_)]
    assert(len(dates) == 4)
    assert("2020-01-10" in dates)
    assert("2020-01-20" in dates)

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

    (root, bom) = d.get_bom_by_code_id2(id_, "2020-01-25")

    assert(find_in_bom("L"))
    assert(not find_in_bom("H"))
    assert(find_in_bom("O"))

    (root, bom) = d.get_bom_by_code_id2(id_, "2020-01-15")

    assert(not find_in_bom("L"))
    assert(find_in_bom("H"))
    assert(find_in_bom("O"))

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
        elif sys.argv[i] == "--sqlserver":
            import configparser
            cfg = configparser.ConfigParser()
            cfg.read_file(open("bombrowser.ini"))
            d = {
                "driver": cfg.get("SQLSERVER", "driver"),
                "server": cfg.get("SQLSERVER", "server"),
                "database": cfg.get("SQLSERVER", "database")+"_test",
                "username": cfg.get("SQLSERVER", "username"),
                "password": cfg.get("SQLSERVER", "password"),
            }
            _connection_string = "SQLSERVER:DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}".format(**d)
        elif sys.argv[i] == "--test":
            run_test(sys.argv[i+1:])

