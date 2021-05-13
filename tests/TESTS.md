 

# BOMBrowser tests list

## Index

- 1 - BOMBrowser - Codes list
- 2 - 'Code gui' panel
- 3 - BOMBrowser - Assembly
- 4 - BOMBrowser - Valid where used
- 5 - BOMBrowser - Where used
- 6 - BOMBrowser - Select date (empty)
- 7 - BOMBrowser - Diff window
- 8 - BOMBrowser - Copy/revise code
- 9 - BOMBrowser - Edit code
- 10 - BOMBrowser - Edit date
- 11 - Generic test
- 12 - Export test
- 13 - Import test

## Preface

This tests list assumes that you are working with the test database generated
by mkdb.py.
This tests list is related to the v0.4.

## 1 - BOMBrowser - Codes list

### Test 1.1 - search a code

Test description:
Insert the code '820037' in the 'Code' field and press **ENTER**

Expected results:
The code 820037 is showed

Passed: [X]

### Test 1.2 - search a code (2)

Test description:
Insert the code '820038' in the 'Code' field and press the button **'Search'**

Expected results:
The code 820038 is showed

Passed: [X]

### Test 1.3 - search a code by description

Test description:
Insert the code 'BOARD 14' in the 'Description' field and press the button 'Search'

Expected results:
The code 610014 - "BOARD 14" is showed

Passed: [X]

### Test 1.4 - search a code by description with a jolly character

Test description:
Insert the code '%BOARD%13' in the 'Description' field and press ENTER

Expected results:
The code 610013 - "BOARD 13" is showed

Passed: [X]

### Test 1.5 - search a code with a jolly character

Test description:
- Insert the code '%6%' in the 'Code' field
- press the button 'Search'

Expected results:
The codes that contains '6' are showed

Passed: [X]

### Test 1.6 - search a code and a description with a jolly character

Test description:
- Insert the code '%6%' in the 'Code' field
- insert %BOARD% in the description filed
- press the button 'Search'

Expected results:
The codes that contains '6' and the description which contains BOARD are showed

Passed: [X]

### Test 1.7 - assembly

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

### Test 1.11 - where used

Test description:
- Insert the code '810036' in the 'Code' field,
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Where used" command.

Expected results:
The "BOMBrowser - Where used" window is showed

Passed: [X]

### Test 1.12 - where used (2)

Test description:
- Insert the code '100037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Where used" command.

Expected results:
The "BOMBrowser - Where used" window is showed. Only one code (100037) is showed.

Passed: [X]

### Test 1.13 - valid where used

Test description:
- Insert the code '810036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Valid where used" command.

Expected results:
The "BOMBrowser - Valid where used" window is showed

Passed: [X]

### Test 1.14 - valid where used (2)

Test description:
- Insert the code '100037' in the 'Code' field
- and press the button 'Search'
- press the right mouse button on the first entry
- select the "Valid where used" command.

Expected results:
The "BOMBrowser - Valid where used" window is showed. Only one code (100037) is showed.

Passed: [X]

### Test 1.15 - Copy/revise code

Test description:
- Insert the code '810037' in the 'Code' field,
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Copy/revise code" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this contains a list of the code 810037.

Passed: [X]

### Test 1.16 - edit code

Test description:
- Insert the code '810036' in the 'Code' field
- and press the button 'Search'
- press the right mouse button on the first entry
- select the "Edit code" command.

Expected results:
The "BOMBrowser - Edit code" window showed; this contains the code 810036 properties.

Passed: [X]

### Test 1.17 - diff from

Test description:
- Insert the code '810037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff from" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 810037 codes.

Passed: [X]

### Test 1.18 - diff from (2x)

Test description:
- Insert the code '820036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff from" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.

Passed: [X]

### Test 1.19 - diff to

Test description:
- Insert the code '810037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff to" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 810037 codes.

Passed: [X]

### Test 1.20 - diff to (2x)

Test description:
- Insert the code '820036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff to" command.

Expected results:
The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.

Passed: [X]

