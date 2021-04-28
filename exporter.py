"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021 Goffredo Baroncelli <kreijack@inwind.it>

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
import os
import json
import io

import csv
import xlwt

import cfg
import utils
import db

def get_template_list():
    ret = []
    template_list = utils.split_with_escape(
                        cfg.config()["BOMBROWSER"]["templates_list"],
                        delimiter=',', quote='"')
    for template_section in template_list:
        if not template_section in cfg.config():
            continue
        if not "name" in cfg.config()[template_section]:
            continue
        ret.append((template_section, cfg.config().get(template_section, "name")))
    return ret

class Exporter:
    def __init__(self, rootnode, data):
        self._data = data
        self._rootnode = rootnode
        self._drawings = dict()

    def export_as_json(self, nf):
        f = open(nf, "w")
        json.dump({
            "root": self._rootnode,
            "data": self._data
        }, f, sort_keys=True, indent=4, default=str)
        f.close()


# available columns type
# seq -> sequential number AFTER the sorting
# level -> level of identation
# code -> code
# paren -> parent_code
# indented_code code indented (prefixe by "... ... " depending by the level )
# descr -> code description
# qty -> code quantity
# unit -> unit
# each -> each
# ref -> ref
# drawings -> drawings path
# gval0, glval1 -> generic fields
# rev -> code revision
# iter -> code iteration
# date_from -> from date
# date_to -> date_to

    def _export_as_table_by_template_it(self, unique, table, columns,
                key, level=0, qty="", each="", unit="", ref="", parent="",
                parent_descr="", maxlevel=-1):

        if maxlevel != -1 and level >= maxlevel:
            return

        if unique:
            if key in self._did:
                return
            self._did.add(key)

        if key in self._path:
            table.append(["loop" for x in columns])
            self._seq += 1
            return

        self._path = self._path[:level] + [key]

        row = []
        item = self._data[key]
        for col in columns:
            if col=="seq":
                row += [self._seq]
            elif col=="level":
                row += [level]
            elif col=="qty":
                row += [qty]
            elif col=="each":
                row += [each]
            elif col=="ref":
                row += [ref]
            elif col=="parent_descr":
                row += [parent_descr]
            elif col=="unit":
                row += [unit]
            elif col=="parent":
                row += [parent]
            elif col=="rev":
                row += [item["ver"]]
            elif col=="drawings":
                rid = item["rid"]
                if rid in self._drawings:
                    l = self._drawings[rid]
                else:
                    l = []
                row += [", ".join(l)]
            elif col=="indented_code":
                row += ["... "*level + item["code"]]
            elif col in ["code", "descr", "iter", "date_from", "date_to"]:
                row += [item[col]]
            elif col.startswith("gval") and col in item:
                row += [item[col]]
            elif col.startswith("'"):
                col = col[1:]
                row += [col]
            elif col == "":
                row += [""]
            else:
                row += ["Unknown col '%s'"%(col)]

        table.append([str(x) for x in row])
        self._seq += 1
        for child_id in item["deps"]:
            child = item["deps"][child_id]
            self._export_as_table_by_template_it(unique, table, columns,
                child_id, level + 1, child["qty"], child["each"],
                child["unit"], child["ref"],
                item["code"], item["descr"],
                maxlevel=maxlevel)

    def _export_as_table_by_template(self, template_name):

        columns = []
        captions = []

        for line in cfg.config()[template_name].get("columns").split("\n"):
            line = line.strip()
            if len(line) == 0:
                continue

            i = line.find(":")
            if i < 0:
                cl = line
                cp = ""
            else:
                cl = line[:i]
                cp = line[i+1:]

            columns.append(cl)
            captions.append(cp)

        if "drawings" in columns and len(self._drawings) == 0:
            d = db.DB()
            fnl = []
            for k, v in self._data.items():
                rid = v["rid"]
                l = d.get_drawings_by_code_id(rid)
                if len(l):
                    self._drawings[rid] = [os.path.basename(x[1]) for x in l]

        sortby=int(cfg.config()[template_name].get("sortby", -1))
        unique=int(cfg.config()[template_name].get("unique", 0))
        maxlevel=int(cfg.config()[template_name].get("maxlevel", -1))
        table = []

        self._seq = 0
        self._did = set()
        self._path = []

        self._export_as_table_by_template_it(unique, table, columns,
            self._rootnode, maxlevel=maxlevel)


        if sortby >= 0:
            table.sort(key=lambda x : x[sortby])

        return table, captions

    def export_as_table_by_template2(self, template_section):
        table, captions = self._export_as_table_by_template(template_section)

        f = io.StringIO()
        writer = csv.writer(f, delimiter="\t",  quoting=csv.QUOTE_MINIMAL)
        writer.writerow(captions)
        for line in table:
            writer.writerow(line)
        return f.getvalue()

    def export_as_file_by_template2(self, nf, template_section):
        table, captions = self._export_as_table_by_template(template_section)

        mode = "UNKNOWN"
        if nf.lower().endswith(".xls"):
            mode = "XLS"
        elif nf.lower().endswith(".csv"):
            mode = "CSV"

        assert(mode in ["XLS", "CSV"])

        if mode == "CSV":
            f = open(nf, "w", encoding='utf-8-sig', newline='')

            quotechar = cfg.config()[template_section].get("quotechar", "DOUBLEQUOTE")
            if quotechar == 'SINGLEQUOTE':
                quotechar = "'"
            else: # 'DOUBLEQUOTE' or other
                quotechar = '"'
            delimiter = cfg.config()[template_section].get("delimiter", "SEMICOLON")
            if delimiter == "COMMA":
                delimiter = ","
            elif delimiter == "TAB":
                delimiter = "\t"
            else: # SEMICOLON or other
                delimiter = ";"

            writer = csv.writer(f, delimiter=delimiter,
                                    quotechar=quotechar,
                                    quoting=csv.QUOTE_ALL)
            writer.writerow(captions)
            for line in table:
                writer.writerow(line)
        elif mode == "XLS":
            wb = xlwt.Workbook()
            ws = wb.add_sheet('BOMBrowser0')
            for c,t in enumerate(captions):
                ws.write(0, c, t)
            for r, line in enumerate(table):
                for c,t in enumerate(line):
                    ws.write(r+1, c, t)
            wb.save(nf)

