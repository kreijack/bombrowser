#  - BOMBrowser tests list

## 1 - Index

- 1 - Index
- 2 - Preface
- 3 - 'Codes list' window
- 4 - 'Date dialog'
- 5 - 'Code gui' panel
- 6 - Assembly window
- 7 - 'Valid where used' window
- 8 - 'Where used' window
- 9 - 'Select date' (empty)
- 10 - Diff window
- 11 - 'Copy/revise code'
- 12 - 'Edit code' window
- 13 - 'Edit date' window
- 14 - Generic test
- 15 - Export test
- 16 - Import test
- 17 - Window menu test
- 18 - Advanced search in the BOM
- 19 - Export data from assemblies
- 20 - Test bombrowser servers backends
- 21 - Run bombrowser selftest
- 22 - Repeat some tests for foreign OS

## 2 - Preface

This tests list assumes that you are working with the test database generated
by mkdb.py.
This tests list is related to the v0.4.x code

## 3 - 'Codes list' window'

### 3.1 - search a code

Test description:
Insert the code '820037' in the 'Code' field and press **ENTER**

Expected results:
The code 820037 is showed

Passed: [X]

### 3.2 - search a code (2)

Test description:
Insert the code '820038' in the 'Code' field and press the button **'Search'**

Expected results:
The code 820038 is showed

Passed: [X]

### 3.3 - search a code by description

Test description:
Insert the code 'BOARD 14' in the 'Description' field and press the button 'Search'

Expected results:
The code 610014 - "BOARD 14" is showed

Passed: [X]

### 3.4 - search a code by description with a jolly character

Test description:
Insert the code '%BOARD%13' in the 'Description' field and press ENTER

Expected results:
The code 610013 - "BOARD 13" is showed

Passed: [X]

### 3.5 - search a code with a jolly character

Test description:
- Insert the code '%6%' in the 'Code' field
- press the button 'Search'

Expected results:
The codes that contains '6' are showed

Passed: [X]

### 3.6 - search a code and a description with a jolly character

Test description:
- Insert the code '%6%' in the 'Code' field
- insert %BOARD% in the description filed
- press the button 'Search'

Expected results:
The codes that contains '6' and the description which contains BOARD are showed

Passed: [X]

### 3.7 - assembly

Test description:
- Insert the code '820037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Show assembly by date" command.

Expected results:
- The "BOMBrowser: select date" dialog is showed
- this dialog contains a list of 820037 codes.

Passed: [X]

Test description #2:
- repeat the steps in the first test
- select the "Show latest assembly" command.

Expected results #2:
- The "BOMBrowser: assembly window" dialog is showed
- the bom showed is related to the latest revision (i.e all the items have a not defined "Date to" date)

Passed: [X]

Test description #3:
- repeat the steps in the first test
- select the "Show prototype assembly" command.

Expected results #3:
- The "BOMBrowser: assembly window" dialog is showed
- the bom showed is related to the latest revision (i.e all the items have a not defined "Date to" date) with the excpetion of few items which have as "date from" the prototype one

Passed: [X]

### 3.10 - where used

Test description:
- Insert the code '810036' in the 'Code' field,
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Where used" command.

Expected results:
The "BOMBrowser - Where used" window is showed

Passed: [X]

### 3.11 - where used (2)

Test description:
- Insert the code '100037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Where used" command.

Expected results:
The "BOMBrowser - Where used" window is showed. Only one code (100037) is showed.

Passed: [X]

### 3.12 - valid where used

Test description:
- Insert the code '810036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Valid where used" command.

Expected results:
The "BOMBrowser - Valid where used" window is showed

Passed: [X]

### 3.13 - valid where used (2)

Test description:
- Insert the code '100037' in the 'Code' field
- and press the button 'Search'
- press the right mouse button on the first entry
- select the "Valid where used" command.

Expected results:
The "BOMBrowser - Valid where used" window is showed. Only one code (100037) is showed.

Passed: [X]

### 3.14 - Copy/revise code

Test description:
- Insert the code '810037' in the 'Code' field,
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Copy/revise code" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this contains a list of the code 810037.

Passed: [X]

### 3.15 - edit code

Test description:
- Insert the code '810036' in the 'Code' field
- and press the button 'Search'
- press the right mouse button on the first entry
- select the "Edit code" command.

Expected results:
The "BOMBrowser - Edit code" window showed; this contains the code 810036 properties.

Passed: [X]

### 3.16 - diff from

Test description:
- Insert the code '810037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff from" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 810037 codes.

Passed: [X]

### 3.17 - diff from (2x)

Test description:
- Insert the code '820036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff from" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.

Passed: [X]

### 3.18 - diff to

Test description:
- Insert the code '810037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff to" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 810037 codes.

Passed: [X]

### 3.19 - diff to (2x)

Test description:
- Insert the code '820036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff to" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.

Passed: [X]

### 3.20 - menu->help->about

Test description:
In the menu select the Help and About subcommand

Expected results:
- The "about" dialog is showed. The dialog contains:
- the current version and the copyright code.
- a text that showed the used connection

Passed: [X]

### 3.21 - menu->window

Test description:
- insert code 820037
- press the right mouse button on the first entry
- select the "Show assembly by date" command
- select the first date and doubleckick on it
- go back to the "BOMBrowser - code list"
- press the right mouse button on the first entry
- select the "Where used" command.
- go back to the "BOMBrowser - code list"
- press the right mouse button on the first entry
- select the "Valid where used" command.
- go back to the "BOMBrowser - code list"
- press the right mouse button on the first entry
- select the "Edit code" command.
- Five windows are opened. Select the "Windows menu" in the "BOMBrowser - Codes list" window:

Expected results:
in the menu are showed the four windows: BOMBrowser - Where used, BOM Browser - valid where used, BOMBrowser assembly, BOMBrowser - edit

Passed: [X]

### 3.22 - menu->file->close

Test description:
- insert code 820037
- press the right mouse button on the first entry and select the "Where used" command.
- Two windows are opened. Select the "File->close" in the "BOMBrowser - Codes list" window:

Expected results:
- The "BOMBrowser - Codes" list is closed. "BOMBrowser - Where used" is opened.

Passed: [X]

Test description #2:
- after the steps above, in the previous opened "where used window", press CTRL-L

Expected results #2:
- The "BOMBrowser - Codes" appears

Passed: [X]

Test description #3:
- after the steps above, re-close "BOMBrowser - Codes list" window.
- in the previous opened "where used window", select from the windows menu the "new codes list window"

Expected results #3:
- The "BOMBrowser - Codes list" appears

Passed: [X]

### 3.25 - Test 1.24 -Ctrl-Q  menu->file->close

Test description:
- insert code 820037
- press the right mouse button on the first entry and select the "Where used" command.
- Two windows are opened. Set the focus to the "BOMBrowser - Codes list"
- press CTRL-Q

Expected results:
The "BOMBrowser - Codes list" is closed. "BOMBrowser - Where used" is opened.

Passed: [X]

### 3.26 - menu->file->exit

Test description:
- insert code 820037
- press the right mouse button on the first entry and select the "Where used" command.
- Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Codes list" window:

Expected results:
a dialog BOMBrowser asking about the possibility to exit is showed.

Passed: [X]

Test description #2:
- After the steps above,  Press No

Expected results #2:
The codes list window is still opened

Passed: [X]

Test description #3:
- Repeat the step above until the dialog is showed, then press yes

Expected results #3:
The application is ended. No window is sowed

Passed: [X]

### 3.29 - Menu->edit->copy

Test description:
- insert code %6% and press ENTER;
- select menu->edit->copy
- Paste the clipboard in an editor

Expected results:
- check that there is the same table showed in the BOMBrowser - Codes list (fields TAB separated).
- Check that the number of row are the same +1 of the "BOMBrowser - Codes list" widow (there is the header)

Passed: [X]

### 3.30 - Code gui

Test description:
- insert code 8200% and press ENTER
- Select the first entry

Expected results:
the information of the selected code is showed in the right panel

Passed: [X]

Test description #2:
- after the steps above, select the 2nd entry.

Expected results #2:
the information of the 2nd selected codes are showed in the right panel

Passed: [X]

### 3.32 - Status bar

Test description:
- insert code 8200% and press ENTER

Expected results:
in the status bar appears the number of the results

Passed: [X]

### 3.33 - Status bar

Test description:
- insert code CODE_INVALID and press ENTER

Expected results:
- in the status bar appears the number of the results (0)
- the previous results are *NOT* cleaned

Passed: [X]

### 3.34 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code 8200% and press "Search"

Expected results:
in the status bar appears the number of the results

Passed: [X]

### 3.35 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code CODE_INVALID and press "Search"

Expected results:
in the status bar appears the number of the results (0)

Passed: [X]

### 3.36 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code CODE_INVALID and press "Search"

Expected results:
- in the status bar appears the number of the results (0)
- the previous results are not cleaned

Passed: [X]

### 3.37 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code 820025 and press "Search"

Expected results:
- in the status bar appears the number of the results (>= 2)
- in the results table, appears the different revisions of the searched code

Passed: [X]

### 3.38 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code 8200% and press "Search"

Expected results:
- in the results table, appears the codes (and their revisions) which start from 8200..

Passed: [X]

### 3.39 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code >820000 and press "Search"

Expected results:
- in the results table, appears the codes greather than 820000

Passed: [X]

### 3.40 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert date-from 2003-06-04 and press "Search"

Expected results:
- in the results table, it appears the codes which have as date from 2003-06-04

Passed: [X]

### 3.41 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert date-from '>2003-06-04' and press "Search"

Expected results:
- in the results table, appears the codes which have as date from greather than 2003-06-04 (prototype too)

Passed: [X]

### 3.42 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code >820000 and press ENTER

Expected results:
- in the results table, appears the codes greather than 820000

Passed: [X]

### 3.43 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code >820000 and press ENTER
- select a code

Expected results:
- depending the code selected, the right panel "code gui" change their values accordling

Passed: [X]

