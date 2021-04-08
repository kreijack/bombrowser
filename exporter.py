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

import db
import cfg
import utils

def get_template_list():
    ret = []
    template_list = utils.split_with_escape(
                        cfg.config().get("BOMBROWSER", "templates_list"),
                        delimiter=',', quote='"')
    for template_section in template_list:
        if not cfg.config().has_section(template_section):
            continue
        if not "name" in cfg.config()[template_section]:
            continue
        ret.append((template_section, cfg.config().get(template_section, "name")))
    return ret

class Exporter:
    def __init__(self, rootnode, data):
        self._data = data
        self._rootnode = rootnode
        self._headers = [
            "Seq", "Level", "Code", "Code",
            "Description", "Unit",
            "Quantity", "Each", "Date from", "Date to"]
        self._add_headers = cfg.get_gvalnames()
        self._headers += self._add_headers
        self._db = db.DB()

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
                row += ["TBD"]
            elif col=="indented_code":
                row += ["... "*level + item["code"]]
            elif col in ["code", "descr", "iter", "date_from", "date_to"]:
                row += [item[col]]
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

        columns = utils.split_with_escape(
                        cfg.config()[template_name].get("columns"),
                        delimiter=',', quote='"')
        captions = utils.split_with_escape(
                        cfg.config()[template_name].get("captions"),
                        delimiter=',', quote='"')
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
