

# BOMBrowser tests list

## Index

- 1 - BOMBrowser - Codes list
- 2 - 'Code gui' panel
- 3 - BOMBrowser - Assembly
- 4 - BOMBrowser - Valid where used
- 5 - BOMBrowser - Where used
- 6 - BOMBrowser - Select date (empty)
- 7 - BOMBrowser - Diff window (TBD)
- 8 - BOMBrowser - Copy/revise code
- 9 - BOMBrowser - Edit code
- 10 - BOMBrowser - Edit date
- 11 - Generic test

## Preface

This tests list assumes that you are working with the test database generaded
by mkdb.py.
This tests list is related to the v0.4.

## 1 - BOMBrowser - Codes list

### Test 1.1 - search a code

Test description: Insert the code '820037' in the 'Code' field and press **ENTER**

Expected results: The code 820037 is showed

Passed: [x]

### Test 1.2 - search a code (2)

Test description: Insert the code '820038' in the 'Code' field and press the button **'Search'**

Expected results: The code 820038 is showed

Passed: [X]

### Test 1.3 - search a code by description

Test description: Insert the code 'BOARD 14' in the 'Description' field and press the button 'Search'

Expected results: The code 610014 - "BOARD 14" is showed

Passed: [X]

### Test 1.4 - search a code by description with a jolly character

Test description: Insert the code '%BOARD%13' in the 'Description' field and press ENTER

Expected results: The code 610013 - "BOARD 13" is showed

Passed: [x]

### Test 1.5 - search a code with a jolly character

Test description:
- Insert the code '%6%' in the 'Code' field
- press the button 'Search'

Expected results: The codes that contains '6' are showed

Passed: [X]

### Test 1.6 - search a code and a description with a jolly character

Test description:
- Insert the code '%6%' in the 'Code' field
- insert %BOARD% in the description filed
- press the button 'Search'

Expected results: The codes that contains '6' and the description which contains BOARD are showed

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

### Test 1.11 - where used

Test description:
- Insert the code '810036' in the 'Code' field,
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Where used" command.

Expected results: The "BOMBrowser - Where used" window is showed

Passed: [X]

### Test 1.12 - where used (2)

Test description:
- Insert the code '100037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Where used" command.

Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".

Passed: [X]

### Test 1.13 - valid where used

Test description:
- Insert the code '810036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Show where used" command.

Expected results: The "BOMBrowser - Valid where used" window is showed

Passed: [X]

### Test 1.14 - valid where used (2)

Test description:
- Insert the code '100037' in the 'Code' field
- and press the button 'Search'
- press the right mouse button on the first entry
- select the "Show where used" command.

Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".

Passed: [X]

### Test 1.15 - revise/copy code

Test description:
- Insert the code '810037' in the 'Code' field,
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Revise/copy code" command.

Expected results: The "BOMBrowser: select date" dialog is showed; this contains a list of the code 810037.

Passed: [X]

### Test 1.16 - edit code

Test description:
- Insert the code '810036' in the 'Code' field
- and press the button 'Search'
- press the right mouse button on the first entry
- select the "Edit code" command.

Expected results: The "BOMBrowser - Edit code" window showed; this contains the code 810036 properties.

Passed: [X]

### Test 1.17 - diff from

Test description:
- Insert the code '810037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff from" command.

Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".

Passed: [X]

### Test 1.18 - diff from (2x)

Test description:
- Insert the code '820036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff from" command.

Expected results: The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.

Passed: [X]

### Test 1.19 - diff to

Test description:
- Insert the code '810037' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff to" command.

Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".

Passed: [X]

### Test 1.20 - diff to (2x)

Test description:
- Insert the code '820036' in the 'Code' field
- press the button 'Search'
- press the right mouse button on the first entry
- select the "Diff to" command.

Expected results: The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.

Passed: [X]

### Test 1.21 - menu->help->about

Test description: In the menu select the Help and About subcommand

Expected results: The "about" dialog is showed. The dialog contains the current version and the copyright code.

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

Expected results: in the menu are showed the four windows: BOMBrowser - Where used, BOM Browser - valid where used, BOMBrowser assembly, BOMBrowser - edit

Passed: [X]

### Test 1.23 - menu->file->close
Test description:
- insert code 820037
- press the right mouse button on the first entry and select the "Where used" command.
- Two windows are opened. Select the "File->close" in the "BOMBrowser - Codes list" window:

Expected results: The "BOMBrowser - Codes" list is closed. "BOMBrowser - Where used" is opened.

Passed: [X]

### Test 1.24 -Ctrl-Q  menu->file->close
Test description:
- insert code 820037
- press the right mouse button on the first entry and select the "Where used" command.
- Two windows are opened. Set the focus to the "BOMBrowser - Codes list"
- press CTRL-Q