Test description #2:
- Selected a different code

Expected results #2:
- depending the code selected, the right panel "code gui" change their values accordling

Passed: [X]

Test description #3:
- Repeat the test #2 several times

Expected results #3:
- the Expected results#2 apply

Passed: [X]

### 3.46 - Revision search, field validation

Preparatory steps:
- select from the menu "Search mode->advanced"
- insert code >820000 and press ENTER


Test description:
insert a number in the 'id' field

Expected results:
a green border appears

Passed: [X]

Test description #2:
insert '=123' in the 'id' field

Expected results #2:
a green border appears

Passed: [X]

Test description #3:
insert '>123' in the 'id' field

Expected results #3:
a green border appears

Passed: [X]

Test description #4:
insert '<123' in the 'id' field

Expected results #4:
a green border appears

Passed: [X]

Test description #5:
insert '!123' in the 'id' field

Expected results #5:
a green border appears

Passed: [X]

Test description #6:
insert a letter in the 'id' field

Expected results #6:
the letter doesn't appear

Passed: [X]

Test description #7:
insert a number in the 'rid' field

Expected results #7:
a green border appears

Passed: [X]

Test description #8:
insert a letter 'rid' field

Expected results #8:
the letter doesn't appear

Passed: [X]

Test description #9:
insert the date '2022-01-01' in the 'date from' field

Expected results #9:
a green border appears

Passed: [X]

Test description #10:
insert the date '20-01-01' in the 'date from' field

Expected results #10:
a brown border appears

Passed: [X]

Test description #11:
insert the date '>2022-01-01' in the 'date from' field

Expected results #11:
a green border appears

Passed: [X]

Test description #12:
insert the date '<2022-01-01' in the 'date from' field

Expected results #12:
a green border appears

Passed: [X]

Test description #13:
insert the date '=2022-01-01' in the 'date from' field

Expected results #13:
a green border appears

Passed: [X]

Test description #14:
insert the date '!2022-01-01' in the 'date from' field

Expected results #14:
a green border appears

Passed: [X]

Test description #15:
insert a letter 'date from' field

Expected results #15:
the letter doesn't appear

Passed: [X]

Test description #16:
insert the date '2022-01-01' in the 'date to' field

Expected results #16:
a green border appears

Passed: [X]

Test description #17:
insert a letter 'date to' field

Expected results #17:
the letter doesn't appear

Passed: [X]

### 3.63 - RMB menu

Test description:
- select from the menu "Search mode->advanced"
- insert code >820000 and press ENTER
- select a code
- press the RMB, and select "show latest assembly"

Expected results:
- The assembling window is showed. the data reflect the latest code

Passed: [X]

Test description #2:
- repeat the steps above until the RMB press
- press the RMB, and select "where used"

Expected results #2:
- The where used window is showed

Passed: [X]

Test description #3:
- repeat the steps above until the RMB press
- press the RMB, and select "valid where used"

Expected results #3:
- The valid where used window is showed

Passed: [X]

Test description #4:
- repeat the steps above until the RMB press
- press the RMB, and select "show assembly by date"

Expected results #4:
- The "select date" dialog is opened (press cancel and return the previous window)

Passed: [X]

Test description #5:
- repeat the steps above until the RMB press
- press the RMB, and select "show assembly by date"

Expected results #5:
- The "select date" dialog is opened (press cancel and return the previous window)

Passed: [X]

Test description #6:
- repeat the steps above until the RMB press
- press the RMB, and select "show this assembly"

Expected results #6:
- The "assembly window" is showed; the assembly is the one dated with the date from of the selected code

Passed: [X]

Test description #7:
- repeat the steps above until the RMB press
- press the RMB, and select "show prototype assembly"

Expected results #7:
- The "prototype assembly window" is showed
- Go through the items and check that some items are prototype

Passed: [X]

Test description #8:
- repeat the steps above until the RMB press
- press the RMB, and select "copy revise a code"

Expected results #8:
- The "select date" dialog is opened (press cancel and return the previous window)

Passed: [X]

Test description #9:
- repeat the steps above until the RMB press
- press the RMB, and select "edit code"

Expected results #9:
- The "edit code" window is showed

Passed: [X]

Test description #10:
- repeat the steps above until the RMB press
- press the RMB, and select "diff from"
- press the RMB, and select "diff to"

Expected results #10:
- The diff window is showed

Passed: [X]

### 3.73 - search <

Test description:
- select from the menu "Search mode->advanced"
- insert code <5000 and press ENTER


Expected results:
- All codes less than 5000 are showed (lexicographica comparation: 10000 is less than 50)

Passed: [X]

### 3.74 - search !

Test description:
- select from the menu "Search mode->advanced"
- insert code !820001 and press ENTER


Expected results:
- All codes less different from 820001 are showed

Passed: [X]

### 3.75 - search =

Test description:
- select from the menu "Search mode->advanced"
- insert code =820001 and press ENTER

Expected results:
- Only the code 820001 (in all its revisions) is showed

Passed: [X]

## 4 - Date dialog test

### 4.1 - Invalid date date

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
type an invalid date (eg. 2001-02-30)

Expected results:
the widget became yellow

Passed: [X]

### 4.2 - Invalid date date (2)

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
type an invalid key (eg. k)

Expected results:
the key is rejected

Passed: [X]

### 4.3 - Invalid date date (3)

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
insert "PRO" (the first part of prototype)

Expected results:
the dialog shows "PRO" but it is yellow

Passed: [X]

### 4.4 - Invalid date date (4)

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
insert "200" (the first part of 2001-01-01)

Expected results:
the dialog shows "200" but it is yellow

Passed: [X]

### 4.5 - Prototype date

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
- insert "prototype"


Expected results:
the dialog shows "prototype" (white background)

Passed: [X]

### 4.6 - Prototype date (2)

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
press the "P" button


Expected results:
the dialog shows "PROTOTYPE

Passed: [X]

### 4.7 - Date dialog

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
press the "..." button


Expected results:
a date dialog is showed

Passed: [X]

Test description #2:
press the Cancel


Expected results #2:
the previous data is showed

Passed: [X]

### 4.9 - Date dialog (2)

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
-press the "..." button
-select a date
-press OK

Expected results:
the selected date is showed

Passed: [X]

### 4.10 - Date dialog (2)

Preparatory steps:
- in the Code list window search the code 810001
- revise it using the command "Copy/Revise code..." in the RBM menu
- select the first row in the dialog
- the Revise code window appears; locate the date widget

Test description:
-press the "..." button
-select a date with a double ckick

Expected results:
the selected date is showed

Passed: [X]

## 5 - 'Code gui' panel

### 5.1 - general

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the first entry (820000)

Expected results:
on the left panel there are the information of the selected code

Passed: [X]

### 5.2 - multiple revision

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Select another date in the rightmost combobox

Expected results:
The information on the panel are changed accordly

Passed: [X]

### 5.3 - multiple revision (2)

Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001)

Expected results:
The right combo box button, contains all the dates

Passed: [X]

### 5.4 - documents

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)

Expected results:
In the bottom part are showed two buttons with two documens

Passed: [X]

### 5.5 - documents (2x)

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Press a document button

Expected results:
Clicking one button document, the related document is opened

Passed: [X]

### 5.6 - Copy info..

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Press copy info button

Expected results:
Pasting the clipboard content in a editor, the relevant information are showed

Passed: [X]

### 5.7 - Check tool tip

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code - gui, drawing button

Expected results:
- a tooltip appears showing file name and full path

Passed: [X]

### 5.8 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Open dir"

Expected results:
- the directory containing the file is opened

Passed: [X]

### 5.9 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy filename"
- paste it in an editor

Expected results:
- the filename is pasted

Passed: [X]

### 5.10 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy dirname"
- paste it in an editor

Expected results:
- the dirname is pasted

Passed: [X]

### 5.11 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy full path"
- paste it in an editor

Expected results:
- the full path (filename+dirname) is pasted

Passed: [X]

### 5.12 - RMB menu of drawing button (windows only)

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy file"
- paste it in a folder

Expected results:
- the file is copied

Passed: [X]

## 6 - 'Assembly' window

### 6.1 - select date

Test description:
- insert code "820037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Check that it is a modal-less dialog trying to click in the "parent"  window menu

Expected results:
The click can raise action (eg. open a menu)

Passed: [X]

Test description #2:
- after the step above, press the cancel button

Expected results #2:
- the dialog disappear and the "codes list" window is showed

Passed: [X]

Test description #3:
- repeat the steps above until the "show assembly by date" dialog appears
- Select the first item
- press the "Select" button.

Expected results #3:
- The "BOMBrowser - Assembly" window appears
- Check that the date in the window title is the same that you selected

Passed: [X]

### 6.4 - show assembly

Test description:
- insert code "810037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.

Expected results:
- The "BOMBrowser - Assembly" window appears
- only one code (810037) is showed

Passed: [X]

### 6.5 - show assembly (2)

Test description:
- insert code "820037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item
- press the "Select" button".
- The Assembly window appears; Select an item with an assembly (e.g electronic board)
- then RMB click and then execute "Show Assembly by date".

Expected results:
A new "Select date" window is showed.

Passed: [X]

### 6.6 - where used (2)

Test description:
- insert code "100000" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item, and press the "Select button". The Assembly window appears
- Select a code below the top one(100000); then RMB and then execute "Where used"

Expected results:
a where used window appears

Passed: [X]

### 6.7 - valid where used (2)

Test description:
- insert code "100000" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item, and press the "Select button". The Assembly window
appears
- Select a code below the top one(100000); then RMB and then execute
"Valid where used"

Expected results:
a where used window appears

Passed: [X]

### 6.8 - menu->help->about

Test description:
In the menu select the Help and About subcommand

Expected results:
The "about" dialog is showed. The dialog contains the current version and the copyright code.

Passed: [X]

### 6.9 - menu->window

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command
- select the first date doubleckicking on it.
Two windows are opened. Select the "Windows menu" in the "BOMBrowser - Assembly" window:

Expected results:
in the menu only one  window is showed: "BOM Browser - Codes list".

Passed: [X]

### 6.10 - menu->file->close

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command
- select the first date doubleckicking on it.
- Two windows are opened. Select the "File->Close" in the "BOMBrowser - Assembly" window:

Expected results:
The "BOMBrowser - Assembly" list is closed. "BOMBrowser - Codes list" is opened.

Passed: [X]

### 6.11 - Test 3.14 -Ctrl-Q  menu->file->close

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command
- select the first date doubleckicking on it.
- two windows are opened. Set the focus to the "BOMBrowser - Assembly", then press CTRL-Q

Expected results:
The "BOMBrowser - Assembly" is closed. "BOMBrowser - Codes list" is opened.

Passed: [X]

### 6.12 - menu->file->exit

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show latest assembly" command
- Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Assembly" window:

Expected results:
a dialog BOMBrowser asking about the possibility to exit is showed.

Passed: [X]

Test description #2:
- After the steops above,  Press No

Expected results #2:
the assembly windows is NOT closed

Passed: [X]

Test description #3:
- After the steops above,  Select the "File->Exit" in the "BOMBrowser - Assembly" window:
- a dialog BOMBrowser asking about the possibility to exit is showed. Press yes

Expected results #3:
The application is ended. No window is showed

Passed: [X]

### 6.15 - menu->file->exit

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Two windows are opened. Press CTRL-X

Expected results:
a dialog BOMBrowser asking about the possibility to exit is showed.

Passed: [X]

Test description #2:
- After the steops above,  Press No

Expected results #2:
the assembly windows is NOT closed

Passed: [X]

Test description #3:
- Press CTRL-X again
- a dialog BOMBrowser asking about the possibility to exit is showed. Press yes

Expected results #3:
The application is ended. No window is showed

Passed: [X]

### 6.18 - menu->file->export as json

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Select File->export as json
- Save the file and reopen it in a editor

Expected results:
The file is in a JSON format

Passed: [X]

Test description #2:
Test description #2
- Select File->export bom
- Save the file (with a .csv extension) and reopen it in a editor

Expected results #2:
- The file is in a CVS (SECOLON separated fields) format

Passed: [X]

### 6.20 - menu->view->show up level 1

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Select View->show up level 1

Expected results:
The bom is collapsed to showing only the first level (top code and its children)

Passed: [X]

Test description #2:
- Select View->show up level 2

Expected results #2:
The bom is collapsed to showing only the two levels (top code and its children, and their children)

Passed: [X]

Test description #3:
- Select View->show all level

Expected results #3:
The bom is showing all levels

Passed: [X]

Test description #4:
- Press CTRL-1

Expected results #4:
The bom is collapsed to showing only the first level (top code and its children)

Passed: [X]

Test description #5:
- Press CTRL-2

Expected results #5:
The bom is collapsed to showing only the two levels (top code and its children, and their children)

Passed: [X]

Test description #6:
- Press CTRL-A

Expected results #6:
The bom is showing all levels

Passed: [X]

### 6.26 - find

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

#### 6.26.1 - find ctrl-f

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
press CTRL-F

Expected results:
The find dialog is showed

Passed: [X]

#### 6.26.2 - find

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
Select Search->Find

Expected results:
The find dialog is showed

Passed: [X]

#### 6.26.3 - cancel

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
- Select Search->Find
- The find dialog is showed
- Press "Close" button

Expected results:
The find dialog is closed

Passed: [X]

#### 6.26.4 - find a code

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '8104'
- Press "next" 3 times

Expected results:
A different instance of the codes starting with 8104 is showed each time

Passed: [X]

Test description #2:
- Press "prev" 2 times

Expected results #2:
A different instance of the codes starting with 8104 is showed each time

Passed: [X]

#### 6.26.6 - find a code

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '8104'
- Press "next" 3 times
- Press "prev" 3 times

Expected results:
After the last action a dialog "Data not found" is showed

Passed: [X]

#### 6.26.7 - find a code

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '8104'
- Press "next" going below the bom until a dialog "Data not found" is showed

Expected results:
After the last action a dialog "Data not found" is showed

Passed: [X]

### 6.27 - show latest assembly

Test description:
- in "Code list" window, select the code 820017
- select the code
- look at right panel codegui. Check that the "Date to" is blank
- if not, edit the code and change the "Date to" date accordling
- from the RBM menu select "Show latest assembly"

Expected results:
- The window "Assembly" is showed
- The date on the title is replaced by "LATEST"
- Each code listed, has the "date to" date empty

Passed: [X]

### 6.28 - show latest assembly

Test description:
- in "Code list" window, select the code 100017
- select the code
- look at right panel codegui. Check that the "Date to" of the **last revision** is **not** blank
- if not, edit the code and change the "Date to" date accordling
- from the RBM menu select "Show latest assembly"

Expected results:
- The window "Assembly" is showed
- The date on the title is replaced by the "Date to" value

Passed: [X]

### 6.29 - Menu file -> export data

Test description:
- open as "latest assembly" in Assembly window the code 820000
- Select File, then "Export data"

Expected results:
- A "Save to" dialog appear

Passed: [X]

Test description #2:
- after the step above, press Close

Expected results #2:
- Nothing

Passed: [X]

Test description #3:
- repeat the step above, but instead pressing Close, select a directory and press export

Expected results #3:
- In the selected folder, the assemblies files are copied

Passed: [X]

### 6.32 - Show prototype assembly

#### 6.32.1 - Show prototype assembly

Preparatory steps:
- look at the code 610004 in the codes list window
- Check in the code gui right panel, that the code has two date and that it is not a prototype

Test description:
- look at the code 610004 in the codes list window
- From the RMB menu, select "Show prototype assembly"

Expected results:
- the assembly window is showed
- looking at the dates of the "code gui" right panel, for some code the "prototype" date from is showed

Passed: [X]

#### 6.32.2 - Show prototype assembly

Preparatory steps:
- look at the code 610004 in the codes list window
- Check in the code gui right panel, that the code has two date and that it is not a prototype

Test description:
- look at the code 610004 in the codes list window
- From the RMB menu, select "Show latest assembly"

Expected results:
- the assembly window is showed
- looking at the dates of the "code gui" right panel, for any code the date from is showed: and is not prototype

Passed: [X]

### 6.33 - Check for loop

Test description:
- look at the code TEST-LOOP-A in the codes list window
- From the RMB menu, select "Show latest assembly"


Expected results:
A message box appears saying 'ERROR loop detected' is showed; the message box suggest to execute File->Tool->Check bom.

Passed: [X]

Test description #2:
- Select menu->Tools->Check bom

Expected results #2:
A report saying 'ERROR loop detected' is showed

Passed: [X]

### 6.35 - Check for loop (2x)

Test description:
- look at the code TEST-LOOP-A in the codes list window
- From the RMB menu, select "Where used"


Expected results:
A message box appears saying 'ERROR loop detected' is showed.

Passed: [X]

## 7 - 'Valid where used' window

### 7.1 - Test 4.1

Test description:
in the "Codes list" window search for the code 820017. Then select  the right click menu command "Valid where used"

Expected results:
- the "valid where used" window is showed
- each code showed (except the top node) has a "end to" date empty
- no code are repeated

Passed: [X]

## 8 - 'Where used' window

### 8.1 - Test 5.1

Test description:
in the "Codes list" window search for the code 820011. Then select  the right click menu command "Where used"

