"""
BOM Browser - tool to browse a bom
Copyright (C) 2021 Goffredo Baroncelli <kreijack@inwind.it>

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

import traceback
import sys
import pprint

from PySide2.QtWidgets import QMessageBox, QFileDialog

import cfg
import db
import utils

_default_unit = "NR"

def import_csv_parent_child(keyword_map, options):

    (fn, _) = QFileDialog.getOpenFileName(None, "Select a file")
    if fn == "":
        return None

    bom = _import_csv_parent_child(open(fn), keyword_map, options)
    return bom

def _split_line(line, sep, ignore_quote):

    while len(line) and line[-1] in "\r\n":
        line = line[:-1]

    if len(line) == 0:
        return []

    if ignore_quote:
        return line.split(sep)

    #fields = line.split('"'+sep+'"')

    #if line[0] != '"' or line[-1] != '"' or len(fields) < 2:
    #    return line.split(sep)

    quote = False
    fields = []
    last_field = ""
    i = 0
    found_sep = False
    while i < len(line):
        if line[i] == '"' and last_field == "" :
            quote = True
            last_field = line[i]
            i += 1
            continue

        if line[i] == '"' and quote and i < (len(line) - 1) and line[i+1]  == '"':
            last_field += line[i]
            i += 2
            continue

        if line[i] == sep and quote:
            last_field += line[i]
            i += 1
            continue

        if line[i] == '"' and quote:
            last_field += line[i]
            quote = False
            i += 1
            continue

        if line[i] == sep: # quote is False
            fields.append(last_field)
            last_field = ""
            found_sep = True
            i += 1
            continue

        last_field += line[i]
        i += 1
    if found_sep:
        fields.append(last_field)

    fields2 = []
    for field in fields:
        if len(field) and field[0] == '"' and field[-1] == '"':
            fields2.append(field[1:-1])
        else:
            fields2.append(field)

    return fields2

def _import_csv_parent_child(f, keyword_map, options):

    separator=";"
    default_unit = "NR"
    ignore_duplicate = False
    ignore_quote = False
    ignore_bom = True
    skip_first_lines = 0

    if "separator" in options:
        separator=options["separator"]
    if "default_unit" in options:
        default_unit = options["default_unit"]
    if "ignore_duplicate" in options:
        ignore_duplicate = int(options["ignore_duplicate"]) > 0
    if "ignore_quote" in options:
        ignore_quote = int(options["ignore_quote"]) > 0
    if "ignore_bom" in options:
        ignore_bom = int(options["ignore_bom"]) > 0
    if "skip_first_lines" in options:
        skip_first_lines = int(options["skip_first_lines"])



    if separator=="COMMA":
        separator=","
    elif separator=="SEMICOLON":
        separator=";"
    elif separator=="COLON":
        separator=":"
    elif separator=="TAB":
        separator="\t"

    while skip_first_lines > 0:
        headers = f.readline()
        skip_first_lines -= 1

    headers = f.readline()

    # ignore the \ufeff code
    if ignore_bom:
        headers = headers.replace("\ufeff", "")
    headers = _split_line(headers, separator, ignore_quote)
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
        s1, s2 = v.split("=")
        map1[s2] = s1

    for i, name in enumerate(headers):
        if name in map1:
            name = map1[name]
        if  name in colmap:
            colmap[name] = i

        # ignore other names

    if colmap["code"] is None or colmap["qty"] is None:
        raise Exception("Some mandatory columns are missing")

    linenr = 0
    bom = dict()

    for line in f.readlines():
        if ignore_bom:
            line = line.replace("\ufeff", "")
        linenr += 1
        fields = _split_line(line, separator, ignore_quote)

        if len(fields) != len(headers):
            raise Exception("Error at line %d: the number of column is different from the header one"%(linenr))

        code_values = {
            "parent_code": 0,
            "unit": default_unit,
            "each": 1,
            "ref": ""
        }

        def xfloat(x):
            x = x.replace(",", ".")
            return float(x)

        for v in colmap:
            if colmap[v] is None:
                continue
            if v in ["qty", "each"]:
                code_values[v] = xfloat(fields[colmap[v]])
            else:
                code_values[v] = fields[colmap[v]]

        if not code_values["parent_code"] in bom:
            bom[code_values["parent_code"]] = {
                "deps": dict(),
                "code:": code_values["parent_code"],
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
            bom[code_values["code"]] = {"deps": dict()}

        for v in code_values:
            if v in ["parent_code", "parent_descr"]:
                continue
            if colmap[v] is None:
                continue
            bom[code_values["code"]][v] = code_values[v]



    return bom

def import_json(keyword_map):
    return { '0': {} }

def get_importer_list():

    l = cfg.config()["BOMBROWSER"].get("importer_list", "").split(",")
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
            separator = cfg.config()[importer_name].get("separator", ";")
            optionss = cfg.config()[importer_name].get("options", "")
            optionsl = optionss.split(",")
            options = {
                "separator": separator,
            }
            if optionss != "":
                for (k,v) in [x.split("=") for x in optionsl]:
                    options[k]=v
            ret.append((importer_name, name,
                utils.Callable(import_csv_parent_child, map_.split(","), options)))
        else: # json
            ret.append((importer_name, name,
                utils.Callable(import_json, map_)))

    return ret


def test_split_line():
    ret = _split_line('"abc","def","ghi""ef"', ",", False)
    assert(ret == ["abc", "def", "ghi\"ef"])

    ret = _split_line('abc,def,ghi"ef', ",", False)
    assert(ret == ["abc", "def", "ghi\"ef"])

    ret = _split_line('abc,"def",ghi"ef', ",", False)
    assert(ret == ["abc", "def", "ghi\"ef"])

    ret = _split_line('"abc","def","ghi""ef"', ",", True)
    assert(ret == ['"abc"', '"def"', '"ghi""ef"'])

    ret = _split_line('abc,"def",ghi"ef', ",", True)
    assert(ret == ["abc", '"def"', "ghi\"ef"])

    ret = _split_line('"abc","def","ghi""ef"', ",", False)
    assert(ret == ["abc", "def", "ghi\"ef"])

    ret = _split_line('abc\tdef\tghi"ef', "\t", False)
    assert(ret == ["abc", "def", "ghi\"ef"])

def test_import_csv_parent_child():
    import io
    f = io.StringIO(""""parent_code";"parent_descr";"code";"descr";"qty";"each";"unit";"gval1"
