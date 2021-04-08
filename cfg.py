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
import utils

_cfg = None

def init():
    global _cfg
    _cfg = configparser.ConfigParser()
    _cfg.read_file(open("bombrowser.ini"))

def config():
    return _cfg

def get_gvalnames():
    l = utils.split_with_escape(
        config().get("BOMBROWSER", "gvalnames"),
        delimiter=',', quote='"')
    ret = []
    for n in l:
        i = n.find("[")
        if i < 0:
            ret.append(n.strip())
        else:
            assert(len(n[:i].strip()))
            ret.append(n[:i].strip())

    return ret


def get_gvalnames_type(name):
    l = utils.split_with_escape(
        config().get("BOMBROWSER", "gvalnames"),
        delimiter=',', quote='"')
    ret = []
    for n in l:
        i = n.find("[")
        if i < 0:
            k = n
        else:
            k = n[:i]

        if k != name:
            continue

        if i < 0:
            return ""

        j = n.find("]")
        return n[i+1:j]

    return ""

def update_cfg(data):
    for key1 in data:
        row1 = data[key1]
        for key2 in row1:
            if not key1 in _cfg:
                _cfg[key1] = dict()
            _cfg[key1][key2] =  row1[key2]