Expected results: The "BOMBrowser - Codes list" is closed. "BOMBrowser - Where used" is opened.

Passed: [X]

### Test 1.25 - menu->file->exit
Test description:
- insert code 820037
- press the right mouse button on the first entry and select the "Where used" command.
- Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Codes list" window:

Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.

Test description #2:
- After the steps above,  Press No

Expected results #2: The codes list window is still opened

Test description #3:
- Repeat the step above until the dialog is showed, then press yes

Expected results #3: The application is ended. Now window is sowed

Passed: [X]


### Test 1.31 - Menu->edit->copy
Test description:
- insert code %6% and press ENTER;
- select menu->edit->copy
- Paste the clipboard in an editor

Expected results:
- check that there is the same table showed in the BOMBrowser - Codes list.
- Check that the number of row are the same +1 of the "BOMBrowser - Codes list" widow (there is the header)

Passed: [X]

### Test 1.33 - Code gui
Test description:
- insert code 8200% and press ENTER
- Select the first entry

Expected result: the information of the selected code is showed in the right panel

Test description #2:
- after the steps above, select the 2nd entry.

Expected resul #2t: the information of the 2nd selected codes are showed in the right panel

Passed: [X]


## 2 - 'Code gui' panel

### Test 2.1 - general
Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the first entry (820000)

Expected result: on the left panel there are the information of the selected code

Passed: [X]

### Test 2.2 - multiple revision
Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Select another date in the rightmost combobox

Expected result: The information on the panel are changed accordly

Passed: [X]

### Test 2.3 - multiple revision (2)
Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001)

Expected result: The right most button, contains all the dates (3)

Passed: [X]

### Test 2.4 - documents
Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)

Expected result: In the bottom part are showed two buttons with two documens

Passed: [X]

### Test 2.5 - documents (2x)
Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Select a document button

Expected result: Clicking one button document, the related document is opened

Passed: [X]

### Test 2.6 - Copy info..
Test description:
- In the "BOMBrowser - codes list" window insert code 8200%
- press ENTER
- Select the 2nd entry (820001)
- Press copy info

Expected result: Pasting the clipboard content in a editor, the relevant information are showed

Passed: [X]

### Test 2.7 - Check tool tip
Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code - gui, drawing button

Expected result:
- a tooltip appears showing file name and full path

Passed: [X]

### Test 2.8 - RMB menu of drawing button
Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Open dir"

Expected result:
- the directory containing the file is opened

Passed: [X]

### Test 2.9 - RMB menu of drawing button
Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy filename"
- paste it in an editor

Expected result:
- the filename is pasted

Passed: [X]

### Test 2.10 - RMB menu of drawing button
Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy dirname"
- paste it in an editor

Expected result:
- the dirname is pasted

Passed: [X]

### Test 2.11 - RMB menu of drawing button
Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy full path"
- paste it in an editor

Expected result:
- the full path (filename+dirname) is pasted

Passed: [X]

### Test 2.12 - RMB menu of drawing button (windows only)
Test description:
- In the "BOMBrowser - codes list" window insert code 820000
- move the mouse pointer over the Code, press the RMB
- select "Copy file"
- paste it in a folder

Expected result:
- the file is copied

Passed: [X]

## 3 - BOMBrowser - Assembly

### Test 3.1 - select date
Test description:
- insert code "820037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Check that it is a modal dialog trying to click in the "parent" window

Expected result: Nothing happens

Test description #2:
- after the step above, press the cancel button

Expected result #2:
- the dialog dsappear and the "codes list" window is showed

Test description #3:
- repeat the steps above until the "show assembly by date" dialog appears
- Select the first item
- press the "Select" button.

Expected result #3:
- The "BOMBrowser - Assembly" window appears
- Check that the date in the window title is the same that you selected

Passed: [X]

### Test 3.4 - show assembly
Test description:
- insert code "810037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.

Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not an assembly".

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

Expected result: A new "Select date" window is showed.

Passed: [X]

### Test 3.8 - where used (2)
- insert code "100000" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item, and press the "Select button". The Assembly window
  appears
- Select a code below the top one(100000); then RMB and then execute "Where used"

Expected result: a where used window appears

Passed: [X]

### Test 3.10 - valid where used (2)
- insert code "100000" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly by date" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item, and press the "Select button". The Assembly window
  appears
- Select a code below the top one(100000); then RMB and then execute
  "Valid where used"

Expected result: a where used window appears

Passed: [X]

### Test 3.11- menu->help->about

Test description: In the menu select the Help and About subcommand

Expected results: The "about" dialog is showed. The dialog contains the current version and the copyright code.

Passed: [X]

### Test 3.12 - menu->window

Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.

Two windows are opened. Select the "Windows menu" in the "BOMBrowser - Assembly" window:

Expected results: in the menu are showed the two windows: "BOMBrowser - Assembly", "BOM Browser - Codes list".

Passed: [X]

### Test 3.13 - menu->file->close
Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Two windows are opened. Select the "File->Close" in the "BOMBrowser - Assembly" window:

Expected results: The "BOMBrowser - Assembly" list is closed. "BOMBrowser - Codes list" is opened.

Passed: [X]

### Test 3.14 -Ctrl-Q  menu->file->close
Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- two windows are opened. Set the focus to the "BOMBrowser - Assembly", then press CTRL-Q

Expected results: The "BOMBrowser - Assembly" is closed. "BOMBrowser - Codes list" is opened.

Passed: [X]

### Test 3.15 - menu->file->exit
Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Assembly" window:

Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.

Test description #2:
- After the steops above,  Press No

Expected results #2: the assembly windows is NOT closed

Test description #3:
- After the steops above,  Select the "File->Exit" in the "BOMBrowser - Assembly" window:
- a dialog BOMBrowser asking about the possibility to exit is showed. Press yes

Expected results #3: The application is ended. No window is showed


Passed: [X]


### Test 3.18 - menu->file->exit
Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Two windows are opened. Press CTRL-X

Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.

Test description #2:
- After the steops above,  Press No

Expected results #2: the assembly windows is NOT closed

Test description #3:
- Press CTRL-X again
- a dialog BOMBrowser asking about the possibility to exit is showed. Press yes

Expected results #3: The application is ended. No window is showed

Passed: [X]

### Test 3.21 - menu->file->export as json
Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Select File->export as json
- Save the file and reopen it in a editor

Expected results: The file is in a JSON format

Test description #2
- Select File->export as csv
- Save the file and reopen it in a editor

Expected results #2:
- The file is in a CVS (tab separated fields) format

Passed: [X]


### Test 3.23 - menu->view->show up level 1
Test description:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- Select View->show up level 1

Expected results: The bom is collapsed to showing only the first level (top code and its children)

Test description #2:
- Select View->show up level 2

Expected results #2: The bom is collapsed to showing only the two levels (top code and its children, and their children)

Test description #3:
- Select View->show all level

Expected results #3: The bom is showing all levels

Test description #4:
- Press CTRL-1

Expected results #4: The bom is collapsed to showing only the first level (top code and its children)

Test description #5:
- Press CTRL-2

Expected results #5: The bom is collapsed to showing only the two levels (top code and its children, and their children)

Test description 65:
- Press CTRL-A

Expected results #7: The bom is showing all levels

Passed: [X]


### Test Set 3.29 - find

Prepratory steps:
- insert code 820037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry
- select the "Show assembly" command
- select the first date doubleckicking on it.
- the BOMBrowser Assembly window is showed

#### Test 3.29.1 - find
Test description: press CTRL-F

Expected results: The find dialog is showed

Passed: [X]

#### Test 3.29.2 - find
Test description: Select Search->Find

Expected results: The find dialog is showed

Passed: [X]

#### Test 3.29.3 - cancel
Test description:
- Select Search->Find
- The find dialog is showed
- Press "Close" button

Expected results: The find dialog is closed

Passed: [X]

#### Test 3.29.4 - find a code
Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" 3 times

Expected results: A different instance of the code 810003 is showed each time

Test description #2:
- Press "prev" 2 times

Expected results #2: A different instance of the code 810003 is showed each time

Passed: [X]


#### Test 3.29.6 - find a code
Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" 3 times
- Press "prev" 3 times

Expected results: After thelast action a dialog "Data not found" is showed

Passed: [X]

#### Test 3.29.7 - find a code

Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" going below the bom until a dialog "Data not found" is showed

Expected results: After the last action a dialog "Data not found" is showed

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

Passed: [X]

### Test 3.31 - show latest assembly

Test description:
- in "Code list" window, select the code 100017
- select the code
- look at right panel codegui. Check that the "Date to" is **not** blank
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

### Test 3.32.2 - Menu file -> copy files

Test description:
- open as "latest assembly" in Assembly window the code 820000
- Select File, then "Copy files"
- A "Save to" dialog appear, select Cancel

Expected results:
- Nothing

Passed: [X]

### Test 3.32.2 - Menu file -> copy files

Test description:
- open as "latest assembly" in Assembly window the code 820000
- Select File, then "Copy files"
- A "Save to" dialog appear, select a directory
- Pressa save/open/select

Expected results:
- In the selected folder, the assemblies files are copied

Passed: [X]

### Test 3.33 - Show prototype assembly

Preparatpry step:
- look at the code 610004 in the codes list window
- Check in the code gui right panel, that the code has two date and that it is not a prototype

#### Test 3.33.1 - Show prototype assembly
Test description:
- look at the code 610004 in the codes list window
- From the RMB menu, select "Show prototype assembly"