### Test 1.21 - menu->help->about

Test description:
In the menu select the Help and About subcommand

Expected results:
- The "about" dialog is showed. The dialog contains:
- the current version and the copyright code.
- a text that showed the used connection

Passed: [X]

### Test 1.22 - menu->window

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

### Test 1.23 - menu->file->close

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

### Test 1.24 -Ctrl-Q  menu->file->close

Test description:
- insert code 820037
- press the right mouse button on the first entry and select the "Where used" command.
- Two windows are opened. Set the focus to the "BOMBrowser - Codes list"
- press CTRL-Q

Expected results:
The "BOMBrowser - Codes list" is closed. "BOMBrowser - Where used" is opened.

Passed: [X]

### Test 1.25 - menu->file->exit

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

### Test 1.31 - Menu->edit->copy

Test description:
- insert code %6% and press ENTER;
- select menu->edit->copy
- Paste the clipboard in an editor

Expected results:
- check that there is the same table showed in the BOMBrowser - Codes list (fields TAB separated).
- Check that the number of row are the same +1 of the "BOMBrowser - Codes list" widow (there is the header)

Passed: [X]

### Test 1.33 - Code gui

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

### Test 1.34 - Status bar

Test description:
- insert code 8200% and press ENTER

Expected results:
in the status bar appears the number of the results

Passed: [X]

### Test 1.35 - Status bar

Test description:
- insert code CODE_INVALID and press ENTER

Expected results:
- in the status bar appears the number of the results (0)
- the previous results are not cleaned

Passed: [X]

### Test 1.36 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code 8200% and press "Search"

Expected results:
in the status bar appears the number of the results

Passed: [X]

### Test 1.37 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code CODE_INVALID and press "Search"

Expected results:
in the status bar appears the number of the results (0)

Passed: [X]

### Test 1.38 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code CODE_INVALID and press "Search"

Expected results:
- in the status bar appears the number of the results (0)
- the previous results are not cleaned

Passed: [X]

### Test 1.39 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code 820017 and press "Search"

Expected results:
- in the status bar appears the number of the results (>= 4)
- in the results table, appears the different revisions of the searched code

Passed: [X]

### Test 1.40 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code 8200% and press "Search"

Expected results:
- in the results table, appears the codes (and their revisions) which start from 8200..

Passed: [X]

### Test 1.41 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code >820000 and press "Search"

Expected results:
- in the results table, appears the codes greather than 820000

Passed: [X]

### Test 1.42 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert date-from 2003-06-04 and press "Search"

Expected results:
- in the results table, it appears the codes which have as date from 2003-06-04

Passed: [X]

### Test 1.43 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert date-from '>2003-06-04' and press "Search"

Expected results:
- in the results table, appears the codes which have as date from greather than 2003-06-04 (prototype too)

Passed: [X]

### Test 1.44 - Revision search

Test description:
- select from the menu "Search mode->advanced"
- insert code >820000 and press ENTER

Expected results:
- in the results table, appears the codes greather than 820000

Passed: [X]

### Test 1.45 - Revision search

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

### Test 1.46 - Revision search - RMB menu

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

### Test 1.47 - Revision search - RMB menu error

Dropped in v0.4.3b4

### Test 1.48 - Revision search - RMB menu error

Dropped in v0.4.3b4

### Test 1.49 - Revision search - search <

Test description:
- select from the menu "Search mode->advanced"
- insert code <5000 and press ENTER


Expected results:
- All codes less than 5000 are showed

Passed: [X]

### Test 1.50 - Revision search - search !

Test description:
- select from the menu "Search mode->advanced"
- insert code !820001 and press ENTER


Expected results:
- All codes less different from 820001 are showed

Passed: [X]

### Test 1.50 - Revision search - search =

Test description:
- select from the menu "Search mode->advanced"
- insert code =820001 and press ENTER

Expected results:
- Only the code 820001 (in all its revisions) is showed

Passed: [X]

## 2 - 'Code gui' panel

### Test 2.1 - general

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the first entry (820000)