def test_get_template_list():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple,template_all,no-section"
        },
        "template_simple" :  {"name": "template simple"},
        "template_all" :  {"name": "template all"},
        "no-key" : {"name": "xxx"},
    }

    r = get_template_list()
    found = 0
    for section_name, d in r:
        if section_name == "template_simple":
            found += 1
            assert(d["name"] == "template simple")
        if section_name == "template_all":
            found += 1
            assert(d["name"] == "template all")
        assert(section_name != "no-key")
        assert(section_name != "no-section")
    assert(found == 2)

def _get_test_bom():
    return {
        "0": {
            "code": "0",
            "descr": "0-descr",
            "ver" : "ver-0",
            "unit": "NR",
            "gval1": "0-gval1",
            "deps" : {
                "A" : { "code": "A", "qty": 2,
                            "each": 2, "unit" : "NR", "ref": "A-ref" },
                "B" : { "code": "B", "qty": 3,
                            "each": 1, "unit" : "NR", "ref": "B-ref" }
            }
        },
        "A": {
            "code": "A",
            "descr": "A-descr",
            "ver" : "ver-A",
            "unit": "NR",
            "gval1": "A-gval1",
            "deps" : {
                "C" : { "code": "C", "qty": 1,
                            "each": 1, "unit" : "NR", "ref": "0-ref" }
            }
        },
        "B": {
            "code": "B",
            "descr": "B-descr",
            "ver" : "ver-B",
            "unit": "NR",
            "gval1": "B-gval1",
            "deps" : {
                "C" : { "code": "C", "qty": 1,
                            "each": 1, "unit" : "NR", "ref": "0-ref" }
            }
        },
        "C": {
            "code": "C",
            "descr": "C-descr",
            "ver" : "ver-C",
            "unit": "NR",
            "gval1": "C-gval1",
            "deps" : { }
        }
    }

def test_export_simple():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                code:Code
                descr:Descr
                parent:Parent code
                qty:Q.ty
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("A-descr" in r)
    assert("B-descr" in r)
    assert("0-descr" in r)
    cnt = 0
    for line in r.split("\n"):
        if "A-descr" in line:
            assert("2" in line)
        if "C-descr" in line:
            cnt += 1
            assert("C" in line)
            assert("A" in line or "B" in line)

    assert(cnt == 2)
    assert("\t" in r)

