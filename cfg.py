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

_cfg = configparser.ConfigParser()
_cfg.read_file(open("bombrowser.ini"))

def config():
    return _cfg

def update_cfg(data):
    for key1 in data:
        row1 = data[key1]
        for key2 in row1:
            if not key1 in _cfg:
                _cfg[key1] = dict()
            _cfg[key1][key2] =  row1[key2]
