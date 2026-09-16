#  - BOMBrowser tests list

## 1 - Index

* 1 - Index
* 2 - Preface
* 3 - Requirements list
* 3.1 - Generic requirements
* 3.2 - 'Code list window' requirements
* 3.3 - 'Code GUI' panel requirements
* 3.4 - Assembly/Where used window requirements
* 3.5 - Diff window requirements
* 3.6 - Edit functions
* 3.7 - Config file requirements
* 3.8 - Advanced search in BOM
* 3.9 - Export data from BOM
* 3.10 - Database management
* 3.11 - Log transaction
* 4 - Tests list
* 4.1 - BOMBrowser - Code list
* 4.2 - 'Code gui' panel
* 4.3 - BOMBrowser - Assembly
* 4.4 - Check for loop
* 4.5 - Check for loop
* 4.6 - BOMBrowser - Copy / revise code
* 4.7 - BomBrowser - Edit date
* 4.8 - Generic test
* 4.9 - Export test
* 4.10 - Import test
* 4.11 - Window menu test
* 4.12 - Advanced search in the BOM
* 4.13 - Export data from assembly
* 4.14 - Dump/Restore/Create a new database
* 4.15 - Log transaction
* 5 - Traceability matrixes
* 5.1 - Test to requirements
* 5.2 - Requirements to tests
* 5.3 - Tests without requirements
* 5.4 - Requirements without tests
* 6 - Conclusion
* 6.1 - Summary of the results
* 6.2 - List of failed tests
* 6.3 - Final result


## 2 - Preface

This document lists the technical requirements and the tests relatet to the project BOMBrowser.


## 3 - Requirements list

This chapter lists all the requirements.

### 3.1 - Generic requirements

These chapters list all the requirements not specific to a single subsystem.

#### 3.1.1 - Common commands

**ID**: req#1009

**Target requirements/tests**: test#1032, test#1033, test#1034, test#1035, test#1036, test#1037, test#1038, test#1039, test#1040, test#1107, test#1108, test#1109, test#1110, test#1111, test#1112, test#1113, test#1114, test#1115, test#1116, test#1254, test#1255, test#1256, test#1257, test#1258, test#1259, test#1260, test#1403, test#1404, test#1405

All windows shall support standard commands:
- Help -> About
- Window menu -> Close all other windows
- Window menu -> Open a new 'Code list' window
- Window menu -> List all open windows
- File -> Close
- File -> Quit

#### 3.1.2 - Copy table

**ID**: req#1010

**Target requirements/tests**: test#1041

It shall be possible to copy a table displayed in a window.

#### 3.1.3 - Document attached to a code

**ID**: req#1464

**Target requirements/tests**: req#1511

It shall be possible to link a drawing/document to a code.

#### 3.1.4 - URL attached to a code

**ID**: req#1465

**Target requirements/tests**: test#1094, test#1095, test#1097, test#1098

It shall be possible to link a URL to a code.

#### 3.1.5 - URL attached to a code

**ID**: req#1495

**Target requirements/tests**: req#1511

It shall be possible to link a URL to a code.

#### 3.1.6 - GVal properties

**ID**: req#1513

**Target requirements/tests**: req#1471, test#1205, test#1206, test#1297, test#1303, test#1309

It shall be possible to attach custom properties to a code.

#### 3.1.7 - GAVal properties

**ID**: req#1514

**Target requirements/tests**: test#1297, test#1303, test#1309

It shall be possible to attach custom properties to a child item of an assembly.

#### 3.1.8 - Check db connection

**ID**: req#1616

**Target requirements/tests**: test#1366, test#1367, test#1368, test#1369

BOMBrowser shall check the db connection and try to reconnect in few attempts.

#### 3.1.9 - Self test

**ID**: req#1632

**Target requirements/tests**: test#1633

BOMBrowser shall have some self test to run during the verification fase

### 3.2 - 'Code list window' requirements

These chapters list all the requirements related to the assembly window.

#### 3.2.1 - Search fields - code and description

**ID**: req#1005

**Target requirements/tests**: test#1013, test#1014, test#1015, test#1016, test#1017, test#1018

The 'Code list window' shall allow searching for codes by 'code' and 'description'.

#### 3.2.2 - Search fields - wildcards

**ID**: req#1006

**Target requirements/tests**: test#1016, test#1017, test#1018, test#1050, test#1051, test#1053, test#1054, test#1057, test#1058, test#1059, test#1060, test#1061, test#1062, test#1063, test#1064, test#1065, test#1068, test#1069, test#1070, test#1071

Search can be performed using wildcard characters such as "_" and "%" according to the standard SQL syntax, as well as operators like >, <, =, !.

#### 3.2.3 - Code property

**ID**: req#1460

**Target requirements/tests**: test#1042, test#1043, test#1055, test#1056

On the right side of the window, a panel shall display all properties of the highlighted code.

#### 3.2.4 - Status bar

**ID**: req#1461

**Target requirements/tests**: test#1044, test#1045, test#1047, test#1048

At the bottom of the window, a status bar shall display:
- the query execution time
- the number of results

#### 3.2.5 - Revision search

**ID**: req#1462

**Target requirements/tests**: test#1046, test#1047, test#1048, test#1049, test#1050, test#1051, test#1052, test#1053, test#1054, test#1057, test#1058, test#1059, test#1060, test#1061, test#1062, test#1063, test#1064, test#1065, test#1068, test#1069, test#1070, test#1071, test#1074, test#1075, test#1076, test#1077, test#1078

The 'Code GUI window' shall allow searching for revisions across all available fields.

#### 3.2.6 - Revision search result colors

**ID**: req#1463

**Target requirements/tests**: test#1074, test#1075, test#1076, test#1077, test#1078

In the 'Search revision window', it shall be possible to apply custom row colors.

#### 3.2.7 - Code commands

**ID**: req#1007

**Target requirements/tests**: test#1019, test#1020, test#1021, test#1022, test#1023, test#1024, test#1025, test#1026, test#1027, test#1028, test#1029, test#1030, test#1031, test#1057, test#1058, test#1059, test#1060, test#1061, test#1062, test#1063, test#1064, test#1065

From the result area, it shall be possible to trigger the following commands:
- Show assembly
- Where used
- Copy / Revise code
- Edit code
- Diff command

### 3.3 - 'Code GUI' panel requirements

These chapters list all the requirements related to the 'Code GUI' panel.

#### 3.3.1 - The 'Code GUI' panel shows code properties

**ID**: req#1471

**Source requirements**: req#1513

**Target requirements/tests**: test#1080

The 'Code GUI' panel shall display code/revision properties such as:
 - Code
 - Description
 - Revision
 - Iteration
 - Date from
 - Date to
 - Documents
 - gvalX variables

#### 3.3.2 - The 'Code GUI' revisions list box

**ID**: req#1466

**Target requirements/tests**: test#1081, test#1082

The 'Code GUI' panel shall include a list box displaying different revision
dates. Selecting a revision/date updates the 'Code GUI' panel with the corresponding properties.

#### 3.3.3 - The 'Code GUI' copy button

**ID**: req#1467

**Target requirements/tests**: test#1085

The 'Code GUI' panel shall feature a copy button that copies all properties to the clipboard.

#### 3.3.4 - The 'Code GUI' 'Document' button

**ID**: req#1468

**Target requirements/tests**: test#1083, test#1084, test#1086, test#1087, test#1088, test#1089, test#1090, test#1091, test#1094, test#1095, test#1096, test#1097

The 'Code GUI' panel shall display a button for each document.
Hovering over a button displays a tooltip showing the document properties.
Clicking the button opens the document or URL.
Right-clicking (RMB) the button opens a context menu with the following commands:
- Copy filename: copies the filename to the clipboard
- Copy dirname: copies the directory path of the file to the clipboard
- Copy fullname: copies the full path (directory + filename) to the clipboard
- Copy file: copies the file object to the clipboard
- Open dir: opens the directory containing the file
- Copy description: copies the description to the clipboard
- Copy URL: copies the URL to the clipboard

#### 3.3.5 - The 'Code GUI' 'Document' button text length

**ID**: req#1469

**Target requirements/tests**: test#1092, test#1093

It shall be possible to configure the maximum filename length displayed on the button caption.

### 3.4 - Assembly/Where used window requirements

This chapter lists all requirements related to the Assembly / Where Used window.

#### 3.4.1 - Content of the assembly window

**ID**: req#1485

**Target requirements/tests**: test#1103, test#1104, test#1105, test#1106, , test#1133, test#1134, test#1140, test#1141, test#1155, test#1157

The 'Assembly window' can display the following hierarchical structures:
- Assembly BOM (latest - i.e., showing only codes with an open 'Date to')
- Assembly BOM for a specific date
- Prototype assembly BOM
- Where used
- Valid where used (i.e., showing only codes with an open 'Date to')
- Smart where used (similar to the above, but displaying only the first 2 levels and the top-level code)

#### 3.4.2 - Code GUI panel

**ID**: req#1490

**Target requirements/tests**: test#1492, test#1491

In the Assembly / Where Used window, a 'Code GUI' panel shall be present on the right side.

#### 3.4.3 - Select date

**ID**: req#1481

**Target requirements/tests**: test#1100, test#1101, test#1102, test#1104

For the 'Show assembly by date' command, a dialog shall allow selecting a specific BOM date to display.

#### 3.4.4 - Export to JSON

**ID**: req#1482

**Target requirements/tests**: test#1117

It shall be possible to export the displayed data in JSON format.

#### 3.4.5 - Show/hide levels

**ID**: req#1483

**Target requirements/tests**: test#1119, test#1120, test#1121, test#1122, test#1123, test#1124

It shall be possible to show or hide different levels of the BOM.

#### 3.4.6 - Search in BOM

**ID**: req#1486

**Target requirements/tests**: test#1126, test#1127, test#1128, test#1129, test#1130, test#1131, test#1132

It shall be possible to search by code and description within the BOM.

#### 3.4.7 - Loop detection

**ID**: req#1487

**Target requirements/tests**: test#1142, test#1143

The system shall detect circular references (loops) in the hierarchical structure.

#### 3.4.8 - Export

**ID**: req#1488

**Target requirements/tests**: test#1118, test#1135, test#1136, test#1137, test#1138, test#1153

It shall be possible to export the data displayed in the window.

#### 3.4.9 - BOM Coloring

**ID**: req#1489

**Target requirements/tests**: test#1146, test#1147, test#1148, test#1149, test#1150, test#1151, test#1152

It shall be possible to color-code the displayed data based on property values.

### 3.5 - Diff window requirements

#### 3.5.1 - Diff window main requirements

**ID**: req#1493

**Target requirements/tests**: test#1160, test#1161, test#1162, test#1163, test#1164, test#1165, test#1166, test#1167, test#1168, test#1169, test#1170, test#1171, test#1172, test#1173, test#1174

It shall be possible to compare two BOMs based on:
- part lists of each assembly
- properties (description, revisions, documents, etc.) of each code
- added codes, removed codes, and updated codes
The BOMs shall be selected by code and date.

#### 3.5.2 - Diff window options

**ID**: req#1494

**Target requirements/tests**: test#1170

The Diff window shall provide an option to swap the two BOMs, inverting the '+' (added) and '-' (removed) markers.

#### 3.5.3 - Diff window options (2)

**ID**: req#1503

**Target requirements/tests**: test#1173

The Diff window shall provide an option to display only key attributes (code, description, revision).

#### 3.5.4 - Diff window options (3)

**ID**: req#1504

**Target requirements/tests**: test#1171, test#1172

The Diff window shall provide an option to compare only the first level of child items.

### 3.6 - Edit functions

#### 3.6.1 - Copy code

**ID**: req#1506

**Target requirements/tests**: test#1177, test#1178, test#1179, test#1181, test#1182, test#1184, test#1185, test#1186, test#1187, test#1188, test#1189, test#1190, test#1191, test#1192, test#1193, test#1194, test#1195

It shall be possible to copy a code.

#### 3.6.2 - Revise the code

**ID**: req#1507

**Target requirements/tests**: test#1197, test#1198, test#1199, test#1200, test#1201, test#1202, test#1203, test#1204, test#1205, test#1206, test#1207, test#1516, test#1517

It shall be possible to revise a code.
The code identifier remains identical, but all other attributes may change.
The date must be different and cannot be earlier than the date of the latest revision.
It shall be possible to create a prototype revision.

#### 3.6.3 - Edit code: edit code properties

**ID**: req#1509

**Target requirements/tests**: , test#1209, test#1210, test#1211, test#1212, test#1273, test#1274, test#1275, test#1276, test#1277, test#1278, test#1279, test#1280, test#1281, test#1282, test#1283, test#1284, test#1294, test#1295, test#1296, test#1297, test#1298, test#1299, test#1300, test#1301, test#1302, test#1303, test#1304, test#1305, test#1306, test#1307, test#1308, test#1309, test#1310, test#1311, test#1312, test#1313, test#1314, test#1315, test#1316, test#1322

It shall be possible to modify the properties of a code revision (description, revision, etc.).

#### 3.6.4 - Edit code: edit child items

**ID**: req#1510

**Target requirements/tests**: test#1222, test#1223, test#1224, test#1225, test#1226, test#1227, test#1228, test#1229, test#1230, test#1231, test#1232, test#1233, test#1234, test#1235, test#1236, test#1237, test#1238, test#1239, test#1240, test#1241, test#1242, test#1243, test#1244, test#1245, test#1246, test#1247, test#1248, test#1249, test#1250, test#1251, test#1252, test#1253, test#1261, test#1262, test#1263, test#1285, test#1286, test#1287, test#1288, test#1291, test#1292, test#1293

It shall be possible to modify the child items of a code:
- add a child code
- remove a child code
- modify the quantity of a child code
- reorder child items
- copy a child item from one code to another
- search for a code to insert

#### 3.6.5 - Edit code: edit code drawings

**ID**: req#1511

**Source requirements**: req#1464, req#1495

**Target requirements/tests**: test#1213, test#1214, test#1215, test#1216, test#1217, test#1218, test#1219, test#1220, test#1289, test#1290, test#1317, test#1318, test#1319, test#1320, test#1321

It shall be possible to manage drawings attached to a code:
- add a drawing
- remove a drawing
- add a URL
- remove a URL
It shall be possible to display a drawing directly from the edit window.

#### 3.6.6 - Edit code: edit code drawings - copy and paste drawings

**ID**: req#1515

**Target requirements/tests**: test#1221

It shall be possible to copy drawings from one code to another.

#### 3.6.7 - Edit code: remove a revision

**ID**: req#1512

**Target requirements/tests**: test#1264, test#1265, test#1266, test#1267, test#1268, test#1269, test#1270, test#1271, test#1272

It shall be possible to delete a code or a specific code revision.

#### 3.6.8 - Edit code: change revision date

**ID**: req#1518

**Target requirements/tests**: test#1327, test#1328, test#1329, test#1330, test#1331, test#1334, test#1335, test#1336, test#1337, test#1338, test#1339, test#1340, test#1341, test#1342, test#1343, test#1344, test#1345, test#1346, test#1347, test#1348, test#1349, test#1350, test#1351, test#1353, test#1354, test#1355, test#1356, test#1357, test#1358, test#1359, test#1360, test#1361, test#1362

It shall be possible to update the date of a revision.

#### 3.6.9 - Edit code: change revision date validation

**ID**: req#1520

**Target requirements/tests**: test#1332, test#1333, test#1334, test#1335, test#1336, test#1337, test#1338, test#1339, test#1340, test#1341, test#1342, test#1343, test#1348, test#1349, test#1350, test#1351, test#1353, test#1354, test#1355, test#1356, test#1357, test#1358, test#1360, test#1362

During a date update, the following validation checks must be performed:
- the dates must be valid calendar dates
- the dates must be consecutive
- date ranges between revisions must not overlap
- if a date is updated, every child item must outlive its parent
- it shall be possible to set only the latest revision's 'Date to' as prototype
- it shall be possible to set the latest revision's 'Date to' as prototype, empty (infinity), or a finite date
- each 'Date to' must be greater than or equal to 'Date from'

### 3.7 - Config file requirements

#### 3.7.1 - Config file: basic requirements

**ID**: req#1610

**Target requirements/tests**: test#1364, test#1365, test#1397, test#1398, test#1399

- BOMBrowser must be configured by a config file named 'bombrowser.ini',
  stored in the same directory as the executable.
- Alternatively, a file named 'bombrowser.forward' (containing the absolute
  path of the 'bombrowser.ini' file) can be used to specify the path to
  the config file.

#### 3.7.2 - Config file: force upper case

**ID**: req#1612

**Target requirements/tests**: test#1371, test#1372, test#1373, test#1374, test#1375, test#1376, test#1377, test#1378

BOMBrowser can be configured to force all codes and/or descriptions
to uppercase.

#### 3.7.3 - Config file: search ignore case

**ID**: req#1613

**Target requirements/tests**: test#1379, test#1380, test#1381, test#1382, test#1383, test#1384, test#1385, test#1386, test#1387, test#1388

BOMBrowser can be configured so that searches are case-insensitive.

#### 3.7.4 - Config file: check file

**ID**: req#1614

**Target requirements/tests**: test#1364, test#1365, test#1389, test#1390, test#1391, test#1392, test#1393, test#1394

During startup, BOMBrowser shall perform basic integrity checks on the
'bombrowser.ini' file.

#### 3.7.5 - Config file: default search mode

**ID**: req#1615

**Target requirements/tests**: test#1395, test#1396

BOMBrowser can be configured so that it starts the "Code list" window in
standard or advance search mode.

### 3.8 - Advanced search in BOM

#### 3.8.1 - Search in BOM

**ID**: req#1618

**Target requirements/tests**: test#1407, test#1408, test#1409, test#1410, test#1411, test#1412, test#1413, test#1414, test#1415, test#1416, test#1417, test#1418, test#1419, test#1420, test#1421

BOMBrowser shall allow to search a code of a BOM in the assembly window.
This search, called "Advance search", can be executed on any property of
a code like: code, description, unit, gval...
It can be possible to use operator like >, <, !

#### 3.8.2 - Search document in BOM

**ID**: req#1619

**Target requirements/tests**: test#1424

BOMBrowser shall allow to search a code of a BOM in the assembly window.
This search, called "Advance search", can be executed on document.

#### 3.8.3 - Search in '[smart/valid] where used windows'

**ID**: req#1620

**Target requirements/tests**: test#1422, test#1423

BOMBrowser shall allow to search a code of '[smart/valid] where used windows'.
This search, called "Advance search", can be executed on any property of
a code like: code, description, unit, gval....

### 3.9 - Export data from BOM

#### 3.9.1 - Export data, main requirements

**ID**: req#1622

**Target requirements/tests**: test#1426, test#1427, test#1428, test#1429, test#1430, test#1431, test#1432, test#1433, test#1434, test#1436, test#1438

BOMBrowser shall allow to export all the iformation of a BOM:
- the BOM in a CSV file
- all the file contained in the BOM

### 3.10 - Database management

#### 3.10.1 - Dump database

**ID**: req#1624

**Target requirements/tests**: test#1440

BOMBrowser shall allow to dump the database

#### 3.10.2 - Restore database

**ID**: req#1625

**Target requirements/tests**: test#1441

BOMBrowser shall allow to restore a database from a dump

#### 3.10.3 - Create a new database

**ID**: req#1626

**Target requirements/tests**: test#1442

BOMBrowser shall allow to create a new database. Only the code 000000000000
shall exist.

#### 3.10.4 - Create a new database

**ID**: req#1627

**Target requirements/tests**: test#1443

The database restore shall consider the count of gval/agval variables.

### 3.11 - Log transaction

#### 3.11.1 - Log transaction: actions to log

**ID**: req#1629

**Target requirements/tests**: test#1445, test#1446, test#1447, test#1448, test#1449, test#1450, test#1451, test#1452

BOMBrowser shall log all the database changes:
- create a new revision
- copy a code
- edit a code
- remove/add a document
- remove/add a child
- change a date
- delete a revision
- delete a code

#### 3.11.2 - Log transaction: cannot write the log

**ID**: req#1630

**Target requirements/tests**: test#1453

BOMBrowser shall inform that it is not possible to log the action.

#### 3.11.3 - Log transaction: compress the log

**ID**: req#1631

**Target requirements/tests**: test#1454

BOMBrowser shall allow to compress the log in .gz format.

## 4 - Tests list

Before executing the tests, verify that the following bombrowser.init parameters are set as shown:

BOMBROWSER.description_force_uppercase=1
BOMBROWSER.code_force_uppercase=1
BOMBROWSER.ignore_case_during_search=1
BOMBROWSER.db=sqlite

SQLITE.ignore_case_during_search=0

Set up the DB with:

python mkdb.py --test_db

### 4.1 - BOMBrowser - Code list

#### 4.1.1 - search a code

**ID**: test#1013

**Source requirements**: req#1005

**Test description**:
Enter code '820037' in the 'Code' field and press **ENTER**

**Expected results**:
Code 820037 is displayed

**Passed**: [X]

#### 4.1.2 - search a code (2)

**ID**: test#1014

**Source requirements**: req#1005

**Test description**:
Enter code '820038' in the 'Code' field and click the **'Search'** button

**Expected results**:
Code 820038 is displayed

**Passed**: [X]

#### 4.1.3 - search a code by description

**ID**: test#1015

**Source requirements**: req#1005

**Test description**:
Clear the 'Code' field
Enter 'BOARD 14' in the 'Description' field and click the 'Search' button

**Expected results**:
Code 610014 - "BOARD 14" is displayed

**Passed**: [X]

#### 4.1.4 - search a code by description with a wildcard

**ID**: test#1016

**Source requirements**: req#1005, req#1006

**Test description**:
Enter '%BOARD%13' in the 'Description' field and press ENTER

**Expected results**:
Code 610013 - "BOARD 13" is displayed

**Passed**: [X]

#### 4.1.5 - search a code with a wildcard

**ID**: test#1017

**Source requirements**: req#1005, req#1006

**Test description**:
- Enter '%6%' in the 'Code' field
- Click the 'Search' button

**Expected results**:
Codes containing '6' are displayed

**Passed**: [X]

#### 4.1.6 - search a code and a description with wildcards

**ID**: test#1018

**Source requirements**: req#1005, req#1006

**Test description**:
- Enter '%7%' in the 'Code' field
- Enter '%BOARD%' in the 'Description' field
- Click the 'Search' button

**Expected results**:
Codes containing '7' with a description containing 'BOARD' are displayed

**Passed**: [X]

#### 4.1.7 - assembly

**ID**: test#1019

**Source requirements**: req#1007

**Test description**:
- Enter code '820037' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Show assembly by date" command.

**Expected results**:
- The "BOMBrowser: select date" dialog is displayed
- This dialog contains a list of dates for code 820037.

**Passed**: [X]

**ID**: test#1020

**Source requirements**: req#1007

**Test description #2**:
- Repeat the steps from the first test
- Select the "Show latest assembly" command.

**Expected results #2**:
- The "BOMBrowser: assembly window" dialog is displayed
- The displayed BOM corresponds to the latest revision (i.e., all items have an undefined "Date to")

**Passed**: [X]

**ID**: test#1021

**Source requirements**: req#1007

**Test description #3**:
- Repeat the steps from the first test
- Select the "Show prototype assembly" command.

**Expected results #3**:
- The "BOMBrowser: assembly window" dialog is displayed
- The displayed BOM corresponds to the latest revision (i.e., all items have an undefined "Date to") with the exception of a few items whose "Date from" is set to prototype

**Passed**: [X]

#### 4.1.10 - where used

**ID**: test#1022

**Source requirements**: req#1007

**Test description**:
- Enter code '810036' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Where used" command.

**Expected results**:
The "BOMBrowser - Where used" window is displayed

**Passed**: [X]

#### 4.1.11 - where used (2)

**ID**: test#1023

**Source requirements**: req#1007

**Test description**:
- Enter code '100037' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Where used" command.

**Expected results**:
The "BOMBrowser - Where used" window is displayed. Only one code (100037) is displayed.

**Passed**: [X]

#### 4.1.12 - valid where used

**ID**: test#1024

**Source requirements**: req#1007

**Test description**:
- Enter code '810036' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Valid where used" command.

**Expected results**:
The "BOMBrowser - Valid where used" window is displayed

**Passed**: [X]

#### 4.1.13 - valid where used (2)

**ID**: test#1025

**Source requirements**: req#1007

**Test description**:
- Enter code '100037' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Valid where used" command.

**Expected results**:
The "BOMBrowser - Valid where used" window is displayed. Only one code (100037) is displayed.

**Passed**: [X]

#### 4.1.14 - Copy/revise code

**ID**: test#1026

**Source requirements**: req#1007

**Test description**:
- Enter code '810031' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Copy code" (or "Revise a code") command.

**Expected results**:
The "BOMBrowser: select date" dialog is displayed, containing a list for code 810031.

**Passed**: [X]

#### 4.1.15 - edit code

**ID**: test#1027

**Source requirements**: req#1007

**Test description**:
- Enter code '810036' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Edit code" command.

**Expected results**:
The "BOMBrowser - Edit code" window is displayed, containing the properties of code 810036.

**Passed**: [X]

#### 4.1.16 - diff from

**ID**: test#1028

**Source requirements**: req#1007

**Test description**:
- Enter code '810031' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Diff from" command.

**Expected results**:
The "BOMBrowser: select date" dialog is displayed, containing a list for code 810031.

**Passed**: [X]

#### 4.1.17 - diff from (2x)

**ID**: test#1029

**Source requirements**: req#1007

**Test description**:
- Enter code '820036' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Diff from" command.

**Expected results**:
The "BOMBrowser: select date" dialog is displayed, containing a list for code 820036.

**Passed**: [X]

#### 4.1.18 - diff to

**ID**: test#1030

**Source requirements**: req#1007

**Test description**:
- Enter code '810031' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Diff to" command.

**Expected results**:
The "BOMBrowser: select date" dialog is displayed, containing a list for code 810031.

**Passed**: [X]

#### 4.1.19 - diff to (2x)

**ID**: test#1031

**Source requirements**: req#1007

**Test description**:
- Enter code '820036' in the 'Code' field
- Click the 'Search' button
- Right-click the first entry
- Select the "Diff to" command.

**Expected results**:
The "BOMBrowser: select date" dialog is displayed, containing a list for code 820036.

**Passed**: [X]

#### 4.1.20 - menu->help->about

**ID**: test#1032

**Source requirements**: req#1009

**Test description**:
From the menu, select Help -> About

**Expected results**:
- The "About" dialog is displayed. The dialog contains:
- the current version and copyright details.
- text showing the active connection

**Passed**: [X]

#### 4.1.21 - menu->window

**ID**: test#1033

**Source requirements**: req#1009

**Test description**:
- Enter code 820037
- Right-click the first entry
- Select "Show assembly by date"
- Select the first date and double-click it
- Return to "BOMBrowser - Code list"
- Right-click the first entry
- Select "Where used"
- Return to "BOMBrowser - Code list"
- Right-click the first entry
- Select "Valid where used"
- Return to "BOMBrowser - Code list"
- Right-click the first entry
- Select "Edit code"
- Five windows are open. Open the "Window menu" in the "BOMBrowser - Codes list" window:

**Expected results**:
The menu displays the four windows: BOMBrowser - Where used, BOMBrowser - Valid where used, BOMBrowser - Assembly, BOMBrowser - Edit

**Passed**: [X]

#### 4.1.22 - menu->file->close

**ID**: test#1034

**Source requirements**: req#1009

**Test description**:
- Enter code 820037
- Right-click the first entry and select "Where used"
- Two windows are open. Select "File -> Close" in the "BOMBrowser - Codes list" window:

**Expected results**:
- The "BOMBrowser - Codes list" closes. "BOMBrowser - Where used" remains open.

**Passed**: [X]

**ID**: test#1035

**Source requirements**: req#1009

**Test description #2**:
- After the steps above, press CTRL+L in the open "Where used" window

**Expected results #2**:
- The "BOMBrowser - Codes list" appears

**Passed**: [X]

**ID**: test#1036

**Source requirements**: req#1009

**Test description #3**:
- After the steps above, close the "BOMBrowser - Codes list" window again.
- In the open "Where used" window, select "New codes list window" from the Window menu

**Expected results #3**:
- The "BOMBrowser - Codes list" appears

**Passed**: [X]

#### 4.1.25 - Ctrl-Q  menu->file->close

**ID**: test#1037

**Source requirements**: req#1009

**Test description**:
- Enter code 820037
- Right-click the first entry and select "Where used"
- Two windows are open. Focus on "BOMBrowser - Codes list"
- Press CTRL+Q

**Expected results**:
The "BOMBrowser - Codes list" closes. "BOMBrowser - Where used" remains open.

**Passed**: [X]

#### 4.1.26 - menu->file->exit

**ID**: test#1038

**Source requirements**: req#1009

**Test description**:
- Enter code 820037
- Right-click the first entry and select "Where used"
- Two windows are open. Select "File -> Exit" in the "BOMBrowser - Codes list" window:

**Expected results**:
A BOMBrowser dialog asking to confirm exit is displayed.

**Passed**: [X]

**ID**: test#1039

**Source requirements**: req#1009

**Test description #2**:
- After the steps above, click No

**Expected results #2**:
The Codes list window remains open

**Passed**: [X]

**ID**: test#1040

**Source requirements**: req#1009

**Test description #3**:
- Repeat the steps above until the dialog appears, then click Yes

**Expected results #3**:
The application closes completely. No windows remain displayed.

**Passed**: [X]

#### 4.1.29 - Menu->edit->copy

**ID**: test#1041

**Source requirements**: req#1010

**Test description**:
- Enter code %6% and press ENTER
- Select Menu -> Edit -> Copy table values
- Paste the clipboard content into a text editor

**Expected results**:
- Verify that the table matches the one in "BOMBrowser - Codes list" (TAB-separated values).
- Verify that the row count matches the "BOMBrowser - Codes list" window + 1 row (header row included)

**Passed**: [X]

#### 4.1.30 - Code GUI

**ID**: test#1042

**Source requirements**: req#1460

**Test description**:
- Enter code 8200% and press ENTER
- Select the first entry

**Expected results**:
Information for the selected code is displayed in the right panel

**Passed**: [X]

**ID**: test#1043

**Source requirements**: req#1460

**Test description #2**:
- After the steps above, select the 2nd entry.

**Expected results #2**:
Information for the 2nd selected code is displayed in the right panel

**Passed**: [X]

#### 4.1.32 - Status bar

**ID**: test#1044

**Source requirements**: req#1461

**Test description**:
- Enter code 8200% and press ENTER

**Expected results**:
The status bar displays the number of results and the query execution time

**Passed**: [X]

#### 4.1.33 - Status bar

**ID**: test#1045

**Source requirements**: req#1461

**Test description**:
- Enter code CODE_INVALID and press ENTER

**Expected results**:
- The status bar displays 0 results
- Previous results are not cleared

**Passed**: [X]

#### 4.1.34 - Revision search

**ID**: test#1046

**Source requirements**: req#1462

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code 8200% and click "Search"

**Expected results**:
The status bar displays the number of results and the query execution time.

**Passed**: [X]

#### 4.1.35 - Revision search

**ID**: test#1047

**Source requirements**: req#1462, req#1461

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code CODE_INVALID and click "Search"

**Expected results**:
The status bar displays 0 results

**Passed**: [X]

#### 4.1.36 - Revision search

**ID**: test#1048

**Source requirements**: req#1462, req#1461

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code CODE_INVALI2D and click "Search"

**Expected results**:
- The status bar displays 0 results
- Previous results are not cleared

**Passed**: [X]

#### 4.1.37 - Revision search

**ID**: test#1049

**Source requirements**: req#1462

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code 820012 and click "Search"

**Expected results**:
- The status bar displays the result count (>= 3)
- The results table displays the different revisions of the searched code

**Passed**: [X]

#### 4.1.38 - Revision search

**ID**: test#1050

**Source requirements**: req#1462, req#1006

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code 8200% and click "Search"

**Expected results**:
- The results table displays codes (and their revisions) starting with 8200..

**Passed**: [X]

#### 4.1.39 - Revision search

**ID**: test#1051

**Source requirements**: req#1462, req#1006

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code >820000 and click "Search"

**Expected results**:
- The results table displays codes greater than 820000

**Passed**: [X]

#### 4.1.40 - Revision search

**ID**: test#1052

**Source requirements**: req#1462

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter date-from 2003-06-04 and click "Search"

**Expected results**:
- The results table displays codes with 'Date from' set to 2003-06-04

**Passed**: [X]

#### 4.1.41 - Revision search

**ID**: test#1053

**Source requirements**: req#1462, req#1006

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter date-from '>2003-06-04' and click "Search"

**Expected results**:
- The results table displays codes with 'Date from' greater than 2003-06-04 (or prototype)

**Passed**: [X]

#### 4.1.42 - Revision search

**ID**: test#1054

**Source requirements**: req#1462, req#1006

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code >820000 and press ENTER
- Select a code

**Expected results**:
- The right panel "Code GUI" updates its values according to the selected code

**Passed**: [X]

**ID**: test#1055

**Source requirements**: req#1460

**Test description #2**:
- Select a different code

**Expected results #2**:
- The right panel "Code GUI" updates its values according to the selected code

**Passed**: [X]

**ID**: test#1056

**Source requirements**: req#1460

**Test description #3**:
- Repeat test #2 several times

**Expected results #3**:
- Expected results from test #2 apply

**Passed**: [X]

#### 4.1.45 - Revision search

**ID**: test#1057

**Source requirements**: req#1462, req#1006, req#1007

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code >820000 and press ENTER
- Select a code
- Right-click and select "Show latest assembly"

**Expected results**:
- The Assembly window is displayed.
- The date of the top-level code is >= to that of the selected code from the previous step

**Passed**: [X]

**ID**: test#1058

**Source requirements**: req#1462, req#1006, req#1007

**Test description #2**:
- Repeat the steps above up to the right-click action
- Right-click and select "Where used"

**Expected results #2**:
- The Where Used window is displayed

**Passed**: [X]

**ID**: test#1059

**Source requirements**: req#1462, req#1006, req#1007

**Test description #3**:
- Repeat the steps above up to the right-click action
- Right-click and select "Valid where used"

**Expected results #3**:
- The Valid Where Used window is displayed

**Passed**: [X]

**ID**: test#1060

**Source requirements**: req#1462, req#1006, req#1007

**Test description #4**:
- Repeat the steps above up to the right-click action
- Right-click and select "Show assembly by date"

**Expected results #4**:
- The "Select date" dialog opens (click Cancel to return to the previous window)

**Passed**: [X]

**ID**: test#1061

**Source requirements**: req#1462, req#1006, req#1007

**Test description #5**:
- Repeat the steps above up to the right-click action
- Select a code with multiple dates, choosing the one with the earliest 'Date from'
- Right-click and select "Show this assembly"

**Expected results #5**:
- The "Assembly window" is displayed
- The assembly corresponds to the 'Date from' of the selected code
- The date in the title bar of the "Assembly window" matches the 'Date from' of the selected revision

**Passed**: [X]

**ID**: test#1062

**Source requirements**: req#1462, req#1006, req#1007

**Test description #6**:
- Repeat the steps above up to the right-click action (make sure to select a code >= 82108)
- Right-click and select "Show prototype assembly"

**Expected results #6**:
- The "Prototype assembly window" is displayed
- Navigate through items and verify that some are marked as prototype

**Passed**: [X]

**ID**: test#1063

**Source requirements**: req#1462, req#1006, req#1007

**Test description #7**:
- Repeat the steps above up to the right-click action
- Right-click and select "Copy code" (or "Revise a code")

**Expected results #7**:
- The "Select date" dialog opens (click Cancel to return to the previous window)

**Passed**: [X]

**ID**: test#1064

**Source requirements**: req#1462, req#1006, req#1007

**Test description #8**:
- Repeat the steps above up to the right-click action
- Right-click and select "Edit code"

**Expected results #8**:
- The "Edit code" window is displayed

**Passed**: [X]

**ID**: test#1065

**Source requirements**: req#1462, req#1006, req#1007

**Test description #9**:
- Repeat the steps above up to the right-click action
- Right-click and select "Diff from"
- Right-click and select "Diff to"
(selecting different revisions of the same code)

**Expected results #9**:
- The Diff window is displayed

**Passed**: [X]

#### 4.1.54 - search <

**ID**: test#1068

**Source requirements**: req#1462, req#1006

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code <5000 and press ENTER

**Expected results**:
- All codes less than 5000 are displayed (alphanumeric comparison)

**Passed**: [X]

#### 4.1.55 - search !

**ID**: test#1069

**Source requirements**: req#1462, req#1006

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code !820001 and press ENTER

**Expected results**:
- All codes except 820001 are displayed

**Passed**: [X]

#### 4.1.56 - search =

**ID**: test#1070

**Source requirements**: req#1462, req#1006

**Test description**:
- Select "Search mode -> Advanced" from the menu
- Enter code =820012 and press ENTER

**Expected results**:
- Only code 820012 (across all its revisions) is displayed

**Passed**: [X]

#### 4.1.57 - search =

**ID**: test#1071

**Source requirements**: req#1462, req#1006

**Test description**:
- select from the menu "Search mode->advanced"
- enter Document "asm" and press ENTER

**Expected results**:
- Only assembly revisions are shown (revisions that have a document with 'asm' in the filename)

**Passed**: [X]

#### 4.1.58 - 'Search revision' color

#### 4.1.59 - Search revision color (prep)

**Preparatory steps**:
the following configuration in bombrowser.ini is assumed:
revlistcolors=
    gval1=COLOR,gval2=!A:fg=green
    gval1=COLOR,gval2=A:bg=pink
    gval1=COLOR,gval2=B:bold,fg=blue
    gval1=COLOR,gval2=C:italic

#### 4.1.60 - Search for CODE-COLORS-xxx

**ID**: test#1074

**Source requirements**: req#1462, req#1463

**Test description**:
In the search revision window (search mode = advanced), search for code %COLOR%

**Expected results**:
The CODE-COLORS-xxxx codes are shown

**Passed**: [X]

**ID**: test#1075

**Source requirements**: req#1462, req#1463

**Test description #2**:
Look at the color of the 1st row

**Expected results #2**:
The first row (TEST-COLOR-A), bg=pink
(gval1=COLOR,gval2=A:bg=pink)

**Passed**: [X]

**ID**: test#1076

**Source requirements**: req#1462, req#1463

**Test description #3**:
Look at the color of the 2nd row

**Expected results #3**:
The 2nd row (TEST-COLOR-B), fg=blue, bold
(gval1=COLOR,gval2=B:bold,fg=blue)

**Passed**: [X]

**ID**: test#1077

**Source requirements**: req#1462, req#1463

**Test description #4**:
Look at the color of the 3rd row

**Expected results #4**:
The 3rd row (TEST-COLOR-C), fg=green, italic
(gval1=COLOR,gval2=C:italic, gval1=COLOR,gval2=!A:fg=green)

**Passed**: [X]

**ID**: test#1078

**Source requirements**: req#1462, req#1463

**Test description #5**:
Look at the color of the 4th row

**Expected results #5**:
The 4th row (TEST-COLOR-D), fg=green
(gval1=COLOR,gval2=!A:fg=green)

**Passed**: [X]

### 4.2 - 'Code gui' panel

#### 4.2.1 - general

**ID**: test#1080

**Source requirements**: req#1471

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 8200%
- press ENTER
- Select the first entry (820000)

**Expected results**:
the left panel displays the information for the selected code (check title and code)

**Passed**: [X]

#### 4.2.2 - multiple revision

**ID**: test#1081

**Source requirements**: req#1466

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 8200%
- press ENTER
- sort by REV
- Select the most revised entry (the latest one)
- Select another date in the rightmost combobox

**Expected results**:
The information on the panel changes accordingly (check the date)

**Passed**: [X]

#### 4.2.3 - multiple revision (2)

**ID**: test#1082

**Source requirements**: req#1466

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 8200%
- press ENTER
- sort by REV
- Select the most revised entry (the latest one)

**Expected results**:
The right combo box dropdown contains all the revision dates for the code (cross-check with the date in the edit dialog)

**Passed**: [X]

#### 4.2.4 - documents

**ID**: test#1083

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 8200%
- press ENTER
- Select the 2nd entry (820001)

**Expected results**:
In the bottom part, two buttons representing two documents are shown

**Passed**: [X]

#### 4.2.5 - documents (2x)

**ID**: test#1084

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Click a document button

**Expected results**:
Clicking a document button opens the corresponding document

**Passed**: [X]

#### 4.2.6 - Copy info..

**ID**: test#1085

**Source requirements**: req#1467

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Click the 'Copy info' button

**Expected results**:
Pasting the clipboard content into an editor displays the relevant information

**Passed**: [X]

#### 4.2.7 - Check tool tip

**ID**: test#1086

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 820000
- hover the mouse pointer over the "Code - gui" drawing button

**Expected results**:
- a tooltip appears showing the file name and full path

**Passed**: [X]

#### 4.2.8 - RMB menu of drawing button

**ID**: test#1087

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 820000
- hover the mouse pointer over the Code gui drawing buttons, press RMB
- select "Open dir"

**Expected results**:
- the directory containing the file opens

**Passed**: [X]

#### 4.2.9 - RMB menu of drawing button

**ID**: test#1088

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 820000
- hover the mouse pointer over the drawing buttons, press RMB
- select "Copy filename"
- paste it into an editor

**Expected results**:
- the filename is pasted

**Passed**: [X]

#### 4.2.10 - RMB menu of drawing button

**ID**: test#1089

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 820000
- hover the mouse pointer over the Code, press RMB
- select "Copy dirname"
- paste it into an editor

**Expected results**:
- the directory name is pasted

**Passed**: [X]

#### 4.2.11 - RMB menu of drawing button

**ID**: test#1090

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 820000
- hover the mouse pointer over the drawing button, press RMB
- select "Copy full path"
- paste it into an editor

**Expected results**:
- the full path (filename + dirname) is pasted

**Passed**: [X]

#### 4.2.12 - RMB menu of drawing button

**ID**: test#1091

**Source requirements**: req#1468

**Test description**:
- In the "BOMBrowser - codes list" window, enter code 820000
- hover the mouse pointer over the drawing button, press RMB
- select "Copy file"
- paste it into a folder

**Expected results**:
- the file is copied

**Passed**: [X]

#### 4.2.13 - Long filename

**ID**: test#1092

**Source requirements**: req#1469

**Test description**:
- Set the parameter btnmaxlength=10
- In the "BOMBrowser - codes list" window, enter code TEST-LONG_FN
- look at the button label

**Expected results**:
- verify that the filename ends with "..."

**Passed**: [X]

#### 4.2.14 - Long filename

**ID**: test#1093

**Source requirements**: req#1469

**Test description**:
- Set the parameter btnmaxlength=0
- In the "BOMBrowser - codes list" window, enter code TEST-LONG_FN
- look at the button label

**Expected results**:
- verify that the filename does NOT end with "..."

**Passed**: [X]

#### 4.2.15 - URL

**ID**: test#1094

**Source requirements**: req#1465, req#1468

**Preparatory steps**:
Search for code CODE_WITH_URL

**Test description**:
In the code gui, hover the mouse over the button with the URL

**Expected results**:
A tooltip with the URL and description appears

**Passed**: [X]

**ID**: test#1095

**Source requirements**: req#1465, req#1468

**Test description #2**:
Right-click on the drawing button

**Expected results #2**:
A context menu showing "Copy description" and "Copy URL" is displayed

**Passed**: [X]

**ID**: test#1096

**Source requirements**: req#1468

**Test description #3**:
Select "Copy description", then paste the clipboard content into an editor

**Expected results #3**:
The pasted content is the description

**Passed**: [X]

**ID**: test#1097

**Source requirements**: req#1465, req#1468

**Test description #4**:
Select "Copy URL", then paste the clipboard content into an editor

**Expected results #4**:
The pasted content is the URL

**Passed**: [X]

**ID**: test#1098

**Source requirements**: req#1465

**Test description #5**:
Click the button with the URL

**Expected results #5**:
A web browser opens, navigating to the URL

**Passed**: [X]

### 4.3 - BOMBrowser - Assembly

#### 4.3.1 - select date

**ID**: test#1100

**Source requirements**: req#1481

**Test description**:
- enter code "820037" in "BOMBrowser - Code list"
- right-click on the first entry
- select the "Show assembly by date" command
- "The BOMBrowser: Select Date" dialog is displayed
- Check that it is a modeless dialog by trying to click the menu in the "parent" window

**Expected results**:
The click can trigger an action (e.g., open a menu)

**Passed**: [X]

**ID**: test#1101

**Source requirements**: req#1481

**Test description #2**:
- after the step above, click the Cancel button

**Expected results #2**:
- the dialog disappears and the "codes list" window is displayed

**Passed**: [X]

**ID**: test#1102

**Source requirements**: req#1481

**Test description #3**:
- repeat the steps above until the "Show assembly by date" dialog appears
- Select the first item
- click the "Select" button

**Expected results #3**:
- The "BOMBrowser - Assembly" window appears
- Check that the date in the window title matches the selected date

**Passed**: [X]

#### 4.3.4 - show assembly

**ID**: test#1103

**Source requirements**: req#1485

**Test description**:
- enter code "810037" in "BOMBrowser - Code list"
- right-click on the first entry
- select the "Show assembly by date" command
- click "Select"

**Expected results**:
- The "BOMBrowser - Assembly" window appears
- only one code (810037) is shown

**Passed**: [X]

#### 4.3.5 - show assembly (2)

**ID**: test#1104

**Source requirements**: req#1481, req#1485

**Test description**:
- enter code "820037" in "BOMBrowser - Code list"
- right-click on the first entry
- select the "Show assembly by date" command
- "The BOMBrowser: Select Date" dialog is displayed
- Select the first item
- click the "Select" button
- The Assembly window appears; select an item that is an assembly
- then right-click and execute "Show Assembly by date"

**Expected results**:
A new "Select date" window is displayed.

**Passed**: [X]

#### 4.3.6 - where used (2)

**ID**: test#1105

**Source requirements**: req#1485

**Test description**:
- enter code "100000" in "BOMBrowser - Code list"
- right-click on the first entry
- select the "Show assembly by date" command
- "The BOMBrowser: Select Date" dialog is displayed
- Select the first item, and click the "Select" button. The Assembly window appears
- Select a code below the top one (100000); then right-click and execute "Where used"

**Expected results**:
a 'Where used' window appears

**Passed**: [X]

#### 4.3.7 - valid where used (2)

**ID**: test#1106

**Source requirements**: req#1485

**Test description**:
- enter code "100000" in "BOMBrowser - Code list"
- right-click on the first entry
- select the "Show assembly by date" command
- "The BOMBrowser: Select Date" dialog is displayed
- Select the first item, and click the "Select" button. The Assembly window appears
- Select a code below the top one (100000); then right-click and execute "Valid where used"

**Expected results**:
a "Valid where used" window appears

**Passed**: [X]

#### 4.3.8 - menu->help->about

**ID**: test#1107

**Source requirements**: req#1009

**Test description**:
In the menu, select the Help -> About command

**Expected results**:
The "About" dialog is displayed. The dialog contains the current version and copyright information.

**Passed**: [X]

#### 4.3.9 - menu->window

**ID**: test#1108

**Source requirements**: req#1009

**Test description**:
- enter code 820037 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- Two windows are open. Select the "Window" menu in the "BOMBrowser - Assembly" window:

**Expected results**:
in the menu only one window is shown: "BOMBrowser - Codes list"

**Passed**: [X]

#### 4.3.10 - menu->file->close

**ID**: test#1109

**Source requirements**: req#1009

**Test description**:
- enter code 820037 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- Two windows are open. Select "File->Close" in the "BOMBrowser - Assembly" window:

**Expected results**:
The "BOMBrowser - Assembly" list closes. "BOMBrowser - Codes list" remains open.

**Passed**: [X]

#### 4.3.11 - Ctrl-Q  menu->file->close

**ID**: test#1110

**Source requirements**: req#1009

**Test description**:
- enter code 820037 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- two windows are open. Focus on "BOMBrowser - Assembly", then press CTRL-Q

**Expected results**:
The "BOMBrowser - Assembly" window closes. "BOMBrowser - Codes list" remains open.

**Passed**: [X]

#### 4.3.12 - menu->file->exit

**ID**: test#1111

**Source requirements**: req#1009

**Test description**:
- enter code 820037 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show latest assembly" command
- Two windows are open. Select "File->Exit" in the "BOMBrowser - Assembly" window:

**Expected results**:
a BOMBrowser confirmation dialog asking to exit is displayed.

**Passed**: [X]

**ID**: test#1112

**Source requirements**: req#1009

**Test description #2**:
- After the step above, click No

**Expected results #2**:
the assembly window is NOT closed

**Passed**: [X]

**ID**: test#1113

**Source requirements**: req#1009

**Test description #3**:
- After the step above, select "File->Exit" in the "BOMBrowser - Assembly" window:
- a BOMBrowser confirmation dialog asking to exit is displayed. Click Yes

**Expected results #3**:
The application terminates. No window is displayed

**Passed**: [X]

#### 4.3.15 - menu->file->exit

**ID**: test#1114

**Source requirements**: req#1009

**Test description**:
- enter code 820037 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- Two windows are open. Press CTRL-X

**Expected results**:
a BOMBrowser confirmation dialog asking to exit is displayed.

**Passed**: [X]

**ID**: test#1115

**Source requirements**: req#1009

**Test description #2**:
- After the step above, click No

**Expected results #2**:
the assembly window is NOT closed

**Passed**: [X]

**ID**: test#1116

**Source requirements**: req#1009

**Test description #3**:
- Press CTRL-X again
- a BOMBrowser confirmation dialog asking to exit is displayed. Click Yes

**Expected results #3**:
The application terminates. No window is displayed

**Passed**: [X]

#### 4.3.18 - menu->file->export as json / csv...

**ID**: test#1117

**Source requirements**: req#1482

**Test description**:
- enter code 820037 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- Select File->Export as JSON
- Save the file and reopen it in an editor

**Expected results**:
The file is formatted as JSON

**Passed**: [X]

**ID**: test#1118

**Source requirements**: req#1488

**Test description #2**:
Test description #2
- Select File->Export BOM...
- Save the file (with a .csv extension) and reopen it in an editor

**Expected results #2**:
- The file is formatted as CSV (SEMICOLON-separated fields)

**Passed**: [X]

#### 4.3.20 - menu->view->show up level 1

**ID**: test#1119

**Source requirements**: req#1483

**Test description**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show latest assembly" command
- select the first date by double-clicking it
- Select View->Show up level 1

**Expected results**:
The BOM is collapsed to display only the first level (top code, no children)

**Passed**: [X]

**ID**: test#1120

**Source requirements**: req#1483

**Test description #2**:
- Select View->Show up level 2

**Expected results #2**:
The BOM is collapsed to display only two levels (top code and its children)

**Passed**: [X]

**ID**: test#1121

**Source requirements**: req#1483

**Test description #3**:
- Select View->Show all levels

**Expected results #3**:
The BOM displays all levels

**Passed**: [X]

**ID**: test#1122

**Source requirements**: req#1483

**Test description #4**:
- Press CTRL-1

**Expected results #4**:
The BOM is collapsed to display only the first level (top code)

**Passed**: [X]

**ID**: test#1123

**Source requirements**: req#1483

**Test description #5**:
- Press CTRL-2

**Expected results #5**:
The BOM is collapsed to display only two levels (top code and its children)

**Passed**: [X]

**ID**: test#1124

**Source requirements**: req#1483

**Test description #6**:
- Press CTRL-A

**Expected results #6**:
The BOM displays all levels

**Passed**: [X]

#### 4.3.26 - Find

**Source requirements**: req#1485

**Preparatory steps**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- the BOMBrowser Assembly window is displayed

#### 4.3.27 - find ctrl-f

**ID**: test#1126

**Source requirements**: req#1486

**Preparatory steps**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- the BOMBrowser Assembly window is displayed

**Test description**:
press CTRL-F

**Expected results**:
The find dialog is displayed

**Passed**: [X]

#### 4.3.28 - find

**ID**: test#1127

**Source requirements**: req#1486

**Preparatory steps**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- the BOMBrowser Assembly window is displayed

**Test description**:
Select Search->Find from the menu

**Expected results**:
The find dialog is displayed

**Passed**: [X]

#### 4.3.29 - cancel

**ID**: test#1128

**Source requirements**: req#1486

**Preparatory steps**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- the BOMBrowser Assembly window is displayed

**Test description**:
- Select Search->Find
- The find dialog is displayed
- Click the "Close" button

**Expected results**:
The find dialog closes

**Passed**: [X]

#### 4.3.30 - find a code

**ID**: test#1129

**Source requirements**: req#1486

**Preparatory steps**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- the BOMBrowser Assembly window is displayed

**Test description**:
- Select Search->Find
- The find dialog is displayed
- Enter the code '810092'
- Click "Next" 3 times

**Expected results**:
A different instance of code 810092 is shown each time

**Passed**: [X]

**ID**: test#1130

**Source requirements**: req#1486

**Test description #2**:
- Click "Prev" 2 times

**Expected results #2**:
A different instance of code 810092 is shown each time

**Passed**: [X]

#### 4.3.32 - find a code

**ID**: test#1131

**Source requirements**: req#1486

**Preparatory steps**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- the BOMBrowser Assembly window is displayed

**Test description**:
- Select Search->Find
- The find dialog is displayed
- Enter the code '810092'
- Click "Next" 5 times
- Click "Prev" 5 times

**Expected results**:
After the last action, a "Data not found" dialog is displayed

**Passed**: [X]

#### 4.3.33 - find a code

**ID**: test#1132

**Source requirements**: req#1486

**Preparatory steps**:
- enter code 820099 in "BOMBrowser - Codes list"
- right-click on the first entry
- select the "Show assembly by date" command
- select the first date by double-clicking it
- the BOMBrowser Assembly window is displayed