def test_export_unique():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                code:Code
                descr:Descr
                parent:Parent code
                qty:Q.ty
            """,
            "unique": "1"
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("A-descr" in r)
    assert("B-descr" in r)
    assert("0-descr" in r)
    cnt = 0
    for line in r.split("\n"):
        if "C-descr" in line:
            cnt += 1
            assert("C" in line)
            assert("A" in line or "B" in line)

    assert(cnt == 1)

def test_export_max_level():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                code:Code
                descr:Descr
                parent:Parent code
                qty:Q.ty
            """,
            "maxlevel": "2"
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("A-descr" in r)
    assert("B-descr" in r)
    assert("0-descr" in r)
    assert(not "C-descr" in r)

def test_export_csv_comma_doublequote():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                code:Code
                descr:Descr
                parent:Parent code
                qty:Q.ty
            """,
            "delimiter": "COMMA",
            "quotechar": "DOUBLEQUOTE",
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    e.export_as_file_by_template2("/tmp/test_bombrowser.csv", "template_simple")

    r = open("/tmp/test_bombrowser.csv").read()

    assert("," in r)
    assert('"' in r)
    assert("A-descr" in r)
    assert("B-descr" in r)
    assert("0-descr" in r)
    assert("C-descr" in r)

def test_export_csv_semicolon_singlequote():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                code:Code
                descr:Descr
                parent:Parent code
                qty:Q.ty
            """,
            "delimiter": "SEMICOLON",
            "quotechar": "SINGLEQUOTE",
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    e.export_as_file_by_template2("/tmp/test_bombrowser.csv", "template_simple")

    r = open("/tmp/test_bombrowser.csv").read()

    assert(";" in r)
    assert("'" in r)
    assert("A-descr" in r)
    assert("B-descr" in r)
    assert("0-descr" in r)
    assert("C-descr" in r)

def test_export_seq():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                seq:Seq
                code:Code
                descr:Descr
                parent:Parent code
                qty:Q.ty
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("Seq" in r.split("\n")[0])
    assert("Descr" in r.split("\n")[0])

    start = None
    cnt = 0
    for line in r.split("\n")[1:]:
        if len(line.strip()) == 0:
            continue
        fields = line.split("\t")
        if not start is None:
            assert(int(fields[0]) == start + 1)
            cnt += 1
        start = int(fields[0])

    assert(cnt > 0)

def test_export_parent_descr():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                code:Code
                descr:Descr
                parent:Parent code
                parent_descr:Parent descr
                qty:Q.ty
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    for line in r.split("\n"):
        if "A-descr" in line:
            assert("0-descr" in line or "C-descr" in line)

def test_export_static_text():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                seq:Seq
                code:Code
                descr:Descr
                'static-text:Static text
                qty:Q.ty
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    for line in r.split("\n")[1:]:
        if len(line.strip()) == 0:
            continue

        assert("static-text" in line)
        assert( not "'" in line)

def test_export_level():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                descr:Description
                level:Level
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("C-descr" in r)

    for line in r.split("\n")[1:]:
        if len(line.strip()) == 0:
            continue

        if "C-descr" in line:
            assert("2" in line)

def test_export_indented_code():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                descr:Description
                indented_code:Code
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("C-descr" in r)

    for line in r.split("\n")[1:]:
        if len(line.strip()) == 0:
            continue

        if "C-descr" in line:
            assert("... ... C" in line)

def test_export_unknown_column():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                descr:Description
                wrong_code:Code
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("Unknown col" in r)
    assert("'wrong_code'" in r)

def test_export_gval1():
    cfg._cfg = {
        "BOMBROWSER": {
            "templates_list": "template_simple"
        },
        "template_simple" :  {
            "name": "template simple",
            "columns": """
                code:code
                descr:Description
                gval1:GVal1
            """
        },
    }

    bom = _get_test_bom()

    e = Exporter("0", bom)
    r = e.export_as_table_by_template2("template_simple")

    assert("C-descr" in r)
    assert("C-gval1" in r)


if __name__ == "__main__":
    last = 1
    import test_db
    test_db.run_test(sys.argv[last:], sys.modules[__name__])
