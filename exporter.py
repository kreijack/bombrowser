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
import configparser

import db

_cfg = configparser.ConfigParser()
_cfg.read_file(open("bombrowser.ini"))

def get_template_list():
    ret = []
    template_list = _cfg.get("BOMBROWSER", "templates_list").split(",")
    for template_section in template_list:
        ret.append(_cfg.get(template_section, "name"))
    return ret

class Exporter:
    def __init__(self, rootnode, data):
        self._data = data
        self._rootnode = rootnode
        self._headers = [
            "Seq", "Level", "Code", "Code",
            "Description", "Unit",
            "Quantity", "Each", "Date from", "Date to"]
        self._add_headers = _cfg.get("BOMBROWSER", "gvalnames").split(",")
        self._headers += self._add_headers
        self._db = db.DB()

    def export_as_bom(self, nf):
        f = open(nf, "w")
        self._export_as_bom(f)
        f.close()

    def _export_as_bom(self, f):
        self._path = []
        self._seq = 0

        f.write("\t".join(self._headers)+"\n")
        self._export_as_bom_it(f, self._rootnode, 0, 0, "N/A", "N/A", "N/A")

    def export_bom_as_string(self):
        f = io.StringIO()
        self._export_as_bom(f)
        return f.getvalue()

    def _export_as_bom_it(self, f, node, level, seq, qty, each, unit):
        item = self._data[node]
        items = [ item["gval%d"%(i+1)] for i in range(len(self._add_headers))]

        f.write("\t".join(map(str, [
            str(self._seq), str(level), item["code"], '"'+"... "*level + item["code"]+'"',
            item["descr"], unit,
            str(qty), str(each),
            *items,
        ])))
        f.write("\n")
        self._seq += 1
        for child_id in item["deps"]:
            child = item["deps"][child_id]
            self._export_as_bom_it(f, child_id, level + 1, seq, child["qty"],
                                child["each"], child["unit"])
            seq += 1

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
                parent_descr=""):

        if unique:
            if key in self._did:
                return
            self._did.add(key)

        row = []
        item = self._data[key]
        for col in columns:
            if col=="seq":
                row += [str(self._seq)]
            elif col=="level":
                row += [str(level)]
            elif col=="qty":
                row += [str(qty)]
            elif col=="each":
                row += [str(each)]
            elif col=="ref":
                row += [ref]
            elif col=="parent_descr":
                row += [parent_descr]
            elif col=="unit":
                row += [unit]
            elif col=="parent":
                row += [parent]
            elif col=="unit":
                row += [unit]
            elif col=="rev":
                row += [item["ver"]]
            elif col=="drawings":
                row += ["TBD"]
            elif col=="indented_code":
                row += ["... "*level + item["code"]]
            elif col in ["code", "descr", "iter", "date_from", "date_to"]:
                row += [str(item[col])]
            elif col.startswith("gval"):
                row += [item[col]]
            elif col.startswith('"'):
                col = col[1:]
                if col.endswith('"'):
                    col = col[:-1]
                row += [col]
            elif col == "":
                row += [""]
            else:
                row += ["Unknown col '%s'"%(col)]

        table += [row]
        self._seq += 1
        for child_id in item["deps"]:
            child = item["deps"][child_id]
            self._export_as_table_by_template_it(unique, table, columns,
                child_id, level + 1, child["qty"], child["each"],
                child["unit"], child["ref"],
                item["code"], item["descr"])


    def export_as_table_by_template(self, template_name):
        template_list = _cfg.get("BOMBROWSER", "templates_list").split(",")
        for template_section in template_list:
            if _cfg.get(template_section, "name") == template_name:
                break
        else:
            # TBD show an error
            assert(False)

        sortby=int(_cfg[template_section].get("sortby", -1))
        columns=_cfg[template_section].get("columns").split(",")
        captions=_cfg[template_section].get("captions").split(",")
        unique=int(_cfg[template_section].get("unique", 0))
        table = []

        self._seq = 0
        self._did = set()
        self._export_as_table_by_template_it(unique, table, columns, self._rootnode)

        if sortby >= 0:
            table.sort(key=lambda x : x[sortby])


        f = io.StringIO()
        f.write("\t".join(captions)+"\n")
        for line in table:
            f.write("\t".join(line)+"\n")

        return f.getvalue()