Expected results:
- the assembly window is showed
- looking at the dates of the "code gui" right panel, for some code the "prototype" date from is showed

Passed: [X]

#### Test 3.33.2 - Show prototype assembly
Test description:
- look at the code 610004 in the codes list window
- From the RMB menu, select "Show latest assembly"

Expected results:
- the assembly window is showed
- looking at the dates of the "code gui" right panel, for any code the "prototype" date from is showed: i.e. all code are not prototype

Passed: [X]

## 4 - BOMBrowser - Valid where used

### Test 4.1

Test description: in the "Codes list" window search for the code 820017. Then select  the right click menu command "Valid where used"

Expected result: the "valid where used" window is showed

Passed: [X]

## 5 - BOMBrowser - Where used

### Test 5.1

Test description: in the "Codes list" window search for the code 820017. Then select  the right click menu command "Where used"

Expected result: the where used window is showed

Passed: [X]

## 6 - BOMBrowser - Select date

This test is covered by the ones of the Assembly window

## 7 - BOMBrowser - Diff window

TBD

## 8 - BOMBrowser - Copy/revise code

### Test 8.1 - date dialog
Test description
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Revise/copy code..." command

Expected results: A "BOM Browser select date dialog" appears

Test description #2:
- after the step above, press cancel

Expected results #2:
- the dialog disappears

Test description #3:
- repeat the steps above until the appearing of the dialog
- press select

Expected results #3: The Revise/copy windows appears

Passed: [X]


### Test 8.3 - date dialog
Test description
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the first entry

Expected results: The Revise/copy windows appears

Passed: [X]

### Test 8.4 - Revise/copy code window
Test description
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Revise/copy windows appears

Expected results: the "old-Iter" are the same as the one selected in the "Select date" window

Passed: [X]

### Test 8.5 - Revise/copy code window
Test description
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the *second* entry
- The Revise/copy windows appears

Expected results: the "Iter" are the same as the one selected in the "Select date" window

Passed: [X]

### Test set 8.6 - Revise/copy code window

Prepratory steps:
- insert code 820040 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Revise/copy windows appears

#### Test 8.6.1 - Cancel
Test description: press Cancel button

Expected results: an exit confirmation dialog will appears

Test description #2:
- after the steps above, press no

Expected results #2: the "Revise/copy windows" is closed

Test description #3:
- repeat the steps above until the dialog appearance
- an exit confirmation dialog will appears; press yes

Expected results #: the dialog is closed; the "Revise/copy windows" is opened

Passed: [X]


#### Test 8.6.4 - *Revise*/copy code window
Check the editability of the following fields: New/Code, New/Iter, New/Description, New/Rev, New/Date from

Expected results: only New/Description, New/date from and New/rev are editable

Passed: [X]

#### Test 8.6.5 - Revise/copy code window
Test description: check the field New/Iter

Expected results: The field New/Iter is Old/Iter + 1

Passed: [X]

#### Test 8.6.6 - Revise/copy code window
Test description:
- check the copy checkbox
- check the editability of the following fields: New/Code, New/Iter, New/Description, New/Rev, New/Date from

Expected results: the field New/Code, New/Description, New/Date from and New/Rev are editable

Passed: [X]

#### Test 8.6.7 - Revise/copy code window
Test description:
- check the copy checkbox
- check the field New/Iter

Expected results: The field New/Iter is 0

Passed: [X]

#### Test 8.6.8 - Copy error
Test description:
- click on the copy checkbox
- press "Copy/Revise button"

Expected results:
- An error dialog appears saying that the code already exists
- pressing OK, the Copy / Revise window still exists

Passed: [X]

#### Test 8.6.10 - Confirmation dialog / success
Test description:
- click on the copy checkbox
- change the new/code in 82004A"
- unmark the checkbox "start edit dialog after copy/revision"
- press "Copy/Revise button"
- A confirmation dialog appears; press no

Expected results: the  confirmation dialog disappear; the "BOMBrowser - copy /revise code" windows is opened.

Test description #2:
- after the steps above, pres again "Copy/Revise button"
- a confirmation dialog appears; press yes

Expected results: A successfull dialog appears

Passed: [X]

#### Test 8.6.12 - Confirmation dialog / success (2)
Test description:
- click on the copy checkbox
- change the new/code in 82004B"
- press "Copy/Revise button"
- A confirmation dialog appears; press yes

Expected results:
- The editor of the new code appears.
- There are attached document and a children list

Passed: [X]

#### Test 8.6.14 - Confirmation dialog / success (3)
Test description:
- check the copy checkbox
- change the new/code in 82004C"
- unmark the "Copy document" checkbox
- press "Copy/Revise button"
- A confirmation dialog appears; press yes