**Test description**:
- Select Search->Find
- The find dialog is displayed
- Enter the code '810092'
- Click "Next" down through the BOM until a "Data not found" dialog appears

**Expected results**:
After the last action, a "Data not found" dialog is displayed

**Passed**: [X]

#### 4.3.34 - show latest assembly

**ID**: test#1133

**Source requirements**: req#1485

**Test description**:
- in the "Code list" window, select code 820017
- look at the right panel codegui. Verify that "Date to" is blank
- if not, edit the code and clear/adjust the "Date to" field accordingly
- from the RMB menu, select "Show latest assembly"

**Expected results**:
- The "Assembly" window is displayed
- The date in the title is replaced by "LATEST"
- Each listed code has an empty "Date to" field

**Passed**: [X]

#### 4.3.35 - show latest assembly

**ID**: test#1134

**Source requirements**: req#1485

**Test description**:
- in the "Code list" window, select code 100017-ENDED
- from the RMB menu, select "Show latest assembly"

**Expected results**:
- The "Assembly" window is displayed
- The date in the title is replaced by the "Date to" value

**Passed**: [X]

#### 4.3.36 - Menu file -> export data

**ID**: test#1135

**Source requirements**: req#1488

**Test description**:
- open code 820000 as "latest assembly" in the Assembly window
- Select File -> "Export data..."

**Expected results**:
- An "Export" dialog appears

**Passed**: [X]

**ID**: test#1136

**Source requirements**: req#1488

**Test description #2**:
- after the step above, click Close

**Expected results #2**:
- The dialog closes

**Passed**: [X]

**ID**: test#1137

**Source requirements**: req#1488

**Test description #3**:
- repeat the step above, but instead of clicking Cancel, select a directory and click "Export"

**Expected results #3**:
- The assembly files are copied into the selected folder

**Passed**: [X]

#### 4.3.39 - Menu file -> export data with url

**ID**: test#1138

**Source requirements**: req#1488

**Test description**:
- open code TEST-ASSY-TO-EXPORT as "latest assembly" in the Assembly window
- Select File -> "Export data..."
- In the new dialog, click the "Export" button

**Expected results**:
- An error dialog appears, but without any reference to CODE_WITH_URL

**Passed**: [X]

#### 4.3.40 - Show prototype assembly

#### 4.3.41 - Show prototype assembly

**ID**: test#1140

**Source requirements**: req#1485

**Preparatory steps**:
- look at code 610005 in the codes list window
- Check in the code gui right panel that the code has two dates and is not a prototype

**Test description**:
- look at code 610005 in the codes list window
- From the RMB menu, select "Show prototype assembly"

**Expected results**:
- the assembly window is displayed
- looking at the dates in the "code gui" right panel, the "prototype" start date is displayed for some codes

**Passed**: [X]

#### 4.3.42 - Show prototype assembly

**ID**: test#1141

**Source requirements**: req#1485

**Preparatory steps**:
- look at code 610005 in the codes list window
- Check in the code gui right panel that the code has two dates and is not a prototype

**Test description**:
- look at code 610005 in the codes list window
- From the RMB menu, select "Show latest assembly"

**Expected results**:
- the assembly window is displayed
- looking at the dates in the "code gui" right panel, no code shows a 'date to' value (i.e., no codes are prototypes)

**Passed**: [X]

### 4.4 - Check for loop

**ID**: test#1142

**Source requirements**: req#1487

**Test description**:
- look at code TEST-LOOP-A in the codes list window
- From the RMB menu, select "Show latest assembly"

**Expected results**:
A dialog reporting a loop error is displayed. The message suggests executing menu->Tools->Check bom

**Passed**: [X]

**ID**: test#1143

**Source requirements**: req#1487

**Test description #2**:
- Select menu->Tools->Check bom

**Expected results #2**:
A report stating 'ERROR loop detected' is displayed

**Passed**: [X]

#### 4.5.1 - BOM Color

##### 4.5.1.1 - Bom color (prep)

**Preparatory steps**:
the following configuration in bombrowser.ini is assumed:
bomcolors=
    gval1=COLOR,gval2=!A:fg=green
    gval1=COLOR,gval2=A:bg=pink
    gval1=COLOR,gval2=B:bold,fg=blue
    gval1=COLOR,gval2=C:italic
    gval1=COLOR,gaval2=Q:fg=red
    gval1=COLOR,qty=10.0=Q:bg=black
    gval1=COLOR,*gval2=F,gval2=G:bg=#00FFFF,fg=black

##### 4.5.1.2 - Bom color

**ID**: test#1146

**Source requirements**: req#1489

**Test description**:
Show the latest assembly "TEST-COLOR-A"

**Expected results**:
The first row (TEST-COLOR-A) is fg=black, bg=pink
(gval1=COLOR,gval2=A:bg=pink)

**Passed**: [X]

**ID**: test#1147

**Source requirements**: req#1489

**Test description #2**:
Look at the BOM color

**Expected results #2**:
The 2nd row (TEST-COLOR-B) is fg=blue, bold
(gval1=COLOR,gval2=B:bold,fg=blue)

**Passed**: [X]

**ID**: test#1148

**Source requirements**: req#1489

**Test description #3**:
Look at the BOM color

**Expected results #3**:
The 3rd row (TEST-COLOR-C) is fg=green, italic
(gval1=COLOR,gval2=C:italic, gval1=COLOR,gval2=!A:fg=green)

**Passed**: [X]

**ID**: test#1149

**Source requirements**: req#1489

**Test description #4**:
Look at the BOM color

**Expected results #4**:
The 4th row (TEST-COLOR-D) is fg=green
(gval1=COLOR,gval2=!A:fg=green)

**Passed**: [X]

**ID**: test#1150

**Source requirements**: req#1489

**Test description #5**:
Look at the BOM color

**Expected results #5**:
The 5th row (TEST-COLOR-E) is fg=green, bg=black
(gval1=COLOR,gval2=!A:fg=green, gval1=COLOR,qty=10.0=Q:bg=black)

**Passed**: [X]

**ID**: test#1151

**Source requirements**: req#1489

**Test description #6**:
Look at the BOM color

**Expected results #6**:
The 6th row (TEST-COLOR-F) is fg=red, bg=black
(gval1=COLOR,gaval2=Q:fg=red, gval1=COLOR,qty=10.0=Q:bg=black)

**Passed**: [X]

**ID**: test#1152

**Source requirements**: req#1489

**Test description #7**:
Look at the BOM color

