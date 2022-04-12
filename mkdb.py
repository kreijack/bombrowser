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

import db
import sqlite3
import os
import datetime
import cfg


board_count = 40
board_components_count_max = 200

mech_number_of_components = 1000

mech_num_assemblies = 200
mech_assy_components_count_max = 50
mech_num_level = 10

top_code_count = 120
top_code_components_count_max = 12

spare_part_count = 120
spare_part_components_count_max = 12

prototype_count = 200
changes_count = 200

cfg.init()

date0 = "2000-01-01"

class MyRandom:
    def __init__(self, seed = 3):
        self._seed = seed
    def get(self):
        # glibc (used by GCC) -- from wikipedia https://en.wikipedia.org/wiki/Linear_congruential_generator
        n = (self._seed *1103515245 +  12345) % (2<<31)
        self._seed = n
        return n

rnd = MyRandom()

dbname="database.sqlite"

def insert_code(c, descr, code, ver='0', iter_=0, default_unit='NR',
                gval1='', gval2='', date=None, date_to=None):

            if date is None:
                date = date0
            if date_to is None:
                date_to = db.days_to_iso(db.end_of_the_world)

            c.execute("INSERT INTO items(code) VALUES (?)", (
                code,)
            )
            c.execute("SELECT MAX(id) FROM items")
            mid = c.fetchone()[0]

            c.execute("""INSERT INTO item_revisions(
                descr, code_id, ver,
                iter, default_unit,
                gval1, gval2,
                date_from, date_from_days,
                date_to, date_to_days) VALUES (
                ?, ?, ?,
                ?, ?,
                ?, ?,
                ?, ?,
                ?, ?)""",
                (descr, mid, ver, iter_, default_unit, gval1, gval2,
                 date, db.iso_to_days(date),
                 date_to, db.iso_to_days(date_to))
            )

# create screws
def insert_screws(c):
    cnt=1
    for l in [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 15, 30, 35]:
        for d in [2, 3, 4, 5, 6, 8, 10, 12]:

            insert_code(c, "SCREW M%dX%d"%(d, l), "710%03d"%(cnt), 0,
                    0, "NR", "M%dX%d"%(d, l), "SCREWS SUPPLIER")
            cnt += 1

# create washer
def insert_washer(c):
    cnt=1
    for d in [2, 3, 4, 5, 6, 8, 10, 12]:
        insert_code(c, "WASHER D%d"%(d), "720%03d"%(cnt), 0,
                0, "NR", "W D%d"%(d, ), "WASHERS SUPPLIER")
        cnt += 1

# create washer
def insert_elastic_washer(c):
    cnt=1
    for d in [2, 3, 4, 5, 6, 8, 10, 12]:
        insert_code(c, "ELASTIC WASHER D%d"%(d, ), "730%03d"%(cnt), 0,
                0, "NR", "EW D%d"%(d, ), "WASHERS SUPPLIER")
        cnt += 1

# create resistor
def insert_resistor(c):
    # from https://www.eeweb.com/tools/resistor-tables/
    # 0.1%, 0.25%, and 0.5% Resistor Table (E192)
    table="""
100 	101 	102 	104 	105 	106 	107 	109 	110 	111 	113 	114
115 	117 	118 	120 	121 	123 	124 	126 	127 	129 	130 	132
133 	135 	137 	138 	140 	142 	143 	145 	147 	149 	150 	152
154 	156 	158 	160 	162 	164 	165 	167 	169 	172 	174 	176
178 	180 	182 	184 	187 	189 	191 	193 	196 	198 	200 	203
205 	208 	210 	213 	215 	218 	221 	223 	226 	229 	232 	234
237 	240 	243 	246 	249 	252 	255 	258 	261 	264 	267 	271
274 	277 	280 	284 	287 	291 	294 	298 	301 	305 	309 	312
316 	320 	324 	328 	332 	336 	340 	344 	348 	352 	357 	361
365 	370 	374 	379 	383 	388 	392 	397 	402 	407 	412 	417
422 	427 	432 	437 	442 	448 	453 	459 	464 	470 	475 	481
487 	493 	499 	505 	511 	517 	523 	530 	536 	542 	549 	556
562 	569 	576 	583 	590 	597 	604 	612 	619 	626 	634 	642
649 	657 	665 	673 	681 	690 	698 	706 	715 	723 	732 	741
750 	759 	768 	777 	787 	796 	806 	816 	825 	835 	845 	856
866 	876 	887 	898 	909 	920 	931 	942 	953 	965 	976 	988
"""
    rows = table.split("\n")
    values = []
    for row in rows:
        row = row.strip()
        if len(row) == 0:
            continue
        values.extend(map(float, row.split("\t")))

    cnt = 1
    for r in values:
        for (k, suffix) in [(100, ""), (10, ""), (1, ""),
                    (100, "k"), (10, "k"), (1, "k"), (100, "M")]:
            insert_code(c,
                    "RESISTOR %.2f%s"%(r / k, suffix), "51%04d"%(cnt), 0,
                    0, "NR", "R%.2f%s"%(r / k, suffix), "RESISTORS SUPPLIER")
            cnt += 1