Expected results:
- The editor of the new code appears.
- There are not attached document.
- There are children list.

Passed: [X]

#### Test 8.6.15 - Revise a code / date error
Test description:
- enter an incorrect date (eg. 'xxxx')
- press "Copy/Revise button"

Expected results:
- An error dialog appears saying that the date format is incorrect
- pressing OK, the Copy / Revise window still exists

Passed: [X]

#### Test 8.6.16 - Revise a code / date error
Test description:
- enter an date eqal to the Old/Date from
- press "Copy/Revise button"
- A confirmation dialog appears; press yes

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
- press "Copy/Revise button"
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
- press "Copy/Revise button"
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- There are attached document.
- There are children list.
- The "From date" in the revision list combobox is equal to the one of the previous dialog
- The "Description" in the editor window is equal to the one of the previous dialog
- The "Rev" in the editor window is equal to the one of the previous dialog

Passed: [X]

### Test 8.9 - copy a code (in proto mode)
Test description:
- revise the code "820041" from the code list window
- check the "Copy" checkbox
- set the "new/code" field to a new one (i.e. it must no exist)
- check the checkbox "Prototype"
- press "Copy/Revise button"
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- The date in date selector reports only prototype
- The date in the titlebar  reports prototype

Passed: [X]

### Test 8.10 - revise a code (in proto mode)
Test description:
- revise the code "820041" from the code list window
- check the checkbox "Prototype"
- press "Copy/Revise button"
- A confirmation dialog appears; press yes

Expected results:
- The editor of the code appears.
- The date in date selector reports  prototype
- The date in date selector reports only prototype

Passed: [X]

### Test 8.10 - revise a code (in proto mode)
Test description:
- revise the code "820004" from the code list window (the code has already a prototype revision, if not create a prototype revision)
- check the checkbox "Prototype"
- press "Copy/Revise button"
- A confirmation dialog appears; press yes

Expected results:
- a dialog error reports that a prototype already exists

Passed: [X]

## 9 - BomBrowser - Edit code

Prepratory steps:
- insert code 820001 in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears

### Test 9.1 - Edit code / Rev field

Test description:
- change the "rev" field prefixing it with "bis_"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the "rev" field is like the one changed

Passed: [X]

### Test 9.2 - Edit code / Default unit field

Test description:
- change the "Default unit" field prefixing it with "bis_"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the "Default unit" field is like the one changed

Passed: [X]

### Test 9.3 - Edit code / Description field

Test description:
- change the "Description" field prefixing it with "bis_"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the "Description" field is like the one changed

Passed: [X]

### Test 9.4 - Edit code / Generic properties field

Test description:
- repeat the test above for all the "Generic properties" fields

Expected result: the "generic property" field is like the one changed

Passed: [X]

### Test 9.5 - Edit code / Drawing list - add drawing

Test description:
- click with the RMB on the drawing list panel
- execute the command "add drawing"
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the added drawing is still present

Passed: [X]

### Test 9.6 - Edit code / Drawing list - del drawing

Test description:
- click with the RMB on the drawing list panel
- execute the command "delete drawing" on a drawing
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the removed drawing is not present

Passed: [X]

### Test 9.7 - Edit code / Drawing list - view drawing

Test description:
- click with the RMB on the drawing list panel
- execute the command "view drawing" on a drawing

Expected result: the selected drawing is showed

Passed: [X]

### Test 9.8 - Edit code / Children panel - del a child

Test description:
- click with the RMB on the children list panel
- execute the command "delete row" on a line
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the removed item is not present

Passed: [X]

### Test 9.9 - Edit code / Children panel - add a child

Test description:
- click with the RMB on the children list panel
- execute the command "insert row after" on a line
- in the new line insert an (existant) code in the "code" column
- the field "code-id" and "description" will autocomplete
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the added item is present

Passed: [X]

### Test 9.10 - Edit code / Children panel - add a child

Test description:
- click with the RMB on the children list panel
- execute the command "insert row before" on a line
- in the new line insert an (existant) code in the "code" column
- the field "code-id" and "description" will autocomplete
- press "save..." button
- press "ok"
- press "close"
- reopen the edit window on the same code as described in the "preparatory steps"

Expected result: the added item is present

Passed: [X]

### Test 9.11 - Edit code / Children panel - edit a field - non existant code

Test description:
- in the children panel, try to change a code in a row with a non existant code (like 'z')

Expected result: the cell changed is yellow

Test description #2:
- press "save"

Expected result #2: an error dialog appears ssaying that there is an error in the code

Passed: [X]


### Test 9.13 - Edit code / Children panel - edit a field - duplicate code

Test description:
- in the children panel, try to change a code in a row with a already existant code (like the previous one or the next one)
- press "save" button

