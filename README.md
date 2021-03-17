# BOMBrowser

## Introduction

BOMBrowser is a small utility written in python3 w/pyside2, with the aim to
manage technical BOM and the related documentation.

The following database backends are supported (tested):
- sqlite
- sqlserver via odbc
- postgresql (using psycopg2)

It is possible to attach to each node of the BOM, several information like:
- code
- description
- revision
- phase-in date / phase-out date
- an arbitrary number of documents

Moreover it is possible to add further fields (up to 20 with the database v0.4).

Of course it is possible to add some children code to create a full product bom.

The main configuration file is bombrowser.ini, where the following settings
are stored:

- the kind of database
- the database parameter connection
- the name of the further fields
- the report configuration

The mains operations implementated are:
- basic search (by code and/or description; remember to use the '%' as jolly
  character)
- view of a bom with the classic tree of nodes
- "where used" view
- edit / revise of a code
- diff of two bom

## Demo

To see this tool in action, the simple way is to create some "test boms"
using the enclosed mkdb.py python script. The first thing is to copy
the file **bombrowser.ini.example** as **bombrowser.ini**; then comment all
'db source' in the file with the exception of the line
```
db=sqlite
```

Then check that the section **SQLITE** is configured accordling to your needing

```
[SQLITE] 
path=database.sqlite 
```

Finally execute the mkdb.py script

```
$ python3 mkdb.py 
Insert resistor 510xxx
Insert capacitor 520xxx
Insert uprocessor 530xxx
Insert screws 710xxx
[...]
197/200) Updating code '810253', rid=1908
198/200) Updating code '810258', rid=2256
199/200) Updating code '810027', rid=2417
UTF8 TEST HELLO WORLD - 你好世界
[(2446, 2246, '2005-06-23', '', 2000, 999999, '0', 0, None, None, 'UTF8 TEST HELLO WORLD - 你好世界', 'NR', '', '', '', '', '', '', '', '', 2246, 'T-HELLOWORLD'), (2447, 2247, '2005-06-23', '', 2000, 999999, '0', 0, None, None, 'all lowercase', 'NR', '', '', '', '', '', '', '', '', 2247, 'T-alllowercase'), (2448, 2248, '2005-06-23', '', 2000, 999999, '0', 0, None, None, 'ALL UPPER CASE', 'NR', '', '', '', '', '', '', '', '', 2248, 'T-ALLUPPERCASE')]
```

The results is a **database.sqlite** file with several boms. The scripts
create several components like capacitor, resistor, washer, boards,assemblies
etc...

The "top level" assemblies codes start with '10' The mechanical subassemblies
codes start with '82'.

It is created a directory named **documentats**, where are stored the documents
linked to the BOM codes.

After the database creation, to run the program it is sufficient to do:
```
$ python3 bombrowser.py
```

You can see some screenshot in the **screenshots** folder.

## LICENSE

The program is licensed under the GPL V2 (or later).


