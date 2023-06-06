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

import configparser
import os

_cfg = None

def init():

    line = open("bombrowser.ini").readline().strip()
    if line != "# -- BOMBROWSER.ini -- v4":
        raise Exception("Incorrect version of bombrowser.ini\nMinimum v4 required")

    global _cfg
    _cfg = configparser.ConfigParser()
    _cfg.read_file(open("bombrowser.ini"))

    if not os.path.exists("bombrowser-local.ini"):
        return

    line = open("bombrowser-local.ini").readline().strip()
    if line != "# -- BOMBROWSER.ini -- v4":
        raise Exception("Incorrect version of bombrowser-local.ini\nMinimum v4 required")

    cfg2 = configparser.ConfigParser()
    cfg2.read_file(open("bombrowser-local.ini"))

    update_cfg(cfg2)

def reload_config():
    global _cfg
    oldcfg = _cfg
    try:
        init()
    except:
        # in case of any error, rollback to the old configuration
        _cfg = oldcfg
        raise

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
        i = n.rfind("[")
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

def get_bomcolors():
    if not "bomcolors" in config()["BOMBROWSER"]:
        return []

    l = [x.strip() for x in
            config().get("BOMBROWSER", "bomcolors").split("\n")
            if len(x.strip()) > 0
        ]

    ret = []
    for line in l:
        assert(":" in line)
        f = [x.strip() for x in line.split(":")[0].split(",")]
        a = [x.strip() for x in line.split(":")[1].split(",")]
        ret.append((f,a))

    return ret

def get_revlistcolors():
    if not "revlistcolors" in config()["BOMBROWSER"]:
        return []

    l = [x.strip() for x in
            config().get("BOMBROWSER", "revlistcolors").split("\n")
            if len(x.strip()) > 0
        ]

    ret = []
    for line in l:
        assert(":" in line)
        f = [x.strip() for x in line.split(":")[0].split(",")]
        a = [x.strip() for x in line.split(":")[1].split(",")]
        ret.append((f,a))

    return ret