Expected result: an error dialog is showed, saying that there is a duplicate code

Passed: [X]

### Test 9.14 - Edit code / Children panel - edit a field - wrong qty

Test description:
- in the children panel, try to change a qty in a row with a non number value

Expected result: the cell become yellow

Test description #2:
- press "save"

Expected result #2: an error dialog appears saying that the value is incorrect

Passed: [X]

### Test 9.16 - Edit code / Children panel - edit a field - wrong each

Test description:
- in the children panel, try to change a each in a row with a non number value

Expected result: the cell become yellow

Test description #2:
- press "save"

Expected result #2: an error dialog appears saying that the value is incorrect

Passed: [X]

### Test 9.18 - Edit code / Children panel - sorting

Test description:
- in the children panel, change the row sequence sort by code (click on the "code" column header)
- take note of the "seq" column values
- remove a row

Expected result: the seq values are reordered on the basis of the last sort

Passed: [X]

### Test 9.19 - Edit code / Children panel - sorting

Test description:
- in the children panel, change the row sequence sort by code (click on the "code" column header)
- take note of the "seq" column values
- do an "insert row before"

Expected result: the seq values are reordered on the basis of the last sort

Passed: [X]

### Test 9.20 - Edit code / Children panel - sorting

Test description:
- in the children panel, change the row sequence sort by code (click on the "code" column header)
- take note of the "seq" column values
- do an "insert row after"

Expected result: the seq values are reordered on the basis of the last sort

Passed: [X]

### Test 9.21 - Edit code / File -> close

Test description:
- select the menu File->close

Expected result: the edit window is closed

Passed: [ ]

### Test 9.22 - Edit code / File -> exit

Test description:
- select the menu File->exit

Expected result: a dialog is opened asking if you want to exit from application

Test description #2:
- press no

Expected result #2: the dialog is closed, the edit windows is showed

Test description #3:
- repeat the steps above and instead of pressing no press yes

Expected result #3: the application is closed, no window is opened

Passed: [X]

### Test 9.25 - Edit code / CTRL-Q

Test description:
- Press CTRL-Q

Expected result: the edit window is closed

Passed: [X]

### Test 9.27 - Edit code / Windows

Test description:
- select the menu Windows menu

Expected result: the opened windows are showed

Passed: [X]

### Test 9.28 - Edit code / Help->about

Test description:
- select the menu Help->about menu

Expected result: the about dialog is showed

Passed: [X]


### Test 9.29 - Edit code / Children panel - search code

Test description:
- click with the RMB on the children list panel
- execute the command "search code" on a line

Expected result: The "BOMBrowser - Search code" dialog appears

Passed: [X]

### Test 9.30 - Edit code / Children panel - search code

Test description:
- click with the RMB on the children list panel
- execute the command "search code" on a line
- The "BOMBrowser - Search code" dialog appears
- search for a code in the dialog (e.g 810001)
- select the first result
- press OK

Expected result: the dialog is closed and the new code replaces the old one

Passed: [X]

### Test 9.31 - Edit code / Children panel - search code

Test description:
- click with the RMB on the children list panel
- execute the command "search code" on a line
- The "BOMBrowser - Search code" dialog appears
- press Cancel

Expected result: the dialog is closed

Passed: [X]

### Test 9.32 - Edit code - delete revision

Test description:
- From menu -> edit, select delete revision

Expected result: a confirmation dialog is showed

Passed: [X]

### Test 9.33 - Edit code - delete revision

Test description:
- From menu -> edit, select delete revision
- a confirmation dialog is showed, press no

Expected result: not happened

Passed: [X]

### Test 9.34 - Edit code - delete revision

Test description:
- From menu -> edit, select delete revision
- a confirmation dialog is showed, press yes

Expected result:
- a comfirmation dialog is showed, saying that the revision is deleted. Press ok.
- the previous selected revision is removed

Passed: [X]

### Test 9.35 - Edit code - delete revision

Test description:
- From menu -> edit, select delete revision
- repeat the step above untile only one revision is present
- From menu -> edit, select delete revision (again)

Expected result: an error dialog box is showed saying that it is not possible to delete the last revision

Passed: [X]

### Test 9.36 - Edit code - delete revision

Test description:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- take this copy, and revise it 3 times (changing the from date to avoid conflicts)
- Edit this code
- Enter in the edit dates window, and insert a valid "end to" date in the first row. Then save the results
- From the edit window, delete the first revision
- Delete the last revision

Expected result: after any delete, the initial "from date" and the final "to date" are the same

Passed: [X]

### Test 9.37 - Edit code - delete code

Test description:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- Edit this code
- From the menu->edit select "delete code"

Expected result: a confirmation dialog appears

Passed: [X]

### Test 9.38 - Edit code - delete code

