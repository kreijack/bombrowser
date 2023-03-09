"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021,2022,2023 Goffredo Baroncelli <kreijack@inwind.it>

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
import csv
import xlrd

from PySide2.QtWidgets import QFileDialog

import cfg
import db
import utils

_default_unit = "NR"

def _csv_parent_child_get_filename(options):

    (fn, _) = QFileDialog.getOpenFileName(None, "Select a file to import",
        None,
        "CSV files (*.csv);;Excel file (*.xls *.xlsx);;All files (*.*)")
    return fn

def _csv_parent_child_import(fn, keyword_map, options):

    if fn == "":
        return None

    data = _read_table(fn, options)

    bom = _import_csv_parent_child2(data, keyword_map, options)
    return bom

def import_csv_parent_child(keyword_map, options):

    fn = _csv_parent_child_get_filename(options)
    return _csv_parent_child_import(fn, keyword_map, options)

def _read_table_xls(nf):
    book = xlrd.open_workbook(nf)
    sh = book.sheet_by_index(0)
    ret = []
    for row in range(sh.nrows):
        ret.append([sh.cell_value(row, col) for col in range(sh.ncols)])

    return ret

def _read_table_csv(nf, options):
    delimiter = ';'
    quotechar = '"'
    if "delimiter" in options:
        delimiter_ = options["delimiter"]
        if delimiter_ == "COMMA":
            delimiter = ","
        elif delimiter_ == "SEMICOLON":
            delimiter = ";"
        elif delimiter_ == "TAB":
            delimiter = "\t"
    if "quotechar" in options:
        quotechar_ = options["quotechar"]
        if quotechar_ == 'SINGLEQUOTE':
            quotechar = "'"
        elif quotechar_ == 'DOUBLEQUOTE':
            quotechar = '"'

    with open(nf, newline='') as csvfile:
        c = csvfile.read(1)
        if c == '\ufeff':
            enc = 'utf-8-sig'
        else:
            enc = 'utf-8'

    if enc is None:
        csvfile = open(nf, newline='')
    else:
        csvfile = open(nf, newline='', encoding=enc)

    dialect = csv.Sniffer().sniff(csvfile.read(1024*16))
    csvfile.seek(0)
    opts = dict()
    reader = csv.reader(csvfile, dialect, quotechar=quotechar,
                            delimiter=delimiter)
    reader = list(reader)

    if reader[0][0][0] == '\ufeff':
        reader[0][0] = reader[0][0][1:]

    return reader

def _read_table(nf, options):
    if nf.lower().endswith(".csv"):
        return _read_table_csv(nf, options)
    elif nf.lower().endswith(".xls") or nf.lower().endswith(".xlsx"):
        return _read_table_xls(nf)
    else:
        raise Exception("Format of file '%s' unknown; supported file: .csv or .xls"%(
            nf))