def insert_capacitor(c):
# from https://www.rfcafe.com/references/electrical/capacitor-values.htm
#pF 	pF 	pF 	    pF 	    µF 	    µF 	    µF 	    µF 	    µF 	µF  	µF
    table="""
1.0 	10 	100 	1000 	0.01 	0.1 	1.0 	10 	100 	1000 	10,000
1.1 	11 	110 	1100
1.2 	12 	120 	1200
1.3 	13 	130 	1300
1.5 	15 	150 	1500 	0.015 	0.15 	1.5 	15 	150 	1500
1.6 	16 	160 	1600
1.8 	18 	180 	1800
2.0 	20 	200 	2000
2.2 	22 	220 	2200 	0.022 	0.22 	2.2 	22 	220 	2200
2.4 	24 	240 	2400
2.7 	27 	270 	2700
3.0 	30 	300 	3000
3.3 	33 	330 	3300 	0.033 	0.33 	3.3 	33 	330 	3300
3.6 	36 	360 	3600
3.9 	39 	390 	3900
4.3 	43 	430 	4300
4.7 	47 	470 	4700 	0.047 	0.47 	4.7 	47 	470 	4700
5.1 	51 	510 	5100
5.6 	56 	560 	5600
6.2 	62 	620 	6200
6.8 	68 	680 	6800 	0.068 	0.68 	6.8 	68 	680 	6800
7.5 	75 	750 	7500
8.2 	82 	820 	8200
9.1 	91 	910 	9100"""

    cnt = 1
    for row in table.split("\n"):
        row = row.strip()
        if len(row) == 0:
            continue
        col = 0
        for v in row.split("\t"):
            if col > 3:
                suffix = "uF"
            else:
                suffix = "pf"
            v = v.strip()

            insert_code(c, "CAPACITOR %s%s"%(v, suffix), "520%03d"%(cnt), 0,
                    0, "NR", "C%s%s"%(v, suffix), "CAPACITORS SUPPLIER"
            )
            cnt += 1
            col += 1

