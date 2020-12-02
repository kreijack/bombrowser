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

import sys
import os
import json
import io

import db

class Exporter:
    def __init__(self, rootnode, data):
        self._data = data
        self._rootnode = rootnode

        self._db = db.DB()

    def export_as_bom(self, nf):
        f = open(nf, "w")
        self._export_as_bom(f)
        f.close()

    def _export_as_bom(self, f):
        self._path = []
        self._seq = 0
        f.write("\t".join([
            "Seq", "Level", "Code", "Code",
            "Description", "Unit",
            "Quantity", "Each", "Date from", "Date to",
            "Supplier", "P/N",
            "Manufacturer", "P/N",
            "Manufacturer", "P/N"
        ])+"\n")
        self._export_as_bom_it(f, self._rootnode, 0, 0, "N/A", "N/A", "N/A")

    def export_bom_as_string(self):
        f = io.StringIO()
        self._export_as_bom(f)
        return f.getvalue()

    def _export_as_bom_it(self, f, node, level, seq, qty, each, unit):
        item = self._data[node]
        f.write("\t".join(map(str, [
            str(self._seq), str(level), item["code"], '"'+"    "*level + item["code"]+'"',
            item["descr"], unit,
            str(qty), str(each),
            item["date_from"], item["date_to"],
            item["for1name"], item["for1cod"],
            item["prod1name"], item["prod1cod"],
            item["prod2name"], item["prod2cod"] ,
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