**Expected results #7**:
The 7th row (TEST-COLOR-G) is fg=black, bg=cyan (#00ffff)
(gval1=COLOR,*gval2=F,gval2=G:bg=#00FFFF,fg=black)

**Passed**: [X]

#### 4.5.2 - Copy assembly

**ID**: test#1153

**Source requirements**: req#1488

**Test description**:
- Open assembly "TEST-ASSY-TO-EXPORT"
- From the menu, select Edit->Copy BOM (Full table)
- Paste the clipboard content into a text editor

**Expected results**:
The content of the BOM is copied:
- File paths are formatted to display only the filename (NOT the path)
- URLs are shown as-is

**Passed**: [X]

#### 4.5.3 - Code gui panel

**ID**: test#1492

**Source requirements**: req#1490

**Test description**:
- Open the latest assembly "820037"
- Verify that a 'Code gui panel' is displayed on the right side of the window

**Expected results**:
A 'Code gui panel' is displayed on the right side of the window

**Passed**: [X]

**ID**: test#1491

**Source requirements**: req#1490

**Test description #2**:
Click different rows and verify that the 'Code gui panel' updates accordingly

**Expected results #2**:
The 'Code gui panel' displays the information for the highlighted code

**Passed**: [X]

#### 4.5.5 - 'Valid where used' test

**ID**: test#1155

**Source requirements**: req#1485

**Test description**:
In the "Codes list" window, search for code 820017. Then select the right-click menu command "Valid where used"

**Expected results**:
- the "Valid where used" window is displayed
- every listed code has an empty "end to" date
- no codes are duplicated (at the top level)

**Passed**: [X]

#### 4.5.6 - 'Where used' test

**ID**: test#1157

**Source requirements**: req#1485

**Test description**:
In the "Codes list" window, search for code 820017. Then select the right-click menu command "Where used"

**Expected results**:
- the "Where used" window is displayed
- a few listed codes (excluding the top node) have a non-empty "end to" date. These codes may sometimes be repeated

**Passed**: [X]

#### 4.5.7 - BOMBrowser - Diff window

#### 4.5.8 - diff the same code

**ID**: test#1160

**Source requirements**: req#1493

**Test description**:
- In the "Codes list" window, search for code 82%
- Select a code with multiple revisions (e.g., 820012)
- Select the right-click menu command "Diff from"

**Expected results**:
- a select date dialog is displayed

**Passed**: [X]

**ID**: test#1161

**Source requirements**: req#1493

**Test description #2**:
- after the previous step, select the **2nd** date
- then click select

**Expected results #2**:
- A small diff dialog is displayed

**Passed**: [X]

**ID**: test#1162

**Source requirements**: req#1493

**Test description #3**:
- after the previous step, select the same code in the codes list window
- then select the right-click menu command "Diff to"

**Expected results #3**:
- a select date dialog is displayed

**Passed**: [X]

**ID**: test#1163

**Source requirements**: req#1493

**Test description #4**:
- after the previous step, select the **1st** date
- then click select

**Expected results #4**:
- The previous small dialog closes
- A new window titled "Diff window" is displayed
- The title bar displays the codes and the two selected dates
- The top part of the window displays the code and the two selected dates
- The body of the window displays the colorized diff between the two BOMs

**Passed**: [X]

**ID**: test#1164

**Source requirements**: req#1493

**Test description #5**:
- search for the selected code in the main body window

**Expected results #5**:
- below the code, the differences between the codes are displayed:
- the dates are different
- the iterations are different
- other differences may be present

**Passed**: [X]

#### 4.5.13 - diff two different codes

**ID**: test#1165

**Source requirements**: req#1493

**Test description**:
- in the "Codes list" window, search for the codes starting with 82%.
- select a code with multiple revisions (e.g. 820012)
- right-click and select the "Diff from" context menu command

**Expected results**:
- a select date dialog is displayed

**Passed**: [X]

**ID**: test#1166

**Source requirements**: req#1493

**Test description #2**:
- after the previous step, select the **2nd** date
- click Select

**Expected results #2**:
- A small diff dialog is displayed

**Passed**: [X]

**ID**: test#1167

**Source requirements**: req#1493

**Test description #3**:
- after the previous step, select a different code (e.g. 820011) in the codes list window
- right-click and select the "Diff to" context menu command

**Expected results #3**:
- a select date dialog is displayed

**Passed**: [X]

**ID**: test#1168

**Source requirements**: req#1493

**Test description #4**:
- after the previous step, select the **1st** date
- click Select

**Expected results #4**:
- The previous small dialog closes
- A new window named "Diff window" is displayed
- The title bar displays the codes and the two selected dates
- The top section of the window displays the code and the two selected dates
- The body of the window displays the color-coded diff of the two BOMs

**Passed**: [X]

**ID**: test#1169

**Source requirements**: req#1493

**Test description #5**:
- search for the 1st selected code in the window body

**Expected results #5**:
- the differences for the code are displayed below it:
- the codes are different
- other differences may be present

**Passed**: [X]

#### 4.5.18 - diff two different codes

**ID**: test#1170

**Source requirements**: req#1493, req#1494

**Test description**:
- open a diff window as described in the previous test
- search for the 1st selected code in the window body
- note which properties are marked with '-' and which ones with '+'
- click the '<->' button
- search for the 2nd selected code in the body

**Expected results**:
- the values previously marked with '-' are now marked with '+'
- the values previously marked with '+' are now marked with '-'

**Passed**: [X]

#### 4.5.19 - diff option: diff only top code

**ID**: test#1171

**Source requirements**: req#1493, req#1504

**Test description**:
- open a diff window between two different revisions *of code 820154*
- check the "Diff only the top code" checkbox

**Expected results**:
- only the top code is displayed
- the differing 'date_from' values are displayed (other fields may also be shown)

**Passed**: [X]

#### 4.5.20 - diff option: diff only top code

**ID**: test#1172

**Source requirements**: req#1493, req#1504

**Test description**:
- open a diff window between two codes:
  - 820017
  - 820018
- check the "Diff only the top code" checkbox

**Expected results**:
- only the top code is displayed
- the differing 'code' and 'descr' values are displayed (other fields may also be shown)

**Passed**: [X]

#### 4.5.21 - diff option: diff only main attributes

**ID**: test#1173

**Source requirements**: req#1493, req#1503

**Test description**:
- open a diff window between two different dates for code TEST-DIFF-ASSY
- check the "Diff only main attributes" checkbox

**Expected results**:
only the main attributes are displayed:
- description
- qty
- code
- ver

**Passed**: [X]

#### 4.5.22 - diff documents

**ID**: test#1174

**Source requirements**: req#1493

**Test description**:
Diff the two revisions of code TEST-DIFF-ASSY

**Expected results**:
The diff dialog reports that the document sets differ between the two codes

**Passed**: [X]

### 4.6 - BOMBrowser - Copy / revise code

#### 4.6.1 - BOMBrowser - Copy code

#### 4.6.2 - Copy code select date dialog

**ID**: test#1177

**Source requirements**: req#1506

**Test description**:
Test description
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command

**Expected results**:
A "BOM Browser select date dialog" appears

**Passed**: [X]

**ID**: test#1178

**Source requirements**: req#1506

**Test description #2**:
- after the step above, click Cancel

**Expected results #2**:
- the dialog disappears

**Passed**: [X]

**ID**: test#1179

**Source requirements**: req#1506

**Test description #3**:
- repeat the steps above until the dialog appears
- click Select

**Expected results #3**:
The Copy window appears

**Passed**: [X]

#### 4.6.5 - Copy code window

**ID**: test#1181

**Source requirements**: req#1506

**Test description**:
Test description
- enter code 820045 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry

**Expected results**:
- The Copy window appears
- the "old-Iter" matches the one selected in the "Select date" window

**Passed**: [X]

#### 4.6.6 - Copy code window

**ID**: test#1182

**Source requirements**: req#1506

**Test description**:
Test description
- enter code 820045 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *second* entry
- The Copy/revise window appears

**Expected results**:
the "Iter" matches the one selected in the "Select date" window

**Passed**: [X]

#### 4.6.7 - Copy code window

#### 4.6.8 - Cancel

**ID**: test#1184

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820045 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
click Close button

**Expected results**:
an exit confirmation dialog appears

**Passed**: [X]

**ID**: test#1185

**Source requirements**: req#1506

**Test description #2**:
- after the steps above, click **YES**

**Expected results #2**:
the "Copy window" closes

**Passed**: [X]

**ID**: test#1186

**Source requirements**: req#1506

**Test description #3**:
- repeat the steps above until the confirmation dialog appears
- click **NO**

**Expected results #3**:
the confirmation dialog closes; the "Copy window" remains open

**Passed**: [X]

#### 4.6.11 - Copy code window

**ID**: test#1187

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
- check editability of the following fields: New/Code, New/Iter, New/Description, New/Rev, New/Date from

**Expected results**:
*ONLY* the fields New/Code, New/Description, New/Date from, and New/Rev are editable

**Passed**: [X]

#### 4.6.12 - Copy code window

**ID**: test#1188

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
- check the New/Iter field

**Expected results**:
The New/Iter field value is 0

**Passed**: [X]

#### 4.6.13 - Copy error

**ID**: test#1189

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
- check that Old/code is equal to New/code
- click "Copy code" button

**Expected results**:
- An error dialog appears stating that the code already exists
- after clicking OK, the Copy window remains open

**Passed**: [X]

#### 4.6.14 - Confirmation dialog / success

**ID**: test#1190

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
- change New/code to "82004A"
- uncheck the "start edit dialog after copy/revision" checkbox
- click "Copy code" button
- A confirmation dialog appears; click No

**Expected results**:
the confirmation dialog disappears; the "BOMBrowser - copy code" window remains open

**Passed**: [X]

**ID**: test#1191

**Source requirements**: req#1506

**Test description #2**:
- after the steps above, click "Copy code" button again
- a confirmation dialog appears; click Yes

**Expected results #2**:
A success dialog appears

**Passed**: [X]

#### 4.6.16 - Confirmation dialog / success (2)

**ID**: test#1192

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
- check the "start edit dialog after copy/revision" checkbox
- change New/code to "82004B"
- click "Copy code" button
- A confirmation dialog appears; click Yes

**Expected results**:
- The editor for the new code appears
- Attached documents and a children list are present

**Passed**: [X]

#### 4.6.17 - Confirmation dialog / success (3)

**ID**: test#1193

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
- change New/code to "82004C"
- uncheck the "Copy document" checkbox
- click "Copy code" button
- A confirmation dialog appears; click Yes

**Expected results**:
- The editor for the new code appears
- Attached documents are NOT present
- The children list is present

**Passed**: [X]

#### 4.6.18 - Copy a code / date error

**ID**: test#1194

**Source requirements**: req#1506

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Copy code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Copy window appears

**Test description**:
- enter an invalid date (e.g. '99-99-1')
- click "Copy code" button

**Expected results**:
- An error dialog appears stating that the date format is incorrect
- after clicking OK, the Copy / Revise window remains open

**Passed**: [X]

#### 4.6.19 - copy a code (in proto mode)

**ID**: test#1195

**Source requirements**: req#1506

**Test description**:
- copy code "820041" from the code list window
- set the "New/code" field to a new non-existing code
- check the "P" ("Prototype") button
- click "Copy code" button
- A confirmation dialog appears; click Yes

**Expected results**:
- The code editor appears
- The date selector displays only prototype
- There is only **one** date in the combo box list
- The title bar date reports prototype

**Passed**: [X]

#### 4.6.20 - BOMBrowser - Revise code

##### 4.6.20.1 - Revise code window

**ID**: test#1197

**Source requirements**: req#1507

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Revise code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Revise window appears

**Test description**:
Check editability of the following fields: New/Code, New/Iter, New/Description, New/Rev, New/Date from

**Expected results**:
*ONLY* New/Description, New/Date from, and New/Rev are editable

**Passed**: [X]

##### 4.6.20.2 - Copy/revise code window

**ID**: test#1198

**Source requirements**: req#1507

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Revise code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Revise window appears

**Test description**:
check the New/Iter field

**Expected results**:
The New/Iter field value is equal to Old/Iter + 1

**Passed**: [X]

##### 4.6.20.3 - Revise a code / date error

**ID**: test#1199

**Source requirements**: req#1507

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Revise code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Revise window appears

**Test description**:
- enter an invalid date (e.g. '99-99-1')
- click "Revise code" button

**Expected results**:
- An error dialog appears stating that the date format is incorrect
- after clicking OK, the Copy / Revise window remains open

**Passed**: [X]

##### 4.6.20.4 - Revise a code / date error

**ID**: test#1200

**Source requirements**: req#1507

**Preparatory steps**:
- enter code 820040 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Revise code..." command
- A "BOM Browser select date dialog" appears; double-click the *first* entry
- The Revise window appears

**Test description**:
- enter a date equal to or earlier than Old/Date from
- click "Revise code" button

**Expected results**:
- An error dialog appears stating that the date is earlier than or equal to the existing one
- after clicking OK, the Copy / Revise window remains open

**Passed**: [X]

##### 4.6.20.5 - Revise a code

**ID**: test#1201

**Source requirements**: req#1507

**Test description**:
- revise code "820042" from the code list window
- set "New/Date from" to "Old/Date from" + 1 (or any date later than the old revision)
- prefix the default "New/Rev" field value with "bis_"
- prefix the default "New/Description" field value with "bis_"
- click "Revise code" button
- A confirmation dialog appears; click Yes

**Expected results**:
- The code editor appears
- Attached documents are present
- The children list is present
- The "From date" in the revision combo box matches the date from the previous dialog
- The "Description" in the editor window matches the value from the previous dialog (prefixed with 'bis_')
- The "Rev" in the editor window matches the value from the previous dialog (prefixed with 'bis_')

**Passed**: [X]

##### 4.6.20.6 - revise a code (in proto mode)

**ID**: test#1202

**Source requirements**: req#1507

**Test description**:
- revise code "820043" from the code list window
- check the "P" (Prototype) checkbox
- click "Revise code" button
- A confirmation dialog appears; click Yes

**Expected results**:
- The code editor appears
- The date selector also displays prototype

**Passed**: [X]

##### 4.6.20.7 - revise a prototype code to prototype

**ID**: test#1203

**Source requirements**: req#1507

**Test description**:
- revise code "820041" from the code list window (ensure the code already has a prototype revision; if not, create one)
- check the "Prototype" checkbox
- click "Revise code" button

**Expected results**:
- an error dialog reports that a prototype already exists

**Passed**: [X]

##### 4.6.20.8 - revise a prototype code to non-prototype

**ID**: test#1204

**Source requirements**: req#1507

**Test description**:
- revise code "820041" from the code list window (ensure the code already has a prototype revision; if not, create one)
- in the select date dialog, select the 2nd date (NOT the prototype one)
- set a date
- click "Revise code" button
- click Yes

**Expected results**:
- an edit dialog is displayed
- verify that the new date exists prior to the prototype date

**Passed**: [X]

##### 4.6.20.9 - Revise a code when some fields will be reset

**ID**: test#1205

**Source requirements**: req#1507, req#1513

**Preparatory steps**:
- Ensure the following settings are configured:
  gvalnames=
      [...]
      gval6:Mfg.2
      gval5:Mfg.2 PN
      [...]
  after_copy_set_values_to=
       gval6=
       gval5=ZZZZ
  after_revise_set_values_to=
       gval6=
       gval5=ZZZZ
- edit code 810077, set Mfg.2 to "aaa" and Mfg.2 PN to "bbb"

**Test description**:
- revise code 810088

**Expected results**:
- in the edit dialog, verify that field Mfg.2 is empty and Mfg.2 PN is equal to ZZZZ

**Passed**: [X]

##### 4.6.20.10 - Copy a code when some fields will be reset

**ID**: test#1206

**Source requirements**: req#1507, req#1513

**Preparatory steps**:
- Ensure the following settings are configured:
  gvalnames=
      [...]
      gval6:Mfg.2
      gval5:Mfg.2 PN
      [...]
  after_copy_set_values_to=
       gval6=
       gval5=ZZZZ
  after_revise_set_values_to=
       gval6=
       gval5=ZZZZ
- edit code 810077, set Mfg.2 to "aaa" and Mfg.2 PN to "bbb"

**Test description**:
- copy code 810088 to 810088-bis

**Expected results**:
- in the edit dialog, verify that field Mfg.2 is empty and Mfg.2 PN is equal to ZZZZ

**Passed**: [X]

##### 4.6.20.11 - revise a code and its gavals

**ID**: test#1207

**Source requirements**: req#1507

**Preparatory steps**:
- Ensure the following settings are configured:
  gavalnames=
      [...]
      gaval1:Planned[clist:1;0]
      [...]
- edit code 820078:
  - set "0" in the first two rows of the children under column "Planned"
  - set "1" in the 3rd row of the children under column "Planned"

**Test description**:
- revise code 820078

**Expected results**:
- in the edit dialog, verify that the "Planned" fields for children
  match the modified values

**Passed**: [X]

##### 4.6.20.12 - revise a standard code

**ID**: test#1516

**Source requirements**: req#1507

**Test description**:
- search for code 820099 in the "codes list window"
- right-click to open the revise dialog for code 820099

**Expected results**:
- in the revise dialog, verify that the new date defaults to today's date

**Passed**: [X]

##### 4.6.20.13 - revise a standard code

**ID**: test#1517

**Source requirements**: req#1507

**Preparatory steps**:
- revise code 820099 (with today as 'new date from')

**Test description**:
- initiate another revision of the same code

**Expected results**:
- in the revise dialog, verify that the date is set to tomorrow (today + 1)

**Passed**: [X]

#### 4.6.21 - BomBrowser - Edit code

**Source requirements**: req#1509

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

#### 4.6.22 - Edit code / Rev field

**ID**: test#1209

**Source requirements**: req#1509

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- modify the "rev" field by prefixing it with "bis_"
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the "rev" field retains the modified value

**Passed**: [X]

#### 4.6.23 - Insert title HERE

**Preparatory steps**:
Insert preparation description HERE

#### 4.6.24 - Edit code / Default unit field

**ID**: test#1210

**Source requirements**: req#1509

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- modify the "Default unit" field by prefixing it with "bis_"
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the "Default unit" field retains the modified value

**Passed**: [X]

#### 4.6.25 - Edit code / Description field

**ID**: test#1211

**Source requirements**: req#1509

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- modify the "Description" field by prefixing it with "bis_"
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the "Description" field retains the modified value

**Passed**: [X]

#### 4.6.26 - Edit code / Generic properties field

**ID**: test#1212

**Source requirements**: req#1509

**Test description**:
repeat the test for all "Generic properties" fields:
- modify the field by prefixing it with "bis_"
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code and verify the field value

**Expected results**:
the "Generic property" field retains the modified value

**Passed**: [X]

#### 4.6.27 - Add/Del/View a drawing

**ID**: test#1213

**Source requirements**: req#1511

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- right-click on the drawing list panel
- execute the "add drawing" command, attaching a file as a drawing
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the added drawing is still present

**Passed**: [X]

**ID**: test#1214

**Source requirements**: req#1511

**Test description #2**:
- drag and drop a file onto the drawing panel
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results #2**:
the added drawing is still present

**Passed**: [X]

**ID**: test#1215

**Source requirements**: req#1511

**Test description #3**:
- right-click on the drawing list panel
- execute the "add drawing" command, selecting MULTIPLE files
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results #3**:
the added drawings are present

**Passed**: [ ]

**ID**: test#1216

**Source requirements**: req#1511

**Test description #4**:
- right-click a drawing on the drawing list panel
- execute the "delete drawing" command
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results #4**:
the removed drawing is no longer present

**Passed**: [X]

**ID**: test#1217

**Source requirements**: req#1511

**Test description #5**:
- right-click on the drawing list panel
- execute the "delete drawing" command on multiple drawings
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results #5**:
the removed drawings are no longer present

**Passed**: [X]

**ID**: test#1218

**Source requirements**: req#1511

**Test description #6**:
- right-click a drawing on the drawing list panel
- execute the "view drawing" command

**Expected results #6**:
the selected drawing is displayed

**Passed**: [X]

**ID**: test#1219

**Source requirements**: req#1511

**Test description #7**:
- double-click a drawing in the drawing list panel

**Expected results #7**:
the selected drawing is displayed

**Passed**: [X]

**ID**: test#1220

**Source requirements**: req#1511

**Test description #8**:
- select multiple drawings
- right-click on the drawing list panel
- execute the "view drawing" command

**Expected results #8**:
the selected drawings are displayed

**Passed**: [X]

#### 4.6.35 - Copy multiple drawings

**ID**: test#1221

**Source requirements**: req#1515

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears
- enter code 820002 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- A second Edit code window appears

**Test description**:
- In the first edit window, select multiple drawings
- right-click the drawings list
- execute the "copy drawings lines" command
- In the second edit window, right-click the drawings list
- execute the "paste drawings lines" command
- click "Save..." button
- click "Close"
- reopen the edit window for the 2nd code as described in the preparatory steps

**Expected results**:
the copied drawings are present

**Passed**: [X]

#### 4.6.36 - del single children

**ID**: test#1222

**Source requirements**: req#1510

**Test description**:
- right-click a row in the children list panel
- execute the "delete row" command
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the removed item is no longer present

**Passed**: [X]

#### 4.6.37 - del multiple children

**ID**: test#1223

**Source requirements**: req#1510

**Test description**:
- right-click on the children list panel
- execute the "delete row" command on multiple lines
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the removed items are no longer present

**Passed**: [X]

#### 4.6.38 - Copy multiple children

**ID**: test#1224

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears
- enter code 820002 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- A second Edit code window appears

**Test description**:
- In the first edit window, select multiple children
- right-click the children list
- execute the "copy lines" command
- In the second edit window, right-click the children list
- execute the "paste lines" command
- click "Save..." button
- click "Close"
- reopen the edit window for the 2nd code as described in the preparatory steps

**Expected results**:
the copied children are present

**Passed**: [X]

#### 4.6.39 - add a child

**ID**: test#1225

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- right-click a line in the children list panel
- execute the "insert row after" command
- in the new row, enter an existing code in the "code" column
- the fields "code-id" and "description" will autocomplete
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the added item is present

**Passed**: [X]

#### 4.6.40 - add a child

**ID**: test#1226

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- right-click a line in the children list panel
- execute the "insert row before" command
- in the new row, enter an existing code in the "code" column
- the fields "code-id" and "description" will autocomplete
- click "Save..." button
- click "OK"
- click "Close"
- reopen the edit window for the same code as described in the preparatory steps

**Expected results**:
the added item is present

**Passed**: [X]

#### 4.6.41 - add multiple child

**ID**: test#1227

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- select multiple lines in the children list panel
- right-click and execute the "insert row before" command

**Expected results**:
Multiple lines are inserted. The number of inserted lines matches
the number of selected lines.

**Passed**: [X]

#### 4.6.42 - non existant code

**ID**: test#1228

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, try to change a code in a row to a non-existing code (e.g. 'z')

**Expected results**:
the modified cell turns yellow

**Passed**: [X]

**ID**: test#1229

**Source requirements**: req#1510

**Test description #2**:
- click "Save"

**Expected results #2**:
an error dialog appears stating "...the code '...' in row..." contains an error

**Passed**: [X]

#### 4.6.44 - duplicate code

**ID**: test#1230

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, try to change a code in a row to an already existing code (e.g. matching the previous or next row)
- click "Save" button

**Expected results**:
an error dialog is displayed stating that there is a duplicate code

**Passed**: [X]

#### 4.6.45 - wrong qty

**ID**: test#1231

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, try to change the 'qty' field in a row to a non-numeric value

**Expected results**:
the cell turns yellow

**Passed**: [X]

**ID**: test#1232

**Source requirements**: req#1510

**Test description #2**:
- click "Save"

**Expected results #2**:
an error dialog appears stating that the value is invalid

**Passed**: [X]

#### 4.6.47 - wrong each

**ID**: test#1233

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, try to change the 'each' field in a row to a non-numeric value

**Expected results**:
the cell turns yellow

**Passed**: [X]

**ID**: test#1234

**Source requirements**: req#1510

**Test description #2**:
- click "Save"

**Expected results #2**:
an error dialog appears stating that the value is invalid

**Passed**: [X]

#### 4.6.49 - sorting

**ID**: test#1235

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, sort the rows by code (click the "code" column header)
- note the values in the "seq" column
- remove a row

**Expected results**:
the seq values are reordered based on the current sequence.

**Passed**: [X]

#### 4.6.50 - sorting

**ID**: test#1236

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, sort the rows by code (click the "code" column header)
- note the values in the "seq" column
- perform an "insert row before"

**Expected results**:
the seq values are reordered based on the current sequence.

**Passed**: [X]

#### 4.6.51 - sorting

**ID**: test#1237

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, sort the rows by code (click the "code" column header)
- note the values in the "seq" column
- perform an "insert row after"

**Expected results**:
the seq values are reordered based on the current sequence.

**Passed**: [X]

#### 4.6.52 - Move the children UP

**ID**: test#1238

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, select a row in the middle
- click the UP button

**Expected results**:
the selected row moves up by one position

**Passed**: [X]

**ID**: test#1239

**Source requirements**: req#1510

**Test description #2**:
- in the children panel, select the first row
- click the UP button

**Expected results #2**:
nothing changes

**Passed**: [X]

**ID**: test#1240

**Source requirements**: req#1510

**Test description #3**:
- in the children panel, select the first rows
- click the UP button

**Expected results #3**:
nothing changes

**Passed**: [X]

**ID**: test#1241

**Source requirements**: req#1510

**Test description #4**:
- in the children panel, select multiple rows in the middle
- click the UP button

**Expected results #4**:
the selected rows move up by one position

**Passed**: [X]

#### 4.6.56 - Move the children DOWN

**ID**: test#1242

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, select a row in the middle
- click the DOWN button

**Expected results**:
the selected row moves down by one position

**Passed**: [X]

**ID**: test#1243

**Source requirements**: req#1510

**Test description #2**:
- in the children panel, select the last row
- click the DOWN button

**Expected results #2**:
nothing changes

**Passed**: [X]

**ID**: test#1244

**Source requirements**: req#1510

**Test description #3**:
- in the children panel, select the last rows
- click the DOWN button

**Expected results #3**:
nothing changes

**Passed**: [X]

**ID**: test#1245

**Source requirements**: req#1510

**Test description #4**:
- in the children panel, select multiple rows in the middle
- click the DOWN button

**Expected results #4**:
the selected rows move down by one position

**Passed**: [X]

#### 4.6.60 - Move the children to the TOP

**ID**: test#1246

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, select a row in the middle
- click the TOP button

**Expected results**:
the selected row moves to the TOP

**Passed**: [X]

**ID**: test#1247

**Source requirements**: req#1510

**Test description #2**:
- in the children panel, select the first row
- click the TOP button

**Expected results #2**:
nothing changes

**Passed**: [X]

**ID**: test#1248

**Source requirements**: req#1510

**Test description #3**:
- in the children panel, select the first rows
- click the TOP button

**Expected results #3**:
nothing changes

**Passed**: [X]

**ID**: test#1249

**Source requirements**: req#1510

**Test description #4**:
- in the children panel, select multiple rows in the middle
- click the TOP button

**Expected results #4**:
the selected rows move to the TOP

**Passed**: [X]

#### 4.6.64 - Move the children BOTTOM

**ID**: test#1250

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- in the children panel, select a row in the middle
- click the BOTTOM button

**Expected results**:
the selected row moves to the BOTTOM

**Passed**: [X]

**ID**: test#1251

**Source requirements**: req#1510

**Test description #2**:
- in the children panel, select the last row
- click the BOTTOM button

**Expected results #2**:
nothing changes

**Passed**: [X]

**ID**: test#1252

**Source requirements**: req#1510

**Test description #3**:
- in the children panel, select the last rows
- click the BOTTOM button

**Expected results #3**:
nothing changes

**Passed**: [X]

**ID**: test#1253

**Source requirements**: req#1510

**Test description #4**:
- in the children panel, select multiple rows in the middle
- click the BOTTOM button

**Expected results #4**:
the selected rows move to the BOTTOM

**Passed**: [X]

#### 4.6.68 - Edit code / File -> close

**ID**: test#1254

**Source requirements**: req#1009

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- select the menu File->close

**Expected results**:
the edit window is closed

**Passed**: [X]

#### 4.6.69 - Edit code / File -> exit

**ID**: test#1255

**Source requirements**: req#1009

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- select the menu File->exit

**Expected results**:
a dialog opens asking if you want to exit the application

**Passed**: [X]

**ID**: test#1256

**Source requirements**: req#1009

**Test description #2**:
- press no

**Expected results #2**:
the dialog is closed, the edit window is shown

**Passed**: [X]

**ID**: test#1257

**Source requirements**: req#1009

**Test description #3**:
- repeat the steps above and press yes instead of pressing no

**Expected results #3**:
the application is closed, no window is open

**Passed**: [X]

#### 4.6.72 - Edit code / CTRL-Q

**ID**: test#1258

**Source requirements**: req#1009

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- Press CTRL-Q

**Expected results**:
the edit window is closed

**Passed**: [X]

#### 4.6.73 - Edit code / Windows

**ID**: test#1259

**Source requirements**: req#1009

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- select the Windows menu

**Expected results**:
the open windows are shown (with the exception of the current one)

**Passed**: [X]

#### 4.6.74 - Edit code / Help->about

**ID**: test#1260

**Source requirements**: req#1009

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- select the menu Help->about

**Expected results**:
the about dialog is shown

**Passed**: [X]

#### 4.6.75 - search code

**ID**: test#1261

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- click with the RMB on the children list panel
- execute the command "search code" on a line

**Expected results**:
The "BOMBrowser - Search code" dialog appears

**Passed**: [X]

#### 4.6.76 - search code

**ID**: test#1262

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- click with the RMB on the children list panel
- execute the command "search code" on a line
- The "BOMBrowser - Search code" dialog appears
- search for a code in the dialog (e.g. 810001)
- select the first result
- press OK

**Expected results**:
the dialog is closed and the new code replaces the old one

**Passed**: [X]

#### 4.6.77 - search code

**ID**: test#1263

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- click with the RMB on the children list panel
- execute the command "search code" on a line
- The "BOMBrowser - Search code" dialog appears
- search for a code in the dialog (e.g. 810007)
- press Cancel

**Expected results**:
- the dialog is closed
- the new code **didn't** replace the original one

**Passed**: [X]

#### 4.6.78 - delete revision

**ID**: test#1264

**Source requirements**: req#1512

**Preparatory steps**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- take this copy, and revise it 3 times (changing the "from" date to avoid conflicts)
- Edit this code

**Test description**:
- From menu -> edit, select delete item revision

**Expected results**:
a confirmation dialog is shown

**Passed**: [X]

**ID**: test#1265

**Source requirements**: req#1512

**Test description #2**:
- press no

**Expected results #2**:
nothing happens

**Passed**: [X]

**ID**: test#1266

**Source requirements**: req#1512

**Test description #3**:
- From menu -> edit, select delete item revision
- a confirmation dialog is shown, press yes

**Expected results #3**:
- a confirmation dialog is shown, saying that the revision is deleted. Press OK.
- the previously selected revision is removed

**Passed**: [X]

#### 4.6.81 - delete revision

**ID**: test#1267

**Source requirements**: req#1512

**Preparatory steps**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- take this copy, and revise it 3 times (changing the "from" date to avoid conflicts)
- Edit this code

**Test description**:
- From menu -> edit, select delete revision
- repeat the step above until only one revision is present
- From menu -> edit, select delete revision (again)

**Expected results**:
an error dialog box is shown saying that it is not possible to delete the last revision

**Passed**: [X]

#### 4.6.82 - delete revision

**ID**: test#1268

**Source requirements**: req#1512

**Preparatory steps**:


**Test description**:
- Enter the edit dates window, and insert a valid "end to" date in the first row. Then save the results
- From the edit window, delete the first revision
- Delete the last revision

**Expected results**:
- after deleting, the code "from date" is the same as the previous first revision
- the final "to date" is the same as the previous last revision

**Passed**: [X]

#### 4.6.83 - delete code

**ID**: test#1269

**Source requirements**: req#1512

**Preparatory steps**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- take this copy, and revise it 3 times (changing the "from" date to avoid conflicts)
- Edit this code

**Test description**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- Edit this code
- From menu->edit select "delete code"

**Expected results**:
a confirmation dialog appears

**Passed**: [X]

#### 4.6.84 - delete code

**ID**: test#1270

**Source requirements**: req#1512

**Preparatory steps**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- take this copy, and revise it 3 times (changing the "from" date to avoid conflicts)
- Edit this code

**Test description**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- Edit this code
- From menu->edit select "delete code"
- a confirmation dialog appears, press no

**Expected results**:
nothing happens

**Passed**: [X]

#### 4.6.85 - delete code

**ID**: test#1271

**Source requirements**: req#1512

**Preparatory steps**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- take this copy, and revise it 3 times (changing the "from" date to avoid conflicts)
- Edit this code

**Test description**:
- Take a code from the code list GUI, copy it (to avoid problems with the parent dates)
- Edit this code
- From menu->edit select "delete code"
- a confirmation dialog appears, press yes

**Expected results**:
- a confirmation dialog appears, press OK
- the edit dialog is no longer shown

**Passed**: [X]

**ID**: test#1272

**Source requirements**: req#1512

**Test description #2**:
- search for the deleted code in the codes list window

**Expected results #2**:
- the code is no longer shown

**Passed**: [X]

#### 4.6.87 - change revision

**ID**: test#1273

**Source requirements**: req#1509

**Preparatory steps**:
- Take a code from the code list GUI with multiple revisions
- Edit this code

**Test description**:
- Using the "From/to date" QComboBox, change the revision of the code
- in parallel make one change in a field for each revision (insert the "from" date to help the test) and press Save
- repeat the step above for each revision
- Using the "From/to date" QComboBox, change the revision of the code

**Expected results**:
- The dialog shows, for each revision, the change performed in the step above
- The dialog title reflects the code date

**Passed**: [X]

#### 4.6.88 - change revision without saving

**ID**: test#1274

**Source requirements**: req#1509

**Preparatory steps**:
- Take a code from the code list GUI with multiple revisions
- Edit this code

**Test description**:
- make one change in the Description field
- Using the "From/to date" QComboBox, change the date of the code

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

**ID**: test#1275

**Source requirements**: req#1509

**Test description #2**:
- press no

**Expected results #2**:
- the confirmation dialog is closed
- the revision is changed
- the change is lost

**Passed**: [X]

#### 4.6.90 - change revision without saving

**ID**: test#1276

**Source requirements**: req#1509

**Preparatory steps**:
- Take a code from the code list GUI with multiple revisions
- Edit this code

**Test description**:
- make one change in the Description field
- Using the "From/to date" QComboBox, change the date of the code

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

**ID**: test#1277

**Source requirements**: req#1509

**Test description #2**:
- press cancel

**Expected results #2**:
- the dialog is closed
- the revision is **not** changed
- the change is still present

**Passed**: [X]

#### 4.6.92 - change revision without saving

**ID**: test#1278

**Source requirements**: req#1509

**Preparatory steps**:
- Take a code from the code list GUI with multiple revisions
- Edit this code

**Test description**:
- make one change in the Description field
- Using the "From/to date" QComboBox, change the date of the code

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

**ID**: test#1279

**Source requirements**: req#1509

**Test description #2**:
- press yes

**Expected results #2**:
- the dialog is closed
- the revision is changed
- the change was saved

**Passed**: [X]

#### 4.6.94 - Make a change without saving

**ID**: test#1280

**Source requirements**: req#1509

**Preparatory steps**:
- Take a code from the code list GUI with multiple revisions
- Edit this code

**Test description**:
- make one change in a field
- press Close

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

**ID**: test#1281

**Source requirements**: req#1509

**Test description #2**:
- Press **cancel**

**Expected results #2**:
- The previous window is shown. The change is not lost

**Passed**: [X]

**ID**: test#1282

**Source requirements**: req#1509

**Test description #3**:
- repeat the test until the dialog is shown
- Press **no**

**Expected results #3**:
- The edit window is closed
- reopening the edit window, check that the change was **not** saved

**Passed**: [X]

#### 4.6.97 - Make a change saving

**ID**: test#1283

**Source requirements**: req#1509

**Preparatory steps**:
- Take a code from the code list GUI with multiple revisions
- Edit this code

**Test description**:
- make one change in a field
- press Close

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

**ID**: test#1284

**Source requirements**: req#1509

**Test description #2**:
- Press **yes**

**Expected results #2**:
- The edit window is closed
- reopening the edit window, check that the change was saved

**Passed**: [X]

#### 4.6.99 - remove a child without saving

**ID**: test#1285

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- remove an item in the children section
- press Close button

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.100 - insert a child without saving

**ID**: test#1286

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- insert (before) an item in the children section
- press Close button

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.101 - insert a child without saving

**ID**: test#1287

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- insert (after) an item in the children section
- press Close button

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.102 - change child without saving

**ID**: test#1288

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- perform a "search code" over an item in the children section
- press OK button
- press "Close"

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.103 - add drawing without saving

**ID**: test#1289

**Source requirements**: req#1511

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- perform an "add drawing" in the drawings section
- press Close button

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.104 - remove a drawing without saving

**ID**: test#1290

**Source requirements**: req#1511

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- perform a "delete drawing" in the drawings section
- press Close button

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.105 - add a duplicate code

**ID**: test#1291

**Source requirements**: req#1510

**Preparatory steps**:
- enter code 820001 in the "BOMBrowser codes list" window
- click Search
- right-click the first entry and select "Edit code..." command
- The Edit code window appears

**Test description**:
- add two identical child codes
- press Save

**Expected results**:
- An error dialog is shown saying that there is a code duplication

**Passed**: [X]

#### 4.6.106 - add a code to an empty children list

**ID**: test#1292

**Source requirements**: req#1510

**Preparatory steps**:
- Take a code from the code list GUI without children (e.g. an 8100xx code)
- Edit this code

**Test description**:
- add a new child code, using the RMB menu
- a new line is added
- insert a new child

**Expected results**:
- the code is added to the child list

**Passed**: [X]

#### 4.6.107 - exit without saving

**ID**: test#1293

**Source requirements**: req#1510

**Preparatory steps**:
- Take a code from the code list GUI without children (e.g. an 8100xx code)
- Edit this code

**Test description**:
- close the window (click on the upper right "X" icon)

**Expected results**:
- the edit window closes

**Passed**: [X]

#### 4.6.108 - exit without saving

**ID**: test#1294

**Source requirements**: req#1509

**Preparatory steps**:
- Take a code from the code list GUI without children (e.g. an 8100xx code)
- Edit this code

**Test description**:
- change a field in the edit window
- close the window (click on the upper right "X" icon)

**Expected results**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

**ID**: test#1295

**Source requirements**: req#1509

**Test description #2**:
- Press **cancel**

**Expected results #2**:
- the edit window is still open

**Passed**: [X]

**ID**: test#1296

**Source requirements**: req#1509

**Test description #3**:
- Repeat the steps of test #2
- Press no

**Expected results #3**:
- the edit window closes

**Passed**: [X]

#### 4.6.111 - Code Properties (file)

**ID**: test#1297

**Source requirements**: req#1509, req#1513, req#1514

**Preparatory steps**:
For the following tests it is assumed that the following
fields are present in bombrowser.ini
gvalnames=
     [...]
     gval7:TestFile[file]
     gval8:Test2[list:T2V1;T2V2;T2V3,with space and comma]
     gval9:Trans.[clist:;T]
[...]
gavalnames=
    [...]
    gaval1:Planned[clist:1;0]

**Test description**:
- Open the edit window on the code 810001
- Locate the field "TestFile"
- Press the "..." button

**Expected results**:
- The Open file dialog opens

**Passed**: [X]

**ID**: test#1298

**Source requirements**: req#1509

**Test description #2**:
- press cancel

**Expected results #2**:
- The Open file dialog closes
- The field remains empty

**Passed**: [X]

**ID**: test#1299

**Source requirements**: req#1509

**Test description #3**:
- press "..." button again
- Select a file then press Open

**Expected results #3**:
- The Open file dialog closes
- The field contains the file path

**Passed**: [X]

**ID**: test#1300

**Source requirements**: req#1509

**Test description #4**:
- press the Save button
- press the Close button
- reopen the edit window on the same code

**Expected results #4**:
- The field still contains the selected value

**Passed**: [X]

**ID**: test#1301

**Source requirements**: req#1509

**Test description #5**:
- change the value of the field by typing directly in the line edit widget
- press the Save button
- press the Close button
- reopen the edit window on the same code

**Expected results #5**:
- The field still contains the selected value

**Passed**: [X]

**ID**: test#1302

**Source requirements**: req#1509

**Test description #6**:
- change the value of the field
- press the Close button

**Expected results #6**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.117 - Code Properties (list)

**ID**: test#1303

**Source requirements**: req#1509, req#1513, req#1514

**Preparatory steps**:
For the following tests it is assumed that the following
fields are present in bombrowser.ini
gvalnames=
     [...]
     gval7:TestFile[file]
     gval8:Test2[list:T2V1;T2V2;T2V3,with space and comma]
     gval9:Trans.[clist:;T]
[...]
gavalnames=
    [...]
    gaval1:Planned[clist:1;0]

**Test description**:
- Open the edit window on the code 810001
- Locate the field "Test2"
- Press the "..." button

**Expected results**:
- The list box dialog opens

**Passed**: [X]

**ID**: test#1304

**Source requirements**: req#1509

**Test description #2**:
- press in the text field (NOT in the list box)
- Press the "..." button
- press in the text field (NOT in the list box)

**Expected results #2**:
- The dialog closes
- The field remains empty

**Passed**: [X]

**ID**: test#1305

**Source requirements**: req#1509

**Test description #3**:
- press "..." button again
- Select a value

**Expected results #3**:
- The field contains the selected value

**Passed**: [X]

**ID**: test#1306

**Source requirements**: req#1509

**Test description #4**:
- press the Save button
- press the Close button
- reopen the edit window on the same code

**Expected results #4**:
- The field still contains the selected value

**Passed**: [X]

**ID**: test#1307

**Source requirements**: req#1509

**Test description #5**:
- change the value of the field by typing directly in the line edit widget
- press the Save button
- press the Close button
- reopen the edit window on the same code

**Expected results #5**:
- The field still contains the selected value

**Passed**: [X]

**ID**: test#1308

**Source requirements**: req#1509

**Test description #6**:
- change the value of the field
- press the Close button

**Expected results #6**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.123 - Code Properties (clist)

**ID**: test#1309

**Source requirements**: req#1509, req#1513, req#1514

**Preparatory steps**:
For the following tests it is assumed that the following
fields are present in bombrowser.ini
gvalnames=
     [...]
     gval7:TestFile[file]
     gval8:Test2[list:T2V1;T2V2;T2V3,with space and comma]
     gval9:Transparent[clist:0;1]
[...]
gavalnames=
    [...]
    gaval1:Planned[clist:1;0]

**Test description**:
- Open the edit window on the code 810001
- Locate the field "Transparent"
- Press the adjacent button

**Expected results**:
- The list box dialog opens

**Passed**: [X]

**ID**: test#1310

**Source requirements**: req#1509

**Test description #2**:
- press elsewhere

**Expected results #2**:
- The menu closes
- The field remains empty

**Passed**: [X]

**ID**: test#1311

**Source requirements**: req#1509

**Test description #3**:
- press button again
- Select a value

**Expected results #3**:
- The field contains the selected value

**Passed**: [X]

**ID**: test#1312

**Source requirements**: req#1509

**Test description #4**:
- press the Save button
- press the Close button
- reopen the edit window on the same code

**Expected results #4**:
- The field still contains the selected value

**Passed**: [X]

**ID**: test#1313

**Source requirements**: req#1509

**Test description #5**:
- change the value of the field
- press the Close button

**Expected results #5**:
- A dialog is shown saying that the form was changed and asking if you want to save.

**Passed**: [X]

#### 4.6.128 - Two changes at the same time

**ID**: test#1314

**Source requirements**: req#1509

**Preparatory steps**:
Open two Edit windows for the same code

**Test description**:
- change a parameter (e.g. rev) in the first edit window
- save in the first edit window
- close the first edit window
- change the same parameter (rev) in the *second* edit window in a different way
- save in the second edit window

**Expected results**:
A dialog showing "The data was changed by another user. Are you sure you want to overwrite it?" appears

**Passed**: [X]

**ID**: test#1315

**Source requirements**: req#1509

**Test description #2**:
- after the dialog is shown, press YES
- check that the parameter changed in the code matches the second change

**Expected results #2**:
- the edit window is closed
- the changed parameter was updated according to the second change

**Passed**: [X]

#### 4.6.130 - Two changes at the same time

**ID**: test#1316

**Source requirements**: req#1509

**Preparatory steps**:
Open two Edit windows for the same code

**Test description**:
- change a parameter (e.g. rev) in the first edit window
- save in the first edit window
- close the first edit window
- change the same parameter (rev) in the *second* edit window in a different way
- save in the second edit window
- A dialog showing "The data was changed by another user. Are you sure you want to overwrite it?" appears
- press NO

**Expected results**:
- the edit window is still open
- the changed parameter was updated according to the first change

**Passed**: [X]

#### 4.6.131 - Edit code, edit URL

**ID**: test#1317

**Source requirements**: req#1511

**Preparatory steps**:
- Open the Edit window on the code CODE_WITH_URL
- Open the drawing tab

**Test description**:
- right-click, and select add URL

**Expected results**:
- an "enter URL" window is opened

**Passed**: [X]

**ID**: test#1318

**Source requirements**: req#1511

**Test description #2**:
- enter a description and a URL
- press Save

**Expected results #2**:
a new URL entry is shown, with the newly inserted values

**Passed**: [X]

**ID**: test#1319

**Source requirements**: req#1511

**Test description #3**:
right-click in the drawing TAB, and select edit drawings

**Expected results #3**:
- an "enter URL" window is opened

**Passed**: [X]

**ID**: test#1320

**Source requirements**: req#1511

**Test description #4**:
- update the description and a URL
- press Save

**Expected results #4**:
the description and URL are updated accordingly

**Passed**: [X]

**ID**: test#1321

**Source requirements**: req#1511

**Test description #5**:
- right-click in the drawing TAB, and select edit drawings
- update the description and a URL
- press Cancel

**Expected results #5**:
the entry is NOT updated

**Passed**: [X]

#### 4.6.136 - Edit code, undo

**ID**: test#1322

**Source requirements**: req#1509

**Preparatory steps**:
- Open the Edit window on the code 810011
- change the description by appending an "w"

**Test description**:
- From the edit menu, select Undo

**Expected results**:
- The description change is reverted

**Passed**: [X]

### 4.7 - BomBrowser - Edit date

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

#### 4.7.1 - Cancel button

**ID**: test#1327

**Source requirements**: req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
press the Cancel button

**Expected results**:
the edit dates dialog is closed

**Passed**: [X]

#### 4.7.2 - Save button

**ID**: test#1328

**Source requirements**: req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
press the Save button

**Expected results**:
an information dialog is shown

**Passed**: [X]

**ID**: test#1329

**Source requirements**: req#1518

**Test description #2**:
- press OK

**Expected results #2**:
the edit dates dialog is closed

**Passed**: [X]

#### 4.7.4 - Modify date

**ID**: test#1330

**Source requirements**: req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the bottom row to a valid one (but earlier)
- press Save
- reopen the edit dates dialog

**Expected results**:
the new date is shown in the last row

**Passed**: [X]

#### 4.7.5 - Modify date

**ID**: test#1331

**Source requirements**: req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the first row to a valid one (but later)

**Expected results**:
the date in the row below and column "To date" is changed accordingly (one day earlier)

**Passed**: [X]

#### 4.7.6 - Modify date with an invalid one

**ID**: test#1332

**Source requirements**: req#1520

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the first row to an invalid one (i.e. 2024-13-32)

**Expected results**:
the cell becomes yellow

**Passed**: [X]

**ID**: test#1333

**Source requirements**: req#1520

**Test description #2**:
Test description #2
- press Save

**Expected results #2**:
an error dialog is shown

**Passed**: [X]

#### 4.7.8 - Modify date with an invalid one

**ID**: test#1334

**Source requirements**: req#1520, req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the first row to an invalid one (i.e. '2021-13-77')
- the cell becomes yellow; press Cancel
- the edit dates dialog is closed, reopen it

**Expected results**:
the valid old date appears

**Passed**: [X]

#### 4.7.9 - Modify date with an invalid one

**ID**: test#1335

**Source requirements**: req#1520, req#1518

**Preparatory steps**:


**Test description**:
- change the "date from" of the first row to an invalid one (i.e. 2001-02-30)

**Expected results**:
the cell becomes yellow

**Passed**: [X]

#### 4.7.10 - Modify date with an invalid one

**ID**: test#1336

**Source requirements**: req#1520, req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the first row to a date equal to the row below
- press Save

**Expected results**:
- an error dialog is shown
- press OK, the edit date window is shown

**Passed**: [X]

**ID**: test#1337

**Source requirements**: req#1520, req#1518

**Test description #2**:
Test description #3
- after the step above, press Cancel
- press the '...' button
- check the dates

**Expected results #2**:
- the dates are unchanged

**Passed**: [X]

#### 4.7.12 - Modify date with an invalid one

**ID**: test#1338

**Source requirements**: req#1520, req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the first row to a date before (-1 day) the row below
- press Save

**Expected results**:
- an error dialog is shown
- press OK, the edit date window is shown

**Passed**: [X]

**ID**: test#1339

**Source requirements**: req#1520, req#1518

**Test description #2**:
Test description #3
- after the step above, press Cancel
- press the '...' button
- check the dates

**Expected results #2**:
- the dates are unchanged

**Passed**: [X]

#### 4.7.14 - Modify date with an invalid one

**ID**: test#1340

**Source requirements**: req#1520, req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the 2nd row to a date equal to the row above
- press Save

**Expected results**:
- an error dialog is shown
- press OK, the edit date window is shown

**Passed**: [X]

**ID**: test#1341

**Source requirements**: req#1520, req#1518

**Test description #2**:
Test description #3
- after the step above, press Cancel
- press the '...' button
- check the dates

**Expected results #2**:
- the dates are unchanged

**Passed**: [X]

#### 4.7.16 - Modify date with an invalid one

**ID**: test#1342

**Source requirements**: req#1520, req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the 2nd row to a date after (+1 day) the row above
- press Save

**Expected results**:
- an error dialog is shown
- press OK, the edit date window is shown

**Passed**: [X]

**ID**: test#1343

**Source requirements**: req#1520, req#1518

**Test description #2**:
Test description #3
- after the step above, press Cancel
- press the '...' button
- check the dates

**Expected results #2**:
- the dates are unchanged

**Passed**: [X]

#### 4.7.18 - Modify date

**ID**: test#1344

**Source requirements**: req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the "date from" of the first row to a date after (+1 day) the row below

**Expected results**:
the cell remains white

**Passed**: [X]

**ID**: test#1345

**Source requirements**: req#1518

**Test description #2**:
- after the steps above, press Save

**Expected results #2**:
- a confirmation dialog is shown, press OK

**Passed**: [X]

**ID**: test#1346

**Source requirements**: req#1518

**Test description #3**:
Test description #3
- after the steps above, press the '...' button
- check the dates

**Expected results #3**:
- the dates are changed

**Passed**: [X]

#### 4.7.21 - Check the read-only/read-write status of the cells

**ID**: test#1347

**Source requirements**: req#1518

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
check that all fields are read-only with the exception of:
- the column "From date"
- the cells of the first row ("From date" and "To date")

**Expected results**:
only the cells listed above are read-write

**Passed**: [X]

#### 4.7.22 - Insert an invalid date

**ID**: test#1348

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the value of the cell in the first row and column "To date" to an invalid one (i.e. '2024-02-32')

**Expected results**:
the cell becomes yellow

**Passed**: [X]

**ID**: test#1349

**Source requirements**: req#1518, req#1520

**Test description #2**:
press Save

**Expected results #2**:
an error dialog appears

**Passed**: [X]

#### 4.7.24 - Insert an invalid date

**ID**: test#1350

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- insert code 810095 (or any other code with multiple revisions) in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select the "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From/to date" field
- An edit dates dialog is shown

**Test description**:
- change the value of the cell in the first row and column "To date" to a date earlier than the left cell
- press Save

**Expected results**:
- an error dialog is shown
- press OK, the edit date window is shown

**Passed**: [X]

#### 4.7.25 - Insert a valid date

**ID**: test#1351

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- insert code 100001 in the "BOMBrowser codes list" window
- press search
- right-click on the first entry and select "Edit code..." command
- The Edit code window appears
- Select the "..." button near the "From / to date" field
- An edit dates dialog is shown

**Test description**:
- change the value of the cell in the first row and column "To date" to a valid one
- press the Save button
- reopen the "Edit dates" dialog

**Expected results**:
the new date appears in the "edit code window"

**Passed**: [X]

#### 4.7.26 - conflict date

#### 4.7.27 - parent too early

**ID**: test#1353

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- Verify if the assembly TEST-ASS-A exists, and if not build it as follows:
- create a component code (copying from an existing component);
  name it TEST-A; set a "Date from" 2020-01-01.
- Create a component code (copying from an existing component);
  name it TEST-B; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Create a component code (copying from an existing component);
  name it TEST-ASS-A; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Edit the code "TEST-ASS-A" adding components TEST-A and TEST-B as children.

**Test description**:
- enter the edit dialog of code TEST-ASS-A
- enter the edit date dialog
- change the "From date" to 2019-01-01
- press "Save" button

**Expected results**:
an error dialog appears saying that the date range is wider than the children's range

**Passed**: [X]

#### 4.7.28 - parent too late

**ID**: test#1354

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- Verify if the assembly TEST-ASS-A exists, and if not build it as follows:
- create a component code (copying from an existing component);
  name it TEST-A; set a "Date from" 2020-01-01.
- Create a component code (copying from an existing component);
  name it TEST-B; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Create a component code (copying from an existing component);
  name it TEST-ASS-A; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Edit the code "TEST-ASS-A" adding components TEST-A and TEST-B as children.

**Test description**:
- enter the edit dialog of code TEST-ASS-A
- enter the edit date dialog
- change the "To date" to 2022-01-01
- press "Save" button

**Expected results**:
an error dialog appears saying that the date range is wider than the children's range

**Passed**: [X]

#### 4.7.29 - children too late

**ID**: test#1355

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- Verify if the assembly TEST-ASS-A exists, and if not build it as follows:
- create a component code (copying from an existing component);
  name it TEST-A; set a "Date from" 2020-01-01.
- Create a component code (copying from an existing component);
  name it TEST-B; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Create a component code (copying from an existing component);
  name it TEST-ASS-A; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Edit the code "TEST-ASS-A" adding components TEST-A and TEST-B as children.

**Test description**:
- enter the edit dialog of code TEST-B
- enter the edit date dialog
- change the "From date" to 2020-06-01
- press "Save" button

**Expected results**:
an error dialog appears saying that the date range of the parent is wider than the child's

**Passed**: [X]

#### 4.7.30 - children too early

**ID**: test#1356

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- Verify if the assembly TEST-ASS-A exists, and if not build it as follows:
- create a component code (copying from an existing component);
  name it TEST-A; set a "Date from" 2020-01-01.
- Create a component code (copying from an existing component);
  name it TEST-B; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Create a component code (copying from an existing component);
  name it TEST-ASS-A; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Edit the code "TEST-ASS-A" adding components TEST-A and TEST-B as children.

**Test description**:
- enter the edit dialog of code TEST-ASS-A
- enter the edit date dialog
- change the "To date" to 2020-06-01
- press "Save" button
- enter the edit dialog of code TEST-B
- enter the edit date dialog
- change the "To date" to 2020-03-01
- press "Save" button

**Expected results**:
an error dialog appears saying that the date range is shorter than the parent's range

**Passed**: [X]

#### 4.7.31 - children too early

**ID**: test#1357

**Source requirements**: req#1518, req#1520

**Preparatory steps**:
- Verify if the assembly TEST-ASS-A exists, and if not build it as follows:
- create a component code (copying from an existing component);
  name it TEST-A; set a "Date from" 2020-01-01.
- Create a component code (copying from an existing component);
  name it TEST-B; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Create a component code (copying from an existing component);
  name it TEST-ASS-A; set a "Date from" 2020-01-01. Set "Date to" 2021-01-01.
- Edit the code "TEST-ASS-A" adding components TEST-A and TEST-B as children.

**Test description**:
- enter the edit dialog of code TEST-ASS-A
- remove the child TEST-B
- press "Save" and then "Close"
- enter the edit dialog of code TEST-B
- enter the edit date dialog
- change the "To date" to 2020-03-01
- enter the edit dialog of code ASS-A
- add child TEST-B
- press Save

**Expected results**:
an error dialog appears saying that the child's date range is shorter than the parent's range

**Passed**: [X]

#### 4.7.32 - prototype date

**ID**: test#1358

**Source requirements**: req#1518, req#1520

**Test description**:
- enter the edit dialog of a code with several revisions without a prototype (e.g. 810203)
- enter the "edit dates" dialog
- change the first (from the top) "From date" to "prototype"

**Expected results**:
- no error (yellow cell) is shown
- **ALL** the cells in the "To date" column are R/O
- the "End to" dates of the 1st and 2nd lines are blanked

**Passed**: [X]

**ID**: test#1359

**Source requirements**: req#1518

**Test description #2**:
- after the above test, press save
- press ok
- you see the "Edit dialog"
- check that the "From/to date" "Revision selector" lists all the dates

**Expected results #2**:
- the "From/to date" "Revision selector" lists all the dates and prototype

**Passed**: [X]

**ID**: test#1360

**Source requirements**: req#1518, req#1520

**Test description #3**:
- after the steps above
- press the "..." button and go to the "edit dates" dialog
- change the "From date" in the first row from "PROTOTYPE" to a date greater than the 2nd line

**Expected results #3**:
- no error (yellow cell) is shown
- the "End to" cell in the second line shows a valid date
- the "End to" cell in the 1st line is editable

**Passed**: [X]

**ID**: test#1361

**Source requirements**: req#1518

**Test description #4**:
- after the steps above
- press save and go to the edit window
- check that the "From/to date" "Revision selector" lists all the dates

**Expected results #4**:
- the "From/to date" "Revision selector" lists all the dates w/o prototype

**Passed**: [X]

#### 4.7.36 - date in the title bar

**ID**: test#1362

**Source requirements**: req#1518, req#1520

**Test description**:
- enter the edit dialog of a code with several revisions
- select a 2nd revision in the "From/to date" selector
- press the "..." button and go to the edit dialog
- change the 2nd row "From date" with a reasonable value
- press "Save", then "OK"

**Expected results**:
- the "From/to date" is changed according to the steps above
- the date shown in the title bar is changed according to the steps above

**Passed**: [X]

### 4.8 - Generic test

#### 4.8.1 - rename bombrowser.ini

**ID**: test#1364

**Source requirements**: req#1610, req#1614

**Test description**:
- rename bombrowser.ini to bombrowser.ini.no
- delete a bombrowser.forward file
- (re)start bombrowser

**Expected results**:
at start-up, an error dialog is shown saying that the configuration cannot be loaded: bombrowser.ini file may be missing

**Passed**: [X]

#### 4.8.2 - rename bombrowser.ini (2)

**ID**: test#1365

**Source requirements**: req#1610, req#1614

**Test description**:
- rename bombrowser.ini to bombrowser.ini.two
- create a bombrowser.forward file containing bombrowser.ini.two
- (re)start bombrowser

**Expected results**:
bombrowser runs correctly

**Passed**: [X]

#### 4.8.3 - shutdown the sql server

**ID**: test#1366

**Source requirements**: req#1616

**Test description**:
- shut down the sql server
- restart bombrowser

**Expected results**:
at start-up, an error dialog is shown saying that it is impossible to access the server (some time may be required)

**Passed**: [ ]

#### 4.8.4 - test re-connection after an sql server disconnection

**ID**: test#1367

**Source requirements**: req#1616

**Test description**:
- perform a query looking for code 100001 in the code list window
- shut down the server
- re-run the same query and check that an error is shown

**Expected results**:
an error dialog is shown

**Passed**: [X]

**ID**: test#1368

**Source requirements**: req#1616

**Test description #2**:
after the previous steps
- start up the server
- wait a few seconds
- re-run the same query and check that an error is shown
- re-run the same query *again*

**Expected results #2**:
the query results are shown

**Passed**: [X]

**ID**: test#1369

**Source requirements**: req#1616

**Test description #3**:
- repeat the same test on a different db

**Expected results #3**:
the previous tests passed

**Passed**: [X]

#### 4.8.7 - Self test

**ID**: test#1633

**Source requirements**: req#1632

**Test description**:
Run the BOMBrowser self test

**Expected results**:
The BOMBrowser shall run succesfully.

**Passed**: [X]

#### 4.8.8 - Config test

#### 4.8.9 - Test description_force_uppercase: edit code

**ID**: test#1371

**Source requirements**: req#1612

**Test description**:
- Set description_force_uppercase = 1 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Edit the code TEST-A
- Change the description of code TEST-A to "lower case test a"
- Save the code
- Search for code TEST-A in the code list window

**Expected results**:
The description is in upper case

**Passed**: [X]

#### 4.8.10 - Test description_force_uppercase: copy code

**ID**: test#1372

**Source requirements**: req#1612

**Test description**:
- Set description_force_uppercase = 1 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Copy code TEST-B to TEST-B-COPY1, and change the description of code TEST-B to "lower case test b copy1"
- Press "copy code" button
- Search for code TEST-B-COPY1 in the code list window

**Expected results**:
The description is in upper case

**Passed**: [X]

#### 4.8.11 - Test description_force_uppercase: revise code

**ID**: test#1373

**Source requirements**: req#1612

**Test description**:
- Set description_force_uppercase = 1 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Revise code TEST-B, and change the description of code TEST-B to "lower case test b new rev"
- Save the code
- Search for code TEST-B in the code list window

**Expected results**:
The description of the latest revision is in upper case

**Passed**: [X]

#### 4.8.12 - Test description_force_uppercase: edit code

**ID**: test#1374

**Source requirements**: req#1612

**Test description**:
- Set description_force_uppercase = 0 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Edit the code TEST-A
- Change the description of code TEST-A to "lower case test a"
- Save the code
- Search for code TEST-A in the code list window

**Expected results**:
The description is in lower case

**Passed**: [X]

#### 4.8.13 - Test description_force_uppercase: copy code

**ID**: test#1375

**Source requirements**: req#1612

**Test description**:
- Set description_force_uppercase = 0 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Copy code TEST-B to TEST-B-COPY2, and change the description of code TEST-B to 
  "lower case test b copy2"
- Press "copy code" button
- Search for code TEST-B-COPY2 in the code list window

**Expected results**:
The description is in lower case

**Passed**: [X]

#### 4.8.14 - Test description_force_uppercase: revise code

**ID**: test#1376

**Source requirements**: req#1612

**Test description**:
- Set description_force_uppercase = 0 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Revise code TEST-B, and change the description of code TEST-B to "lower case test b new rev 2"
- Save the code
- Search for code TEST-B in the code list window

**Expected results**:
The description of the latest revision is in lower case

**Passed**: [X]

#### 4.8.15 - Test code_force_uppercase: copy code

**ID**: test#1377

**Source requirements**: req#1612

**Test description**:
- Set code_force_uppercase = 1 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Copy code TEST-B to test-b-copy
- Save the code
- Search for code test-b-copy in the code list window

**Expected results**:
The code is in upper case

**Passed**: [X]

#### 4.8.16 - Test code_force_uppercase: copy code

**ID**: test#1378

**Source requirements**: req#1612

**Test description**:
- Set code_force_uppercase = 0 in bombrowser.ini
- Re-Start bombrowser (or click File->Reload)
- Copy code TEST-B to test-b-copy
- Save the code
- Search for code test-b-copy in the code list window

**Expected results**:
The code is in lower case

**Passed**: [X]

#### 4.8.17 - Test ignore_case_during_search: search code

**ID**: test#1379

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 1 in bombrowser.ini
- Restart bombrowser
- In the "code list window", search for code "%ALLLOWERCASE"

**Expected results**:
The code "TEST-alllowercase" is returned

**Passed**: [X]

#### 4.8.18 - Test ignore_case_during_search: search code

**ID**: test#1380

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 1 in bombrowser.ini
- Restart bombrowser
- In the "code list window", search for description "ALL LOWERCASE"

**Expected results**:
The description "alllowercase" is returned

**Passed**: [X]

#### 4.8.19 - Test ignore_case_during_search: search code

**ID**: test#1381

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 0 in bombrowser.ini
- Restart bombrowser
- In the "code list window", search for code "%ALLLOWERCASE"

**Expected results**:
No code is found

**Passed**: [X]

#### 4.8.20 - Test ignore_case_during_search: search code

**ID**: test#1382

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 0 in bombrowser.ini
- Restart bombrowser
- In the "code list window", search for description "ALL LOWERCASE"

**Expected results**:
No code is found

**Passed**: [X]

#### 4.8.21 - Test ignore_case_during_search: search revision

**ID**: test#1383

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 1 in bombrowser.ini
- Restart bombrowser
- In the "Code list" window, "search mode=advanced", search for code "ALLLOWERCASE"

**Expected results**:
The code "TEST-alllowercase" is returned

**Passed**: [X]

#### 4.8.22 - Test ignore_case_during_search: search revision

**ID**: test#1384

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 1 in bombrowser.ini
- Restart bombrowser
- In the "Code list" window, "search mode=advanced", search for description "ALL LOWERCASE"

**Expected results**:
The description "all lowercase" is returned

**Passed**: [X]

#### 4.8.23 - Test ignore_case_during_search: search revision

**ID**: test#1385

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 1 in bombrowser.ini
- Restart bombrowser
- In the "Code list" window, "search mode=advanced",  search for gval2 "lower"

**Expected results**:
The gval2 "gval2 lower" is returned

**Passed**: [X]

#### 4.8.24 - Test ignore_case_during_search: search revision

**ID**: test#1386

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 0 in bombrowser.ini
- Restart bombrowser
- In the "Code list" window, "search mode=advanced", search for code "%ALLLOWERCASE"

**Expected results**:
No code is found

**Passed**: [X]

#### 4.8.25 - Test ignore_case_during_search: search revision

**ID**: test#1387

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 0 in bombrowser.ini
- Restart bombrowser
- In the "Code list" window, "search mode=advanced", search for description "ALL LOWERCASE"

**Expected results**:
No code is found

**Passed**: [X]

#### 4.8.26 - Test ignore_case_during_search: search revision

**ID**: test#1388

**Source requirements**: req#1613

**Preparatory steps**:
This test is not applicable with MySQL/MariaDB/SQLSERVER

**Test description**:
- Set ignore_case_during_search = 0 in bombrowser.ini
- Restart bombrowser
- In the "Code list" window, "search mode=advanced", search for gval2 "LOWER"

**Expected results**:
No code is found

**Passed**: [X]

#### 4.8.27 - bombrowser.ini missing parameter

**ID**: test#1389

**Source requirements**: req#1614

**Test description**:
- in bombrowser.ini, comment out the parameter "db" in the BOMBROWSER section
- Start bombrowser

**Expected results**:
An error dialog shows that the parameter "db" is missing in section BOMBROWSER

**Passed**: [X]

#### 4.8.28 - bombrowser.ini missing section

**ID**: test#1390

**Source requirements**: req#1614

**Test description**:
- in bombrowser.ini, comment out section FILES_UPLOAD
- Start bombrowser

**Expected results**:
An error dialog shows that section FILES_UPLOAD is missing

**Passed**: [X]

#### 4.8.29 - bombrowser.ini unknown parameter

**ID**: test#1391

**Source requirements**: req#1614

**Test description**:
- in bombrowser.ini, in section BOMBROWSER, add parameter "unknown=foo"
- Start bombrowser

**Expected results**:
An error dialog shows that there is an unknown parameter in section BOMBROWSER

**Passed**: [X]

#### 4.8.30 - bombrowser.ini unknown section

**ID**: test#1392

**Source requirements**: req#1614

**Test description**:
- in bombrowser.ini, add:
   [UNKNOWNSECTION]
   unk=unk
- Start bombrowser

**Expected results**:
An error dialog shows that there is an unreferenced section UNKNOWNSECTION

**Passed**: [X]

#### 4.8.31 - bombrowser.ini missing template

**ID**: test#1393

**Source requirements**: req#1614

**Test description**:
- in bombrowser.ini, add an "x" before the first section of BOMBROWSER.templates_list
- Start bombrowser

**Expected results**:
An error dialog shows that:
- an unreferenced section exists
- a section is missing

**Passed**: [X]

#### 4.8.32 - bombrowser.ini missing importer

**ID**: test#1394

**Source requirements**: req#1614

**Test description**:
- in bombrowser.ini, add an "x" before the first section of BOMBROWSER.importer_list
- Start bombrowser

**Expected results**:
An error dialog shows that:
- an unreferenced section exists
- a section is missing

**Passed**: [X]

#### 4.8.33 - bombrowser.ini: list_code_default_mode

**ID**: test#1395

**Source requirements**: req#1615

**Test description**:
- in bombrowser.ini, set list_code_default_mode=1
- start bombrowser

**Expected results**:
- the code search is shown in "Advanced" mode

**Passed**: [X]

#### 4.8.34 - bombrowser.ini: list_code_default_mode

**ID**: test#1396

**Source requirements**: req#1615

**Test description**:
- in bombrowser.ini, set list_code_default_mode=0
- start bombrowser

**Expected results**:
- the code search is shown in "Simple" mode

**Passed**: [X]

#### 4.8.35 - bombrowser.forward

**ID**: test#1397

**Source requirements**: req#1610

**Test description**:
- rename bombrowser.ini to bombrowser.1.ini
- create a file bombrowser.forward containing bombrowser.1.ini
- start bombrowser

**Expected results**:
BOMBrowser will open

**Passed**: [X]

**ID**: test#1398

**Source requirements**: req#1610

**Test description #2**:
- rename bombrowser.1.ini to bombrowser.2.ini
- make sure that no bombrowser-local.ini file exists
- start bombrowser

**Expected results #2**:
BOMBrowser will not open, and an error dialog will appear

**Passed**: [X]

#### 4.8.37 - bombrowser-local.ini

**ID**: test#1399

**Source requirements**: req#1610

**Test description**:
- in bombrowser.ini, set list_code_default_mode=0
- in bombrowser-local.ini, set list_code_default_mode=1
- set the content of 'bombrowser.forward' to 'bombrowser-local.ini'
- start bombrowser

**Expected results**:
- the code search is shown in "Advanced" mode

**Passed**: [X]

### 4.9 - Export test

TBD

### 4.10 - Import test

TBD

### 4.11 - Window menu test

#### 4.11.1 - Window menu test, close all other windows

**ID**: test#1403

**Source requirements**: req#1009

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- open a where used window
- open a valid where used window

**Test description**:
from the 'where used' window, select menu->windows->close all other windows

**Expected results**:
all windows are closed except the 'where used' window

**Passed**: [X]

#### 4.11.2 - Window menu test, new code list window

**ID**: test#1404

**Source requirements**: req#1009

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- open a where used window
- open a valid where used window

**Test description**:
from the 'where used' window, select menu->windows->new code list window

**Expected results**:
a NEW 'Code list' window is opened

**Passed**: [X]

**ID**: test#1405

**Source requirements**: req#1009

**Test description #2**:
from the 'where used' window, select menu->windows->new code list window

**Expected results #2**:
a 3rd 'Code list' window is opened

**Passed**: [X]

### 4.12 - Advanced search in the BOM

#### 4.12.1 - Advanced search in the BOM

**ID**: test#1407

**Source requirements**: req#1618

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window

**Test description**:
From the 'Search' menu select 'Advanced search'

**Expected results**:
- A 'Search in BOM' window is shown
- In the title window it is possible to read:
  - Search in BOM
  - The code and the date (or LATEST if applicable)

**Passed**: [X]

#### 4.12.2 - Advanced search in the BOM - search by code

**ID**: test#1408

**Source requirements**: req#1618

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'

**Test description**:
Enter '04' in the code field and press 'Search'

**Expected results**:
Only codes containing '04' are shown

**Passed**: [X]

#### 4.12.3 - Advanced search in the BOM - search by descr

**ID**: test#1409

**Source requirements**: req#1618

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'

**Test description**:
Enter '44' in the Description field and press 'Search'

**Expected results**:
Only code descriptions containing '44' are shown

**Passed**: [X]

**ID**: test#1410

**Source requirements**: req#1618

**Test description #2**:
Select a code and check that the codegui panel changes accordingly

**Expected results #2**:
The codegui panel changes accordingly

**Passed**: [X]

**ID**: test#1411

**Source requirements**: req#1618

**Test description #3**:
- Select a row and right-click (RMB)
- Press edit code

**Expected results #3**:
The edit code window is opened

**Passed**: [X]

#### 4.12.6 - Advanced search in the BOM - search by descr and code

**ID**: test#1412

**Source requirements**: req#1618

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'

**Test description**:
- Enter '2' in the Description field
- Enter '7' in the Code field
- Press 'Search'

**Expected results**:
Only codes containing '7' with description containing '2' are shown

**Passed**: [X]

#### 4.12.7 - Advanced search in the BOM search w/multiple fields

**ID**: test#1413

**Source requirements**: req#1618

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'
- from the 'Search mode' menu select 'Advanced'

**Test description**:
Enter 44 in the code field, then press Search

**Expected results**:
Only codes containing 44 are shown

**Passed**: [X]

**ID**: test#1414

**Source requirements**: req#1618

**Test description #2**:
- Clear all fields
- Enter 87 in the description field, then press Search

**Expected results #2**:
Only codes containing '87' in description are shown

**Passed**: [X]

**ID**: test#1415

**Source requirements**: req#1618

**Test description #3**:
- Clear all fields
- Enter 6 in the description field, then enter 6 in the 'Sup.1 PN' field, then press Search

**Expected results #3**:
Only items containing 6 in description and PN containing 6 are shown

**Passed**: [X]

**ID**: test#1416

**Source requirements**: req#1618

**Test description #4**:
- Clear all fields
- Enter >8 in the code field, then press Search

**Expected results #4**:
Only codes starting with 8 are shown

**Passed**: [X]

**ID**: test#1417

**Source requirements**: req#1618

**Test description #5**:
- Clear all fields
- Enter >8 in the code field
- Enter 8 in the description field
then press Search

**Expected results #5**:
Only codes starting with 8 and containing 8 in the description are shown

**Passed**: [X]

**ID**: test#1418

**Source requirements**: req#1618

**Test description #6**:
- Clear all fields
- Enter <8 in the code field
- Enter 3 in the description field
then press Search

**Expected results #6**:
Only codes starting with 7 and containing 3 in the description are shown

**Passed**: [X]

**ID**: test#1419

**Source requirements**: req#1618

**Test description #7**:
- Clear all fields
- Enter !820007 in the code field
- Enter 7 in the description field
then press Search

**Expected results #7**:
Only codes different from 820007 and containing 7 in the description are shown

**Passed**: [X]

**ID**: test#1420

**Source requirements**: req#1618

**Test description #8**:
- Clear all fields
- Enter >2000 in the rid field
- Enter 7 in the description field
then press Search

**Expected results #8**:
Only codes with rid greater than 2200 and containing 3 in the description are shown

**Passed**: [X]

**ID**: test#1421

**Source requirements**: req#1618

**Test description #9**:
- Clear all fields
- Enter <2000 in the rid field
- Enter 3 in the description field
then press Search

**Expected results #9**:
Only codes with rid less than 2000 and containing 3 in the description are shown

**Passed**: [X]

#### 4.12.16 - Advanced search in the BOM - where used

**ID**: test#1422

**Source requirements**: req#1620

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open a where used window
- from the 'Search' menu select 'Advanced search'

**Test description**:
Enter '02' in the code field and press 'Search'

**Expected results**:
Only codes containing '02' are shown

**Passed**: [X]

#### 4.12.17 - Advanced search in the BOM - smart where used

**ID**: test#1423

**Source requirements**: req#1620

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open a smart where used window
- from the 'Search' menu select 'Advanced search'

**Test description**:
Enter '17' in the code field and press 'Search'

**Expected results**:
Only codes containing '17' are shown

**Passed**: [X]

#### 4.12.18 - Advanced search in the BOM - search by doc

**ID**: test#1424

**Source requirements**: req#1619

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open a smart where used window
- from the 'Search' menu select 'Advanced search'
- from the 'Search mode' menu select 'Advanced search'

**Test description**:
Enter '17' in the Document field and press 'Search'

**Expected results**:
Only codes containing '17' in the document column are shown

**Passed**: [X]

### 4.13 - Export data from assembly

#### 4.13.1 - Export data

**ID**: test#1426

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window

**Test description**:
From the 'File' menu select 'Export data...'

**Expected results**:
An 'Export' dialog is shown

**Passed**: [X]

#### 4.13.2 - Export data

**ID**: test#1427

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

**Test description**:
Check that the date shown in the window title is the latest one for the code

**Expected results**:
The date is the latest one (compare it wiith the select date dialog 
of the command "Show assembly by date")

**Passed**: [X]

**ID**: test#1428

**Source requirements**: req#1622

**Test description #2**:
Press the Close button

**Expected results #2**:
The dialog disappears

**Passed**: [X]

#### 4.13.4 - Export data

**ID**: test#1429

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

**Test description**:
Press the Export button

**Expected results**:
- The success dialog appeared (maybe below another window)
- A folder containing all the files appeared
- In the folder there is a zip file containing all the files
- In the folder there is a BOM in the same format specified in the dialog
- Executing a 'paste' command in a folder copies the zip file

**Passed**: [X]

#### 4.13.5 - Export data

**ID**: test#1430

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

**Test description**:
Uncheck the 'zip all' option; press the Export button

**Expected results**:
- The success dialog appeared (maybe below another window)
- A folder containing all the files appeared
- In the folder there is NO zip file containing all the files
- Executing a 'paste' command in a folder copies the folder with all the files

**Passed**: [X]

#### 4.13.6 - Export data

**ID**: test#1431

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

**Test description**:
Uncheck the 'export files' option; press the Export button

**Expected results**:
- The success dialog appeared (maybe below another window)
- A folder containing only the zip file and the bom appeared

**Passed**: [X]

#### 4.13.7 - Export data

**ID**: test#1432

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

**Test description**:
Uncheck the 'open destination folder' option; press the Export button

**Expected results**:
The success dialog appeared

**Passed**: [X]

#### 4.13.8 - Export data

**ID**: test#1433

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

**Test description**:
Change the destination directory; press the Export button

**Expected results**:
The selected destination directory is shown

**Passed**: [X]

#### 4.13.9 - Export data - where used

**ID**: test#1434

**Source requirements**: req#1622

**Preparatory steps**:
From code list window:
- search for a code (e.g. 820007)
- open the Where used window
- from the 'File' menu select 'Export data...'"

**Test description**:
Change the destination directory; press the Export button

**Expected results**:
- The success dialog appeared (maybe below another window)
- The folder containing all the files appeared, the folder is the one set before

**Passed**: [X]

#### 4.13.10 - Export data - error in file

**ID**: test#1436

**Source requirements**: req#1622

**Preparatory steps**:
- Open the assembly TEST-ASSY-TO-EXPORT.
- from the 'File' menu select 'Export data...'

**Test description**:
press the Export button

**Expected results**:
An error dialog showing that:
- a file does not exist
- a file is too big
The error dialog asks if the user wants to END the copy

**Passed**: [X]

**ID**: test#1437

**Test description #2**:
press the "Yes" button

**Expected results #2**:
The dialog disappears

**Passed**: [X]

#### 4.13.12 - Export data - error in file

**ID**: test#1438

**Source requirements**: req#1622

**Preparatory steps**:
- Open the assembly TEST-ASSY-TO-EXPORT.
- from the 'File' menu select 'Export data...'
- press the Export button
- an error dialog appears

**Test description**:
press the "No" button

**Expected results**:
- The dialog disappears.
- the export continues and finishes without the files that raised an error

**Passed**: [X]

### 4.14 - Dump/Restore/Create a new database

#### 4.14.1 - Dump the database

**ID**: test#1440

**Source requirements**: req#1624

**Test description**:
- run "[python] bombrowser[.py] --manage-db --dump-tables <filename>"

**Expected results**:
- the <filename> file is created

**Passed**: [X]

#### 4.14.2 - Restore the database

**ID**: test#1441

**Source requirements**: req#1625

**Test description**:
- edit code 100001
- select Edit->Delete code. The code is now deleted
- copy code 100002 to code 100002-cpy
- run "[python] bombrowser[.py] --manage-db --restore-tables --yes-really-i-know-what-i-want <filename>"
- search for code 100001 again

**Expected results**:
- code 100001 exists
- code 100002 doesn't exist

**Passed**: [X]

#### 4.14.3 - Create a new (empty) database

**ID**: test#1442

**Source requirements**: req#1626

**Test description**:
- run "[python] bombrowser[.py] --manage-db --new-db --yes-really-i-know-what-i-want"
- search for "%"

**Expected results**:
- only code "000000000000" is returned

**Passed**: [X]

#### 4.14.4 - Restore a database with a specific gaval/gval column count

**ID**: test#1443

**Source requirements**: req#1627

**Test description**:
- run "python mkdb.py --test-db --gval_count=40 --gaval_count=40"
- set the following options in bombrowser.ini:
     [BOMBROWSER]
     [...]
       gvalnames=
     [...]
           gval40:Test gval40
     [...]
       gavalnames=
     [...]
           gaval40:Test gaval40
- from bombrowser, copy code 820001 to 820001-test
- from bombrowser, set (use edit code) the following values for code 820001-test:
     In main window: Test gval40 -> test1
     In children list: Test gaval40 -> test2
- run "[python] bombrowser[.py] --manage-db --dump-tables <filename>"
- from bombrowser, delete (use edit code) code 820001-test
- run "[python] bombrowser[.py] --manage-db --restore-tables --yes-really-i-know-what-i-want <filename>"
- search for and edit code 820001-test again

**Expected results**:
- check that the following parameters exist (use edit window)
     In main window: Test gval40 -> test1
     In children list: Test gaval40 -> test2

**Passed**: [X]

### 4.15 - Log transaction

**Preparatory steps**:
To enable the tests of the "Log transaction" functionality, ensure that in
the 'bombrowser.ini' file the following lines exist:
    [LOGGER]
    enable=1
    #filename=log.txt
    filename=/tmp/log.txt
    # 0 or 1
    compress=0
    # none
    # weekly
    # monthly
    # yearly
    logrotate=monthly

#### 4.15.1 - Log create a new revision

**ID**: test#1445

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 820123, right-click,
select the command "revise code", and create a new code revision
 setting all properties in the dialog and pressing OK

**Expected results**:
- In the log file, all info for the new revision appears
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.2 - Log create a new code

**ID**: test#1446

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 820123, right-click,
select the command "copy code", and create a new code
 setting all properties in the dialog and pressing OK

**Expected results**:
- In the log file, all info for the new **revision** appears
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.3 - Log edit a code (1/6)

**ID**: test#1447

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 820123, right-click,
select the command "edit code".
Update the description and the revision by adding "-bis" as a suffix, and then save the changes

**Expected results**:
- In the log file, all info for the updated revision appears with '-' and '+'
  to highlight which information has changed
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.4 - Log edit a code (2/6)

**ID**: test#1448

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 820123, right-click,
select the command "edit code".
Update the code by adding a child and removing another one.
Then save the changes

**Expected results**:
- In the log file, all info for the updated revision appears with '-' and '+'
  to highlight which information has changed
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.5 - Log edit a code (3/6)

**ID**: test#1449

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 820123, right-click,
select the command "edit code".
Update the code by adding a new document and removing another one.
Then save the changes

**Expected results**:
- In the log file, all info for the updated revision appears with '-' and '+'
  to highlight which information has changed
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.6 - Log edit a code (4/6)

**ID**: test#1450

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 820154, right-click,
select the command "edit code".
Enter the edit date dialog and advance the intermediate date by 2 days.
Then save the changes

**Expected results**:
- In the log file, all info for the updated dates appears with '-' and '+'
  to highlight which information has changed
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.7 - Log edit a code (5/6)

**ID**: test#1451

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 820154, right-click,
select the command "edit code".
Delete the intermediate revision

**Expected results**:
- In the log file, all info for the deleted revision appears, along with the
  new date revisions
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.8 - Log edit a code (6/6)

**ID**: test#1452

**Source requirements**: req#1629

**Test description**:
In the code list window, search for code 100046, revise it so that it has at
least two revisions.
Select the command "edit code".
Delete the code

**Expected results**:
- In the log file, all info for the deleted revisions appears
- At the beginning of the log transaction section, the header reports the
  correct logged action, date, and user

**Passed**: [X]

#### 4.15.9 - Log edit a code: path doesn't exist

**ID**: test#1453

**Source requirements**: req#1630

**Preparatory steps**:
In the 'bombrowser.ini' file set 'filename' to a path that
doesn't exist.
  [LOGGER]
    [...]
    filename=/path-that-doesnt-exist/tmp/log.txt
    [...]

**Test description**:
In the code list window, search for code 100047, revise it.
Select the command "revise code".
Make a new code revision

**Expected results**:
A backtrace appears stating that the path does not exist.

**Passed**: [X]

#### 4.15.10 - Log edit a code: compress the file

**ID**: test#1454

**Source requirements**: req#1631

**Preparatory steps**:
In the 'bombrowser.ini' file 'compress' to 1
  [LOGGER]
    [...]
    filename=/tmp/log.txt
    compress=1
    [...]

**Test description**:
In the code list window, search for code 100047, revise it.
Select the command "revise code".
Make a new code revision

**Expected results**:
- The log file is a compressed (.gz) file
- The content of the zip file is the log file

**Passed**: [ ]

## 5 - Traceability matrixes

### 5.1 - Test to requirements

* 3.3.1 - The 'Code GUI' panel shows code properties(ID:req#1471)
    * 3.1.6 - GVal properties (ID:req#1513)
* 3.6.5 - Edit code: edit code drawings(ID:req#1511)
    * 3.1.3 - Document attached to a code (ID:req#1464)
    * 3.1.5 - URL attached to a code (ID:req#1495)
* 4.1.1 - search a code(ID:test#1013)
    * 3.2.1 - Search fields - code and description (ID:req#1005)
* 4.1.2 - search a code (2)(ID:test#1014)
    * 3.2.1 - Search fields - code and description (ID:req#1005)
* 4.1.3 - search a code by description(ID:test#1015)
    * 3.2.1 - Search fields - code and description (ID:req#1005)
* 4.1.4 - search a code by description with a wildcard(ID:test#1016)
    * 3.2.1 - Search fields - code and description (ID:req#1005)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.5 - search a code with a wildcard(ID:test#1017)
    * 3.2.1 - Search fields - code and description (ID:req#1005)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.6 - search a code and a description with wildcards(ID:test#1018)
    * 3.2.1 - Search fields - code and description (ID:req#1005)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.7 - assembly(ID:test#1019)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.8 - assembly(ID:test#1020)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.9 - assembly(ID:test#1021)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.10 - where used(ID:test#1022)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.11 - where used (2)(ID:test#1023)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.12 - valid where used(ID:test#1024)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.13 - valid where used (2)(ID:test#1025)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.14 - Copy/revise code(ID:test#1026)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.15 - edit code(ID:test#1027)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.16 - diff from(ID:test#1028)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.17 - diff from (2x)(ID:test#1029)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.18 - diff to(ID:test#1030)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.19 - diff to (2x)(ID:test#1031)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.20 - menu->help->about(ID:test#1032)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.21 - menu->window(ID:test#1033)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.22 - menu->file->close(ID:test#1034)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.23 - menu->file->close(ID:test#1035)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.24 - menu->file->close(ID:test#1036)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.25 - Ctrl-Q  menu->file->close(ID:test#1037)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.26 - menu->file->exit(ID:test#1038)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.27 - menu->file->exit(ID:test#1039)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.28 - menu->file->exit(ID:test#1040)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.1.29 - Menu->edit->copy(ID:test#1041)
    * 3.1.2 - Copy table (ID:req#1010)
* 4.1.30 - Code GUI(ID:test#1042)
    * 3.2.3 - Code property (ID:req#1460)
* 4.1.31 - Code GUI(ID:test#1043)
    * 3.2.3 - Code property (ID:req#1460)
* 4.1.32 - Status bar(ID:test#1044)
    * 3.2.4 - Status bar (ID:req#1461)
* 4.1.33 - Status bar(ID:test#1045)
    * 3.2.4 - Status bar (ID:req#1461)
* 4.1.34 - Revision search(ID:test#1046)
    * 3.2.5 - Revision search (ID:req#1462)
* 4.1.35 - Revision search(ID:test#1047)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.4 - Status bar (ID:req#1461)
* 4.1.36 - Revision search(ID:test#1048)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.4 - Status bar (ID:req#1461)
* 4.1.37 - Revision search(ID:test#1049)
    * 3.2.5 - Revision search (ID:req#1462)
* 4.1.38 - Revision search(ID:test#1050)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.39 - Revision search(ID:test#1051)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.40 - Revision search(ID:test#1052)
    * 3.2.5 - Revision search (ID:req#1462)
* 4.1.41 - Revision search(ID:test#1053)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.42 - Revision search(ID:test#1054)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.43 - Revision search(ID:test#1055)
    * 3.2.3 - Code property (ID:req#1460)
* 4.1.44 - Revision search(ID:test#1056)
    * 3.2.3 - Code property (ID:req#1460)
* 4.1.45 - Revision search(ID:test#1057)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.46 - Revision search(ID:test#1058)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.47 - Revision search(ID:test#1059)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.48 - Revision search(ID:test#1060)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.49 - Revision search(ID:test#1061)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.50 - Revision search(ID:test#1062)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.51 - Revision search(ID:test#1063)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.52 - Revision search(ID:test#1064)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.53 - Revision search(ID:test#1065)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
    * 3.2.7 - Code commands (ID:req#1007)
* 4.1.54 - search <(ID:test#1068)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.55 - search !(ID:test#1069)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.56 - search =(ID:test#1070)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.57 - search =(ID:test#1071)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.2 - Search fields - wildcards (ID:req#1006)
* 4.1.60 - Search for CODE-COLORS-xxx(ID:test#1074)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.6 - Revision search result colors (ID:req#1463)
* 4.1.61 - Search for CODE-COLORS-xxx(ID:test#1075)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.6 - Revision search result colors (ID:req#1463)
* 4.1.62 - Search for CODE-COLORS-xxx(ID:test#1076)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.6 - Revision search result colors (ID:req#1463)
* 4.1.63 - Search for CODE-COLORS-xxx(ID:test#1077)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.6 - Revision search result colors (ID:req#1463)
* 4.1.64 - Search for CODE-COLORS-xxx(ID:test#1078)
    * 3.2.5 - Revision search (ID:req#1462)
    * 3.2.6 - Revision search result colors (ID:req#1463)
* 4.2.1 - general(ID:test#1080)
    * 3.3.1 - The 'Code GUI' panel shows code properties (ID:req#1471)
* 4.2.2 - multiple revision(ID:test#1081)
    * 3.3.2 - The 'Code GUI' revisions list box (ID:req#1466)
* 4.2.3 - multiple revision (2)(ID:test#1082)
    * 3.3.2 - The 'Code GUI' revisions list box (ID:req#1466)
* 4.2.4 - documents(ID:test#1083)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.5 - documents (2x)(ID:test#1084)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.6 - Copy info..(ID:test#1085)
    * 3.3.3 - The 'Code GUI' copy button (ID:req#1467)
* 4.2.7 - Check tool tip(ID:test#1086)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.8 - RMB menu of drawing button(ID:test#1087)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.9 - RMB menu of drawing button(ID:test#1088)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.10 - RMB menu of drawing button(ID:test#1089)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.11 - RMB menu of drawing button(ID:test#1090)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.12 - RMB menu of drawing button(ID:test#1091)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.13 - Long filename(ID:test#1092)
    * 3.3.5 - The 'Code GUI' 'Document' button text length (ID:req#1469)
* 4.2.14 - Long filename(ID:test#1093)
    * 3.3.5 - The 'Code GUI' 'Document' button text length (ID:req#1469)
* 4.2.15 - URL(ID:test#1094)
    * 3.1.4 - URL attached to a code (ID:req#1465)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.16 - URL(ID:test#1095)
    * 3.1.4 - URL attached to a code (ID:req#1465)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.17 - URL(ID:test#1096)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.18 - URL(ID:test#1097)
    * 3.1.4 - URL attached to a code (ID:req#1465)
    * 3.3.4 - The 'Code GUI' 'Document' button (ID:req#1468)
* 4.2.19 - URL(ID:test#1098)
    * 3.1.4 - URL attached to a code (ID:req#1465)
* 4.3.1 - select date(ID:test#1100)
    * 3.4.3 - Select date (ID:req#1481)
* 4.3.2 - select date(ID:test#1101)
    * 3.4.3 - Select date (ID:req#1481)
* 4.3.3 - select date(ID:test#1102)
    * 3.4.3 - Select date (ID:req#1481)
* 4.3.4 - show assembly(ID:test#1103)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.5 - show assembly (2)(ID:test#1104)
    * 3.4.3 - Select date (ID:req#1481)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.6 - where used (2)(ID:test#1105)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.7 - valid where used (2)(ID:test#1106)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.8 - menu->help->about(ID:test#1107)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.9 - menu->window(ID:test#1108)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.10 - menu->file->close(ID:test#1109)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.11 - Ctrl-Q  menu->file->close(ID:test#1110)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.12 - menu->file->exit(ID:test#1111)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.13 - menu->file->exit(ID:test#1112)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.14 - menu->file->exit(ID:test#1113)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.15 - menu->file->exit(ID:test#1114)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.16 - menu->file->exit(ID:test#1115)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.17 - menu->file->exit(ID:test#1116)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.3.18 - menu->file->export as json / csv...(ID:test#1117)
    * 3.4.4 - Export to JSON (ID:req#1482)
* 4.3.19 - menu->file->export as json / csv...(ID:test#1118)
    * 3.4.8 - Export (ID:req#1488)
* 4.3.20 - menu->view->show up level 1(ID:test#1119)
    * 3.4.5 - Show/hide levels (ID:req#1483)
* 4.3.21 - menu->view->show up level 1(ID:test#1120)
    * 3.4.5 - Show/hide levels (ID:req#1483)
* 4.3.22 - menu->view->show up level 1(ID:test#1121)
    * 3.4.5 - Show/hide levels (ID:req#1483)
* 4.3.23 - menu->view->show up level 1(ID:test#1122)
    * 3.4.5 - Show/hide levels (ID:req#1483)
* 4.3.24 - menu->view->show up level 1(ID:test#1123)
    * 3.4.5 - Show/hide levels (ID:req#1483)
* 4.3.25 - menu->view->show up level 1(ID:test#1124)
    * 3.4.5 - Show/hide levels (ID:req#1483)
* 4.3.26 - Find(ID:)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.27 - find ctrl-f(ID:test#1126)
    * 3.4.6 - Search in BOM (ID:req#1486)
* 4.3.28 - find(ID:test#1127)
    * 3.4.6 - Search in BOM (ID:req#1486)
* 4.3.29 - cancel(ID:test#1128)
    * 3.4.6 - Search in BOM (ID:req#1486)
* 4.3.30 - find a code(ID:test#1129)
    * 3.4.6 - Search in BOM (ID:req#1486)
* 4.3.31 - find a code(ID:test#1130)
    * 3.4.6 - Search in BOM (ID:req#1486)
* 4.3.32 - find a code(ID:test#1131)
    * 3.4.6 - Search in BOM (ID:req#1486)
* 4.3.33 - find a code(ID:test#1132)
    * 3.4.6 - Search in BOM (ID:req#1486)
* 4.3.34 - show latest assembly(ID:test#1133)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.35 - show latest assembly(ID:test#1134)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.36 - Menu file -> export data(ID:test#1135)
    * 3.4.8 - Export (ID:req#1488)
* 4.3.37 - Menu file -> export data(ID:test#1136)
    * 3.4.8 - Export (ID:req#1488)
* 4.3.38 - Menu file -> export data(ID:test#1137)
    * 3.4.8 - Export (ID:req#1488)
* 4.3.39 - Menu file -> export data with url(ID:test#1138)
    * 3.4.8 - Export (ID:req#1488)
* 4.3.41 - Show prototype assembly(ID:test#1140)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.3.42 - Show prototype assembly(ID:test#1141)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.4 - Check for loop(ID:test#1142)
    * 3.4.7 - Loop detection (ID:req#1487)
* 4.5 - Check for loop(ID:test#1143)
    * 3.4.7 - Loop detection (ID:req#1487)
* 4.5.1.2 - Bom color(ID:test#1146)
    * 3.4.9 - BOM Coloring (ID:req#1489)
* 4.5.1.3 - Bom color(ID:test#1147)
    * 3.4.9 - BOM Coloring (ID:req#1489)
* 4.5.1.4 - Bom color(ID:test#1148)
    * 3.4.9 - BOM Coloring (ID:req#1489)
* 4.5.1.5 - Bom color(ID:test#1149)
    * 3.4.9 - BOM Coloring (ID:req#1489)
* 4.5.1.6 - Bom color(ID:test#1150)
    * 3.4.9 - BOM Coloring (ID:req#1489)
* 4.5.1.7 - Bom color(ID:test#1151)
    * 3.4.9 - BOM Coloring (ID:req#1489)
* 4.5.1.8 - Bom color(ID:test#1152)
    * 3.4.9 - BOM Coloring (ID:req#1489)
* 4.5.2 - Copy assembly(ID:test#1153)
    * 3.4.8 - Export (ID:req#1488)
* 4.5.3 - Code gui panel(ID:test#1492)
    * 3.4.2 - Code GUI panel (ID:req#1490)
* 4.5.4 - Code gui panel(ID:test#1491)
    * 3.4.2 - Code GUI panel (ID:req#1490)
* 4.5.5 - 'Valid where used' test(ID:test#1155)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.5.6 - 'Where used' test(ID:test#1157)
    * 3.4.1 - Content of the assembly window (ID:req#1485)
* 4.5.8 - diff the same code(ID:test#1160)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.9 - diff the same code(ID:test#1161)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.10 - diff the same code(ID:test#1162)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.11 - diff the same code(ID:test#1163)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.12 - diff the same code(ID:test#1164)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.13 - diff two different codes(ID:test#1165)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.14 - diff two different codes(ID:test#1166)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.15 - diff two different codes(ID:test#1167)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.16 - diff two different codes(ID:test#1168)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.17 - diff two different codes(ID:test#1169)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.5.18 - diff two different codes(ID:test#1170)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
    * 3.5.2 - Diff window options (ID:req#1494)
* 4.5.19 - diff option: diff only top code(ID:test#1171)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
    * 3.5.4 - Diff window options (3) (ID:req#1504)
* 4.5.20 - diff option: diff only top code(ID:test#1172)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
    * 3.5.4 - Diff window options (3) (ID:req#1504)
* 4.5.21 - diff option: diff only main attributes(ID:test#1173)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
    * 3.5.3 - Diff window options (2) (ID:req#1503)
* 4.5.22 - diff documents(ID:test#1174)
    * 3.5.1 - Diff window main requirements (ID:req#1493)
* 4.6.2 - Copy code select date dialog(ID:test#1177)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.3 - Copy code select date dialog(ID:test#1178)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.4 - Copy code select date dialog(ID:test#1179)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.5 - Copy code window(ID:test#1181)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.6 - Copy code window(ID:test#1182)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.8 - Cancel(ID:test#1184)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.9 - Cancel(ID:test#1185)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.10 - Cancel(ID:test#1186)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.11 - Copy code window(ID:test#1187)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.12 - Copy code window(ID:test#1188)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.13 - Copy error(ID:test#1189)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.14 - Confirmation dialog / success(ID:test#1190)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.15 - Confirmation dialog / success(ID:test#1191)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.16 - Confirmation dialog / success (2)(ID:test#1192)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.17 - Confirmation dialog / success (3)(ID:test#1193)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.18 - Copy a code / date error(ID:test#1194)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.19 - copy a code (in proto mode)(ID:test#1195)
    * 3.6.1 - Copy code (ID:req#1506)
* 4.6.20.1 - Revise code window(ID:test#1197)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.2 - Copy/revise code window(ID:test#1198)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.3 - Revise a code / date error(ID:test#1199)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.4 - Revise a code / date error(ID:test#1200)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.5 - Revise a code(ID:test#1201)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.6 - revise a code (in proto mode)(ID:test#1202)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.7 - revise a prototype code to prototype(ID:test#1203)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.8 - revise a prototype code to non-prototype(ID:test#1204)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.9 - Revise a code when some fields will be reset(ID:test#1205)
    * 3.6.2 - Revise the code (ID:req#1507)
    * 3.1.6 - GVal properties (ID:req#1513)
* 4.6.20.10 - Copy a code when some fields will be reset(ID:test#1206)
    * 3.6.2 - Revise the code (ID:req#1507)
    * 3.1.6 - GVal properties (ID:req#1513)
* 4.6.20.11 - revise a code and its gavals(ID:test#1207)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.12 - revise a standard code(ID:test#1516)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.20.13 - revise a standard code(ID:test#1517)
    * 3.6.2 - Revise the code (ID:req#1507)
* 4.6.21 - BomBrowser - Edit code(ID:)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.22 - Edit code / Rev field(ID:test#1209)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.24 - Edit code / Default unit field(ID:test#1210)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.25 - Edit code / Description field(ID:test#1211)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.26 - Edit code / Generic properties field(ID:test#1212)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.27 - Add/Del/View a drawing(ID:test#1213)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.28 - Add/Del/View a drawing(ID:test#1214)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.29 - Add/Del/View a drawing(ID:test#1215)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.30 - Add/Del/View a drawing(ID:test#1216)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.31 - Add/Del/View a drawing(ID:test#1217)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.32 - Add/Del/View a drawing(ID:test#1218)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.33 - Add/Del/View a drawing(ID:test#1219)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.34 - Add/Del/View a drawing(ID:test#1220)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.35 - Copy multiple drawings(ID:test#1221)
    * 3.6.6 - Edit code: edit code drawings - copy and paste drawings (ID:req#1515)
* 4.6.36 - del single children(ID:test#1222)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.37 - del multiple children(ID:test#1223)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.38 - Copy multiple children(ID:test#1224)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.39 - add a child(ID:test#1225)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.40 - add a child(ID:test#1226)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.41 - add multiple child(ID:test#1227)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.42 - non existant code(ID:test#1228)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.43 - non existant code(ID:test#1229)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.44 - duplicate code(ID:test#1230)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.45 - wrong qty(ID:test#1231)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.46 - wrong qty(ID:test#1232)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.47 - wrong each(ID:test#1233)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.48 - wrong each(ID:test#1234)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.49 - sorting(ID:test#1235)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.50 - sorting(ID:test#1236)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.51 - sorting(ID:test#1237)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.52 - Move the children UP(ID:test#1238)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.53 - Move the children UP(ID:test#1239)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.54 - Move the children UP(ID:test#1240)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.55 - Move the children UP(ID:test#1241)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.56 - Move the children DOWN(ID:test#1242)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.57 - Move the children DOWN(ID:test#1243)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.58 - Move the children DOWN(ID:test#1244)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.59 - Move the children DOWN(ID:test#1245)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.60 - Move the children to the TOP(ID:test#1246)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.61 - Move the children to the TOP(ID:test#1247)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.62 - Move the children to the TOP(ID:test#1248)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.63 - Move the children to the TOP(ID:test#1249)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.64 - Move the children BOTTOM(ID:test#1250)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.65 - Move the children BOTTOM(ID:test#1251)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.66 - Move the children BOTTOM(ID:test#1252)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.67 - Move the children BOTTOM(ID:test#1253)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.68 - Edit code / File -> close(ID:test#1254)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.6.69 - Edit code / File -> exit(ID:test#1255)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.6.70 - Edit code / File -> exit(ID:test#1256)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.6.71 - Edit code / File -> exit(ID:test#1257)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.6.72 - Edit code / CTRL-Q(ID:test#1258)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.6.73 - Edit code / Windows(ID:test#1259)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.6.74 - Edit code / Help->about(ID:test#1260)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.6.75 - search code(ID:test#1261)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.76 - search code(ID:test#1262)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.77 - search code(ID:test#1263)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.78 - delete revision(ID:test#1264)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.79 - delete revision(ID:test#1265)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.80 - delete revision(ID:test#1266)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.81 - delete revision(ID:test#1267)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.82 - delete revision(ID:test#1268)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.83 - delete code(ID:test#1269)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.84 - delete code(ID:test#1270)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.85 - delete code(ID:test#1271)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.86 - delete code(ID:test#1272)
    * 3.6.7 - Edit code: remove a revision (ID:req#1512)
* 4.6.87 - change revision(ID:test#1273)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.88 - change revision without saving(ID:test#1274)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.89 - change revision without saving(ID:test#1275)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.90 - change revision without saving(ID:test#1276)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.91 - change revision without saving(ID:test#1277)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.92 - change revision without saving(ID:test#1278)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.93 - change revision without saving(ID:test#1279)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.94 - Make a change without saving(ID:test#1280)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.95 - Make a change without saving(ID:test#1281)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.96 - Make a change without saving(ID:test#1282)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.97 - Make a change saving(ID:test#1283)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.98 - Make a change saving(ID:test#1284)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.99 - remove a child without saving(ID:test#1285)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.100 - insert a child without saving(ID:test#1286)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.101 - insert a child without saving(ID:test#1287)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.102 - change child without saving(ID:test#1288)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.103 - add drawing without saving(ID:test#1289)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.104 - remove a drawing without saving(ID:test#1290)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.105 - add a duplicate code(ID:test#1291)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.106 - add a code to an empty children list(ID:test#1292)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.107 - exit without saving(ID:test#1293)
    * 3.6.4 - Edit code: edit child items (ID:req#1510)
* 4.6.108 - exit without saving(ID:test#1294)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.109 - exit without saving(ID:test#1295)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.110 - exit without saving(ID:test#1296)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.111 - Code Properties (file)(ID:test#1297)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
    * 3.1.6 - GVal properties (ID:req#1513)
    * 3.1.7 - GAVal properties (ID:req#1514)
* 4.6.112 - Code Properties (file)(ID:test#1298)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.113 - Code Properties (file)(ID:test#1299)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.114 - Code Properties (file)(ID:test#1300)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.115 - Code Properties (file)(ID:test#1301)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.116 - Code Properties (file)(ID:test#1302)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.117 - Code Properties (list)(ID:test#1303)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
    * 3.1.6 - GVal properties (ID:req#1513)
    * 3.1.7 - GAVal properties (ID:req#1514)
* 4.6.118 - Code Properties (list)(ID:test#1304)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.119 - Code Properties (list)(ID:test#1305)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.120 - Code Properties (list)(ID:test#1306)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.121 - Code Properties (list)(ID:test#1307)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.122 - Code Properties (list)(ID:test#1308)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.123 - Code Properties (clist)(ID:test#1309)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
    * 3.1.6 - GVal properties (ID:req#1513)
    * 3.1.7 - GAVal properties (ID:req#1514)
* 4.6.124 - Code Properties (clist)(ID:test#1310)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.125 - Code Properties (clist)(ID:test#1311)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.126 - Code Properties (clist)(ID:test#1312)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.127 - Code Properties (clist)(ID:test#1313)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.128 - Two changes at the same time(ID:test#1314)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.129 - Two changes at the same time(ID:test#1315)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.130 - Two changes at the same time(ID:test#1316)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.6.131 - Edit code, edit URL(ID:test#1317)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.132 - Edit code, edit URL(ID:test#1318)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.133 - Edit code, edit URL(ID:test#1319)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.134 - Edit code, edit URL(ID:test#1320)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.135 - Edit code, edit URL(ID:test#1321)
    * 3.6.5 - Edit code: edit code drawings (ID:req#1511)
* 4.6.136 - Edit code, undo(ID:test#1322)
    * 3.6.3 - Edit code: edit code properties (ID:req#1509)
* 4.7.1 - Cancel button(ID:test#1327)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.2 - Save button(ID:test#1328)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.3 - Save button(ID:test#1329)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.4 - Modify date(ID:test#1330)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.5 - Modify date(ID:test#1331)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.6 - Modify date with an invalid one(ID:test#1332)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.7 - Modify date with an invalid one(ID:test#1333)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.8 - Modify date with an invalid one(ID:test#1334)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.9 - Modify date with an invalid one(ID:test#1335)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.10 - Modify date with an invalid one(ID:test#1336)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.11 - Modify date with an invalid one(ID:test#1337)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.12 - Modify date with an invalid one(ID:test#1338)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.13 - Modify date with an invalid one(ID:test#1339)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.14 - Modify date with an invalid one(ID:test#1340)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.15 - Modify date with an invalid one(ID:test#1341)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.16 - Modify date with an invalid one(ID:test#1342)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.17 - Modify date with an invalid one(ID:test#1343)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.18 - Modify date(ID:test#1344)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.19 - Modify date(ID:test#1345)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.20 - Modify date(ID:test#1346)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.21 - Check the read-only/read-write status of the cells(ID:test#1347)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.22 - Insert an invalid date(ID:test#1348)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.23 - Insert an invalid date(ID:test#1349)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.24 - Insert an invalid date(ID:test#1350)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.25 - Insert a valid date(ID:test#1351)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.27 - parent too early(ID:test#1353)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.28 - parent too late(ID:test#1354)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.29 - children too late(ID:test#1355)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.30 - children too early(ID:test#1356)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.31 - children too early(ID:test#1357)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.32 - prototype date(ID:test#1358)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.33 - prototype date(ID:test#1359)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.34 - prototype date(ID:test#1360)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.7.35 - prototype date(ID:test#1361)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
* 4.7.36 - date in the title bar(ID:test#1362)
    * 3.6.8 - Edit code: change revision date (ID:req#1518)
    * 3.6.9 - Edit code: change revision date validation (ID:req#1520)
* 4.8.1 - rename bombrowser.ini(ID:test#1364)
    * 3.7.1 - Config file: basic requirements (ID:req#1610)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.2 - rename bombrowser.ini (2)(ID:test#1365)
    * 3.7.1 - Config file: basic requirements (ID:req#1610)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.3 - shutdown the sql server(ID:test#1366)
    * 3.1.8 - Check db connection (ID:req#1616)
* 4.8.4 - test re-connection after an sql server disconnection(ID:test#1367)
    * 3.1.8 - Check db connection (ID:req#1616)
* 4.8.5 - test re-connection after an sql server disconnection(ID:test#1368)
    * 3.1.8 - Check db connection (ID:req#1616)
* 4.8.6 - test re-connection after an sql server disconnection(ID:test#1369)
    * 3.1.8 - Check db connection (ID:req#1616)
* 4.8.7 - Self test(ID:test#1633)
    * 3.1.9 - Self test (ID:req#1632)
* 4.8.9 - Test description_force_uppercase: edit code(ID:test#1371)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.10 - Test description_force_uppercase: copy code(ID:test#1372)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.11 - Test description_force_uppercase: revise code(ID:test#1373)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.12 - Test description_force_uppercase: edit code(ID:test#1374)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.13 - Test description_force_uppercase: copy code(ID:test#1375)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.14 - Test description_force_uppercase: revise code(ID:test#1376)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.15 - Test code_force_uppercase: copy code(ID:test#1377)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.16 - Test code_force_uppercase: copy code(ID:test#1378)
    * 3.7.2 - Config file: force upper case (ID:req#1612)
* 4.8.17 - Test ignore_case_during_search: search code(ID:test#1379)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.18 - Test ignore_case_during_search: search code(ID:test#1380)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.19 - Test ignore_case_during_search: search code(ID:test#1381)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.20 - Test ignore_case_during_search: search code(ID:test#1382)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.21 - Test ignore_case_during_search: search revision(ID:test#1383)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.22 - Test ignore_case_during_search: search revision(ID:test#1384)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.23 - Test ignore_case_during_search: search revision(ID:test#1385)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.24 - Test ignore_case_during_search: search revision(ID:test#1386)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.25 - Test ignore_case_during_search: search revision(ID:test#1387)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.26 - Test ignore_case_during_search: search revision(ID:test#1388)
    * 3.7.3 - Config file: search ignore case (ID:req#1613)
* 4.8.27 - bombrowser.ini missing parameter(ID:test#1389)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.28 - bombrowser.ini missing section(ID:test#1390)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.29 - bombrowser.ini unknown parameter(ID:test#1391)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.30 - bombrowser.ini unknown section(ID:test#1392)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.31 - bombrowser.ini missing template(ID:test#1393)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.32 - bombrowser.ini missing importer(ID:test#1394)
    * 3.7.4 - Config file: check file (ID:req#1614)
* 4.8.33 - bombrowser.ini: list_code_default_mode(ID:test#1395)
    * 3.7.5 - Config file: default search mode (ID:req#1615)
* 4.8.34 - bombrowser.ini: list_code_default_mode(ID:test#1396)
    * 3.7.5 - Config file: default search mode (ID:req#1615)
* 4.8.35 - bombrowser.forward(ID:test#1397)
    * 3.7.1 - Config file: basic requirements (ID:req#1610)
* 4.8.36 - bombrowser.forward(ID:test#1398)
    * 3.7.1 - Config file: basic requirements (ID:req#1610)
* 4.8.37 - bombrowser-local.ini(ID:test#1399)
    * 3.7.1 - Config file: basic requirements (ID:req#1610)
* 4.11.1 - Window menu test, close all other windows(ID:test#1403)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.11.2 - Window menu test, new code list window(ID:test#1404)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.11.3 - Window menu test, new code list window(ID:test#1405)
    * 3.1.1 - Common commands (ID:req#1009)
* 4.12.1 - Advanced search in the BOM(ID:test#1407)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.2 - Advanced search in the BOM - search by code(ID:test#1408)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.3 - Advanced search in the BOM - search by descr(ID:test#1409)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.4 - Advanced search in the BOM - search by descr(ID:test#1410)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.5 - Advanced search in the BOM - search by descr(ID:test#1411)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.6 - Advanced search in the BOM - search by descr and code(ID:test#1412)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.7 - Advanced search in the BOM search w/multiple fields(ID:test#1413)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.8 - Advanced search in the BOM search w/multiple fields(ID:test#1414)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.9 - Advanced search in the BOM search w/multiple fields(ID:test#1415)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.10 - Advanced search in the BOM search w/multiple fields(ID:test#1416)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.11 - Advanced search in the BOM search w/multiple fields(ID:test#1417)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.12 - Advanced search in the BOM search w/multiple fields(ID:test#1418)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.13 - Advanced search in the BOM search w/multiple fields(ID:test#1419)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.14 - Advanced search in the BOM search w/multiple fields(ID:test#1420)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.15 - Advanced search in the BOM search w/multiple fields(ID:test#1421)
    * 3.8.1 - Search in BOM (ID:req#1618)
* 4.12.16 - Advanced search in the BOM - where used(ID:test#1422)
    * 3.8.3 - Search in '[smart/valid] where used windows' (ID:req#1620)
* 4.12.17 - Advanced search in the BOM - smart where used(ID:test#1423)
    * 3.8.3 - Search in '[smart/valid] where used windows' (ID:req#1620)
* 4.12.18 - Advanced search in the BOM - search by doc(ID:test#1424)
    * 3.8.2 - Search document in BOM (ID:req#1619)
* 4.13.1 - Export data(ID:test#1426)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.2 - Export data(ID:test#1427)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.3 - Export data(ID:test#1428)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.4 - Export data(ID:test#1429)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.5 - Export data(ID:test#1430)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.6 - Export data(ID:test#1431)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.7 - Export data(ID:test#1432)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.8 - Export data(ID:test#1433)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.9 - Export data - where used(ID:test#1434)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.10 - Export data - error in file(ID:test#1436)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.13.12 - Export data - error in file(ID:test#1438)
    * 3.9.1 - Export data, main requirements (ID:req#1622)
* 4.14.1 - Dump the database(ID:test#1440)
    * 3.10.1 - Dump database (ID:req#1624)
* 4.14.2 - Restore the database(ID:test#1441)
    * 3.10.2 - Restore database (ID:req#1625)
* 4.14.3 - Create a new (empty) database(ID:test#1442)
    * 3.10.3 - Create a new database (ID:req#1626)
* 4.14.4 - Restore a database with a specific gaval/gval column count(ID:test#1443)
    * 3.10.4 - Create a new database (ID:req#1627)
* 4.15.1 - Log create a new revision(ID:test#1445)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.2 - Log create a new code(ID:test#1446)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.3 - Log edit a code (1/6)(ID:test#1447)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.4 - Log edit a code (2/6)(ID:test#1448)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.5 - Log edit a code (3/6)(ID:test#1449)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.6 - Log edit a code (4/6)(ID:test#1450)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.7 - Log edit a code (5/6)(ID:test#1451)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.8 - Log edit a code (6/6)(ID:test#1452)
    * 3.11.1 - Log transaction: actions to log (ID:req#1629)
* 4.15.9 - Log edit a code: path doesn't exist(ID:test#1453)
    * 3.11.2 - Log transaction: cannot write the log (ID:req#1630)
* 4.15.10 - Log edit a code: compress the file(ID:test#1454)
    * 3.11.3 - Log transaction: compress the log (ID:req#1631)


### 5.2 - Requirements to tests

* 3.1.1 - Common commands(ID:req#1009)
    * 4.1.20 - menu->help->about(ID:test#1032)
    * 4.1.21 - menu->window(ID:test#1033)
    * 4.1.22 - menu->file->close(ID:test#1034)
    * 4.1.23 - menu->file->close(ID:test#1035)
    * 4.1.24 - menu->file->close(ID:test#1036)
    * 4.1.25 - Ctrl-Q  menu->file->close(ID:test#1037)
    * 4.1.26 - menu->file->exit(ID:test#1038)
    * 4.1.27 - menu->file->exit(ID:test#1039)
    * 4.1.28 - menu->file->exit(ID:test#1040)
    * 4.3.8 - menu->help->about(ID:test#1107)
    * 4.3.9 - menu->window(ID:test#1108)
    * 4.3.10 - menu->file->close(ID:test#1109)
    * 4.3.11 - Ctrl-Q  menu->file->close(ID:test#1110)
    * 4.3.12 - menu->file->exit(ID:test#1111)
    * 4.3.13 - menu->file->exit(ID:test#1112)
    * 4.3.14 - menu->file->exit(ID:test#1113)
    * 4.3.15 - menu->file->exit(ID:test#1114)
    * 4.3.16 - menu->file->exit(ID:test#1115)
    * 4.3.17 - menu->file->exit(ID:test#1116)
    * 4.6.68 - Edit code / File -> close(ID:test#1254)
    * 4.6.69 - Edit code / File -> exit(ID:test#1255)
    * 4.6.70 - Edit code / File -> exit(ID:test#1256)
    * 4.6.71 - Edit code / File -> exit(ID:test#1257)
    * 4.6.72 - Edit code / CTRL-Q(ID:test#1258)
    * 4.6.73 - Edit code / Windows(ID:test#1259)
    * 4.6.74 - Edit code / Help->about(ID:test#1260)
    * 4.11.1 - Window menu test, close all other windows(ID:test#1403)
    * 4.11.2 - Window menu test, new code list window(ID:test#1404)
    * 4.11.3 - Window menu test, new code list window(ID:test#1405)
* 3.1.2 - Copy table(ID:req#1010)
    * 4.1.29 - Menu->edit->copy(ID:test#1041)
* 3.1.3 - Document attached to a code(ID:req#1464)
    * 3.6.5 - Edit code: edit code drawings(ID:req#1511)
* 3.1.4 - URL attached to a code(ID:req#1465)
    * 4.2.15 - URL(ID:test#1094)
    * 4.2.16 - URL(ID:test#1095)
    * 4.2.18 - URL(ID:test#1097)
    * 4.2.19 - URL(ID:test#1098)
* 3.1.5 - URL attached to a code(ID:req#1495)
    * 3.6.5 - Edit code: edit code drawings(ID:req#1511)
* 3.1.6 - GVal properties(ID:req#1513)
    * 3.3.1 - The 'Code GUI' panel shows code properties(ID:req#1471)
    * 4.6.20.9 - Revise a code when some fields will be reset(ID:test#1205)
    * 4.6.20.10 - Copy a code when some fields will be reset(ID:test#1206)
    * 4.6.111 - Code Properties (file)(ID:test#1297)
    * 4.6.117 - Code Properties (list)(ID:test#1303)
    * 4.6.123 - Code Properties (clist)(ID:test#1309)
* 3.1.7 - GAVal properties(ID:req#1514)
    * 4.6.111 - Code Properties (file)(ID:test#1297)
    * 4.6.117 - Code Properties (list)(ID:test#1303)
    * 4.6.123 - Code Properties (clist)(ID:test#1309)
* 3.1.8 - Check db connection(ID:req#1616)
    * 4.8.3 - shutdown the sql server(ID:test#1366)
    * 4.8.4 - test re-connection after an sql server disconnection(ID:test#1367)
    * 4.8.5 - test re-connection after an sql server disconnection(ID:test#1368)
    * 4.8.6 - test re-connection after an sql server disconnection(ID:test#1369)
* 3.1.9 - Self test(ID:req#1632)
    * 4.8.7 - Self test(ID:test#1633)
* 3.2.1 - Search fields - code and description(ID:req#1005)
    * 4.1.1 - search a code(ID:test#1013)
    * 4.1.2 - search a code (2)(ID:test#1014)
    * 4.1.3 - search a code by description(ID:test#1015)
    * 4.1.4 - search a code by description with a wildcard(ID:test#1016)
    * 4.1.5 - search a code with a wildcard(ID:test#1017)
    * 4.1.6 - search a code and a description with wildcards(ID:test#1018)
* 3.2.2 - Search fields - wildcards(ID:req#1006)
    * 4.1.4 - search a code by description with a wildcard(ID:test#1016)
    * 4.1.5 - search a code with a wildcard(ID:test#1017)
    * 4.1.6 - search a code and a description with wildcards(ID:test#1018)
    * 4.1.38 - Revision search(ID:test#1050)
    * 4.1.39 - Revision search(ID:test#1051)
    * 4.1.41 - Revision search(ID:test#1053)
    * 4.1.42 - Revision search(ID:test#1054)
    * 4.1.45 - Revision search(ID:test#1057)
    * 4.1.46 - Revision search(ID:test#1058)
    * 4.1.47 - Revision search(ID:test#1059)
    * 4.1.48 - Revision search(ID:test#1060)
    * 4.1.49 - Revision search(ID:test#1061)
    * 4.1.50 - Revision search(ID:test#1062)
    * 4.1.51 - Revision search(ID:test#1063)
    * 4.1.52 - Revision search(ID:test#1064)
    * 4.1.53 - Revision search(ID:test#1065)
    * 4.1.54 - search <(ID:test#1068)
    * 4.1.55 - search !(ID:test#1069)
    * 4.1.56 - search =(ID:test#1070)
    * 4.1.57 - search =(ID:test#1071)
* 3.2.3 - Code property(ID:req#1460)
    * 4.1.30 - Code GUI(ID:test#1042)
    * 4.1.31 - Code GUI(ID:test#1043)
    * 4.1.43 - Revision search(ID:test#1055)
    * 4.1.44 - Revision search(ID:test#1056)
* 3.2.4 - Status bar(ID:req#1461)
    * 4.1.32 - Status bar(ID:test#1044)
    * 4.1.33 - Status bar(ID:test#1045)
    * 4.1.35 - Revision search(ID:test#1047)
    * 4.1.36 - Revision search(ID:test#1048)
* 3.2.5 - Revision search(ID:req#1462)
    * 4.1.34 - Revision search(ID:test#1046)
    * 4.1.35 - Revision search(ID:test#1047)
    * 4.1.36 - Revision search(ID:test#1048)
    * 4.1.37 - Revision search(ID:test#1049)
    * 4.1.38 - Revision search(ID:test#1050)
    * 4.1.39 - Revision search(ID:test#1051)
    * 4.1.40 - Revision search(ID:test#1052)
    * 4.1.41 - Revision search(ID:test#1053)
    * 4.1.42 - Revision search(ID:test#1054)
    * 4.1.45 - Revision search(ID:test#1057)
    * 4.1.46 - Revision search(ID:test#1058)
    * 4.1.47 - Revision search(ID:test#1059)
    * 4.1.48 - Revision search(ID:test#1060)
    * 4.1.49 - Revision search(ID:test#1061)
    * 4.1.50 - Revision search(ID:test#1062)
    * 4.1.51 - Revision search(ID:test#1063)
    * 4.1.52 - Revision search(ID:test#1064)
    * 4.1.53 - Revision search(ID:test#1065)
    * 4.1.54 - search <(ID:test#1068)
    * 4.1.55 - search !(ID:test#1069)
    * 4.1.56 - search =(ID:test#1070)
    * 4.1.57 - search =(ID:test#1071)
    * 4.1.60 - Search for CODE-COLORS-xxx(ID:test#1074)
    * 4.1.61 - Search for CODE-COLORS-xxx(ID:test#1075)
    * 4.1.62 - Search for CODE-COLORS-xxx(ID:test#1076)
    * 4.1.63 - Search for CODE-COLORS-xxx(ID:test#1077)
    * 4.1.64 - Search for CODE-COLORS-xxx(ID:test#1078)
* 3.2.6 - Revision search result colors(ID:req#1463)
    * 4.1.60 - Search for CODE-COLORS-xxx(ID:test#1074)
    * 4.1.61 - Search for CODE-COLORS-xxx(ID:test#1075)
    * 4.1.62 - Search for CODE-COLORS-xxx(ID:test#1076)
    * 4.1.63 - Search for CODE-COLORS-xxx(ID:test#1077)
    * 4.1.64 - Search for CODE-COLORS-xxx(ID:test#1078)
* 3.2.7 - Code commands(ID:req#1007)
    * 4.1.7 - assembly(ID:test#1019)
    * 4.1.8 - assembly(ID:test#1020)
    * 4.1.9 - assembly(ID:test#1021)
    * 4.1.10 - where used(ID:test#1022)
    * 4.1.11 - where used (2)(ID:test#1023)
    * 4.1.12 - valid where used(ID:test#1024)
    * 4.1.13 - valid where used (2)(ID:test#1025)
    * 4.1.14 - Copy/revise code(ID:test#1026)
    * 4.1.15 - edit code(ID:test#1027)
    * 4.1.16 - diff from(ID:test#1028)
    * 4.1.17 - diff from (2x)(ID:test#1029)
    * 4.1.18 - diff to(ID:test#1030)
    * 4.1.19 - diff to (2x)(ID:test#1031)
    * 4.1.45 - Revision search(ID:test#1057)
    * 4.1.46 - Revision search(ID:test#1058)
    * 4.1.47 - Revision search(ID:test#1059)
    * 4.1.48 - Revision search(ID:test#1060)
    * 4.1.49 - Revision search(ID:test#1061)
    * 4.1.50 - Revision search(ID:test#1062)
    * 4.1.51 - Revision search(ID:test#1063)
    * 4.1.52 - Revision search(ID:test#1064)
    * 4.1.53 - Revision search(ID:test#1065)
* 3.3.1 - The 'Code GUI' panel shows code properties(ID:req#1471)
    * 4.2.1 - general(ID:test#1080)
* 3.3.2 - The 'Code GUI' revisions list box(ID:req#1466)
    * 4.2.2 - multiple revision(ID:test#1081)
    * 4.2.3 - multiple revision (2)(ID:test#1082)
* 3.3.3 - The 'Code GUI' copy button(ID:req#1467)
    * 4.2.6 - Copy info..(ID:test#1085)
* 3.3.4 - The 'Code GUI' 'Document' button(ID:req#1468)
    * 4.2.4 - documents(ID:test#1083)
    * 4.2.5 - documents (2x)(ID:test#1084)
    * 4.2.7 - Check tool tip(ID:test#1086)
    * 4.2.8 - RMB menu of drawing button(ID:test#1087)
    * 4.2.9 - RMB menu of drawing button(ID:test#1088)
    * 4.2.10 - RMB menu of drawing button(ID:test#1089)
    * 4.2.11 - RMB menu of drawing button(ID:test#1090)
    * 4.2.12 - RMB menu of drawing button(ID:test#1091)
    * 4.2.15 - URL(ID:test#1094)
    * 4.2.16 - URL(ID:test#1095)
    * 4.2.17 - URL(ID:test#1096)
    * 4.2.18 - URL(ID:test#1097)
* 3.3.5 - The 'Code GUI' 'Document' button text length(ID:req#1469)
    * 4.2.13 - Long filename(ID:test#1092)
    * 4.2.14 - Long filename(ID:test#1093)
* 3.4.1 - Content of the assembly window(ID:req#1485)
    * 4.3.4 - show assembly(ID:test#1103)
    * 4.3.5 - show assembly (2)(ID:test#1104)
    * 4.3.6 - where used (2)(ID:test#1105)
    * 4.3.7 - valid where used (2)(ID:test#1106)
    * 4.3.26 - Find(ID:)
    * 4.3.34 - show latest assembly(ID:test#1133)
    * 4.3.35 - show latest assembly(ID:test#1134)
    * 4.3.41 - Show prototype assembly(ID:test#1140)
    * 4.3.42 - Show prototype assembly(ID:test#1141)
    * 4.5.5 - 'Valid where used' test(ID:test#1155)
    * 4.5.6 - 'Where used' test(ID:test#1157)
* 3.4.2 - Code GUI panel(ID:req#1490)
    * 4.5.3 - Code gui panel(ID:test#1492)
    * 4.5.4 - Code gui panel(ID:test#1491)
* 3.4.3 - Select date(ID:req#1481)
    * 4.3.1 - select date(ID:test#1100)
    * 4.3.2 - select date(ID:test#1101)
    * 4.3.3 - select date(ID:test#1102)
    * 4.3.5 - show assembly (2)(ID:test#1104)
* 3.4.4 - Export to JSON(ID:req#1482)
    * 4.3.18 - menu->file->export as json / csv...(ID:test#1117)
* 3.4.5 - Show/hide levels(ID:req#1483)
    * 4.3.20 - menu->view->show up level 1(ID:test#1119)
    * 4.3.21 - menu->view->show up level 1(ID:test#1120)
    * 4.3.22 - menu->view->show up level 1(ID:test#1121)
    * 4.3.23 - menu->view->show up level 1(ID:test#1122)
    * 4.3.24 - menu->view->show up level 1(ID:test#1123)
    * 4.3.25 - menu->view->show up level 1(ID:test#1124)
* 3.4.6 - Search in BOM(ID:req#1486)
    * 4.3.27 - find ctrl-f(ID:test#1126)
    * 4.3.28 - find(ID:test#1127)
    * 4.3.29 - cancel(ID:test#1128)
    * 4.3.30 - find a code(ID:test#1129)
    * 4.3.31 - find a code(ID:test#1130)
    * 4.3.32 - find a code(ID:test#1131)
    * 4.3.33 - find a code(ID:test#1132)
* 3.4.7 - Loop detection(ID:req#1487)
    * 4.4 - Check for loop(ID:test#1142)
    * 4.5 - Check for loop(ID:test#1143)
* 3.4.8 - Export(ID:req#1488)
    * 4.3.19 - menu->file->export as json / csv...(ID:test#1118)
    * 4.3.36 - Menu file -> export data(ID:test#1135)
    * 4.3.37 - Menu file -> export data(ID:test#1136)
    * 4.3.38 - Menu file -> export data(ID:test#1137)
    * 4.3.39 - Menu file -> export data with url(ID:test#1138)
    * 4.5.2 - Copy assembly(ID:test#1153)
* 3.4.9 - BOM Coloring(ID:req#1489)
    * 4.5.1.2 - Bom color(ID:test#1146)
    * 4.5.1.3 - Bom color(ID:test#1147)
    * 4.5.1.4 - Bom color(ID:test#1148)
    * 4.5.1.5 - Bom color(ID:test#1149)
    * 4.5.1.6 - Bom color(ID:test#1150)
    * 4.5.1.7 - Bom color(ID:test#1151)
    * 4.5.1.8 - Bom color(ID:test#1152)
* 3.5.1 - Diff window main requirements(ID:req#1493)
    * 4.5.8 - diff the same code(ID:test#1160)
    * 4.5.9 - diff the same code(ID:test#1161)
    * 4.5.10 - diff the same code(ID:test#1162)
    * 4.5.11 - diff the same code(ID:test#1163)
    * 4.5.12 - diff the same code(ID:test#1164)
    * 4.5.13 - diff two different codes(ID:test#1165)
    * 4.5.14 - diff two different codes(ID:test#1166)
    * 4.5.15 - diff two different codes(ID:test#1167)
    * 4.5.16 - diff two different codes(ID:test#1168)
    * 4.5.17 - diff two different codes(ID:test#1169)
    * 4.5.18 - diff two different codes(ID:test#1170)
    * 4.5.19 - diff option: diff only top code(ID:test#1171)
    * 4.5.20 - diff option: diff only top code(ID:test#1172)
    * 4.5.21 - diff option: diff only main attributes(ID:test#1173)
    * 4.5.22 - diff documents(ID:test#1174)
* 3.5.2 - Diff window options(ID:req#1494)
    * 4.5.18 - diff two different codes(ID:test#1170)
* 3.5.3 - Diff window options (2)(ID:req#1503)
    * 4.5.21 - diff option: diff only main attributes(ID:test#1173)
* 3.5.4 - Diff window options (3)(ID:req#1504)
    * 4.5.19 - diff option: diff only top code(ID:test#1171)
    * 4.5.20 - diff option: diff only top code(ID:test#1172)
* 3.6.1 - Copy code(ID:req#1506)
    * 4.6.2 - Copy code select date dialog(ID:test#1177)
    * 4.6.3 - Copy code select date dialog(ID:test#1178)
    * 4.6.4 - Copy code select date dialog(ID:test#1179)
    * 4.6.5 - Copy code window(ID:test#1181)
    * 4.6.6 - Copy code window(ID:test#1182)
    * 4.6.8 - Cancel(ID:test#1184)
    * 4.6.9 - Cancel(ID:test#1185)
    * 4.6.10 - Cancel(ID:test#1186)
    * 4.6.11 - Copy code window(ID:test#1187)
    * 4.6.12 - Copy code window(ID:test#1188)
    * 4.6.13 - Copy error(ID:test#1189)
    * 4.6.14 - Confirmation dialog / success(ID:test#1190)
    * 4.6.15 - Confirmation dialog / success(ID:test#1191)
    * 4.6.16 - Confirmation dialog / success (2)(ID:test#1192)
    * 4.6.17 - Confirmation dialog / success (3)(ID:test#1193)
    * 4.6.18 - Copy a code / date error(ID:test#1194)
    * 4.6.19 - copy a code (in proto mode)(ID:test#1195)
* 3.6.2 - Revise the code(ID:req#1507)
    * 4.6.20.1 - Revise code window(ID:test#1197)
    * 4.6.20.2 - Copy/revise code window(ID:test#1198)
    * 4.6.20.3 - Revise a code / date error(ID:test#1199)
    * 4.6.20.4 - Revise a code / date error(ID:test#1200)
    * 4.6.20.5 - Revise a code(ID:test#1201)
    * 4.6.20.6 - revise a code (in proto mode)(ID:test#1202)
    * 4.6.20.7 - revise a prototype code to prototype(ID:test#1203)
    * 4.6.20.8 - revise a prototype code to non-prototype(ID:test#1204)
    * 4.6.20.9 - Revise a code when some fields will be reset(ID:test#1205)
    * 4.6.20.10 - Copy a code when some fields will be reset(ID:test#1206)
    * 4.6.20.11 - revise a code and its gavals(ID:test#1207)
    * 4.6.20.12 - revise a standard code(ID:test#1516)
    * 4.6.20.13 - revise a standard code(ID:test#1517)
* 3.6.3 - Edit code: edit code properties(ID:req#1509)
    * 4.6.21 - BomBrowser - Edit code(ID:)
    * 4.6.22 - Edit code / Rev field(ID:test#1209)
    * 4.6.24 - Edit code / Default unit field(ID:test#1210)
    * 4.6.25 - Edit code / Description field(ID:test#1211)
    * 4.6.26 - Edit code / Generic properties field(ID:test#1212)
    * 4.6.87 - change revision(ID:test#1273)
    * 4.6.88 - change revision without saving(ID:test#1274)
    * 4.6.89 - change revision without saving(ID:test#1275)
    * 4.6.90 - change revision without saving(ID:test#1276)
    * 4.6.91 - change revision without saving(ID:test#1277)
    * 4.6.92 - change revision without saving(ID:test#1278)
    * 4.6.93 - change revision without saving(ID:test#1279)
    * 4.6.94 - Make a change without saving(ID:test#1280)
    * 4.6.95 - Make a change without saving(ID:test#1281)
    * 4.6.96 - Make a change without saving(ID:test#1282)
    * 4.6.97 - Make a change saving(ID:test#1283)
    * 4.6.98 - Make a change saving(ID:test#1284)
    * 4.6.108 - exit without saving(ID:test#1294)
    * 4.6.109 - exit without saving(ID:test#1295)
    * 4.6.110 - exit without saving(ID:test#1296)
    * 4.6.111 - Code Properties (file)(ID:test#1297)
    * 4.6.112 - Code Properties (file)(ID:test#1298)
    * 4.6.113 - Code Properties (file)(ID:test#1299)
    * 4.6.114 - Code Properties (file)(ID:test#1300)
    * 4.6.115 - Code Properties (file)(ID:test#1301)
    * 4.6.116 - Code Properties (file)(ID:test#1302)
    * 4.6.117 - Code Properties (list)(ID:test#1303)
    * 4.6.118 - Code Properties (list)(ID:test#1304)
    * 4.6.119 - Code Properties (list)(ID:test#1305)
    * 4.6.120 - Code Properties (list)(ID:test#1306)
    * 4.6.121 - Code Properties (list)(ID:test#1307)
    * 4.6.122 - Code Properties (list)(ID:test#1308)
    * 4.6.123 - Code Properties (clist)(ID:test#1309)
    * 4.6.124 - Code Properties (clist)(ID:test#1310)
    * 4.6.125 - Code Properties (clist)(ID:test#1311)
    * 4.6.126 - Code Properties (clist)(ID:test#1312)
    * 4.6.127 - Code Properties (clist)(ID:test#1313)
    * 4.6.128 - Two changes at the same time(ID:test#1314)
    * 4.6.129 - Two changes at the same time(ID:test#1315)
    * 4.6.130 - Two changes at the same time(ID:test#1316)
    * 4.6.136 - Edit code, undo(ID:test#1322)
* 3.6.4 - Edit code: edit child items(ID:req#1510)
    * 4.6.36 - del single children(ID:test#1222)
    * 4.6.37 - del multiple children(ID:test#1223)
    * 4.6.38 - Copy multiple children(ID:test#1224)
    * 4.6.39 - add a child(ID:test#1225)
    * 4.6.40 - add a child(ID:test#1226)
    * 4.6.41 - add multiple child(ID:test#1227)
    * 4.6.42 - non existant code(ID:test#1228)
    * 4.6.43 - non existant code(ID:test#1229)
    * 4.6.44 - duplicate code(ID:test#1230)
    * 4.6.45 - wrong qty(ID:test#1231)
    * 4.6.46 - wrong qty(ID:test#1232)
    * 4.6.47 - wrong each(ID:test#1233)
    * 4.6.48 - wrong each(ID:test#1234)
    * 4.6.49 - sorting(ID:test#1235)
    * 4.6.50 - sorting(ID:test#1236)
    * 4.6.51 - sorting(ID:test#1237)
    * 4.6.52 - Move the children UP(ID:test#1238)
    * 4.6.53 - Move the children UP(ID:test#1239)
    * 4.6.54 - Move the children UP(ID:test#1240)
    * 4.6.55 - Move the children UP(ID:test#1241)
    * 4.6.56 - Move the children DOWN(ID:test#1242)
    * 4.6.57 - Move the children DOWN(ID:test#1243)
    * 4.6.58 - Move the children DOWN(ID:test#1244)
    * 4.6.59 - Move the children DOWN(ID:test#1245)
    * 4.6.60 - Move the children to the TOP(ID:test#1246)
    * 4.6.61 - Move the children to the TOP(ID:test#1247)
    * 4.6.62 - Move the children to the TOP(ID:test#1248)
    * 4.6.63 - Move the children to the TOP(ID:test#1249)
    * 4.6.64 - Move the children BOTTOM(ID:test#1250)
    * 4.6.65 - Move the children BOTTOM(ID:test#1251)
    * 4.6.66 - Move the children BOTTOM(ID:test#1252)
    * 4.6.67 - Move the children BOTTOM(ID:test#1253)
    * 4.6.75 - search code(ID:test#1261)
    * 4.6.76 - search code(ID:test#1262)
    * 4.6.77 - search code(ID:test#1263)
    * 4.6.99 - remove a child without saving(ID:test#1285)
    * 4.6.100 - insert a child without saving(ID:test#1286)
    * 4.6.101 - insert a child without saving(ID:test#1287)
    * 4.6.102 - change child without saving(ID:test#1288)
    * 4.6.105 - add a duplicate code(ID:test#1291)
    * 4.6.106 - add a code to an empty children list(ID:test#1292)
    * 4.6.107 - exit without saving(ID:test#1293)
* 3.6.5 - Edit code: edit code drawings(ID:req#1511)
    * 4.6.27 - Add/Del/View a drawing(ID:test#1213)
    * 4.6.28 - Add/Del/View a drawing(ID:test#1214)
    * 4.6.29 - Add/Del/View a drawing(ID:test#1215)
    * 4.6.30 - Add/Del/View a drawing(ID:test#1216)
    * 4.6.31 - Add/Del/View a drawing(ID:test#1217)
    * 4.6.32 - Add/Del/View a drawing(ID:test#1218)
    * 4.6.33 - Add/Del/View a drawing(ID:test#1219)
    * 4.6.34 - Add/Del/View a drawing(ID:test#1220)
    * 4.6.103 - add drawing without saving(ID:test#1289)
    * 4.6.104 - remove a drawing without saving(ID:test#1290)
    * 4.6.131 - Edit code, edit URL(ID:test#1317)
    * 4.6.132 - Edit code, edit URL(ID:test#1318)
    * 4.6.133 - Edit code, edit URL(ID:test#1319)
    * 4.6.134 - Edit code, edit URL(ID:test#1320)
    * 4.6.135 - Edit code, edit URL(ID:test#1321)
* 3.6.6 - Edit code: edit code drawings - copy and paste drawings(ID:req#1515)
    * 4.6.35 - Copy multiple drawings(ID:test#1221)
* 3.6.7 - Edit code: remove a revision(ID:req#1512)
    * 4.6.78 - delete revision(ID:test#1264)
    * 4.6.79 - delete revision(ID:test#1265)
    * 4.6.80 - delete revision(ID:test#1266)
    * 4.6.81 - delete revision(ID:test#1267)
    * 4.6.82 - delete revision(ID:test#1268)
    * 4.6.83 - delete code(ID:test#1269)
    * 4.6.84 - delete code(ID:test#1270)
    * 4.6.85 - delete code(ID:test#1271)
    * 4.6.86 - delete code(ID:test#1272)
* 3.6.8 - Edit code: change revision date(ID:req#1518)
    * 4.7.1 - Cancel button(ID:test#1327)
    * 4.7.2 - Save button(ID:test#1328)
    * 4.7.3 - Save button(ID:test#1329)
    * 4.7.4 - Modify date(ID:test#1330)
    * 4.7.5 - Modify date(ID:test#1331)
    * 4.7.8 - Modify date with an invalid one(ID:test#1334)
    * 4.7.9 - Modify date with an invalid one(ID:test#1335)
    * 4.7.10 - Modify date with an invalid one(ID:test#1336)
    * 4.7.11 - Modify date with an invalid one(ID:test#1337)
    * 4.7.12 - Modify date with an invalid one(ID:test#1338)
    * 4.7.13 - Modify date with an invalid one(ID:test#1339)
    * 4.7.14 - Modify date with an invalid one(ID:test#1340)
    * 4.7.15 - Modify date with an invalid one(ID:test#1341)
    * 4.7.16 - Modify date with an invalid one(ID:test#1342)
    * 4.7.17 - Modify date with an invalid one(ID:test#1343)
    * 4.7.18 - Modify date(ID:test#1344)
    * 4.7.19 - Modify date(ID:test#1345)
    * 4.7.20 - Modify date(ID:test#1346)
    * 4.7.21 - Check the read-only/read-write status of the cells(ID:test#1347)
    * 4.7.22 - Insert an invalid date(ID:test#1348)
    * 4.7.23 - Insert an invalid date(ID:test#1349)
    * 4.7.24 - Insert an invalid date(ID:test#1350)
    * 4.7.25 - Insert a valid date(ID:test#1351)
    * 4.7.27 - parent too early(ID:test#1353)
    * 4.7.28 - parent too late(ID:test#1354)
    * 4.7.29 - children too late(ID:test#1355)
    * 4.7.30 - children too early(ID:test#1356)
    * 4.7.31 - children too early(ID:test#1357)
    * 4.7.32 - prototype date(ID:test#1358)
    * 4.7.33 - prototype date(ID:test#1359)
    * 4.7.34 - prototype date(ID:test#1360)
    * 4.7.35 - prototype date(ID:test#1361)
    * 4.7.36 - date in the title bar(ID:test#1362)
* 3.6.9 - Edit code: change revision date validation(ID:req#1520)
    * 4.7.6 - Modify date with an invalid one(ID:test#1332)
    * 4.7.7 - Modify date with an invalid one(ID:test#1333)
    * 4.7.8 - Modify date with an invalid one(ID:test#1334)
    * 4.7.9 - Modify date with an invalid one(ID:test#1335)
    * 4.7.10 - Modify date with an invalid one(ID:test#1336)
    * 4.7.11 - Modify date with an invalid one(ID:test#1337)
    * 4.7.12 - Modify date with an invalid one(ID:test#1338)
    * 4.7.13 - Modify date with an invalid one(ID:test#1339)
    * 4.7.14 - Modify date with an invalid one(ID:test#1340)
    * 4.7.15 - Modify date with an invalid one(ID:test#1341)
    * 4.7.16 - Modify date with an invalid one(ID:test#1342)
    * 4.7.17 - Modify date with an invalid one(ID:test#1343)
    * 4.7.22 - Insert an invalid date(ID:test#1348)
    * 4.7.23 - Insert an invalid date(ID:test#1349)
    * 4.7.24 - Insert an invalid date(ID:test#1350)
    * 4.7.25 - Insert a valid date(ID:test#1351)
    * 4.7.27 - parent too early(ID:test#1353)
    * 4.7.28 - parent too late(ID:test#1354)
    * 4.7.29 - children too late(ID:test#1355)
    * 4.7.30 - children too early(ID:test#1356)
    * 4.7.31 - children too early(ID:test#1357)
    * 4.7.32 - prototype date(ID:test#1358)
    * 4.7.34 - prototype date(ID:test#1360)
    * 4.7.36 - date in the title bar(ID:test#1362)
* 3.7.1 - Config file: basic requirements(ID:req#1610)
    * 4.8.1 - rename bombrowser.ini(ID:test#1364)
    * 4.8.2 - rename bombrowser.ini (2)(ID:test#1365)
    * 4.8.35 - bombrowser.forward(ID:test#1397)
    * 4.8.36 - bombrowser.forward(ID:test#1398)
    * 4.8.37 - bombrowser-local.ini(ID:test#1399)
* 3.7.2 - Config file: force upper case(ID:req#1612)
    * 4.8.9 - Test description_force_uppercase: edit code(ID:test#1371)
    * 4.8.10 - Test description_force_uppercase: copy code(ID:test#1372)
    * 4.8.11 - Test description_force_uppercase: revise code(ID:test#1373)
    * 4.8.12 - Test description_force_uppercase: edit code(ID:test#1374)
    * 4.8.13 - Test description_force_uppercase: copy code(ID:test#1375)
    * 4.8.14 - Test description_force_uppercase: revise code(ID:test#1376)
    * 4.8.15 - Test code_force_uppercase: copy code(ID:test#1377)
    * 4.8.16 - Test code_force_uppercase: copy code(ID:test#1378)
* 3.7.3 - Config file: search ignore case(ID:req#1613)
    * 4.8.17 - Test ignore_case_during_search: search code(ID:test#1379)
    * 4.8.18 - Test ignore_case_during_search: search code(ID:test#1380)
    * 4.8.19 - Test ignore_case_during_search: search code(ID:test#1381)
    * 4.8.20 - Test ignore_case_during_search: search code(ID:test#1382)
    * 4.8.21 - Test ignore_case_during_search: search revision(ID:test#1383)
    * 4.8.22 - Test ignore_case_during_search: search revision(ID:test#1384)
    * 4.8.23 - Test ignore_case_during_search: search revision(ID:test#1385)
    * 4.8.24 - Test ignore_case_during_search: search revision(ID:test#1386)
    * 4.8.25 - Test ignore_case_during_search: search revision(ID:test#1387)
    * 4.8.26 - Test ignore_case_during_search: search revision(ID:test#1388)
* 3.7.4 - Config file: check file(ID:req#1614)
    * 4.8.1 - rename bombrowser.ini(ID:test#1364)
    * 4.8.2 - rename bombrowser.ini (2)(ID:test#1365)
    * 4.8.27 - bombrowser.ini missing parameter(ID:test#1389)
    * 4.8.28 - bombrowser.ini missing section(ID:test#1390)
    * 4.8.29 - bombrowser.ini unknown parameter(ID:test#1391)
    * 4.8.30 - bombrowser.ini unknown section(ID:test#1392)
    * 4.8.31 - bombrowser.ini missing template(ID:test#1393)
    * 4.8.32 - bombrowser.ini missing importer(ID:test#1394)
* 3.7.5 - Config file: default search mode(ID:req#1615)
    * 4.8.33 - bombrowser.ini: list_code_default_mode(ID:test#1395)
    * 4.8.34 - bombrowser.ini: list_code_default_mode(ID:test#1396)
* 3.8.1 - Search in BOM(ID:req#1618)
    * 4.12.1 - Advanced search in the BOM(ID:test#1407)
    * 4.12.2 - Advanced search in the BOM - search by code(ID:test#1408)
    * 4.12.3 - Advanced search in the BOM - search by descr(ID:test#1409)
    * 4.12.4 - Advanced search in the BOM - search by descr(ID:test#1410)
    * 4.12.5 - Advanced search in the BOM - search by descr(ID:test#1411)
    * 4.12.6 - Advanced search in the BOM - search by descr and code(ID:test#1412)
    * 4.12.7 - Advanced search in the BOM search w/multiple fields(ID:test#1413)
    * 4.12.8 - Advanced search in the BOM search w/multiple fields(ID:test#1414)
    * 4.12.9 - Advanced search in the BOM search w/multiple fields(ID:test#1415)
    * 4.12.10 - Advanced search in the BOM search w/multiple fields(ID:test#1416)
    * 4.12.11 - Advanced search in the BOM search w/multiple fields(ID:test#1417)
    * 4.12.12 - Advanced search in the BOM search w/multiple fields(ID:test#1418)
    * 4.12.13 - Advanced search in the BOM search w/multiple fields(ID:test#1419)
    * 4.12.14 - Advanced search in the BOM search w/multiple fields(ID:test#1420)
    * 4.12.15 - Advanced search in the BOM search w/multiple fields(ID:test#1421)
* 3.8.2 - Search document in BOM(ID:req#1619)
    * 4.12.18 - Advanced search in the BOM - search by doc(ID:test#1424)
* 3.8.3 - Search in '[smart/valid] where used windows'(ID:req#1620)
    * 4.12.16 - Advanced search in the BOM - where used(ID:test#1422)
    * 4.12.17 - Advanced search in the BOM - smart where used(ID:test#1423)
* 3.9.1 - Export data, main requirements(ID:req#1622)
    * 4.13.1 - Export data(ID:test#1426)
    * 4.13.2 - Export data(ID:test#1427)
    * 4.13.3 - Export data(ID:test#1428)
    * 4.13.4 - Export data(ID:test#1429)
    * 4.13.5 - Export data(ID:test#1430)
    * 4.13.6 - Export data(ID:test#1431)
    * 4.13.7 - Export data(ID:test#1432)
    * 4.13.8 - Export data(ID:test#1433)
    * 4.13.9 - Export data - where used(ID:test#1434)
    * 4.13.10 - Export data - error in file(ID:test#1436)
    * 4.13.12 - Export data - error in file(ID:test#1438)
* 3.10.1 - Dump database(ID:req#1624)
    * 4.14.1 - Dump the database(ID:test#1440)
* 3.10.2 - Restore database(ID:req#1625)
    * 4.14.2 - Restore the database(ID:test#1441)
* 3.10.3 - Create a new database(ID:req#1626)
    * 4.14.3 - Create a new (empty) database(ID:test#1442)
* 3.10.4 - Create a new database(ID:req#1627)
    * 4.14.4 - Restore a database with a specific gaval/gval column count(ID:test#1443)
* 3.11.1 - Log transaction: actions to log(ID:req#1629)
    * 4.15.1 - Log create a new revision(ID:test#1445)
    * 4.15.2 - Log create a new code(ID:test#1446)
    * 4.15.3 - Log edit a code (1/6)(ID:test#1447)
    * 4.15.4 - Log edit a code (2/6)(ID:test#1448)
    * 4.15.5 - Log edit a code (3/6)(ID:test#1449)
    * 4.15.6 - Log edit a code (4/6)(ID:test#1450)
    * 4.15.7 - Log edit a code (5/6)(ID:test#1451)
    * 4.15.8 - Log edit a code (6/6)(ID:test#1452)
* 3.11.2 - Log transaction: cannot write the log(ID:req#1630)
    * 4.15.9 - Log edit a code: path doesn't exist(ID:test#1453)
* 3.11.3 - Log transaction: compress the log(ID:req#1631)
    * 4.15.10 - Log edit a code: compress the file(ID:test#1454)


### 5.3 - Tests without requirements

* 4.13.11 - Export data - error in file (ID:test#1437)


### 5.4 - Requirements without tests

@@show_reqs_without_child()

## 6 - Conclusion

### 6.1 - Summary of the results

Date: 2026-09-19
'bombrowser' version: v1.0.4
Total requirements: 59
Total tests: 412
Passed tests: 409

### 6.2 - List of failed tests

* 4.6.29 - Add/Del/View a drawing (ID:test#1215)
* 4.8.3 - shutdown the sql server (ID:test#1366)
* 4.15.10 - Log edit a code: compress the file (ID:test#1454)


### 6.3 - Final result

xxx