def insert_microprocessor(c):
# from https://en.wikipedia.org/wiki/Microprocessor_chronology
    table = """
1971 	4004 	Intel 	740 kHz 	4 	10 μm 	1 	2,250 	pMOS 	[1]
1972 	PPS-25 	Fairchild 	400 kHz 	4 	  	2 		pMOS 	[2][a]
1972 	μPD700 	NEC 	  	4 	  	1 			[3]
1972 	8008 	Intel 	500 kHz 	8 	10 μm 	1 	3,500 	pMOS
1972 	PPS-4 	Rockwell 	200 kHz 	4 	  	1 		pMOS 	[4][5]
1973 	μCOM-4 	NEC 	2 MHz 	4 	7.5 μm 	1 	2,500 	NMOS 	[6][7][3][1]
1973 	TLCS-12 	Toshiba 	1 MHz 	12 	6 μm 	1 	2,800 silicon gates 	pMOS 	[8][9][1]
1973 	Mini-D 	Burroughs 	1 MHz 	8 	  	1 		pMOS 	[10]
1974 	IMP-8 	National 	715 kHz 	8 	  	3 		pMOS 	[8]
1974 	8080 	Intel 	2 MHz 	8 	6 μm 	1 	6,000 	NMOS
1974 	μCOM-8 	NEC 	2 MHz 	8 	  	1 		NMOS 	[3][1]
1974 	5065 	Mostek 	1.4 MHz 	8 	  	1 		pMOS 	[11]
1974 	μCOM-16 	NEC 	2 MHz 	16 	  	2 		NMOS 	[3][1]
1974 	IMP-4 	National 	500 kHz 	4 	  	3 		pMOS 	[8]
1974 	4040 	Intel 	740 kHz 	4 	10 μm 	1 	3,000 	pMOS
1974 	6800 	Motorola 	1 MHz 	8 	- 	1 	4,100 	NMOS 	[8]
1974 	TMS 1000 	Texas Instruments 	400 kHz 	4 	8 μm 	1 	8,000
1974 	PACE 	National 	  	16 	  	1 		pMOS 	[12][13]
1974 	ISP-8A/500 (SC/MP) 	National 	1 MHz 	8 	  	1 		pMOS
1975 	6100 	Intersil 	4 MHz 	12 	- 	1 	4,000 	CMOS 	[14][15]
1975 	TLCS-12A 	Toshiba 	1.2 MHz 	12 	- 	1 		pMOS 	[1]
1975 	2650 	Signetics 	1.2 MHz 	8 	  	1 		NMOS 	[8]
1975 	PPS-8 	Rockwell 	256 kHz 	8 	  	1 		pMOS 	[8]
1975 	F-8 	Fairchild 	2 MHz 	8 	  	1 		NMOS 	[8]
1975 	CDP 1801 	RCA 	2 MHz 	8 	5 μm 	2 	5,000 	CMOS 	[16][17]
1975 	6502 	MOS Technology 	1 MHz 	8 	- 	1 	3,510 	NMOS (dynamic)
1975 	IMP-16 	National 	715 kHz 	16 	  	5 		pMOS 	[18][1][19]
1975 	PFL-16A (MN 1610) 	Panafacom 	2 MHz 	16 	- 	1 		NMOS 	[1]
1975 	BPC 	Hewlett Packard 	10 MHz 	16 	- 	1 	6,000 (+ ROM) 	NMOS 	[20][21]
1975 	MCP-1600 	Western Digital 	3.3 MHz 	16 	- 	3 		NMOS
1975 	CP1600 	General Instrument 	3.3 MHz 	16 	  	1 		NMOS 	[12][22][23][1]
1976 	CDP 1802 	RCA 	6.4 MHz 	8 	  	1 		CMOS 	[24][25]
1976 	Z-80 	Zilog 	2.5 MHz 	8 	4 μm 	1 	8,500 	NMOS
1976 	TMS9900 	Texas Instruments 	3.3 MHz 	16 	- 	1 	8,000
1976 	8x300 	Signetics 	8 MHz 	8 	  	1 		Bipolar 	[26][27]
1977 	Bellmac-8 (WE212) 	Bell Labs 	2.0 MHz 	8 	5 μm 	1 	7,000 	CMOS
1977 	8085 	Intel 	3.0 MHz 	8 	3 μm 	1 	6,500
1977 	MC14500B 	Motorola 	1.0 MHz 	1 		1 		CMOS
1978 	6809 	Motorola 	1 MHz 	8 	5 μm 	1 	9,000
1978 	8086 	Intel 	5 MHz 	16 	3 μm 	1 	29,000
1978 	6801 	Motorola 	- 	8 	5 μm 	1 	35,000
1979 	Z8000 	Zilog 	- 	16 	- 	1 	17,500
1979 	8088 	Intel 	5 MHz 	8/16[b] 	3 μm 	1 	29,000 	NMOS (HMOS)
1979 	68000 	Motorola 	8 MHz
"""

    cnt = 1
    for row in table.split("\n"):
        row = row.strip()
        if len(row) == 0:
            continue

        (ucode, manufacturer, clock) = row.split("\t")[1:4]

        insert_code(c,
                "MICROPROCESSOR %s %s %s"%(ucode, manufacturer, clock),
                "530%03d"%(cnt), 0,
                0, "NR", "%s AT %s"%(ucode, clock), manufacturer
        )
        cnt += 1

def get_max_by_code(c, pattern):
    c.execute("""SELECT MAX(id)
                 FROM items
                 WHERE code LIKE ?""",
                 (pattern,))
    return c.fetchone()[0]

def get_min_by_code(c, pattern):
    c.execute("""SELECT MIN(id)
                 FROM items
                 WHERE code LIKE ?""",
                 (pattern,))
    return c.fetchone()[0]


def insert_board(c):

    min_id = get_min_by_code(c, '5%')
    max_id = get_max_by_code(c, '5%')

    # TODO build revision

    # make 15 boards
    for cnt in range(1, board_count):

        ncomponents = rnd.get() % board_components_count_max + \
            board_components_count_max / 10

        code = "610%03d"%(cnt)

        fn1 = "documents/boards/%s_(wl)_rev0.txt"%(code)
        open(fn1, "w").write("Type: board drawing\nCode: %s\nNr components: %d\n"%(
            code, ncomponents))

        insert_code(c,
                "BOARD %d"%(cnt), "610%03d"%(cnt), 0,
                0, "NR", "BOARD %d"%(cnt), "BOARDS MANUFACTURER %d"%(cnt %3, )
        )

        c.execute("SELECT MAX(id) FROM item_revisions")
        board_id = c.fetchone()[0]

        c.execute("""INSERT INTO drawings(
                code, revision_id, filename, fullpath
            ) VALUES ( ?, ?, ?, ? )
                """, (code, board_id, os.path.basename(fn1), os.path.abspath(fn1))
        )

        # create the board assy
        components_table = []

        #resistor
        did = set()
        for i in range(rnd.get() % 120 + 5):
            while True:
                cid = rnd.get() % (max_id - min_id) + min_id
                if not cid in did:
                    break
            did.add(cid)

            ts = datetime.date.fromisoformat(date0).toordinal()

            c.execute("""INSERT INTO assemblies (
                unit,
                child_id, revision_id,
                qty,
                each,
                ref) VALUES (
                ?,
                ?, ?,
                ?,
                ?,
                ? )""", (
                    "NR",
                    cid, board_id,
                    (i * cnt % 10) + 1,
                    0, '//')
            )