Expected results:
on the left panel there are the information of the selected code

Passed: [X]

### Test 2.2 - multiple revision

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Select another date in the rightmost combobox

Expected results:
The information on the panel are changed accordly

Passed: [X]

### Test 2.3 - multiple revision (2)

Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001)

Expected results:
The right combo box button, contains all the dates

Passed: [X]

### Test 2.4 - documents

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)

Expected results:
In the bottom part are showed two buttons with two documens

Passed: [X]

### Test 2.5 - documents (2x)

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Press a document button

Expected results:
Clicking one button document, the related document is opened

Passed: [X]

### Test 2.6 - Copy info..

Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Press copy info button

Expected results:
Pasting the clipboard content in a editor, the relevant information are showed

Passed: [X]

### Test 2.7 - Check tool tip

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code - gui, drawing button

Expected results:
- a tooltip appears showing file name and full path

Passed: [X]

### Test 2.8 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Open dir"

Expected results:
- the directory containing the file is opened

Passed: [X]

### Test 2.9 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy filename"
- paste it in an editor

Expected results:
- the filename is pasted

Passed: [X]

### Test 2.10 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy dirname"
- paste it in an editor

Expected results:
- the dirname is pasted

Passed: [X]

### Test 2.11 - RMB menu of drawing button

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy full path"
- paste it in an editor

Expected results:
- the full path (filename+dirname) is pasted

Passed: [X]

### Test 2.12 - RMB menu of drawing button (windows only)

Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy file"
- paste it in a folder

Expected results:
- the file is copied

Passed: [X]

## 3 - BOMBrowser - Assembly

### Test 3.1 - select date

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

### Test 3.4 - show assembly

Test description:
- insert code "810037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.

Expected results:
- The "BOMBrowser - Assembly" window appears
- only one code (810037) is showed

Passed: [X]

### Test 3.6 - show assembly (2)

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

### Test 3.8 - where used (2)

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

### Test 3.10 - valid where used (2)

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

### Test 3.11- menu->help->about

Test description:
In the menu select the Help and About subcommand

Expected results:
The "about" dialog is showed. The dialog contains the current version and the copyright code.

Passed: [X]

### Test 3.12 - menu->window

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command
- select the first date doubleckicking on it.
Two windows are opened. Select the "Windows menu" in the "BOMBrowser - Assembly" window:

Expected results:
in the menu only one  window is showed: "BOM Browser - Codes list".

Passed: [X]

### Test 3.13 - menu->file->close

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command
- select the first date doubleckicking on it.
- Two windows are opened. Select the "File->Close" in the "BOMBrowser - Assembly" window:

Expected results:
The "BOMBrowser - Assembly" list is closed. "BOMBrowser - Codes list" is opened.

Passed: [X]

### Test 3.14 -Ctrl-Q  menu->file->close

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command
- select the first date doubleckicking on it.
- two windows are opened. Set the focus to the "BOMBrowser - Assembly", then press CTRL-Q

Expected results:
The "BOMBrowser - Assembly" is closed. "BOMBrowser - Codes list" is opened.

Passed: [X]

### Test 3.15 - menu->file->exit

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

### Test 3.18 - menu->file->exit

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

### Test 3.21 - menu->file->export as json

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

### Test 3.23 - menu->view->show up level 1

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

### Test Set 3.29 - find

#### Test 3.29.1 - find

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

#### Test 3.29.2 - find

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

#### Test 3.29.3 - cancel

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

#### Test 3.29.4 - find a code

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" 3 times

Expected results:
A different instance of the code 810003 is showed each time

Passed: [X]

Test description #2:
- Press "prev" 2 times

Expected results #2:
A different instance of the code 810003 is showed each time

Passed: [X]

#### Test 3.29.6 - find a code

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" 3 times
- Press "prev" 3 times

Expected results:
After thelast action a dialog "Data not found" is showed

Passed: [X]

#### Test 3.29.7 - find a code

Preparatory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" going below the bom until a dialog "Data not found" is showed

