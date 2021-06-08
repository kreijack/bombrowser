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

import configparser
import utils, os

_cfg = None

def init():

    line = open("bombrowser.ini").readline().strip()
    if line != "# -- BOMBROWSER.ini -- v3":
        raise Exception("Incorrect version of bombrowser.ini\nMinimum v3 required")

    global _cfg
    _cfg = configparser.ConfigParser()
    _cfg.read_file(open("bombrowser.ini"))

    if not os.path.exists("bombrowser-local.ini"):
        return

    line = open("bombrowser-local.ini").readline().strip()
    if line != "# -- BOMBROWSER.ini -- v3":
        raise Exception("Incorrect version of bombrowser-local.ini\nMinimum v3 required")

    cfg2 = configparser.ConfigParser()
    cfg2.read_file(open("bombrowser-local.ini"))

    update_cfg(cfg2)

def config():
    return _cfg

def get_gvalnames2():
    l = [x.strip() for x in
            config().get("BOMBROWSER", "gvalnames").split("\n")
            if len(x.strip()) > 0
        ]
    ret = []
    alreadyinserted = set()
    c = 0
    for n in l:
        j = n.find(":")
        gvalname = n[:j]

        assert(gvalname.startswith("gval"))
        assert(not gvalname in alreadyinserted)
        alreadyinserted.add(gvalname)
        idx = int(gvalname[4:])

        n = n[j+1:]
        if len(n) == 0:
            n = gvalname
        i = n.find("[")
        if i < 0:
            ret.append((c, idx, gvalname, n, "free"))
            c += 1
            continue

        j = n.find("]")
        assert(j >= 0)
        v = n[i+1:j].strip()
        ret.append((c, idx, gvalname, n[:i], v))
        c += 1

    return ret

def get_gavalnames():
    l = [x.strip() for x in
            config().get("BOMBROWSER", "gavalnames").split("\n")
            if len(x.strip()) > 0
        ]
    ret = []
    alreadyinserted = set()
    c = 0
    for n in l:
        j = n.find(":")
        gvalname = n[:j]

        assert(gvalname.startswith("gaval"))
        assert(not gvalname in alreadyinserted)
        alreadyinserted.add(gvalname)
        idx = int(gvalname[5:])

        n = n[j+1:]
        if len(n) == 0:
            n = gvalname
        i = n.find("[")
        if i < 0:
            ret.append((c, idx, gvalname, n, "free"))
            c += 1
            continue

        j = n.find("]")
        assert(j >= 0)
        v = n[i+1:j].strip()
        ret.append((c, idx, gvalname, n[:i], v))
        c += 1

    return ret

def update_cfg(data):
    for key1 in data:
        row1 = data[key1]
        for key2 in row1:
            if not key1 in _cfg:
                _cfg[key1] = dict()
            _cfg[key1][key2] =  row1[key2]