def insert_mechanical_components(c):
    cnt=1
    for d in range(mech_number_of_components):
        code = "810%03d"%(cnt)
        insert_code(c,
                "MECHANICAL COMPONENT NR.%d"%(d, ), "810%03d"%(cnt), 0,
                0, "NR", "", "MECHANICAL SUPPLIER %d"%(d % 4,)
        )

        c.execute("SELECT MAX(id) FROM item_revisions")
        mech_id = c.fetchone()[0]

        fn1 = "documents/drawings/%s_(drw)_rev0.txt"%(code)
        open(fn1, "w").write("Type: mechanical drawing\nCode:%s\n"%(
            code, ))
        c.execute("""INSERT INTO drawings(
                code, revision_id, filename, fullpath
            ) VALUES ( ?, ?, ?, ? )
                """, (code, mech_id, os.path.basename(fn1), os.path.abspath(fn1))
        )
        cnt += 1

def insert_mechanical_assemblies(c):

    boards_min_id = get_min_by_code(c, '7%')

    # TODO build revision

    # make 120 assemblies
    for cnt in range(mech_num_assemblies):

        if (cnt % (mech_num_assemblies / mech_num_level)) == 0:
            old_mech_max_id = get_max_by_code(c, '8%')

        # each components between [boards_min_id, old_mech_max_id] are a
        # valid child

        ncomponents = rnd.get() % mech_assy_components_count_max + \
            mech_assy_components_count_max // 10

        code = "820%03d"%(cnt)

        fn1 = "documents/drawings/%s_(drw)_rev0.txt"%(code)
        open(fn1, "w").write("Type: mechanical drawing\nCode: %s\nNr components: %d\n"%(
            code, ncomponents))
        fn2 = "documents/assembling-procedures/%s_(asm)_rev0.txt"%(code)
        open(fn2, "w").write("Type: assembling procedure\nCode: %s\nNr components: %d\n"%(
            code, ncomponents))

        insert_code(c,
                "MECHANICAL ASSEMBLIES %d - LEVEL %d"%(cnt,
                    cnt/(mech_num_assemblies / mech_num_level) + 1), code, 0,
                0, "NR", "", "INTERNAL SUPPLIER"
        )

        c.execute("SELECT MAX(id) FROM item_revisions")
        mech_id = c.fetchone()[0]

        c.execute("""INSERT INTO drawings(
                code, revision_id, filename, fullpath
            ) VALUES ( ?, ?, ?, ? )
                """, (code, mech_id, os.path.basename(fn1), os.path.abspath(fn1))
        )
        c.execute("""INSERT INTO drawings(
                code, revision_id, filename, fullpath
            ) VALUES ( ?, ?, ?, ? )
                """, (code, mech_id, os.path.basename(fn2), os.path.abspath(fn2))
        )


        #up to 127 sub assemblies
        did =set()
        for i in range(ncomponents):
            while True:
                cid = (rnd.get() %
                    (old_mech_max_id - boards_min_id) + boards_min_id)
                if not cid in did:
                    break
            did.add(cid)

            ts = datetime.date.fromisoformat(date0).toordinal()

            c.execute("""INSERT INTO assemblies (
                unit,
                child_id, revision_id,
                qty,
                each,
                ref) VALUES (
                ?,
                ?, ?,
                ?,
                ?,
                ? )""", (
                    "NR",
                    cid, mech_id,
                    (i * cnt % 10) + 1,
                    1,
                    '//')
            )

def insert_top_codes(c):

    mech_min = get_min_by_code(c,'82%')
    mech_max = get_max_by_code(c,'82%')

    # TODO build revision

    for cnt in range(top_code_count):

        ncomponents = rnd.get() % top_code_components_count_max + \
            top_code_components_count_max // 10

        code = "100%03d"%(cnt)

        fn1 = "documents/packaging-procedure/%s_rev0.txt"%(code)
        open(fn1, "w").write("Type: packaging procedure\nCode: %s\nNr components: %d\n"%(
            code, ncomponents))


        insert_code(c,
                "TOP ASSEMBLY %d"%(cnt, ), code, 0,
                0, "NR", "", "INTERNAL SUPPLIER"
        )

        c.execute("SELECT MAX(id) FROM item_revisions")
        top_id = c.fetchone()[0]

        c.execute("""INSERT INTO drawings(
                code, revision_id, filename, fullpath
            ) VALUES ( ?, ?, ?, ? )
                """, (code, top_id, os.path.basename(fn1), os.path.abspath(fn1))
        )

        #up to 127 sub assemblies
        did = set()
        for i in range(ncomponents):
            while True:
                cid = (rnd.get() %
                    (mech_max - mech_min + 1) + mech_min)
                if not cid in did:
                    break
            did.add(cid)

            ts = datetime.date.fromisoformat(date0).toordinal()

            c.execute("""INSERT INTO assemblies (
                unit,
                child_id, revision_id,
                qty,
                each,
                ref) VALUES (
                ?,
                ?, ?,
                ?,
                ?,
                ? )""", (
                    "NR",
                    cid, top_id,
                    (i * cnt % 10) + 1,
                    1,
                    '//')
            )