def _check_cfg(cfg):
    ret = []
    check_table = [
        ('BOMBROWSER', (
                ('db', True),
                ('description_force_uppercase', True),
                ('code_force_uppercase', True),
                ('templates_list', True),
                ('importer_list', True),
                ('gvalnames', True),
                ('gavalnames', True),
                ('bomcolors', True),
                ('revlistcolors', True),
                ('scalefont', True),
                ('btnmaxlength', True),
                ('ignore_case_during_search', True),
        )),
        ('FILES_UPLOAD', (
                ('method', True),
                ('simple_destination_dir', True),
                ('regexpmap_case_sensitive', True),
                ('regexpmap_separator', True),
                ('regexpmap_table', True),
                ('default_dirs', True),
        )),
        ('SQLITE',      (
                ('path', True),
                ('ignore_case_during_search', True),
        )),
        ('SQLSERVER',   (('conn', True),),),
        ('ORACLE',      (('conn', True),),),
        ('POSTGRESQL', (
                ('server', True),
                ('database', True),
                ('username', True),
                ('password', True),
        )),
        ('MYSQL', (
                ('server', True),
                ('database', True),
                ('username', True),
                ('password', True),
        )),
        ('REMOTEBBSERVER', (
                ('host', True),
                ('port', True),
                ('username', True),
                ('password', True),
        )),
        ('LOCALBBSERVER', (
                ('db', True),
                ('host', True),
                ('port', True),
                ('verbose', True),
        )),
    ]
    template_check_table = [
        ('name', True),
        ('columns', True),
        ('sortby', False),
        ('maxlevel', False),
        ('unique', False),
        ('quotechar', False),
        ('delimiter', False),
    ]
    import_check_table = [
        ('name', True),
        ('type', True),
        ('map', True),
        ('delimiter', False),
        ('default_unit', False),
        ('ignore_duplicate', False),
        ('skip_first_lines', False),
        ('translate', False),
    ]

    ####

    if not "BOMBROWSER" in cfg.sections():
        return [("MISSING", "Missing 'BOMBROWSER' section")]
    if not "templates_list" in cfg["BOMBROWSER"].keys():
        return [("MISSING", "Missing 'BOMBROWSER.templates_list' parameter")]
    if not "importer_list" in cfg["BOMBROWSER"].keys():
        return [("MISSING", "Missing 'BOMBROWSER.importer_list' parameter")]

    secs = set([s for (s, ps) in check_table])
    for s in cfg["BOMBROWSER"]["templates_list"].split(","):
        secs.add(s)
    for s in cfg["BOMBROWSER"]["importer_list"].split(","):
        secs.add(s)

    diff = set(cfg.sections()).difference(secs)
    if len(diff):
        ret += [("MORE", "Unreferenced sections: %s"%(", ".join(list(diff))))]

    diff = set(secs).difference(cfg.sections())
    if len(diff):
        ret += [("MISSING", "Missing sections: %s"%(", ".join(list(diff))))]

    for (s, ps) in check_table:
        if not s in cfg.sections():
            continue
        for p, m in ps:
            if m and not p in cfg[s].keys():
                ret += [("MISSING", "Missing parameter: %s.%s"%(s, p))]

        diff = set(cfg[s].keys()).difference(set([x[0] for x in ps]))
        if len(diff):
            ret += [("MORE", "Unknown parameter of section %s: %s"%(s,
                ", ".join(list(diff))))]

    for s in cfg["BOMBROWSER"]["templates_list"].split(","):
        if not s in cfg.sections():
            continue
        for p, m in template_check_table:
            if m and not p in cfg[s].keys():
                ret += [("MISSING", "Missing parameter: %s.%s"%(s, p))]
        diff = set(cfg[s].keys()).difference(set([x[0] for x in template_check_table]))
        if len(diff):
            ret += [("MORE", "Unknown parameter of section %s: %s"%(s,
                ", ".join(list(diff))))]

    for s in cfg["BOMBROWSER"]["importer_list"].split(","):
        if not s in cfg.sections():
            continue
        for p, m in import_check_table:
            if m and not p in cfg[s].keys():
                ret += [("MISSING", "Missing parameter: %s.%s"%(s, p))]
        diff = set(cfg[s].keys()).difference(set([x[0] for x in import_check_table]))
        if len(diff):
            ret += [("MORE", "Unknown parameter of section %s: %s"%(s,
                ", ".join(list(diff))))]

    if len(ret) == 0:
        ret = [("OK", "")]

    return ret

def check_cfg():
    init()
    return _check_cfg(config())


def _build_checker():
    cfg = configparser.ConfigParser()
    cfg.read_file(open("bombrowser.ini"))

    template_sections = cfg["BOMBROWSER"]["templates_list"].split(",")
    importer_sections = cfg["BOMBROWSER"]["importer_list"].split(",")
    sections = cfg.sections() 
    for s in template_sections + importer_sections:
        sections.remove(s)

    checker = ""
    checker += """
    check_table = ["""

    sections.remove("BOMBROWSER")
    for sec in ["BOMBROWSER"] + sections:
        for p in cfg[sec].keys():
            checker += """
        (%r, %r, True),"""%(sec, p)
    checker += """
    ]
"""
    print(checker)
    return

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == "--build-checker":
        _build_checker()
    elif len(sys.argv) in [2, 3] and sys.argv[1] == "--check-cfg":
        if len(sys.argv) == 3:
            cfg = configparser.ConfigParser()
            cfg.read_file(open(sys.argv[2]))
        else:
            init()
            cfg = config()
        ret = _check_cfg(cfg)
        if len(ret) == 1 and ret[0][0] == 'OK':
            print("Ok")
        else:
            for l in ret:
                if l[0] == "MORE":
                    print("WARNING: ", l[1])
                else:
                    print("CRITICAL:", l[1])
    else:
        print("Unkown command")