"Z";"0-descr";"1";"1-descr";"1";"2";"nr";"gval-1"
"Z";"0-descr";"2";"2-descr";"2";"3";"nr";"gval-2"
"4";"4-descr";"3";"3-descr";"8";"9";"nr";"gval-7"
"Z";"0-descr";"4";"4-descr";"1.5";"3";"gr";"gval-4"
""")

    bom = _import_csv_parent_child(f,[], {})

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

def test_import_csv_parent_child_error_on_duplicate_row():
    import io
    s = """"parent_code";"parent_descr";"code";"descr";"qty";"each";"unit";"gval1"
"0";"0-descr";"1";"1-descr";"1";"2";"nr";"gval-1"
"0";"0-descr";"2";"2-descr";"2";"3";"nr";"gval-2"
"4";"4-descr";"3";"3-descr";"8";"9";"nr";"gval-7"
"0";"0-descr";"4";"4-descr";"1.5";"3";"gr";"gval-4"
"""

    f = io.StringIO(s)
    bom = _import_csv_parent_child(f,[], {})

    # ok the file is ok

    # add a duplicate
    s1 = s + '"0";"0-descr";"4";"4-descr";"1.5";"3";"gr";"gval-4"'
    failed = True
    try:
        f = io.StringIO(s1)
        bom = _import_csv_parent_child(f,[], {})
    except:
        failed = False

    assert(not failed)

    s1 = s + '"0";"0-descr";"4";"4-descr";"1.5";"3";"gr";"gval-4"'
    f = io.StringIO(s1)
    bom = _import_csv_parent_child(f,[], {"ignore_duplicate":"1"})

def test_import_csv_parent_child_error_on_less_columns():
    import io
    s = """"parent_code";"parent_descr";"code";"descr";"qty";"each";"unit";"gval1"
"0";"0-descr";"1";"1-descr";"1";"2";"nr";"gval-1"
"0";"0-descr";"2";"2-descr";"2";"3";"nr";"gval-2"
"4";"4-descr";"3";"3-descr";"8";"9";"nr";"gval-7"
"0";"0-descr";"4";"4-descr";"1.5";"3";"gr";"gval-4"
"""

    f = io.StringIO(s)
    bom = _import_csv_parent_child(f,[], {})

    # ok the file is ok

    # add a row with less columns
    s1 = s + '"0";"0-descr";"7";"4-descr";"1.5";"3";"gr"'
    failed = True
    try:
        f = io.StringIO(s1)
        bom = _import_csv_parent_child(f,[], {})
    except:
        failed = False

    assert(not failed)

    s2 = s1 + ';"gval-4"'
    f = io.StringIO(s2)
    bom = _import_csv_parent_child(f,[], {})

def test_import_csv_parent_child_error_on_more_columns():
    import io
    s = """"parent_code";"parent_descr";"code";"descr";"qty";"each";"unit";"gval1"