def insert_spare_parts(c):

    mech_min = get_min_by_code(c,'6%')
    mech_max = get_max_by_code(c,'81%')
    # TODO build revision

    # make 120 top code
    for cnt in range(spare_part_count):


        ncomponents = rnd.get() % spare_part_components_count_max + \
            spare_part_components_count_max // 10

        code = "101%03d"%(cnt)

        fn1 = "documents/packaging-procedure/%s_packaging.txt"%(code)
        open(fn1, "w").write("Type: packaging procedure\nCode: %s\nNr components: %d\n"%(
            code, ncomponents))


        insert_code(c,
                "SPARE PART %d"%(cnt, ), code, 0,
                0, "NR", "", "INTERNAL SUPPLIER"
        )

        c.execute("SELECT MAX(id) FROM item_revisions")
        top_id = c.fetchone()[0]

        c.execute("""INSERT INTO drawings(
                code, revision_id, filename, fullpath
            ) VALUES ( ?, ?, ?, ? )
                """, (code, top_id, os.path.basename(fn1), os.path.abspath(fn1))
        )

        ts = datetime.date.fromisoformat(date0).toordinal()
        did = set()
        for i in range(ncomponents):
            while True:
                cid = (rnd.get() %
                    (mech_max - mech_min + 1) + mech_min)
                if not cid in did:
                    break
            did.add(cid)

            c.execute("""INSERT INTO assemblies (
                unit,
                child_id, revision_id,
                qty,
                each,
                ref) VALUES (
                ?,
                ?, ?,
                ?,
                ?,
                ? )""", (
                    "NR",
                    cid, top_id,
                    (i * cnt % 10) + 1,
                    1,
                    '//')
            )

def revise_code(c, old_rid, new_date=None):

        global date0

        c.execute("""
            SELECT code_id, MAX(iter)
            FROM item_revisions
            WHERE code_id = (
                SELECT code_id
                FROM item_revisions
                WHERE id = ?
            )
            GROUP BY code_id
            """, (old_rid, ))
        (code_id, old_iter) = c.fetchone()

        c.execute("""
            SELECT id, date_from_days, ver
            FROM item_revisions
            WHERE code_id = ?
            AND iter = ?
            """, (code_id, old_iter))

        (latest_rid, old_date_from_days, rev) = c.fetchone()

        #print("Code, ver, iter=", code, ver, iter_)
        if rev == '0':
            rev = 'A'
        else:
            rev = chr(ord(rev)+1)

        if new_date is None:
            new_date_from_days = db.iso_to_days(date0)
        else:
            new_date_from_days = new_date
        new_date_from = db.days_to_iso(new_date_from_days)

        if new_date_from_days == db.prototype_date:
            new_iter = db.prototype_iter
        else:
            new_iter = old_iter + 1

        c.execute("""
                INSERT INTO item_revisions(
                    code_id,
                    date_from,
                    date_from_days,
                    date_to,
                    ver,
                    iter,
                    note,
                    descr,
                    default_unit,
                    gval1, gval2, gval3, gval4, gval5, gval6, gval7, gval8
                ) SELECT
                    code_id,
                    ?,
                    ?,
                    '',
                    ?,
                    ?,
                    note,
                    descr,
                    default_unit,
                    gval1, gval2, gval3, gval4, gval5, gval6, gval7, gval8
                FROM item_revisions
                WHERE id = ?
            """, (new_date_from, new_date_from_days, rev, new_iter, old_rid))

        old_date_to_days = new_date_from_days-1
        old_date_to = db.days_to_iso(old_date_to_days)
        c.execute("""
            UPDATE item_revisions
            SET date_to=?, date_to_days=?
            WHERE id= ?
        """, (old_date_to, old_date_to_days, latest_rid))

        c.execute("""SELECT MAX(id) FROM item_revisions""")
        new_rid = c.fetchone()[0]

        return (new_rid, rev)


def revise_assembly(c, old_rid, new_date = None):

    (new_rid, rev) = revise_code(c, old_rid, new_date)

    c.execute("""
        INSERT INTO assemblies(
                    unit, child_id,
                    revision_id,
                    qty, each, ref
        ) SELECT unit, child_id,
                    ?,
                    qty, each, ref
        FROM assemblies
        WHERE revision_id=?
    """, (new_rid, old_rid))

    # TODO: make some changes to the assembly
    return (new_rid, rev)