Test description:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- Edit this code
- From the menu->edit select "delete code"
- a confirmation dialog appears, press no

Expected result: nothing happened

Passed: [X]

### Test 9.39 - Edit code - delete code

Test description:
- Take a code from the code list gui, copy it (to avoid problem about the parent dates)
- Edit this code
- From the menu->edit select "delete code"
- a confirmation dialog appears, press yes

Expected result:
- a confirmation dialog appears, press ok
- the edit dialog is not showed anymore

Passed: [X]

### Test 9.40 - Edit code - change revision

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- Acting to the "From/to date" QComboBox, change the revision of the code
- in parallel make one change in a field for each revision (insert the from date to help the test) and press Save
- repeat the step above for each revision
- Acting to the "From/to date" QComboBox, change the revision of the code

Expected result:
- The dialog show for each revision the change performed in the step above

Passed: [X]

### Test 9.41 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- make one change in a field - Acting to the "From/to date" QComboBox, change the revision of the code

Expected result:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### Test 9.42 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- make one change in a field - Acting to the "From/to date" QComboBox, change the revision of the code
- An error dialog is showed  saying that the change are not saved, press no

Expected result:
- the revision is not changed

Passed: [X]

### Test 9.42 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- make one change in a field
- Acting to the "From/to date" QComboBox, change the revision of the code
- An error dialog is showed  saying that the change are not saved, press yes

Expected result:
- go back to the previous revision
- check that the change was not saved

Passed: [X]

### Test 9.43 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- make one change in a field
- press Close

Expected result #1:
- An error dialog is showed saying that the change are not saved

Test description #2:
- Press no

Expected result #2:
- The previous window is showed. the change is not lost

Test description #3:
- repeat the test until the dialog is showed
- Press yes

Expected result #3:
- The edit window is closed

Passed: [X]

### Test 9.43 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- remove an item in the children section
- press close button

Expected result:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### Test 9.44 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- insert (before) item in the children section
- press close button

Expected result:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### Test 9.45 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- insert (after) item in the children section
- press close button

Expected result:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### Test 9.46 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- do a "search code" over an item in the children section
- press close button

Expected result:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### Test 9.47 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- do an "add drawing" in the drawings section
- press close button

Expected result:
- An error dialog is showed  saying that the change are not saved

Passed: [X]

### Test 9.48 - Edit code - change revision without saving

Test description:
- Take a code from the code list gui with multiple revision
- Edit this code
- do an "delete drawing" in the drawings section
- press close button

Expected result:
- An error dialog is showed  saying that the change are not saved

Passed: [X]


## 10 - BomBrowser - Edit date

Prepratory steps:
- insert code 820017 (or any other code with more revisions) in the "BOMBrowser codes list" window
- press search
- press the right mouse button on the first entry and select "Edit code..." command
- The Edit code windows appears
- Select the "..." button near the "to date" field
- An edit dates dialog is showed

### Test 10.1

Test description: press the cancel button

Expected result: the edit dates dialog is closed

Passed: [X]

### Test 10.2

Test description: press the save button

Expected result: a confirmation dialog is showed

Test description #2:
- press ok

Expected result #2: the edit dates dialog is closed

Passed: [X]

### Test 10.4

Test description:
- use the procedure described in the "preparatory steps" using the code 810036 instead of the code 820017.
- change the "date from" of the bottom row with a valid one (but lower than the row above)
- press save
- reopen the edit dates dialog

Expected result: the new date is showed in the last row

Passed: [X]

### Test 10.5

Test description:
- change the "date from" of the first row with a valid one (but higher than the row below)

Expected result: the date in the row below and column "To date" is changed accordling (a day before)

Passed: [ ]

### Test 10.6

Test description:
- change the "date from" of the first row with a not valid one (i.e. 'z')

Expected result: the cell become yellow

Test description #2
- press save

Expected result #2: an error dialog is showed

Passed: [X]


### Test 10.8

Test description:
- change the "date from" of the first row with a not valid one (i.e. 'z')
- the cell become yellow; press cancel
- the edit dates dialog is closed, reopen it

Expected result: the valid old date appear

Passed: [X]

### Test 10.9

Test description:
- change the "date from" of the first row with a not valid one (i.e. 2001-02-30)

Expected result: the cell become yellow

Passed: [ ]

### Test 10.10

Test description:
- change the "date from" of the first row with a a date before the row below

Expected result: the cell become yellow

Passed: [X]

### Test 10.11

Test description: check that all fields are read only with the exception of
- the column From date
- the Cell of the first row and column "To date"

Expected result: only the cells listed above are read write

Passed: [X]

### Test 10.12

Test description:
- change the value of the cell of the first row and column "To date" with an
  invalid one (i.e. 'z')

Expected result: the cell become yellow

Test description #2:
press save