"0";"0-descr";"1";"1-descr";"1";"2";"nr";"gval-1"
"0";"0-descr";"2";"2-descr";"2";"3";"nr";"gval-2"
"4";"4-descr";"3";"3-descr";"8";"9";"nr";"gval-7"
"0";"0-descr";"4";"4-descr";"1.5";"3";"gr";"gval-4"
"""

    f = io.StringIO(s)
    bom = _import_csv_parent_child(f,[], {})

    # ok the file is ok

    # add a row with the same column columns
    s1 = s + '"0";"0-descr";"7";"4-descr";"1.5";"3";"gr";"gval-4"'

    f = io.StringIO(s1)
    bom = _import_csv_parent_child(f,[], {})

    s2 = s1 + ';"gval-4"'
    failed = True
    try:
        f = io.StringIO(s2)
        bom = _import_csv_parent_child(f,[], {})
    except:
        failed = False

    assert(not failed)

def test_import_csv_parent_child_comma_separator():
    import io
    f = io.StringIO(""""parent_code","parent_descr","code","descr","qty","each","unit","gval1"
"0","0-descr","1","1-descr","1","2","nr","gval-1"
"0","0-descr","2","2-descr","2","3","nr","gval-2"
"4","4-descr","3","3-descr","8","9","nr","gval-7"
"0","0-descr","4","4-descr","1.5","3","gr","gval-4"
""")

    bom = _import_csv_parent_child(f,[], {"separator":"COMMA"})

    assert("0" in bom)
    assert("1" in bom)

    assert(bom["0"]["descr"] == "0-descr")
    assert(bom["1"]["descr"] == "1-descr")
    assert(bom["1"]["gval1"] == "gval-1")

def test_import_csv_parent_child_tab_separator():
    import io
    f = io.StringIO(""""parent_code"\t"parent_descr"\t"code"\t"descr"\t"qty"\t"each"\t"unit"\t"gval1"
"0"\t"0-descr"\t"1"\t"1-descr"\t"1"\t"2"\t"nr"\t"gval-1"
"0"\t"0-descr"\t"2"\t"2-descr"\t"2"\t"3"\t"nr"\t"gval-2"
"4"\t"4-descr"\t"3"\t"3-descr"\t"8"\t"9"\t"nr"\t"gval-7"
"0"\t"0-descr"\t"4"\t"4-descr"\t"1.5"\t"3"\t"gr"\t"gval-4"
""")

    bom = _import_csv_parent_child(f,[], {"separator":"TAB"})

    assert("0" in bom)
    assert("1" in bom)

    assert(bom["0"]["descr"] == "0-descr")
    assert(bom["1"]["descr"] == "1-descr")
    assert(bom["1"]["gval1"] == "gval-1")

def test_import_csv_parent_child_utf8_bom():
    import io
    s = """"parent_code"\t"parent_descr"\t"code"\t"descr"\t"qty"\t"each"\t"unit"\t"gval1"
"0"\t"0-descr"\t"1"\t"1-descr"\t"1"\t"2"\t"nr"\t"gval-1"
"0"\t"0-descr"\t"2"\t"2-descr"\t"2"\t"3"\t"nr"\t"gval-2"
"4"\t"4-descr"\t"3"\t"3-descr"\t"8"\t"9"\t"nr"\t"gval-7"
"0"\t"0-descr"\t"4"\t"4-descr"\t"1.5"\t"3"\t"gr"\t"gval-4"
"""

    f = io.StringIO(s)
    bom = _import_csv_parent_child(f,[], {"separator":"TAB"})

    assert("0" in bom)
    assert("1" in bom)
    assert(not 0 in bom)

    s1 = "\ufeff" + s
    f = io.StringIO(s1)
    bom = _import_csv_parent_child(f,[], {"separator":"TAB", "ignore_bom":"0"})

    assert(0 in bom)
    assert(not "0" in bom)

    f = io.StringIO(s1)
    bom = _import_csv_parent_child(f,[], {"separator":"TAB", "ignore_bom":"1"})

    assert("0" in bom)
    assert("1" in bom)

def test_import_csv_parent_child_wo_parent_columns():
    import io
    s = """"code"\t"descr"\t"qty"\t"each"\t"unit"\t"gval1"
"1"\t"1-descr"\t"1"\t"2"\t"nr"\t"gval-1"
"2"\t"2-descr"\t"2"\t"3"\t"nr"\t"gval-2"
"3"\t"3-descr"\t"8"\t"9"\t"nr"\t"gval-7"
"4"\t"4-descr"\t"1.5"\t"3"\t"gr"\t"gval-4"
"""

    f = io.StringIO(s)
    bom = _import_csv_parent_child(f,[], {"separator":"TAB"})

    assert(0 in bom)
    assert("1" in bom)

    assert( bom[0]["deps"]["2"]["qty"] == 2)
    assert( bom[0]["deps"]["2"]["each"] == 3)


if __name__ == "__main__":
    last = 1
    import test_db
    test_db.run_test(sys.argv[last:], sys.modules[__name__])