# make some changes
def make_changes(c):
    global date0

    min_id = get_min_by_code(c, '6%')
    max_id = get_max_by_code(c, '82%')

    print("Make few changes")

    for cnt in range(changes_count):

        date0 = db.increase_date(date0, 10)

        code_id = rnd.get() % (max_id - min_id + 1) + min_id

        # fetch the latest code revision
        c.execute("""SELECT MAX(iter)
                     FROM item_revisions
                     WHERE code_id=?""", (code_id,))
        (iter_,) = c.fetchone()
        c.execute("""SELECT id
                     FROM item_revisions
                     WHERE code_id=?
                       AND iter=?""", (code_id, iter_))
        (rev_id,) = c.fetchone()
        c.execute("""SELECT code
                     FROM items
                     WHERE id=?""", (code_id,))
        (code,) = c.fetchone()

        #print("%s/%s) Updating code '%s', rid=%d"%(cnt, 200, code, rev_id))

        if code.startswith("81"):
            # no assembly
            new_id, new_rev = revise_code(c, rev_id)
            fn1 = "documents/drawings/%s_(drw)_rev%s.txt"%(code, new_rev)
            open(fn1, "w").write("Type: mechanical drawing\nCode:%s\n"%(
                code, ))
            c.execute("""INSERT INTO drawings(
                    code, revision_id, filename, fullpath
                ) VALUES ( ?, ?, ?, ? )
                    """, (code, new_id, os.path.basename(fn1), os.path.abspath(fn1))
            )

        elif code.startswith("82"):
                # assembly
                new_id, new_rev = revise_assembly(c, rev_id)
                fn1 = "documents/drawings/%s_(drw)_rev%s.txt"%(code, new_rev)
                open(fn1, "w").write("Type: mechanical drawing\nCode:%s\n"%(
                    code, ))
                c.execute("""INSERT INTO drawings(
                        code, revision_id, filename, fullpath
                    ) VALUES ( ?, ?, ?, ? )
                        """, (code, new_id, os.path.basename(fn1), os.path.abspath(fn1))
                )
                fn2 = "documents/assembling-procedures/%s_(ass)_rev%s.txt"%(code, new_rev)
                open(fn2, "w").write("Type: assembling procedure\nCode:%s\n"%(
                    code, ))
                c.execute("""INSERT INTO drawings(
                        code, revision_id, filename, fullpath
                    ) VALUES ( ?, ?, ?, ? )
                        """, (code, new_id, os.path.basename(fn2), os.path.abspath(fn2))
                )

        elif code.startswith("6"):
                new_id, new_rev = revise_assembly(c, rev_id)
                fn1 = "documents/boards/%s_(el)_rev%s.txt"%(code, new_rev)
                open(fn1, "w").write("Type: board drawing\nCode: %s\n"%(
                    code,))
                c.execute("""INSERT INTO drawings(
                        code, revision_id, filename, fullpath
                    ) VALUES ( ?, ?, ?, ? )
                        """, (code, new_id, os.path.basename(fn1), os.path.abspath(fn1))
                )


        elif code.startswith("1"):
            print("WARNING: code ", code, " is ignore")
            continue
            # topcode
            # update the packaging procedure
            # update the assembly
        else:
            # ??
            print("Code=", code)
            assert(False)


        #parents = update_assemblies_for_new_code(c, the_id, new_id)
        #print("parents=",len(parents))
        #rec_update_assemblies(c, parents)