def _import_csv_parent_child2(data, keyword_map, options):

    default_unit = "NR"
    ignore_duplicate = False
    skip_first_lines = 0

    if "default_unit" in options:
        default_unit = options["default_unit"]
    if "ignore_duplicate" in options:
        ignore_duplicate = int(options["ignore_duplicate"]) > 0
    if "skip_first_lines" in options:
        skip_first_lines = int(options["skip_first_lines"])

    headers = data[skip_first_lines]

    if len(headers) < 1:
        raise Exception("Too few column")

    map1 = dict()
    colmap = {
        "code": None,
        "descr": None,
        "parent_code": None,
        "parent_descr": None,
        "qty" : None,
        "unit" : None,
        "each" : None,
        "ref": None,
        "ver": None,
    }
    for i in range(0, db.gvals_count):
        colmap["gval%d"%(i)] = None

    for v in keyword_map:
        s1, s2 = v.split(":")
        map1[s2] = s1

    # check that each mapped keyword is present in header
    for k in map1.keys():
        if not k in headers:
            raise Exception(
                "import: cannot find column '%s' in the file to be imported"%(
                k))

    for i, name in enumerate(headers):
        if name in map1:
            name = map1[name]
        if  name in colmap:
            colmap[name] = i

        # ignore other names

    for col in ["code", "qty"] :
        if colmap[col] is None:
            raise Exception("The mandatory column '%s' is missing"%(col))

    linenr = skip_first_lines
    bom = dict()

    for fields in data[skip_first_lines+1:]:
        linenr += 1

        if len(fields) != len(headers):
            raise Exception("Error at line %d: the number of column is different from the header one"%(linenr))

        code_values = {
            "parent_code": 0,
            "unit": default_unit,
            "each": 1,
            "ref": ""
        }

        def xfloat(x):
            if isinstance(x, str):
                if x == "":
                    x = 0
                else:
                    x = str(x).replace(",", ".")
            return float(x)

        for v in colmap:
            if colmap[v] is None:
                continue
            if v in ["qty", "each"]:
                code_values[v] = xfloat(fields[colmap[v]])
            elif isinstance(fields[colmap[v]], int):
                # it is an int convert to str
                code_values[v] = str(fields[colmap[v]])
            elif (isinstance(fields[colmap[v]], float) and
                  (float(int(fields[colmap[v]])) == fields[colmap[v]])):
                    # it is a float convert to int then to str
                    # only if this doesn't change its value (i.e. the
                    # decimal part is .0)
                    code_values[v] = str(int(fields[colmap[v]]))
            else:
                code_values[v] = str(fields[colmap[v]])

        if "translate" in options:
            translate = options["translate"]
            for v in colmap:
                if not v in translate:
                    continue
                if not code_values[v] in translate[v]:
                    continue
                code_values[v] = translate[v][code_values[v]]

        if not code_values["parent_code"] in bom:
            bom[code_values["parent_code"]] = {
                "deps": dict(),
                "code": code_values["parent_code"],
            }
            if "parent_descr" in code_values:
                bom[code_values["parent_code"]]["descr"] = code_values["parent_descr"]

        if code_values["code"] in bom[code_values["parent_code"]]["deps"]:
            if not ignore_duplicate:
                raise Exception("Error at line %d: this line is a duplicated"%(linenr))

        bom[code_values["parent_code"]]["deps"][code_values["code"]] = {
            "code": code_values["code"],
            "qty": code_values["qty"],
            "each": code_values["each"],
            "unit": code_values["unit"],
            "ref": code_values["ref"],
        }

        if not code_values["code"] in bom:
            bom[code_values["code"]] = {
                "deps": dict(),
            }

        for v in code_values:
            if v in ["parent_code", "parent_descr", "qty", "each", "ref"]:
                continue
            if colmap[v] is None:
                continue
            bom[code_values["code"]][v] = code_values[v]

    return bom

def import_json(keyword_map):
    return { '0': {} }

def _parse_translate_parameter(s):
    ret = dict()
    l = s.split("\n")
    key = None
    for i in l:
        i = i.strip()

        if len(i) == 0:
            continue

        if i.endswith(":"):
            assert(len(i) > 1)
            key = i[:-1]
            ret[key] = dict()
            continue
        assert(key)

        l2 = utils.split_with_escape(i, "=", quote='"')
        assert(len(l2) == 2)

        ret[key][l2[0]] = l2[1]

    return ret

def get_importer_list():

    l = utils.split_with_escape(
                    cfg.config()["BOMBROWSER"].get("importer_list"),
                    delimiter=',', quote='"')
    if l == [""]:
        return None
    ret = []
    for importer_name in l:
        if not cfg.config().has_section(importer_name):
            continue
        name = cfg.config()[importer_name].get("name", None)
        type_ = cfg.config()[importer_name].get("type", None)
        map_ = cfg.config()[importer_name].get("map", None)
        translate = cfg.config()[importer_name].get("translate", None)
        if translate:
            translate = _parse_translate_parameter(translate)
        else:
            translate = dict()

        if map_ is None or type_ is None or name is None:
            print("Importer '%s' is not defined properly"%(importer_name))
            continue

        if not type_ in ["parent_child", "json"]:
            print("Importer '%s': unknown type '%s'"%(importer_name, type_))
            continue

        name, map_, type_ = map(lambda x : x.strip(), (name, map_, type_))

        if type_ == "parent_child":
            options = dict()
            for k in ["default_unit", "skip_first_lines", "ignore_duplicate",
                        "delimiter", "quotechar"]:
                if k in cfg.config()[importer_name]:
                    options[k] = cfg.config()[importer_name].get(k)
            mapl = [x.strip() for x in map_.split("\n") if len(x.strip()) > 0]
            ret.append((importer_name, name,
                utils.Callable(import_csv_parent_child, mapl, options)))
        else: # json
            ret.append((importer_name, name,
                utils.Callable(import_json, map_)))

    return ret