Expected result #2: an error dialog appear

Passed: [X]

### Test 10.14

Test description:
- change the value of the cell of the first row and column "To date" with a date before of the left cell

Expected result: the cell become yellow

Passed: [X]

### Test 10.15

Test description:
- use the procedure described in the "preparatory steps" using the code 100036 instead of the code 820017.
- change the value of the cell of the first row and column "To date" with a valid one
- press the save button
- reopen the Edit dates" dialog

Expected result: the new date appears

Passed: [X]

### Test 10.16 - conflict date

Preparatory steps:
- create a component code (copying from an existing component); name it as COMP-A; set a Date from 2020-01-01.
- Create a component code (copying from an existing component); name it as COMP-B; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Create a component code (copying from an existing component); name it as ASS-A; set a Date from 2020-01-01. Set "Date to" 2021-01-01
- Edit the code "ASS-A" adding as child the coponents COMP-A and COMP-B.

### Test 10.16.1 - parent too early

Test description:
- enter in the edit dialog of code ASS-A
- enter in the edit date dialog
- change the "From date" to 2019-01-01
- press "Save button"

Expected result: an error dialog appears saying that the date range is wider than the children one

Passed: [X]

### Test 10.16.2 - parent too late

Test description:
- enter in the edit dialog of code ASS-A
- enter in the edit date dialog
- change the "To date" to 2022-01-01
- press "Save button"

Expected result: an error dialog appears saying that the date range is wider than the children one

Passed: [X]

### Test 10.16.3 - children too late

Test description:
- enter in the edit dialog of code COMP-B
- enter in the edit date dialog
- change the "From date" to 2020-06-01
- press "Save button"

Expected result: an error dialog appears saying that the date range is shorter than the parent one

Passed: [X]

### Test 10.16.4 - children too early

Test description:
- enter in the edit dialog of code ASS-A
- enter in the edit date dialog
- change the "To date" to 2020-06-01
- press "Save button"
- enter in the edit dialog of code COMP-B
- enter in the edit date dialog
- change the "To date" to 2020-03-01
- press "Save button"

Expected result: an error dialog appears saying that the date range is shorter than the parent one

Passed: [X]

### Test 10.16.5 - children too early

Test description:
- enter in the edit dialog of code ASS-A
- remove the child COMP-B
- press "Save" and the "Cancel"
- enter in the edit dialog of code COMP-B
- enter in the edit date dialog
- change the "To date" to 2020-03-01
- enter in the edit dialog of code ASS-A
- add as child COMP-B

Expected result: an error dialog appears saying that the child date range is shorter than the parent one

Passed: [X]

### Test 10.17 - prototype date

Test description:
- enter in the edit dialog of code with several revisions without prototype
- enter in the "edit dates" dialog
- change the first (from the top) "From date" to "prototype"

Expected result:
- no error (yellow cell) is showed
- **ALL** the cell in the "To date" column are R/O
- the date "End to" of the 1st and 2nd line are blanked

Test description #2:
- after the above test, press save and ok until you reach the "Edit dialog"
- check that the "From/to date" "Revision selector" lists all the dates

Expected result #2:
- the "From/to date" "Revision selector" lists all the dates and prototype

Test description #3:
- after the steps above
- press the "..." button and go in the "edit dates" dialog
- change the "From date" in the first row from "PROTOTYPE" to a date grather than the 2nd line

Expected result #3:
- no error (yellow cell) is showed
- the "End to" cell in the second line show a valid date
- the "End to" cell in the 1st line is editable

Test description #4:
- after the steps above
- press save and go in the edit window
- check that the "From/to date" "Revision selector" lists all the dates

Expected result #4:
- the "From/to date" "Revision selector" lists all the dates w/o prototype

Passed: [X]

### Test 10.17 - prototype date

Test description:
- enter in the edit dialog of code with several revisions
- select a 2nd revision in the "From/to date" selector
- press the "..." button and go in the edit dialog
- change the 2nd row "From date" with a reasonable value
- press "Save", then "OK"

Expected result:
- the "From/to date" is changed accordling to the steps above
- the date showed in the title bar is changed accordling to the steps above

Passed: [X]

## 11 - Generic test

### Test 11.1

Test description: rename bombrowser.ini as bombrowser.ini.no

Expected result: at start up time, an error dialog is showed saying that the confuguration cannot be load: bombrowser.ini file may be missing

Passed: [X]

### Test 11.2

Test description: shutdown the sql server

Expected result: at start up time, an error dialog is showed saying that it is imposible to access to the server

Passed: [ ]

### Test 11.3 - Config test

TBD: test the configuration:
- force_*_uppercase
- template
- the overriding of the configuration store in the server

# RESULTS:
2020-03-23 v0.4.1
Failed tests list: 0