def make_prototype(c):
    global date0

    min_id = get_min_by_code(c, '5%')
    max_id = get_max_by_code(c, '82%')

    code_ids = set()
    for cnt in range(prototype_count):
        code_id = rnd.get() % (max_id - min_id + 1) + min_id
        code_ids.add(code_id)

    print("Make few prototypes")

    for code_id in code_ids:


        # fetch the latest code revision
        c.execute("""SELECT MAX(iter)
                     FROM item_revisions
                     WHERE code_id=?""", (code_id,))
        (iter_,) = c.fetchone()
        c.execute("""SELECT id
                     FROM item_revisions
                     WHERE code_id=?
                       AND iter=?""", (code_id, iter_))
        (rev_id,) = c.fetchone()
        c.execute("""SELECT code
                     FROM items
                     WHERE id=?""", (code_id,))
        (code,) = c.fetchone()

        if code.startswith("81"):
            # no assembly
            new_id, new_rev = revise_code(c, rev_id, db.prototype_date)
            fn1 = "documents/drawings/%s_(drw)_rev%s.txt"%(code, new_rev)
            open(fn1, "w").write("Type: mechanical drawing\nCode:%s\n"%(
                code, ))
            c.execute("""INSERT INTO drawings(
                    code, revision_id, filename, fullpath
                ) VALUES ( ?, ?, ?, ? )
                    """, (code, new_id, os.path.basename(fn1), os.path.abspath(fn1))
            )

        elif code.startswith("82"):
                # assembly
                new_id, new_rev = revise_assembly(c, rev_id, db.prototype_date)
                fn1 = "documents/drawings/%s_(drw)_rev%s.txt"%(code, new_rev)
                open(fn1, "w").write("Type: mechanical drawing\nCode:%s\n"%(
                    code, ))
                c.execute("""INSERT INTO drawings(
                        code, revision_id, filename, fullpath
                    ) VALUES ( ?, ?, ?, ? )
                        """, (code, new_id, os.path.basename(fn1), os.path.abspath(fn1))
                )
                fn2 = "documents/assembling-procedures/%s_(ass)_rev%s.txt"%(code, new_rev)
                open(fn2, "w").write("Type: assembling procedure\nCode:%s\n"%(
                    code, ))
                c.execute("""INSERT INTO drawings(
                        code, revision_id, filename, fullpath
                    ) VALUES ( ?, ?, ?, ? )
                        """, (code, new_id, os.path.basename(fn2), os.path.abspath(fn2))
                )

        elif code.startswith("6"):
                new_id, new_rev = revise_assembly(c, rev_id, db.prototype_date)
                fn1 = "documents/boards/%s_(el)_rev%s.txt"%(code, new_rev)
                open(fn1, "w").write("Type: board drawing\nCode: %s\n"%(
                    code,))
                c.execute("""INSERT INTO drawings(
                        code, revision_id, filename, fullpath
                    ) VALUES ( ?, ?, ?, ? )
                        """, (code, new_id, os.path.basename(fn1), os.path.abspath(fn1))
                )

        elif code[0] in "57":
            new_id, new_rev = revise_code(c, rev_id, db.prototype_date)
        elif code.startswith("1"):
            print("WARNING: code ", code, " is ignore")
            continue
            # topcode
            # update the packaging procedure
            # update the assembly
        else:
            # ??
            print("Code=", code)
            assert(False)


        #parents = update_assemblies_for_new_code(c, the_id, new_id)
        #print("parents=",len(parents))
        #rec_update_assemblies(c, parents)



def xrmdir(path):
        if os.path.isdir(path):
            for fn in os.listdir(path):
                ffn = os.path.join(path, fn)
                xrmdir(ffn)
            os.rmdir(path)
        elif os.path.exists(path):
            os.unlink(path)

# insert non ascii string
def insert_unicode_code(c):
    s="UTF8 TEST HELLO WORLD - 你好世界"
    insert_code(c, s, "TEST-HELLOWORLD", 0,
                0, "NR", "", "")
    insert_code(c, "all lowercase", "TEST-alllowercase", 0,
                0, "NR", "", "")
    insert_code(c, "ALL UPPER CASE", "TEST-ALLUPPERCASE", 0,
                0, "NR", "", "")
    insert_code(c, "DEGREE SYMBOL '°'", "TEST-DEGREE", 0,
                0, "NR", "", "")
    insert_code(c, "A-ACUTE 'à'", "TEST-AACUTE", 0,
                0, "NR", "", "")

def insert_codes_with_date(c):

    insert_code(c, "TEST-ASS-A", "TEST-ASS-A", 0,
                0, "NR", date='2020-01-01', date_to='2021-01-01')
    c.execute("""SELECT MAX(id) FROM item_revisions""")
    aaid = c.fetchone()[0]


    insert_code(c, "TEST-A", "TEST-A", 0,
                0, "NR", date='2020-01-01')
    c.execute("""SELECT MAX(id) FROM items""")
    caid = c.fetchone()[0]

    insert_code(c, "TEST-B", "TEST-B", 0,
                0, "NR", date='2020-01-01', date_to='2021-01-01')
    c.execute("""SELECT MAX(id) FROM items""")
    cbid = c.fetchone()[0]

    for child_id in [caid, cbid]:
        c.execute("""
            INSERT INTO assemblies(
                        unit, child_id,
                        revision_id,
                        qty, each, ref
            ) VALUES (
                ?, ?,
                ?,
                ?, ?, ?
            )""",  ('NR', child_id, aaid, 1, 1, '//'))

def insert_codes_with_date(c):

    insert_code(c, "TEST-ASS-A", "TEST-ASS-A", 0,
                0, "NR", date='2020-01-01', date_to='2021-01-01')
    c.execute("""SELECT MAX(id) FROM item_revisions""")
    aaid = c.fetchone()[0]


    insert_code(c, "TEST-A", "TEST-A", 0,
                0, "NR", date='2020-01-01')
    c.execute("""SELECT MAX(id) FROM items""")
    caid = c.fetchone()[0]

    insert_code(c, "TEST-B", "TEST-B", 0,
                0, "NR", date='2020-01-01', date_to='2021-01-01')
    c.execute("""SELECT MAX(id) FROM items""")
    cbid = c.fetchone()[0]

    for child_id in [caid, cbid]:
        c.execute("""
            INSERT INTO assemblies(
                        unit, child_id,
                        revision_id,
                        qty, each, ref
            ) VALUES (
                ?, ?,
                ?,
                ?, ?, ?
            )""",  ('NR', child_id, aaid, 1, 1, '//'))