def get_diff_importer_list():

    l = utils.split_with_escape(
                    cfg.config()["BOMBROWSER"].get("importer_list"),
                    delimiter=',', quote='"')
    if l == [""]:
        return None
    ret = []
    for importer_name in l:
        if not cfg.config().has_section(importer_name):
            continue
        name = cfg.config()[importer_name].get("name", None)
        type_ = cfg.config()[importer_name].get("type", None)
        map_ = cfg.config()[importer_name].get("map", None)

        if map_ is None or type_ is None or name is None:
            print("Importer '%s' is not defined properly"%(importer_name))
            continue

        if not type_ in ["parent_child", "json"]:
            print("Importer '%s': unknown type '%s'"%(importer_name, type_))
            continue

        name, map_, type_ = map(lambda x : x.strip(), (name, map_, type_))

        if type_ == "parent_child":
            options = dict()
            for k in ["default_unit", "skip_first_lines", "ignore_duplicate",
                        "delimiter", "quotechar"]:
                if k in cfg.config()[importer_name]:
                    options[k] = cfg.config()[importer_name].get(k)
            mapl = [x.strip() for x in map_.split("\n") if len(x.strip()) > 0]
            ret.append((importer_name, name,
                utils.Callable(_csv_parent_child_get_filename, options.copy()),
                utils.Callable(_csv_parent_child_import, mapl[:], options.copy()))
            )
        #else: # json
        #    ret.append((importer_name, name,
        #        utils.Callable(import_json, map_)))

    return ret

def test_import_csv_parent_child2():
    import io
    data = """parent_code;parent_descr;code;descr;qty;each;unit;gval1
Z;0-descr;1;1-descr;1;2;nr;gval-1
Z;0-descr;2;2-descr;2;3;nr;gval-2
4;4-descr;3;3-descr;8;9;nr;gval-7
Z;0-descr;4;4-descr;1.5;3;gr;gval-4"""

    data = [x.split(";") for x in data.split("\n")]

    bom = _import_csv_parent_child2(data,[], {})

    assert("Z" in bom)
    assert("1" in bom)

    assert(bom["Z"]["descr"] == "0-descr")
    assert(bom["1"]["descr"] == "1-descr")
    assert(bom["1"]["gval1"] == "gval-1")

    assert("1" in bom["Z"]["deps"])
    assert(bom["Z"]["deps"]["1"]["qty"] == 1)
    assert(bom["Z"]["deps"]["1"]["each"] == 2)
    assert(bom["Z"]["deps"]["1"]["unit"] == "nr")
    assert(bom["Z"]["deps"]["4"]["qty"] == 1.5)

    assert("2" in bom["Z"]["deps"])
    assert("4" in bom["Z"]["deps"])

    assert("3" in bom["4"]["deps"])

    assert("4" in bom["Z"]["deps"])

def test_import_csv_parent_child2_error_on_duplicate_row():
    import io
    s = """parent_code;parent_descr;code;descr;qty;each;unit;gval1
0;0-descr;1;1-descr;1;2;nr;gval-1
0;0-descr;2;2-descr;2;3;nr;gval-2
4;4-descr;3;3-descr;8;9;nr;gval-7
0;0-descr;4;4-descr;1.5;3;gr;gval-4"""

    data = [x.split(";") for x in s.split("\n")]
    bom = _import_csv_parent_child2(data,[], {})

    # ok the file is ok

    # add a duplicate
    s1 = s + '\n0;0-descr;4;4-descr;1.5;3;gr;gval-4'
    data = [x.split(";") for x in s1.split("\n")]
    failed = True
    try:
        f = io.StringIO(s1)
        bom = _import_csv_parent_child2(data,[], {})
    except:
        failed = False

    assert(not failed)

    s1 = s + '\n0;0-descr;4;4-descr;1.5;3;gr;gval-4'
    data = [x.split(";") for x in s1.split("\n")]
    bom = _import_csv_parent_child2(data,[], {"ignore_duplicate":"1"})