Expected results:
After the last action a dialog "Data not found" is showed

Passed: [X]

### Test 3.30 - show latest assembly

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

### Test 3.31 - show latest assembly

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

### Test 3.32.1 - Menu file -> copy files

Test description:
- open as "latest assembly" in Assembly window the code 820000
- Select File, then "Copy files"

Expected results:
- A "Save to" dialog appear

Passed: [X]

Test description #2:
- after the step above, press Cancel

Expected results #2:
- Nothing

Passed: [X]

Test description #3:
- repeat the step above, but instead pressing Cancel, select a directory and press save

Expected results #3:
- In the selected folder, the assemblies files are copied

Passed: [X]

### Test 3.33 - Show prototype assembly

#### Test 3.33.1 - Show prototype assembly

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

#### Test 3.33.2 - Show prototype assembly

Preparatory steps:
- look at the code 610004 in the codes list window
- Check in the code gui right panel, that the code has two date and that it is not a prototype

Test description:
- look at the code 610004 in the codes list window
- From the RMB menu, select "Show latest assembly"

Expected results:
- the assembly window is showed
- looking at the dates of the "code gui" right panel, for any code the "prototype" date from is showed: i.e. all code are not prototype

Passed: [X]

## 4 - BOMBrowser - Valid where used

### Test 4.1

Test description:
in the "Codes list" window search for the code 820017. Then select  the right click menu command "Valid where used"

Expected results:
- the "valid where used" window is showed
- each code showed (except the top node) has a "end to" date empty
- no code are repeated

Passed: [X]

## 5 - BOMBrowser - Where used

### Test 5.1

Test description:
in the "Codes list" window search for the code 820017. Then select  the right click menu command "Where used"