Expected results:
- the where used window is showed
- few codes showed (the top node doesn't matter) have a "end to" date not empty. These code sometime are repeated

Passed: [X]

## 9 - 'Select date' window

This test is covered by the ones of the Assembly window

## 10 - 'Diff window' window

### 10.1 - diff the same code

Test description:
- in the "Codes list" window search for the codes 82%.
- then select a code with multiple revision (e.g. 820009)
- then right click menu command "Diff from"

Expected results:
- a select date dialog is showed

Passed: [X]

Test description #2:
- after the previous step, select the **2nd** date
- then press select

Expected results #2:
- A small diff dialog is showed

Passed: [X]

Test description #3:
- after the previous step, select the same code in the codes list window
- then right click menu command "Diff to"

Expected results #3:
- a select date dialog is showed

Passed: [X]

Test description #4:
- after the previous step, select the **1st** date
- then press select

Expected results #4:
- The previous small dialog is closed
- A new window called "Diff window" is showed
- In the title bar there are showed the codes and the two selected date
- In the top part of the window there are showed the code and the two selected date
- in the body of the windows it is showed the colorized diff of the two boms

Passed: [X]

Test description #5:
- search in the body window the selected code

Expected results #5:
- below the code are showed the differences between the code:
- the dates are different
- the iterations are different
- other differences are possible

Passed: [X]

### 10.6 - diff two different codes

Test description:
- in the "Codes list" window search for the codes 82%.
- then select a code with multiple revision (e.g. 820009)
- then right click menu command "Diff from"

Expected results:
- a select date dialog is showed

Passed: [X]

Test description #2:
- after the previous step, select the **2nd** date
- then press select

Expected results #2:
- A small diff dialog is showed

Passed: [X]

Test description #3:
- after the previous step, select a different code (e.g. 820011) in the codes list window
- then right click menu command "Diff to"

Expected results #3:
- a select date dialog is showed

Passed: [X]

Test description #4:
- after the previous step, select the **1st** date
- then press select

Expected results #4:
- The previous small dialog is closed
- A new window called "Diff window" is showed
- In the title bar there are showed the codes and the two selected date
- In the top part of the window there are showed the code and the two selected date
- in the body of the windows there is showed the colorized diff of the two boms

Passed: [X]

Test description #5:
- search in the body window the 1st selected code

Expected results #5:
- below the code are showed the differences between the code:
- the codes are different
- other differences are possible

Passed: [X]

### 10.11 - diff two different codes

Test description:
- open a diff window as described in the previous test
- search in the body window the 1st selected code
- annotate which properties are marked with '-' and which one with '+'
- press the button '<->'
- search in the body the 2nd selected code

Expected results:
- the previous values marked with '-' are marked with '+'
- the previous values marked with '+' are marked with '-'

Passed: [X]

### 10.12 - diff option: diff only top code

Test description:
- open a diff window against two different date of the code 820017
- check the checkbox "Diff only the top code

Expected results:
- only the top code is showed
- the differents 'date_from' are showed (other fields may be showed)

Passed: [X]

### 10.13 - diff option: diff only top code

Test description:
- open a diff window against two codes:  - 820017
  - 820018
- check the checkbox "Diff only the top code

Expected results:
- only the top code is showed
- the differents 'code' and 'descr' are showed (other fields may be showed)
- the dufferences between the bomn are showed

Passed: [X]

### 10.14 - diff option: diff only main attributes

Test description:
- open a diff window against two different date of the code820017
- check the checkbox "Diff only main attributes

Expected results:
only the main attributes are showed:
- description
- qty
- code


Passed: [X]

## 11 - 'Copy/revise code' window

### 11.1 - change from revision to copy mode

Test description:
- revise the code "820041" from the code list window
- mark the copy checkbox

Expected results:
- the window title changed in "... - copy code"
- the left button title changed in  "Copy code"

Passed: [X]

Test description #2:
- unmark the copy checkbox

Expected results #2:
- the window title changed in "... - revise code"
- the left button title changed in  "Revise code"

Passed: [X]

### 11.3 - date dialog

Test description:
Test description
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command

Expected results:
A "BOM Browser select date dialog" appears

Passed: [X]

Test description #2:
- after the step above, press cancel

Expected results #2:
- the dialog disappears

Passed: [X]

Test description #3:
- repeat the steps above until the appearing of the dialog
- press select

Expected results #3:
The Copy/revise windows appears

Passed: [X]

### 11.6 - date dialog

INtegrated in 8.4

### 11.7 - Copy/revise code window

Test description:
Test description
- insert code 820039 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry

Expected results:
- The Copy/revise windows appears
- the "old-Iter" are the same as the one selected in the "Select date" window

Passed: [X]

### 11.8 - Copy/revise code window

Test description:
Test description
- insert code 820039 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *second* entry
- The Copy/revise windows appears

Expected results:
the "Iter" are the same as the one selected in the "Select date" window

Passed: [X]

### 11.9 - Copy/revise code window

#### 11.9.1 - Cancel

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
press Close button

Expected results:
an exit confirmation dialog will appears

Passed: [X]

Test description #2:
- after the steps above, press **YES**

Expected results #2:
the "Copy/revise windows" is closed

Passed: [X]

Test description #3:
- repeat the steps above until the dialog appearance
- an exit confirmation dialog will appears; press **NO**

Expected results #3:
the dialog is closed; the "Copy/revise windows" is opened

Passed: [X]

#### 11.9.4 - *Revise*/copy code window

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
Check the editability of the following fields: New/Code, New/Iter, New/Description, New/Rev, New/Date from

Expected results:
only New/Description, New/date from and New/rev are editable

Passed: [X]

#### 11.9.5 - Copy/revise code window

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
check the field New/Iter

Expected results:
The field New/Iter is Old/Iter + 1

Passed: [X]

#### 11.9.6 - Copy/revise code window

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- mark the copy checkbox
- check the editability of the following fields: New/Code, New/Iter, New/Description, New/Rev, New/Date from

Expected results:
the field New/Code, New/Description, New/Date from and New/Rev are editable

Passed: [X]

#### 11.9.7 - Copy/revise code window

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- mark the copy checkbox
- check the field New/Iter

Expected results:
The field New/Iter is 0

Passed: [X]

#### 11.9.8 - Copy error

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- mark the copy checkbox
- check that the Old/code is equal to the new/code
- press "Copy code" button

Expected results:
- An error dialog appears saying that the code already exists
- pressing OK, the Copy / Revise window still exists

Passed: [X]

#### 11.9.9 - Confirmation dialog / success

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- **mark** on the copy checkbox
- change the new/code in 82004A"
- **unmark** the checkbox "start edit dialog after copy/revision"
- press "Copy code" button
- A confirmation dialog appears; press no

Expected results:
the  confirmation dialog disappear; the "BOMBrowser - copy /revise code" windows is opened.

Passed: [X]

Test description #2:
- after the steps above, pres again "Copy/Revise button"
- a confirmation dialog appears; press yes

Expected results #2:
a confirmation dialog appears

Passed: [X]

#### 11.9.11 - Confirmation dialog / success (2)

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- mark the copy checkbox
- mark the checkbox "start edit dialog after copy/revision"
- change the new/code in 82004B"
- press "Copy code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the new code appears.
- There are attached document and a children list

Passed: [X]

#### 11.9.12 - Confirmation dialog / success (3)

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- check the copy checkbox
- change the new/code in 82004C"
- unmark the "Copy document" checkbox
- press "Copy code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the new code appears.
- There are not attached document.
- There are children list.

Passed: [X]

#### 11.9.13 - Revise a code / date error

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- enter an incorrect date (eg. 'xxxx')
- press "Revise code" button

Expected results:
- An error dialog appears saying that the date format is incorrect
- pressing OK, the Copy / Revise window still exists

Passed: [X]

#### 11.9.14 - Revise a code / date error

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- enter an date equal to the Old/Date from
- press "Revise code" button


Expected results:
- An error dialog appears saying that the date is earlier than the old one
- pressing OK, the Copy / Revise window still exists

Passed: [X]

### 11.10 - revise a code

Test description:
- revise the code "820041" from the code list window
- adjust the "new/from date" field to "old/from date" + 1 (or more, in any case a value different from the default one)
- set the new/rev field to the default one + "bis_" as prefix
- set the "new/description" field to the default one + "bis_" as prefix
- press "Revise code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- There are attached document.
- There are children list.
- The "From date" in the revision list combobox is equal to the one of the previous dialog
- The "Description" in the editor window is equal to the one of the previous dialog (with 'bis_' as prefix)
- The "Rev" in the editor window is equal to the one of the previous dialog (with 'bis_' as prefix)

Passed: [X]

### 11.11 - copy a code

Test description:
- revise the code "820041" from the code list window
- check the "Copy" checkbox
- set the "new/code" field to a new one (i.e. it must no exist)
- adjust the "new/from date" field to "old/from date" + 1 (or more, in any case a value different from the default one)
- set the new/rev field to the default one + "bis_" as prefix
- set the "new/description" field to the default one + "bis_" as prefix
- press "Copy code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- There are attached document.
- There are children list.
- The "From date" in the revision list combobox is equal to the one of the previous dialog
- There is only **one** date in the combobox list
- The "Description" in the editor window is equal to the one of the previous dialog
- The "Rev" in the editor window is equal to the one of the previous dialog

Passed: [X]

### 11.12 - copy a code (in proto mode)

Test description:
- revise the code "820041" from the code list window
- check the "Copy" checkbox
- set the "new/code" field to a new one (i.e. it must no exist)
- check the checkbox "Prototype"
- press "Copy code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- The date in date selector reports only prototype
- There is only **one** date in the combobox list
- The date in the titlebar  reports prototype

Passed: [X]

### 11.13 - revise a code (in proto mode)

Test description:
- revise the code "820041" from the code list window
- check the checkbox "Prototype"
- press "Revise code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- The date in date selector reports also prototype

Passed: [X]

### 11.14 - revise a code (in proto mode)

Test description:
- revise the code "820004" from the code list window (the code has already a prototype revision, if not create a prototype revision)
- check the checkbox "Prototype"
- press "Revise code" button


Expected results:
- a dialog error reports that a prototype already exists

Passed: [X]

## 12 - 'Edit code' window

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

### 12.1 - Edit code / Rev field

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- change the "rev" field prefixing it with "bis_"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the "rev" field is like the one changed

Passed: [X]

### 12.2 - Edit code / Default unit field

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- change the "Default unit" field prefixing it with "bis_"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the "Default unit" field is like the one changed

Passed: [X]

### 12.3 - Edit code / Description field

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- change the "Description" field prefixing it with "bis_"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the "Description" field is like the one changed

Passed: [X]

### 12.4 - Edit code / Generic properties field

Preparatory steps:


Test description:
- repeat the test above for all the "Generic properties" fields

Expected results:
the "generic property" field is like the one changed

Passed: [X]

### 12.5 - Add/Del/View a drawing

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the drawing list panel
- execute the command "add drawing"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the added drawing is still present

Passed: [X]

Test description #2:
- click with the RMB on the drawing list panel
- drag and drop a file in the drawing panel
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results #2:
the added drawing is still present

Passed: [X]

Test description #3:
- click with the RMB on the drawing list panel
- execute the command "add drawing", selecting MULTIPLE files
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results #3:
the added drawings are present

Passed: [X]

Test description #4:
- click with the RMB on the drawing list panel
- execute the command "delete drawing" on a drawing
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results #4:
the removed drawing is not present

Passed: [X]

Test description #5:
- click with the RMB on the drawing list panel
- execute the command "delete drawing" on mutiple drawings
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results #5:
the removed drawings are not present

Passed: [X]

Test description #6:
- click with the RMB on the drawing list panel
- execute the command "view drawing" on a drawing

Expected results #6:
the selected drawing is showed

Passed: [X]

Test description #7:
- doubleclick on a drawing in the drawing list panel

Expected results #7:
the selected drawing is showed

Passed: [X]

Test description #8:
- select multiple drawings
- click with the RMB on the drawing list panel
- execute the command "view drawing" on a drawing

Expected results #8:
the selected drawings are showed

Passed: [X]

### 12.13 - Copy multiple drawings

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- insert code 820002 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- A second Edit code windows appears

Test description:
- In the first edit window select multiple drawings
- click with the RMB on the drawings list
- execute the command "copy drawings lines"
- In the second edit window click with the RMB on the drawings list
- execute the command "paste drawings lines"
- press "save..." button
- press "close"
- reopen the edit window on the 2n code as described in the "preparatory steps"

Expected results:
the copied drawings are present

Passed: [X]

Test description #2:
drag and drop some file in the "Edit window"


Expected results #2:
- the new files are added in the drawings window
- the files counter in the tab title is increased

Passed: [X]

### 12.15 - del multiple children

Test description:
- click with the RMB on the children list panel
- execute the command "delete row" on multiple lines
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the removed items are not present

Passed: [X]

Test description #2:
- click with the RMB on the children list panel
- execute the command "delete row" on a line
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results #2:
the removed item is not present

Passed: [X]

### 12.17 - Copy multiple children

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- insert code 820002 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- A second Edit code windows appears

Test description:
- In the first edit window select multiple children
- click with the RMB on the children list
- execute the command "copy lines"
- In the second edit window click with the RMB on the children list
- execute the command "paste lines"
- press "save..." button
- press "close"
- reopen the edit window on the 2n code as described in the "preparatory steps"

Expected results:
the copied children are present

Passed: [X]

### 12.18 - add a child

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the children list panel
- execute the command "insert row after" on a line
- in the new line insert an (existant) code in the "code" column
- the field "code-id" and "description" will autocomplete
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the added item is present in the same position as showed before

Passed: [X]

### 12.19 - add a child

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the children list panel
- execute the command "insert row before" on a line
- in the new line insert an (existant) code in the "code" column
- the field "code-id" and "description" will autocomplete
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the added item is present in the same position as showed before

Passed: [X]

### 12.20 - add multiple child

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the children list panel
- select multiple lines
- execute the command "insert row before" on a line


Expected results:
Multiple lines are inserted. The number of lines are equal
to the selected ones.

Passed: [X]

### 12.21 - non existant code

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel, try to change a code in a row with a non existant code (like 'z')

Expected results:
the cell changed is yellow

Passed: [X]

Test description #2:
- press "save"

Expected results #2:
an error dialog appears saying that there is an error in "...the code '...' in row..."

Passed: [X]

### 12.23 - duplicate code

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel, try to change a code in a row with a already existant code (like the previous one or the next one)
- press "save" button

Expected results:
an error dialog is showed, saying that there is a duplicate code

Passed: [X]

### 12.24 - wrong qty

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel, try to change the 'qty' field in a row with a non number value

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
- press "save"

Expected results #2:
an error dialog appears saying that the value is incorrect

Passed: [X]

### 12.26 - wrong each

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel, try to change the 'each' field in a row with a non number value

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
- press "save"

Expected results #2:
an error dialog appears saying that the value is incorrect

Passed: [X]

### 12.28 - sorting

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel, change the row sequence sort by code (click on the "code" column header)
- take note of the "seq" column values
- remove a row

Expected results:
the seq values are reordered on the basis of the current sequence.

Passed: [X]

### 12.29 - sorting

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel, change the row sequence sort by code (click on the "code" column header)
- take note of the "seq" column values
- do an "insert row before"

Expected results:
the seq values are reordered on the basis of the current sequence.

Passed: [X]

### 12.30 - sorting

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel, change the row sequence sort by code (click on the "code" column header)
- take note of the "seq" column values
- do an "insert row after"

Expected results:
the seq values are reordered on the basis of the current sequence.

Passed: [X]

### 12.31 - Move the children UP

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel select one line in the middle
- press UP button

Expected results:
the selected line is moved up of one line

Passed: [X]

Test description #2:
- in the children panel select the first line
- press UP button

Expected results #2:
nothing is changed

Passed: [X]

Test description #3:
- in the children panel select the first lineS
- press UP button

Expected results #3:
nothing is changed

Passed: [X]

Test description #4:
- in the children panel select some lines in the middle
- press UP button

Expected results #4:
the lines are moved up of one line

Passed: [X]

### 12.35 - Move the children DOWN

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel select one line in the middle
- press DOWN button

Expected results:
the selected line is moved down of one line

Passed: [X]

Test description #2:
- in the children panel select the last line
- press DOWN button

Expected results #2:
nothing is changed

Passed: [X]

Test description #3:
- in the children panel select the last lines
- press DOWN button

Expected results #3:
nothing is changed

Passed: [X]

Test description #4:
- in the children panel select some lines in the middle
- press DOWN button

Expected results #4:
the lines are moved down of one line

Passed: [X]

### 12.39 - Move the children to the TOP

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel select one line in the middle
- press TOP button

Expected results:
the selected line is moved to the TOP

Passed: [X]

Test description #2:
- in the children panel select the first line
- press TOP button

Expected results #2:
nothing is changed

Passed: [X]

Test description #3:
- in the children panel select the first lines
- press TOP button

Expected results #3:
nothing is changed

Passed: [X]

Test description #4:
- in the children panel select some lines in the middle
- press TOP button

Expected results #4:
the lines are moved to the TOP

Passed: [X]

### 12.43 - Move the children BOTTOM

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- in the children panel select one line in the middle
- press BOTTOM button

Expected results:
the selected line is to the bottom

Passed: [X]

Test description #2:
- in the children panel select the last line
- press BOTTOM button

Expected results #2:
nothing is changed

Passed: [X]

Test description #3:
- in the children panel select the last lines
- press BOTTOM button

Expected results #3:
nothing is changed

Passed: [X]

Test description #4:
- in the children panel select some lines in the middle
- press BOTTOM button

Expected results #4:
the lines are moved to the bottom

Passed: [X]

### 12.47 - Edit code / File -> close

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- select the menu File->close

Expected results:
the edit window is closed

Passed: [X]

### 12.48 - Edit code / File -> exit

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- select the menu File->exit

Expected results:
a dialog is opened asking if you want to exit from application

Passed: [X]

Test description #2:
- press no

Expected results #2:
the dialog is closed, the edit windows is showed

Passed: [X]

Test description #3:
- repeat the steps above and instead of pressing no press yes

Expected results #3:
the application is closed, no window is opened

Passed: [X]

### 12.51 - Edit code / CTRL-Q

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- Press CTRL-Q

Expected results:
the edit window is closed

Passed: [X]

### 12.52 - Edit code / Windows

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- select the menu Windows menu

Expected results:
the opened windows are showed (except the edit one).

Passed: [X]

### 12.53 - Edit code / Help->about

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- select the menu Help->about menu

Expected results:
the about dialog is showed

Passed: [X]

### 12.54 - search code

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the children list panel
- execute the command "search code" on a line

Expected results:
The "BOMBrowser - Search code" dialog appears

Passed: [X]

### 12.55 - search code

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the children list panel
- execute the command "search code" on a line
- The "BOMBrowser - Search code" dialog appears
- search for a code in the dialog (e.g 810001)
- select the first result
- press OK

Expected results:
the dialog is closed and the new code replaces the old one

Passed: [X]

### 12.56 - search code

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the children list panel
- execute the command "search code" on a line
- The "BOMBrowser - Search code" dialog appears
- search for a code in the dialog (e.g 810007)
- press Cancel

Expected results:
- the dialog is closed
- the new code **didn't** replace the original one

Passed: [X]

### 12.57 - delete revision

Preparatory steps:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- take this copy, and revise it 5 times (changing the from date to avoid conflicts)
- Edit this code


Test description:
- From menu -> edit, select delete revision

Expected results:
a confirmation dialog is showed

Passed: [X]

Test description #2:
- press no

Expected results #2:
nothing happened

Passed: [X]

Test description #3:
- select the first revision (no "date to")
- From menu -> edit, select delete revision
- a confirmation dialog is showed, press yes

Expected results #3:
- a comfirmation dialog is showed, saying that the revision is deleted. Press ok.
- the previous selected revision is removed
- the "date to" of the new latest revision is empty

Passed: [X]

Test description #4:
- select the 3rd revision
- take note of its "date to" value
- From menu -> edit, select delete revision
- a confirmation dialog is showed, press yes

Expected results #4:
- a comfirmation dialog is showed, saying that the revision is deleted. Press ok.
- the previous selected revision is removed- the "date to" of the previous revision is equal to the "date to" of the removed revision.

Passed: [X]

Test description #5:
- select the 1st revision (the oldest one)
- take note of its "date from" value
- From menu -> edit, select delete revision
- a confirmation dialog is showed, press yes

Expected results #5:
- a comfirmation dialog is showed, saying that the revision is deleted. Press ok.
- the previous selected revision is removed- the "date from" of the 1st revision is equal to the "date from" of the removed revision.

Passed: [X]

Test description #6:
- From menu -> edit, select delete revision
- repeat the step above until only one revision is present
- From menu -> edit, select delete revision (again)

Expected results #6:
an error dialog box is showed saying that it is not possible to delete the last revision

Passed: [X]

### 12.63 - Delete code

Preparatory steps:
- select a code from teh 'Codes list' gui and copy it
- select the new code and edit it in the 'Edit' window


Test description:
- From the menu->edit select "delete code"

Expected results:
a confirmation dialog appears

Passed: [X]

Test description #2:
press no

Expected results #2:
nothing happened

Passed: [X]

Test description #3:
- From the menu->edit select "delete code"
- a confirmation dialog appears, press yes

Expected results #3:
- a confirmation dialog appears, press yes
- a confirmation dialog appears, press ok
- the edit dialog is not showed anymore

Passed: [X]

Test description #4:
- search for the deleted code

Expected results #4:
- the code is not showed anymore

Passed: [X]

### 12.67 - change revision

Preparatory steps:
- Take a code from the code list gui with multiple revision
- Edit this code


Test description:
- Acting to the "From/to date" QComboBox, change the revision of the code to the newest
- make one change in a field for each revision (insert the from date to help the test) and press Save
- repeat the step above for each revision
- Acting to the "From/to date" QComboBox, change the revision of the code

Expected results:
- The dialog show for each revision the change performed in the step above

Passed: [X]

### 12.68 - change revision without saving

Preparatory steps:
- Take a code from the code list gui with multiple revision
- Edit this code


Test description:
- make one change in a field - Acting to the "From/to date" QComboBox, change the date of the code

Expected results:
- An dialog is showed saying that the change are not saved. It ask if the user want to continue.

Passed: [X]

Test description #2:
- press no

Expected results #2:
- the revision is not changed

Passed: [X]

Test description #3:
- Acting to the "From/to date" QComboBox, change the revision of the code
- An error dialog is showed saying that the change are not saved, press yes

Expected results #3:
- go back to the previous revision
- check that the change was not saved

Passed: [X]

### 12.71 - change revision without saving

Preparatory steps:
- Take a code from the code list gui with multiple revision
- Edit this code


Test description:
- make one change in a field
- press Close

Expected results:
- An error dialog is showed saying that the change are not saved

Passed: [X]

Test description #2:
- Press no

Expected results #2:
- The previous window is showed. the change is not lost

Passed: [X]

Test description #3:
- repeat the test until the dialog is showed
- Press yes

Expected results #3:
- The edit window is closed
- reopening the edit window, check that the change was not saved

Passed: [X]

### 12.74 - remove a child without saving

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- remove an item in the children section
- press close button

Expected results:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### 12.75 - insert a child without saving

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- insert (before) item in the children section
- press close button

Expected results:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### 12.76 - insert a child  without saving

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- insert (after) item in the children section
- press close button

Expected results:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### 12.77 - change child without saving

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- do a "search code" over an item in the children section
- press "ok button

Expected results:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### 12.78 - add drawing without saving

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- do an "add drawing" in the drawings section
- press close button

Expected results:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### 12.79 - remove a drawing without saving

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- do an "delete drawing" in the drawings section
- press close button

Expected results:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### 12.80 - add a duplicated code

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- add a two new equal children code
- press save

Expected results:
- An error dialog is showed  saying that there is a code duplication

Passed: [X]

### 12.81 - add a code to an empty children list

Preparatory steps:
- Take a code from the code list gui without children (eg an 8100xx code)
- Edit this code


Test description:
- add a new child code, using the RBM menu

Expected results:
- clicking the right mouse button shows a menu that allows to insert a code

Passed: [X]

### 12.82 - exit without saving

Preparatory steps:
- Take a code from the code list gui without children (eg an 8100xx code)
- Edit this code


Test description:
- close the window (click on the upper right "X" icon)

Expected results:
- the edit window closes itself

Passed: [X]

### 12.83 - exit without saving

Preparatory steps:
- Take a code from the code list gui without children (eg an 8100xx code)
- Edit this code


Test description:
- change a field in the edit window
- close the window (click on the upper right "X" icon)

Expected results:
- a confirmation dialog appears

Passed: [X]

Test description #2:
- Press no

Expected results #2:
- the edit window is still opened

Passed: [X]

Test description #3:
- Repeat the steps of test #2
- Press yes

Expected results #3:
- the edit window closes itself

Passed: [X]

### 12.86 - Code Properties (file)

Preparatory steps:
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


Test description:
- Open the edit window on the code 810001
- Locate the field "TestFile"
- Press the "..." button

Expected results:
- The Open file dialog opens

Passed: [X]

Test description #2:
- press cancel

Expected results #2:
- The Open file dialog closes
- The fields remains empty

Passed: [X]

Test description #3:
- press "..." button again
- Select a file then press Open


Expected results #3:
- The Open file dialog closes
- The fields contains the file path

Passed: [X]

Test description #4:
- press the Save button
- press the close button
- re-open the edit window on the same code


Expected results #4:
- The fields still contains the value selected

Passed: [X]

Test description #5:
- change the value of the field typing directly in the line edit widget
- press the Save button
- press the close button
- re-open the edit window on the same code


Expected results #5:
- The fields still contains the value selected

Passed: [X]

Test description #6:
- change the value of the field 
- press the close button


Expected results #6:
- A dialog point out that the data is changed but not saved

Passed: [X]

### 12.92 - Code Properties (list)

Preparatory steps:
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


Test description:
- Open the edit window on the code 810001
- Locate the field "Test2"
- Press the "..." button

Expected results:
- The list box dialog opens

Passed: [X]

Test description #2:
- click in the text field (NOT in the list box)
- Press the "..." button
- click in the text field (NOT in the list box)

Expected results #2:
- The dialog closes
- The fields remains empty

Passed: [X]

Test description #3:
- press "..." button again
- Select a value


Expected results #3:
- The fields contains the value selected

Passed: [X]

Test description #4:
- press the Save button
- press the close button
- re-open the edit window on the same code


Expected results #4:
- The fields still contains the value selected

Passed: [X]

Test description #5:
- change the value of the field typing directly in the line edit widget
- press the Save button
- press the close button
- re-open the edit window on the same code


Expected results #5:
- The fields still contains the value selected

Passed: [X]

Test description #6:
- change the value of the field 
- press the close button


Expected results #6:
- A dialog point out that the data is changed but not saved

Passed: [X]

### 12.98 - Code Properties (clist)

Preparatory steps:
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


Test description:
- Open the edit window on the code 810001
- Locate the field "Transparent"
- Press the "..." button

Expected results:
- The list box dialog opens

Passed: [X]

Test description #2:
- press in another field (NOT in the list box)

Expected results #2:
- The Open file dialog closes
- The fields remains empty

Passed: [X]

Test description #3:
- press button again
- Select a value


Expected results #3:
- The fields contains the value selected

Passed: [X]

Test description #4:
- press the Save button
- press the close button
- re-open the edit window on the same code


Expected results #4:
- The fields still contains the value selected

Passed: [X]

Test description #5:
- change the value of the field 
- press the close button


Expected results #5:
- A dialog point out that the data is changed but not saved

Passed: [X]

### 12.103 - Order of children

Preparatory steps:
- Open the assembly window 820002
- Open the edit window of the same code above

Test description:
check that the order of the children is the same in both the windows

Expected results:
the order of the children is the same in both the windows

Passed: [X]

Test description #2:
In the edit window:
- move the first code in the 3rd position
- move the fourth code in the 1st position
- press save
- refresh the assembly window (press F5)

Expected results #2:
the order of the children is the same in both the windows

Passed: [X]

## 13 - 'Edit date' window

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

### 13.1 - Cancel button

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
press the cancel button

Expected results:
the edit dates dialog is closed

Passed: [X]

### 13.2 - Save button

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
press the save button

Expected results:
a information dialog is showed

Passed: [X]

Test description #2:
- press ok

Expected results #2:
the edit dates dialog is closed

Passed: [X]

### 13.4 - Modify date

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the bottom row with a valid one (but lower than the row above)
- press save
- reopen the edit dates dialog

Expected results:
the new date is showed in the last row

Passed: [X]

### 13.5 - Modify date

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a valid one (but higher than the row below)

Expected results:
the date in the row below and column "To date" is changed accordling (a day before)

Passed: [X]

### 13.6 - Modify date with an invalid one

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a not valid one (i.e. 'z')

Expected results:
the key is not accepted

Passed: [X]

### 13.7 - Modify date with an invalid one

Preparatory steps:


Test description:
- change the "date from" of the first row with a not valid one (i.e. 2001-02-30)

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
- press save

Expected results #2:
an dialog error is showed

Passed: [X]

### 13.9 - Modify date with an invalid one

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a a date equal the row below
- press save

Expected results:
- an error dialog is showed
- press ok, the edit date window is showed

Passed: [X]

Test description #2:
- after the step above, press cancel
- press the '...' button
- check the dates

Expected results #2:
- the dates are unchanged

Passed: [X]

### 13.11 - Modify date with an invalid one

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a a date before (-1) the row below
- press save

Expected results:
- an error dialog is showed
- press ok, the edit date window is showed

Passed: [X]

Test description #2:
Test description #3
- after the step above, press cancel
- press the '...' button
- check the dates

Expected results #2:
- the date are unchanged

Passed: [X]

### 13.13 - Modify date with an invalid one

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the 2nd row with a a date after (+1) the row above
- press save

Expected results:
- an error dialog is showed
- press ok, the edit date window is showed

Passed: [X]

Test description #2:
Test description #3
- after the step above, press cancel
- press the '...' button
- check the dates

Expected results #2:
- the date are unchanged

Passed: [X]

### 13.15 - Check the read-only/read-write ness of the cells

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
check that all fields are read only with the exception of
- the column From date
- the Cell of the first row and column "To date"

Expected results:
only the cells listed above are read write

Passed: [X]

### 13.16 - Insert an invalid date

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the value of the cell of the first row and column "To date" with an invalid one (i.e. 'z')

Expected results:
the key is not accepted

Passed: [X]

### 13.17 - Insert an invalid date

Preparatory steps:
- insert code 810025 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the value of the cell of the first row and column "To date" with a date before of the left cell
- press save

Expected results:
a dialog error is showed

Passed: [X]

### 13.18 - Insert a valid date

Preparatory steps:
- insert code 100001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the value of the cell of the first row and column "To date" with a valid one
- press the save button
- reopen the Edit dates" dialog

Expected results:
the new date appears in the "edit code window"

Passed: [X]

### 13.19 - conflict date

#### 13.19.1 - parent too early

Preparatory steps:
- create a component code (copying from an existing component); name it as TEST-A; set a Date from 2020-01-01.
- Create a component code (copying from an existing component); name it as TEST-B; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Create a component code (copying from an existing component); name it as TEST-ASS-A; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Edit the code "TEST-ASS-A" adding as child the coponents TEST-A and TEST-B.

Test description:
- enter in the edit dialog of code TEST-ASS-A
- enter in the edit date dialog
- change the "From date" to 2019-01-01
- press "Save button"

Expected results:
an error dialog appears saying that the date range is wider than the children one

Passed: [X]

#### 13.19.2 - parent too late

Preparatory steps:
- create a component code (copying from an existing component); name it as TEST-A; set a Date from 2020-01-01.
- Create a component code (copying from an existing component); name it as TEST-B; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Create a component code (copying from an existing component); name it as TEST-ASS-A; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Edit the code "TEST-ASS-A" adding as child the coponents TEST-A and TEST-B.

Test description:
- enter in the edit dialog of code TEST-ASS-A
- enter in the edit date dialog
- change the "To date" to 2022-01-01
- press "Save button"

Expected results:
an error dialog appears saying that the date range is wider than the children one

Passed: [X]

#### 13.19.3 - children too late

Preparatory steps:
- create a component code (copying from an existing component); name it as TEST-A; set a Date from 2020-01-01.
- Create a component code (copying from an existing component); name it as TEST-B; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Create a component code (copying from an existing component); name it as TEST-ASS-A; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Edit the code "TEST-ASS-A" adding as child the coponents TEST-A and TEST-B.

Test description:
- enter in the edit dialog of code TEST-B
- enter in the edit date dialog
- change the "From date" to 2020-06-01
- press "Save button"

Expected results:
an error dialog appears saying that the date range is shorter than the parent one

Passed: [X]

#### 13.19.4 - children too early

Preparatory steps:
- create a component code (copying from an existing component); name it as TEST-A; set a Date from 2020-01-01.
- Create a component code (copying from an existing component); name it as TEST-B; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Create a component code (copying from an existing component); name it as TEST-ASS-A; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Edit the code "TEST-ASS-A" adding as child the coponents TEST-A and TEST-B.

Test description:
- enter in the edit dialog of code TEST.ASS-A
- enter in the edit date dialog
- change the "To date" to 2020-06-01
- press "Save button"
- enter in the edit dialog of code TEST-B
- enter in the edit date dialog
- change the "To date" to 2020-03-01
- press "Save button"

Expected results:
an error dialog appears saying that the date range is shorter than the parent one

Passed: [X]

#### 13.19.5 - children too early

Preparatory steps:
- create a component code (copying from an existing component); name it as TEST-A; set a Date from 2020-01-01.
- Create a component code (copying from an existing component); name it as TEST-B; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Create a component code (copying from an existing component); name it as TEST-ASS-A; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Edit the code "TEST-ASS-A" adding as child the coponents TEST-A and TEST-B.

Test description:
- enter in the edit dialog of code TEST-ASS-A
- remove the child TEST-B
- press "Save" and the "Cancel"
- enter in the edit dialog of code TEST-B
- enter in the edit date dialog
- change the "To date" to 2020-03-01
- enter in the edit dialog of code ASS-A
- add child TEST-B
- press save

Expected results:
an error dialog appears saying that the child date range is shorter than the parent one

Passed: [X]

### 13.20 - prototype date

Test description:
- enter in the edit dialog of code with several revisions without prototype
- enter in the "edit dates" dialog
- change the first (from the top) "From date" to "prototype"

Expected results:
- no error (yellow cell) is showed
- **ALL** the cell in the "To date" column are R/O
- the date "End to" of the 1st and 2nd line are blanked

Passed: [X]

Test description #2:
- after the above test, press save and ok until you reach the "Edit dialog"
- check that the "From/to date" "Revision selector" lists all the dates

Expected results #2:
- the "From/to date" "Revision selector" lists all the dates and prototype

Passed: [X]

Test description #3:
- after the steps above
- press the "..." button and go in the "edit dates" dialog
- change the "From date" in the first row from "PROTOTYPE" to a date grather than the 2nd line

Expected results #3:
- no error (yellow cell) is showed
- the "End to" cell in the second line show a valid date
- the "End to" cell in the 1st line is editable

Passed: [X]

Test description #4:
- after the steps above
- press save and go in the edit window
- check that the "From/to date" "Revision selector" lists all the dates

Expected results #4:
- the "From/to date" "Revision selector" lists all the dates w/o prototype

Passed: [X]

### 13.24 - date in the title bar

Test description:
- enter in the edit dialog of code with several revisions
- select a 2nd revision in the "From/to date" selector
- press the "..." button and go in the edit dialog
- change the 2nd row "From date" with a reasonable value
- press "Save", then "OK"

Expected results:
- the "From/to date" is changed accordling to the steps above
- the date showed in the title bar is changed accordling to the steps above

Passed: [X]

### 13.25 - Edit date dialog layout

Test description:
- enter in the edit dialog of code with several revisions
- check that in the "from date" column, only the 1st row has the "P" button

Expected results:
only the 1st row has the "P" buttons

Passed: [X]

Test description #2:
check that in the "from date" column, all the rows have the "..." buttons

Expected results #2:
all the rows have the "..." buttons

Passed: [X]

Test description #3:
check that in the "to date" column, only the 1st row has the "..." button

Expected results #3:
the first row has the "..." button

Passed: [X]

Test description #4:
in the "from date", enter in the first row the date "PROTOTYPE"

Expected results #4:
the date "PROTOTYPE" in entered

Passed: [X]

Test description #5:
 - in the "from date", enter in the first row a valid date
- in the "from date", press the "P"

Expected results #5:
the date "PROTOTYPE" in entered

Passed: [X]

Test description #6:
in the "from date", enter in the 2nd row the date "PROTOTYPE"

Expected results #6:
the date "PROTOTYPE" cannot be entered

Passed: [X]

## 14 - Generic test

### 14.1 - rename bombrowser.ini

Test description:
rename bombrowser.ini as bombrowser.ini.no

Expected results:
at start up time, an error dialog is showed saying that the confuguration cannot be load: bombrowser.ini file may be missing

Passed: [X]

### 14.2 - shutdown the sql server

Test description:
shutdown the sql server

Expected results:
at start up time, an error dialog is showed saying that it is imposible to access to the server

Passed: [X]

### 14.3 - test re-connection after an sql server disconnection

Test description:
- perform a query looking for the code 100001 in code list window
- shutdown the server
- re-do the same query and check that an error is showed

Expected results:
a dialog error is showed

Passed: [X]

Test description #2:
- startup the server
- wait few seconds
- re-do the same query and check that an error is showed
- re-do *again* the same query

Expected results #2:
the query results is showed

Passed: [X]

Test description #3:
- re-do the same test on a different db


Expected results #3:
the previous tests were passed

Passed: [X]

### 14.6 - Config test

TBD: test the configuration:
- force_*_uppercase
- template
- the overriding of the configuration store in the server

## 15 - Export test

TBD

## 16 - Import test

TBD

## 17 - Window menu test

### 17.1 - Window menu test, close all other window

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- where used window
- valid where used window


Test description:
from the 'where used' window, select menu->windows->close all other windows

Expected results:
all windows closed but the 'where used' window

Passed: [X]

### 17.2 - Window menu test, new codes list window

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- where used window
- valid where used window


Test description:
from the 'where used' window, select menu->windows->new codes list window

Expected results:
a NEW 'Codes list' window is opened

Passed: [X]

Test description #2:
from the 'where used' window, select menu->windows->new codes list window

Expected results #2:
a 3rd 'Codes list' window is opened

Passed: [X]

## 18 - Advanced search in the BOM

### 18.1 - Advanced search in the BOM

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window


Test description:
From the 'Search' menu select 'Advanced search'

Expected results:
A 'Search in BOM window' is showed

Passed: [X]

### 18.2 - Advanced search in the BOM - search by code

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'

Test description:
Insert '81' in the code field and press 'Search'

Expected results:
Only codes containg '81' are showed

Passed: [X]

### 18.3 - Advanced search in the BOM - search by descr

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'

Test description:
Insert '8' in the Description field and press 'Search'

Expected results:
Only the code description containg '8' are showed

Passed: [X]

Test description #2:
Select a code and check that the codegui panel changes accordling


Expected results #2:
The codegui panel changes accordling

Passed: [X]

Test description #3:
- Select with a row and click the RMB
- Press edit code

Expected results #3:
The edit code window is opened

Passed: [X]

### 18.6 - Advanced search in the BOM - search by descr and code

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'

Test description:
- Insert '7' in the Description field
- Insert '7' in the Code field
- Press 'Search'

Expected results:
Only the code containg '7' with description containg '7' are showed

Passed: [X]

### 18.7 - Advanced search in the BOM search w/multiple fields

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'Search' menu select 'Advanced search'
- from the 'Search mode' menu select 'Advanced'


Test description:
Insert 7 in the code field, then press Search

Expected results:
Only codes containing 7 are showed

Passed: [X]

Test description #2:
- Clean all the fields
- Insert 7 in the description field, then press Search

Expected results #2:
Only codes containing '7' in description are showed

Passed: [X]

Test description #3:
- Clean all the fields
- Insert 7 in the description field, then insert 7 in the 'Supplier#1 PN' field, then press Search

Expected results #3:
Only codes containing 7 with PN containing 7 are showed

Passed: [X]

Test description #4:
- Clean all the fields
- Insert >7 in the code field, then press Search

Expected results #4:
Only codes which starts from 8 are showed

Passed: [X]

Test description #5:
- Clean all the fields
- Insert >7 in the code field
- Insert 7 in the description field
then press Search

Expected results #5:
Only codes which start from 8 and contains 7 in the description are showed

Passed: [X]

Test description #6:
- Clean all the fields
- Insert <6 in the code field
- Insert 7 in the description field
then press Search

Expected results #6:
Only codes which start from 5 and contains 7 in the description are showed

Passed: [X]

Test description #7:
- Clean all the fields
- Insert !820007 in the code field
- Insert 7 in the description field
then press Search

Expected results #7:
Only codes different from 820007 and contains 7 in the description are showed

Passed: [X]

Test description #8:
- Clean all the fields
- Insert >2000 in the rid field
- Insert 7 in the description field
then press Search

Expected results #8:
Only codes with rid greather than 2000 and contains 7 in the description are showed

Passed: [X]

Test description #9:
- Clean all the fields
- Insert <2000 in the rid field
- Insert 7 in the description field
then press Search

Expected results #9:
Only codes with rid less than 2000 and contains 7 in the description are showed

Passed: [X]

### 18.16 - Advanced search in the BOM - where used

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an where used window
- from the 'Search' menu select 'Advanced search'

Test description:
Insert '17' in the code field and press 'Search'

Expected results:
Only codes containg '17' are showed

Passed: [X]

### 18.17 - Advanced search in the BOM - smart where used

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an smart where used window
- from the 'Search' menu select 'Advanced search'

Test description:
Insert '17' in the code field and press 'Search'

Expected results:
Only codes containg '17' are showed

Passed: [X]

## 19 - Export data from assembly

### 19.1 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window


Test description:
From the 'File' menu select 'Export data...'

Expected results:
A 'Export' dialog is showed

Passed: [X]

### 19.2 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

Test description:
Check that the data showed in the window title is the greatest one of the code

Expected results:
The data is the greatest one

Passed: [X]

### 19.3 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

Test description:
Press the Close button

Expected results:
The dialog disappear

Passed: [X]

### 19.4 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

Test description:
Press the Export button

Expected results:
- The successful dialog appeared (maybe below other window)
- A folder containing all the files appeared
- In the folder there is a zip file containing all the files
- In the folder there is a BOM in the same format specified in the dialog
- Doing a 'paste' command in a folder, the zip file is copied

Passed: [X]

### 19.5 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

Test description:
Umark the 'zip' option; press the Export button

Expected results:
- The successful dialog appeared (maybe below other window)
- A folder containing all the files appeared
- In the folder there NO a zip file containing all the files
- Doing a 'paste' command in a folder, the folder with all the files is copied

Passed: [X]

### 19.6 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

Test description:
Umark the 'export files' option; press the Export button

Expected results:
- The successful dialog appeared (maybe below other window)
- A folder containing only the zip file and the bom appeared


Passed: [X]

### 19.7 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

Test description:
Umark the 'open destination folder' option; press the Export button

Expected results:
The successful dialog appeared


Passed: [X]

### 19.8 - Export data

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open an assembly window
- from the 'File' menu select 'Export data...'

Test description:
Change the destination directory; press the Export button

Expected results:
The selected destination directory is showed


Passed: [X]

### 19.9 - Export data - where used

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open the Where used window
- from the 'File' menu select 'Export data...'

Test description:
Change the destination directory; press the Export button

Expected results:
- The successful dialog appeared (maybe below other window)
- A folder containing all the files appeared


Passed: [X]

### 19.10 - Export data - where used

Preparatory steps:
From codes list window:
- search a code (eg. 820007)
- open the Smart where used window
- from the 'File' menu select 'Export data...'

Test description:
Change the destination directory; press the Export button

Expected results:
- The successful dialog appeared (maybe below other window)
- A folder containing all the files appeared


Passed: [X]

## 20 - Test bombrowser servers backends

### 20.1 - SQLServer backend

#### 20.1.1 - Create a test database

Test description:
- set up a sqlserver database and start it
- run "python mkdb.py

Expected results:
- no error is returned


Passed: [X]

#### 20.1.2 - Check test database

Test description:
- run bombrowser
- check the existance of the assembly 100000


Expected results:
- the assembly has a bom


Passed: [X]

#### 20.1.3 - Dump the database

Test description:
- run "[python] bombrowser[.py] --manage-db --dump-tables <namefile>


Expected results:
- the <namefile> file is created


Passed: [X]

#### 20.1.4 - Restore the database

Test description:
- edit the code 100001
- select Edit->Delete code. The code is now deleted
- run "[python] bombrowser[.py] --manage-db --restore-tables --yes-really-i-know-what-i-want <namefile>
- search the code 100001 again

Expected results:
- the 100001 exists


Passed: [X]

#### 20.1.5 - Create a new (empty) database

Test description:
- run "[python] bombrowser[.py] --manage-db --new-db --yes-really-i-know-what-i-want
- search for "%"

Expected results:
- only the code "000000000000" is returned


Passed: [X]

#### 20.1.6 - Run bombrowser db self test

Test description:
run 'python3 python3 test_db.py --use-ini-config'

Expected results:
- no error is returned


Passed: [X]

### 20.2 - SQLite backend

#### 20.2.1 - Create a test database

Test description:
- set up a sqlite database and start it
- run "python mkdb.py

Expected results:
- no error is returned


Passed: [X]

#### 20.2.2 - Check test database

Test description:
- run bombrowser
- check the existance of the assembly 100000


Expected results:
- the assembly has a bom


Passed: [X]

#### 20.2.3 - Dump the database

Test description:
- run "[python] bombrowser[.py] --manage-db --dump-tables <namefile>


Expected results:
- the <namefile> file is created


Passed: [X]

#### 20.2.4 - Restore the database

Test description:
- edit the code 100001
- select Edit->Delete code. The code is now deleted
- run "[python] bombrowser[.py] --manage-db --restore-tables --yes-really-i-know-what-i-want <namefile>
- search the code 100001 again

Expected results:
- the 100001 exists


Passed: [X]

#### 20.2.5 - Create a new (empty) database

Test description:
- run "[python] bombrowser[.py] --manage-db --new-db --yes-really-i-know-what-i-want
- search for "%"

Expected results:
- only the code "000000000000" is returned


Passed: [X]

#### 20.2.6 - Run bombrowser db self test

Test description:
run 'python3 python3 test_db.py --use-ini-config'

Expected results:
- no error is returned


Passed: [X]

### 20.3 - Postgresql backend

#### 20.3.1 - Create a test database

Test description:
- set up a postgresql database and start it
- run "python mkdb.py

Expected results:
- no error is returned


Passed: [X]

#### 20.3.2 - Check test database

Test description:
- run bombrowser
- check the existance of the assembly 100000


Expected results:
- the assembly has a bom


Passed: [X]

#### 20.3.3 - Dump the database

Test description:
- run "[python] bombrowser[.py] --manage-db --dump-tables <namefile>


Expected results:
- the <namefile> file is created


Passed: [X]

#### 20.3.4 - Restore the database

Test description:
- edit the code 100001
- select Edit->Delete code. The code is now deleted
- run "[python] bombrowser[.py] --manage-db --restore-tables --yes-really-i-know-what-i-want <namefile>
- search the code 100001 again

Expected results:
- the 100001 exists


Passed: [X]

#### 20.3.5 - Create a new (empty) database

Test description:
- run "[python] bombrowser[.py] --manage-db --new-db --yes-really-i-know-what-i-want
- search for "%"

Expected results:
- only the code "000000000000" is returned


Passed: [X]

#### 20.3.6 - Run bombrowser db self test

Test description:
run 'python3 python3 test_db.py --use-ini-config'

Expected results:
- no error is returned


Passed: [X]

### 20.4 - Oracle backend

#### 20.4.1 - Create a test database

Test description:
- set up a oracle database and start it
- run "python mkdb.py

Expected results:
- no error is returned


Passed: [X]

#### 20.4.2 - Check test database

Test description:
- run bombrowser
- check the existance of the assembly 100000


Expected results:
- the assembly has a bom


Passed: [X]

#### 20.4.3 - Dump the database

Test description:
- run "[python] bombrowser[.py] --manage-db --dump-tables <namefile>


Expected results:
- the <namefile> file is created


Passed: [X]

#### 20.4.4 - Restore the database

Test description:
- edit the code 100001
- select Edit->Delete code. The code is now deleted
- run "[python] bombrowser[.py] --manage-db --restore-tables --yes-really-i-know-what-i-want <namefile>
- search the code 100001 again

Expected results:
- the 100001 exists


Passed: [X]

#### 20.4.5 - Create a new (empty) database

Test description:
- run "[python] bombrowser[.py] --manage-db --new-db --yes-really-i-know-what-i-want
- search for "%"

Expected results:
- only the code "000000000000" is returned


Passed: [X]

#### 20.4.6 - Run bombrowser db self test

Test description:
run 'python3 python3 test_db.py --use-ini-config'

Expected results:
- no error is returned


Passed: [X]

### 20.5 - Mysql backend

#### 20.5.1 - Create a test database

Test description:
NOTE: for this test, you shuld shutdown bombrowser before the db creation
- set up a mysql database and start it
- run "python mkdb.py

Expected results:
- no error is returned


Passed: [X]

#### 20.5.2 - Check test database

Test description:
- run bombrowser
- check the existance of the assembly 100000


Expected results:
- the assembly has a bom


Passed: [X]

#### 20.5.3 - Dump the database

Test description:
- run "[python] bombrowser[.py] --manage-db --dump-tables <namefile>


Expected results:
- the <namefile> file is created


Passed: [X]

#### 20.5.4 - Restore the database

Test description:
- edit the code 100001
- select Edit->Delete code. The code is now deleted
NOTE: for this test, you shuld shutdown bombrowser before the db restoration
- run "[python] bombrowser[.py] --manage-db --restore-tables --yes-really-i-know-what-i-want <namefile>
- search the code 100001 again

Expected results:
- the 100001 exists


Passed: [X]

#### 20.5.5 - Create a new (empty) database

Test description:
- run "[python] bombrowser[.py] --manage-db --new-db --yes-really-i-know-what-i-want
- search for "%"

Expected results:
- only the code "000000000000" is returned


Passed: [X]

#### 20.5.6 - Run bombrowser db self test

Test description:
run 'python3 python3 test_db.py --use-ini-config'

Expected results:
- no error is returned


Passed: [X]

## 21 - Run bombrowser self test

### 21.1 - Run bombrowser self test

Test description:
run 'python3 python3 -self-test'

Expected results:
- no error is returned


Passed: [X]

## 22 - Repeat some tests for foreign OS

### 22.1 - Drawings drag and drop

Test description:
do a drang and drop of the drawings in the edit dialog

Expected results:
- the drawing are added
- it is possible to re-open the drawings

Passed: [X]

### 22.2 - Copy and paste of the code gui information

Test description:
- press the 'Copy info' button in the CODE GUI
- do a 'Paste' in an text editor

Expected results:
the code information are copied in the editor

Passed: [X]

### 22.3 - Assembly copy

Test description:
- open an assembly of a code
- from the menu select Edit->Copy- do a 'Paste' in an text editor

Expected results:
the assembly data is copied in the editor

Passed: [X]

#  - RESULTS:

2022-09-03 v0.4.6
Failed tests: 0