def test_import_csv_parent_child2_error_on_less_columns():
    import io
    s = """parent_code;parent_descr;code;descr;qty;each;unit;gval1
0;0-descr;1;1-descr;1;2;nr;gval-1
0;0-descr;2;2-descr;2;3;nr;gval-2
4;4-descr;3;3-descr;8;9;nr;gval-7
0;0-descr;4;4-descr;1.5;3;gr;gval-4"""

    data = [x.split(";") for x in s.split("\n")]
    bom = _import_csv_parent_child2(data,[], {})

    # ok the file is ok

    # add a row with less columns
    s1 = s + '\n0;0-descr;7;4-descr;1.5;3;gr'
    failed = True
    try:
        data = [x.split(";") for x in s1.split("\n")]
        bom = _import_csv_parent_child2(data, [], {})
    except:
        failed = False

    assert(not failed)

    s2 = s1 + ';"gval-4"'
    data = [x.split(";") for x in s2.split("\n")]
    bom = _import_csv_parent_child2(data, [], {})

def test_import_csv_parent_child2_error_on_more_columns():
    import io
    s = """parent_code;parent_descr;code;descr;qty;each;unit;gval1
0;0-descr;1;1-descr;1;2;nr;gval-1
0;0-descr;2;2-descr;2;3;nr;gval-2
4;4-descr;3;3-descr;8;9;nr;gval-7
0;0-descr;4;4-descr;1.5;3;gr;gval-4"""

    data = [x.split(";") for x in s.split("\n")]
    bom = _import_csv_parent_child2(data,[], {})

    # ok the file is ok

    # add a row with the same column columns
    s1 = s + '\n0;0-descr;7;4-descr;1.5;3;gr;gval-4'

    data = [x.split(";") for x in s1.split("\n")]
    bom = _import_csv_parent_child2(data, [], {})

    s2 = s1 + ';gval-4'
    failed = True
    try:
        data = [x.split(";") for x in s2.split("\n")]
        bom = _import_csv_parent_child2(data,[], {})
    except:
        failed = False

    assert(not failed)

def test_import_csv_parent_child2_wo_parent_columns():
    import io
    s = """code\tdescr\tqty\teach\tunit\tgval1
1\t1-descr\t1\t2\tnr\tgval-1
2\t2-descr\t2\t3\tnr\tgval-2
3\t3-descr\t8\t9\tnr\tgval-7
4\t4-descr\t1.5\t3\tgr\tgval-4"""

    data = [x.split("\t") for x in s.split("\n")]
    bom = _import_csv_parent_child2(data,[], {})

    assert(0 in bom)
    assert("1" in bom)

    assert( bom[0]["deps"]["2"]["qty"] == 2)
    assert( bom[0]["deps"]["2"]["each"] == 3)


def test_import_csv_parent_child2_fields_convesrion():
    import io
    s = """code\tdescr\tqty\teach\tunit\tgval1
1\t1-descr\t1\t2\tnr\tgval-1
2\t2-descr\t2.0\t3.1\tnr\tgval-2
3\t3-descr\t8\t9\tnr\tgval-7
4\t4-descr\t1.5\t3\tgr\tgval-4"""

    data = [x.split("\t") for x in s.split("\n")]

    data[1][0] = 1
    data[2][0] = 2.0
    data[3][0] = 3.1
    data[4][0] = "4.0"
    bom = _import_csv_parent_child2(data,[], {})

    assert(0 in bom)
    assert("1" in bom)      # 1 -> '1'          int -> str
    assert("2" in bom)      # 2.0 -> 2 -> '2'   int -> floar -> str
    assert("3.1" in bom)    # 3.1 -> '3.1'      float -> str, because
                            #                   float(int(3..1)) != 3.1
    assert("4.0" in bom)    # '4.0'             no conversion

    assert( bom[0]["deps"]["2"]["qty"] == 2.0)
    assert( bom[0]["deps"]["2"]["each"] == 3.1)