Expected results:
- the where used window is showed
- few codes showed (the top node doesn't matter) have a "end to" date not empty. These code sometime are repeated

Passed: [X]

## 6 - BOMBrowser - Select date

This test is covered by the ones of the Assembly window

## 7 - BOMBrowser - Diff window

### Test 7.1 - diff the same code

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

### Test 7.2 - diff two different codes

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

### Test 7.3 - diff two different codes

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

## 8 - BOMBrowser - Copy/revise code

### Test 8.1 - date dialog

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

### Test 8.3 - date dialog

INtegrated in 8.4

### Test 8.4 - Copy/revise code window

Test description:
Test description
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry

Expected results:
- The Copy/revise windows appears
- the "old-Iter" are the same as the one selected in the "Select date" window

Passed: [X]

### Test 8.5 - Copy/revise code window

Test description:
Test description
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *second* entry
- The Copy/revise windows appears

Expected results:
the "Iter" are the same as the one selected in the "Select date" window

Passed: [X]

### Test set 8.6 - Copy/revise code window

#### Test 8.6.1 - Cancel

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

#### Test 8.6.4 - *Revise*/copy code window

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

#### Test 8.6.5 - Copy/revise code window

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

#### Test 8.6.6 - Copy/revise code window

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- check the copy checkbox
- check the editability of the following fields: New/Code, New/Iter, New/Description, New/Rev, New/Date from

Expected results:
the field New/Code, New/Description, New/Date from and New/Rev are editable

Passed: [X]

#### Test 8.6.7 - Copy/revise code window

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- check the copy checkbox
- check the field New/Iter

Expected results:
The field New/Iter is 0

Passed: [X]

#### Test 8.6.8 - Copy error

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- click on the copy checkbox
- check that the Old/code is equal to the new/code
- press "Copy code" button

Expected results:
- An error dialog appears saying that the code already exists
- pressing OK, the Copy / Revise window still exists

Passed: [X]

#### Test 8.6.10 - Confirmation dialog / success

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- click on the copy checkbox
- change the new/code in 82004A"
- unmark the checkbox "start edit dialog after copy/revision"
- press "Copy code" button
- A confirmation dialog appears; press no

Expected results:
the  confirmation dialog disappear; the "BOMBrowser - copy /revise code" windows is opened.

Passed: [X]

Test description #2:
- after the steps above, pres again "Copy/Revise button"
- a confirmation dialog appears; press yes

Expected results #2:
A successfull dialog appears

Passed: [X]

#### Test 8.6.12 - Confirmation dialog / success (2)

Preparatory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Copy/revise code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Copy/revise windows appears

Test description:
- click on the copy checkbox
- mark the checkbox "start edit dialog after copy/revision"
- change the new/code in 82004B"
- press "Copy code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the new code appears.
- There are attached document and a children list

Passed: [X]

#### Test 8.6.14 - Confirmation dialog / success (3)

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

#### Test 8.6.15 - Revise a code / date error

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

#### Test 8.6.16 - Revise a code / date error

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

### Test 8.7 - revise a code

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

### Test 8.8 - copy a code

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

### Test 8.9 - copy a code (in proto mode)

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

### Test 8.10 - revise a code (in proto mode)

Test description:
- revise the code "820041" from the code list window
- check the checkbox "Prototype"
- press "Revise code" button
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- The date in date selector reports also prototype

Passed: [X]

### Test 8.11 - revise a code (in proto mode)

Test description:
- revise the code "820004" from the code list window (the code has already a prototype revision, if not create a prototype revision)
- check the checkbox "Prototype"
- press "Revise code" button


Expected results:
- a dialog error reports that a prototype already exists

Passed: [X]

### Test 8.12 - chenge from revision to copy mode

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

## 9 - BomBrowser - Edit code

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

### Test 9.1 - Edit code / Rev field

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

### Test 9.2 - Edit code / Default unit field

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

### Test 9.3 - Edit code / Description field

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

### Test 9.4 - Edit code / Generic properties field

Preparatory steps:


Test description:
- repeat the test above for all the "Generic properties" fields

Expected results:
the "generic property" field is like the one changed

Passed: [X]

### Test 9.5 - Edit code / Drawing list - add drawing

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

### Test 9.6 - Edit code / Drawing list - del drawing

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the drawing list panel
- execute the command "delete drawing" on a drawing
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the removed drawing is not present

Passed: [X]

### Test 9.7 - Edit code / Drawing list - view drawing

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the drawing list panel
- execute the command "view drawing" on a drawing

Expected results:
the selected drawing is showed

Passed: [X]

Test description #2:
- doubleclick on a drawing in the drawing list panel

Expected results #2:
the selected drawing is showed

Passed: [X]

### Test 9.8 - Edit code / Children panel - del a child

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- click with the RMB on the children list panel
- execute the command "delete row" on a line
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected results:
the removed item is not present

Passed: [X]

### Test 9.9 - Edit code / Children panel - add a child

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
the added item is present

Passed: [X]

### Test 9.10 - Edit code / Children panel - add a child

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
the added item is present

Passed: [X]

### Test 9.11 - Edit code / Children panel - edit a field - non existant code

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

### Test 9.13 - Edit code / Children panel - edit a field - duplicate code

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

### Test 9.14 - Edit code / Children panel - edit a field - wrong qty

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

### Test 9.16 - Edit code / Children panel - edit a field - wrong each

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

### Test 9.18 - Edit code / Children panel - sorting

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

### Test 9.19 - Edit code / Children panel - sorting

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

### Test 9.20 - Edit code / Children panel - sorting

Preparatory steps:


Test description:
- in the children panel, change the row sequence sort by code (click on the "code" column header)
- take note of the "seq" column values
- do an "insert row after"

Expected results:
the seq values are reordered on the basis of the current sequence.

Passed: [X]

### Test 9.21 - Edit code / File -> close

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

### Test 9.22 - Edit code / File -> exit

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

### Test 9.25 - Edit code / CTRL-Q

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

### Test 9.27 - Edit code / Windows

Preparatory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

Test description:
- select the menu Windows menu

Expected results:
the opened windows are showed

Passed: [X]

### Test 9.28 - Edit code / Help->about

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

### Test 9.29 - Edit code / Children panel - search code

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

### Test 9.30 - Edit code / Children panel - search code

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

### Test 9.31 - Edit code / Children panel - search code

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

### Test 9.32 - Edit code - delete revision

Preparatory steps:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- take this copy, and revise it 3 times (changing the from date to avoid conflicts)
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
- From menu -> edit, select delete revision
- a confirmation dialog is showed, press yes

Expected results #3:
- a comfirmation dialog is showed, saying that the revision is deleted. Press ok.
- the previous selected revision is removed

Passed: [X]

### Test 9.35 - Edit code - delete revision

Preparatory steps:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- take this copy, and revise it 3 times (changing the from date to avoid conflicts)
- Edit this code


Test description:
- From menu -> edit, select delete revision
- repeat the step above until only one revision is present
- From menu -> edit, select delete revision (again)

Expected results:
an error dialog box is showed saying that it is not possible to delete the last revision

Passed: [X]

### Test 9.36 - Edit code - delete revision

Preparatory steps:


Test description:
- Enter in the edit dates window, and insert a valid "end to" date in the first row. Then save the results
- From the edit window, delete the first revision
- Delete the last revision

Expected results:
- after the deletes, the code "from date" is the same of the first code
- the final "to date" are the same of the last code

Passed: [X]

### Test 9.37 - Edit code - delete code

Preparatory steps:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- take this copy, and revise it 3 times (changing the from date to avoid conflicts)
- Edit this code


Test description:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- Edit this code
- From the menu->edit select "delete code"

Expected results:
a confirmation dialog appears

Passed: [X]

### Test 9.38 - Edit code - delete code

Preparatory steps:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- take this copy, and revise it 3 times (changing the from date to avoid conflicts)
- Edit this code


Test description:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- Edit this code
- From the menu->edit select "delete code"
- a confirmation dialog appears, press no

Expected results:
nothing happened

Passed: [X]

### Test 9.39 - Edit code - delete code

Preparatory steps:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- take this copy, and revise it 3 times (changing the from date to avoid conflicts)
- Edit this code


Test description:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- Edit this code
- From the menu->edit select "delete code"
- a confirmation dialog appears, press yes

Expected results:
- a confirmation dialog appears, press ok
- the edit dialog is not showed anymore

Passed: [X]

Test description #2:
- search for the deleted code

Expected results #2:
- the code is not showed anymore

Passed: [X]

### Test 9.40 - Edit code - change revision

Preparatory steps:
- Take a code from the code list gui with multiple revision
- Edit this code


Test description:
- Acting to the "From/to date" QComboBox, change the revision of the code
- in parallel make one change in a field for each revision (insert the from date to help the test) and press Save
- repeat the step above for each revision
- Acting to the "From/to date" QComboBox, change the revision of the code

Expected results:
- The dialog show for each revision the change performed in the step above

Passed: [X]

### Test 9.41 - Edit code - change revision without saving

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

### Test 9.42 - Edit code - change revision without saving

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

### Test 9.43 - Edit code - remove a child without saving

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

### Test 9.44 - Edit code - insert a child without saving

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

### Test 9.45 - Edit code - insert a child  without saving

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

### Test 9.46 - Edit code - change child without saving

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

### Test 9.47 - Edit code - add drawing without saving

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

### Test 9.48 - Edit code - remove a drawing without saving

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

### Test 9.49 - Edit code - add a duplicated code

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

### Test 9.50 - Edit code - add a code to an empty children list

Preparatory steps:
- Take a code from the code list gui without children (eg an 8100xx code)
- Edit this code


Test description:
- add a new child code, using the RBM menu

Expected results:
- clicking the right mouse button shows a menu that allows to insert a code

Passed: [X]

### Test 9.51 - Edit code - exit without saving

Preparatory steps:
- Take a code from the code list gui without children (eg an 8100xx code)
- Edit this code


Test description:
- close the window (click on the upper right "X" icon)

Expected results:
- the edit window closes itself

Passed: [X]

### Test 9.51 - Edit code - exit without saving

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
- Continue from the previous steps
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

## 10 - BomBrowser - Edit date

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

### Test 10.1

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
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

### Test 10.2

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
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

### Test 10.4

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
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

### Test 10.5

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
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

### Test 10.6

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a not valid one (i.e. 'z')

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
Test description #2
- press save

Expected results #2:
an error dialog is showed

Passed: [X]

### Test 10.8

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a not valid one (i.e. 'z')
- the cell become yellow; press cancel
- the edit dates dialog is closed, reopen it

Expected results:
the valid old date appear

Passed: [X]

### Test 10.9

Preparatory steps:


Test description:
- change the "date from" of the first row with a not valid one (i.e. 2001-02-30)

Expected results:
the cell become yellow

Passed: [X]

### Test 10.10

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a a date equal the row below

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
- after the steps above, press save

Expected results #2:
- an error dialog is showed
- press ok, the edit date window is showed

Passed: [X]

Test description #3:
Test description #3
- after the step above, press cancel
- press the '...' button
- check the dates

Expected results #3:
- the dates are unchanged

Passed: [X]

### Test 10.10.1

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a a date before (-1) the row below

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
- after the steps above, press save

Expected results #2:
- an error dialog is showed
- press ok, the edit date window is showed

Passed: [X]

Test description #3:
Test description #3
- after the step above, press cancel
- press the '...' button
- check the dates

Expected results #3:
- the date are unchanged

Passed: [X]

### Test 10.10.2

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the 2nd row with a a date equal the row above

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
- after the steps above, press save

Expected results #2:
- an error dialog is showed
- press ok, the edit date window is showed

Passed: [X]

Test description #3:
Test description #3
- after the step above, press cancel
- press the '...' button
- check the dates

Expected results #3:
- the date are unchanged

Passed: [X]

### Test 10.10.3

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the 2nd row with a a date after (+1) the row above

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
- after the steps above, press save

Expected results #2:
- an error dialog is showed
- press ok, the edit date window is showed

Passed: [X]

Test description #3:
Test description #3
- after the step above, press cancel
- press the '...' button
- check the dates

Expected results #3:
- the date are unchanged

Passed: [X]

### Test 10.10.3

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the "date from" of the first row with a a date after (+1) the row below

Expected results:
the cell still be white

Passed: [X]

Test description #2:
- after the steps above, press save

Expected results #2:
- press ok, a confirmation dialog is showed

Passed: [X]

Test description #3:
Test description #3
- after the steps above press the '...' button
- check the dates

Expected results #3:
- the date are changed

Passed: [X]

### Test 10.11

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
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

### Test 10.12

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the value of the cell of the first row and column "To date" with an invalid one (i.e. 'z')

Expected results:
the cell become yellow

Passed: [X]

Test description #2:
press save

Expected results #2:
an error dialog appear

Passed: [X]

### Test 10.14

Preparatory steps:
- insert code 810036 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

Test description:
- change the value of the cell of the first row and column "To date" with a date before of the left cell

Expected results:
the cell become yellow

Passed: [X]

### Test 10.15

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

### Test 10.16 - conflict date

#### Test 10.16.1 - parent too early

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

#### Test 10.16.2 - parent too late

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

#### Test 10.16.3 - children too late

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

#### Test 10.16.4 - children too early

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

#### Test 10.16.5 - children too early

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

### Test 10.17 - prototype date

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

### Test 10.18 - date in the title bar

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

## 11 - Generic test

### Test 11.1

Test description:
rename bombrowser.ini as bombrowser.ini.no

Expected results:
at start up time, an error dialog is showed saying that the confuguration cannot be load: bombrowser.ini file may be missing

Passed: [X]

### Test 11.2

Test description:
shutdown the sql server

Expected results:
at start up time, an error dialog is showed saying that it is imposible to access to the server

Passed: [X]

### Test 11.3 - Config test

TBD: test the configuration:
- force_*_uppercase
- template
- the overriding of the configuration store in the server

## 12 - Export test

# RESULTS:

2020-05-12 v0.4.4b3
Failed tests list: 0