def insert_codes_with_loop(c):

    insert_code(c, "TEST-LOOP-A", "TEST-LOOP-A")
    c.execute("""SELECT MAX(id) FROM item_revisions""")
    car = c.fetchone()[0]
    c.execute("""SELECT MAX(id) FROM items""")
    cai = c.fetchone()[0]

    insert_code(c, "TEST-LOOP-B", "TEST-LOOP-B")
    c.execute("""SELECT MAX(id) FROM item_revisions""")
    cbr = c.fetchone()[0]
    c.execute("""SELECT MAX(id) FROM items""")
    cbi = c.fetchone()[0]

    insert_code(c, "TEST-LOOP-C", "TEST-LOOP-C")
    c.execute("""SELECT MAX(id) FROM item_revisions""")
    ccr = c.fetchone()[0]
    c.execute("""SELECT MAX(id) FROM items""")
    cci = c.fetchone()[0]

    c.execute("""
        INSERT INTO assemblies(
                    unit, child_id,
                    revision_id,
                    qty, each, ref
        ) VALUES (
            ?, ?,
            ?,
            ?, ?, ?
        )""",  ('NR', cbi, car, 1, 1, '//'))

    c.execute("""
        INSERT INTO assemblies(
                    unit, child_id,
                    revision_id,
                    qty, each, ref
        ) VALUES (
            ?, ?,
            ?,
            ?, ?, ?
        )""",  ('NR', cci, cbr, 1, 1, '//'))

    c.execute("""
        INSERT INTO assemblies(
                    unit, child_id,
                    revision_id,
                    qty, each, ref
        ) VALUES (
            ?, ?,
            ?,
            ?, ?, ?
        )""",  ('NR', cai, ccr, 1, 1, '//'))


def create_db():
    d = db.DB()
    d.create_db()

    xrmdir("documents")
    os.mkdir("documents")
    os.mkdir("documents/drawings")
    os.mkdir("documents/boards")
    os.mkdir("documents/assembling-procedures")
    os.mkdir("documents/packaging-procedure")

    with db.Transaction(d) as c:
        # 510xxx
        print("Insert resistor 510xxx")
        insert_resistor(c)
        # 520xxx
        print("Insert capacitor 520xxx")
        insert_capacitor(c)
        # 530xxx
        print("Insert uprocessor 530xxx")
        insert_microprocessor(c)

        # 710xxx
        print("Insert screws 710xxx")
        insert_screws(c)
        # 720xxx
        print("Insert washer 720xxx")
        insert_washer(c)
        # 730xxx
        print("Insert elastic washer 730xxx")
        insert_elastic_washer(c)

        # 610xxx
        print("Insert boards 610xxx")
        insert_board(c)

        # 810###
        print("Insert mechanical componets 810xxx")
        insert_mechanical_components(c)

        # 820 #
        print("Insert mechanical assemblies 820xxx")
        insert_mechanical_assemblies(c)

        # 100xxx
        print("Insert top codes 100xxx")
        insert_top_codes(c)

        # 101xxx
        print("Insert spare parts 101xxx")
        insert_spare_parts(c)

        make_changes(c)
        make_prototype(c)

        if False:
            c.executemany("""
                INSERT INTO database_props(name, value)
                VALUES (?, ?)
            """,(
                    ("cfg.template_simple.name", "Simple table"),
                    ("cfg.template_simple.columns", "seq,level,code,indented_code,descr,qty,each,unit,ref,rev,iter,date_from,date_to"),
                    ("cfg.template_simple.captions", "Seq,Level,Code,Code,Description,Q.ty,Each,Unit,Reference,Rev,Iter,From date,To date"),

                    ("cfg.template_all.name", "Full table"),
                    ("cfg.template_all.columns", "seq,level,parent,parent_descr,\"-\",code,indented_code,descr,qty,each,unit,ref,rev,iter,date_from,date_to,gval1,gval2,gval3,gval4,gval5,gval6"),
                    ("cfg.template_all.captions", "Seq,Level,Parent code,Parent descritpion,-,Code,Code,Description,Q.ty,Each,Unit,Reference,Rev,Iter,From date,To date,Supplier#1 PN,Supplier#1 name,Manufacturer#1 PN,Manufacturer#1 name,Manufacturer#2 PN,Manufacturer#2 name"),

                    ("cfg.template_dummy.name", "Dummy table"),
                    ("cfg.template_dummy.columns", "seq,parent,code,descr,qty,each,unit,ref,rev,iter,date_from,date_to"),
                    ("cfg.template_dummy.captions", "Seq,Parent code,Code,Description,Q.ty,Each,Unit,Reference,Rev,Iter,From date,To date")

            ))

        print("Insert unicode codes")
        insert_unicode_code(c)
        print("Insert code with date")
        insert_codes_with_date(c)
        print("Insert assembly with a loop")
        insert_codes_with_loop(c)

create_db()