def test_import_csv_parent_child2_qty_each_conversion():
    import io
    s = """code\tdescr\tqty\teach\tunit\tgval1
1\t1-descr\t1\t2\tnr\tgval-1
2\t2-descr\t2.0\t3.1\tnr\tgval-2
3\t3-descr\t\t9\tnr\tgval-7
4\t4-descr\t1,5\t3\tgr\tgval-4"""

    data = [x.split("\t") for x in s.split("\n")]

    bom = _import_csv_parent_child2(data,[], {})

    assert( bom[0]["deps"]["1"]["qty"] == 1)    #  '1' -> 1.0
    assert( bom[0]["deps"]["2"]["qty"] == 2)    #  '2.0' -> 2.0
    assert( bom[0]["deps"]["2"]["each"] == 3.1) #  '3.1' -> 3.1
    assert( bom[0]["deps"]["3"]["qty"] == 0)    #  '' -> 0.0
    assert( bom[0]["deps"]["4"]["qty"] == 1.5)  #   '1,5' -> '1.5' -> 1.5

def test_check_presence_of_columns():
    s = """code\tdescr\tqty2\teach\tunit\tgval1
1\t1-descr\t1\t2\tnr\tgval-1
2\t2-descr\t2.0\t3.1\tnr\tgval-2
3\t3-descr\t\t9\tnr\tgval-7
4\t4-descr\t1,5\t3\tgr\tgval-4"""

    data = [x.split("\t") for x in s.split("\n")]
    bom = _import_csv_parent_child2(data,["qty:qty2"], {})

    excp = False
    try:
        bom = _import_csv_parent_child2(data,["qty:qty3"], {})
    except Exception as e:
        assert("import: cannot find column" in str(e))
        assert("qty3" in str(e))
        excp = True
    assert(excp)


def test_parse_translate_parameter_ok():
    s="\nqty:\na=b\nc=d\n\ngval1:\ne=f\nk=l"
    ret = _parse_translate_parameter(s)
    assert("qty" in ret)
    assert("gval1" in ret)
    assert(len(ret["qty"].keys()) == 2)
    assert(len(ret["gval1"].keys()) == 2)
    assert("a" in ret["qty"])
    assert(ret["qty"]["c"] == "d")
    assert("e" in ret["gval1"])
    assert(ret["gval1"]["k"] == "l")

def test_parse_translate_parameter_fail_no_key():
    s="\n\na=b\nc=d\n\ngval1:\ne=f\nk=l"
    ok = False
    try:
        ret = _parse_translate_parameter(s)
    except:
        ok = True
    assert(ok)

def test_parse_translate_parameter_fail_no_eq():
    s="\n\nab:\ncd\n\ngval1:\ne=f\nk=l"
    ok = False
    try:
        ret = _parse_translate_parameter(s)
    except:
        ok = True
    assert(ok)

def test_parse_translate_parameter_ok_quote():
    s="\n\nab:\n\"c=\"=d\n\ngval1:\ne=f\nk=l"
    ret = _parse_translate_parameter(s)
    assert(ret["ab"]["c="] == 'd')

def test_parse_translate_parameter_ok_quote_2():
    s="\n\nab:\nc=\"=d\"\n\ngval1:\ne=f\nk=l"
    ret = _parse_translate_parameter(s)
    assert(ret["ab"]["c"] == '=d')

def test_import_csv_parent_child2_translate():
    data = """parent_code;parent_descr;code;descr;qty;each;unit;gval1
Z;0-descr;1;1-descr;1;2;nr;gval-1
Z;0-descr;2;2-descr;2;3;nr;gval-2
4;4-descr;2;3-descr;8;9;mt;mt
Z;0-descr;4;4-descr;1.5;3;gr;gval-4"""

    data = [x.split(";") for x in data.split("\n")]

    bom = _import_csv_parent_child2(data,[], {
                "translate": { "unit": { "nr" : "NR", "mt": "MT" } }
    })
    assert(bom["Z"]["deps"]["1"]["unit"] == "NR")
    assert(bom["4"]["deps"]["2"]["unit"] == "MT")
    assert(bom["2"]["gval1"] == "mt")


if __name__ == "__main__":
    last = 1
    import test_db
    test_db.run_test(sys.argv[last:], sys.modules[__name__])
