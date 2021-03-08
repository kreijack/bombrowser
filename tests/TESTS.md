

# BOMBrowser tests list

## Preface

This tests list assumes that you are working with the test database generaded
by mkdb.py.
This tests list is related to the v0.4.

## 1 - BOMBrowser - Codes list

### Test 1.1 - search a code

Test description: Insert the code '820037' in the 'Code' field and press ENTER
Expected results: The code 820037 is showed
Passed: [X]

### Test 1.2 - search a code (2)

Test description: Insert the code '820038' in the 'Code' field and press the button 'Search'
Expected results: The code 820038 is showed
Passed: [X]

### Test 1.3 - search a code by description

Test description: Insert the code 'BOARD 14' in the 'Description' field and press the button 'Search'
Expected results: The code 610014 - "BOARD 14" is showed
Passed: [X]

### Test 1.4 - search a code by description with a jolly character

Test description: Insert the code '%BOARD%13' in the 'Description' field and press ENTER
Expected results: The code 610014 - "BOARD 13" is showed
Passed: [X]

### Test 1.5 - search a code with a jolly character

Test description: Insert the code '%6%' in the 'Code' field and press the button 'Search'
Expected results: The codes that contains '6' are showed
Passed: [X]

### Test 1.6 - search a code and a description with a jolly character

Test description: Insert the code '%6%' in the 'Code' field, insert %BOARD% in the description filed and press the button 'Search'
Expected results: The codes that contains '6' and the description which contains BOARD are showed
Passed: [X]

### Test 1.7 - assembly

Test description: Insert the code '820037' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Show assembly" command.
Expected results: The "BOMBrowser: select date" dialog is showed; thsi dialog contains a list of 820037 codes.
Passed: [X]

### Test 1.9 - assembly

Test description: Insert the code '820037' in the 'Code' field,  and press the button 'Search'; ipress the right mouse button on the first entry and select the "Show assembly" command.
Expected results: The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820037 codes.
Passed: [X]

### Test 1.11 - where used

Test description: Insert the code '810036' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Show where used" command.
Expected results: The "BOMBrowser - Where used" window is showed
Passed: [X]

### Test 1.12 - where used (2)

Test description: Insert the code '100037' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Show where used" command.
Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".
Passed: [X]

### Test 1.13 - valid where used

Test description: Insert the code '810036' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Show where used" command.
Expected results: The "BOMBrowser - Valid where used" window is showed
Passed: [X]

### Test 1.14 - valid where used (2)

Test description: Insert the code '100037' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Show where used" command.
Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".
Passed: [X]

### Test 1.15 - revise/copy code

Test description: Insert the code '810037' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Revise/copy code" command.
Expected results: The "BOMBrowser: select date" dialog is showed; this contains a list of the code 810037.
Passed: [X]

### Test 1.16 - edit code

Test description: Insert the code '810036' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Edit code" command.
Expected results: The "BOMBrowser - Edit code" window showed; this contains the code 810036 properties.
Passed: [X]

### Test 1.17 - diff from

Test description: Insert the code '810037' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Diff from" command.
Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".
Passed: [X]

### Test 1.18 - diff from (2x)

Test description: Insert the code '820036' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Diff from" command.
Expected results: The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.
Passed: [X]

### Test 1.19 - diff to

Test description: Insert the code '810037' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Diff to" command.
Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not in an assembly".
Passed: [X]

### Test 1.20 - diff to (2x)

Test description: Insert the code '820036' in the 'Code' field,  and press the button 'Search'; press the right mouse button on the first entry and select the "Diff to" command.
Expected results: The "BOMBrowser: select date" dialog is showed; this dialog contains a list of 820036 codes.
Passed: [X]

### Test 1.21 - menu->help->about

Test description: In the menu select the Help and About subcommand
Expected results: The "about" dialog is showed. The dialog contains the current version and the copyright code.
Passed: [X]

### Test 1.22 - menu->window

Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Valid where used" command.
- go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Edit code" command.

Four windows are opened. Select the "Windows menu" in the "BOMBrowser - Codes list" window:

Expected results: in the menu are showed the three windows: BOMBrowser - Where used, BOM Browser - valid where used, BOMBrowser assembly.
Passed: [X]

### Test 1.23 - menu->file->close
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Select the "File->Quit" in the "BOMBrowser - Codes list" window:
Expected results: The "BOMBrowser - Codes" list is closed. "BOMBrowser - Where used" is opened.
Passed: [X]

### Test 1.24 -Ctrl-Q  menu->file->close
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Set the focus to the "BOMBrowser - Codes list", then press CTRL-Q
Expected results: The "BOMBrowser - Codes list" is closed. "BOMBrowser - Where used" is opened.
Passed: [X]

### Test 1.25 - menu->file->exit
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Codes list" window:
Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.
Passed: [X]

### Test 1.26 - menu->file->exit (2)
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Codes list" window:
A dialog BOMBrowser asking about the possibility to exit is showed. Press No
Expected results: Two windows are opened
Passed: [X]

### Test 1.27 - menu->file->exit (3)
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Codes list" window:
A dialog BOMBrowser asking about the possibility to exit is showed. Press Yes
Expected results: The application is ended. Now window is hsowed
Passed: [X]


### Test 1.28 -Ctrl-X menu->file->exit
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Set the focus to the "BOMBrowser - Codes list", then press CTRL-X
Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.
Passed: [X]

### Test 1.29 -Ctrl-X menu->file->exit (2)
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Set the focus to the "BOMBrowser - Codes list", then press CTRL-X. a dialog BOMBrowser asking about the possibility to exit is showed. Press no.
Expected results: Two windows are opened
Passed: [X]

### Test 1.30 -Ctrl-X menu->file->exit (3)
Test description:
 - insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Set the focus to the "BOMBrowser - Codes list", then press CTRL-X. a dialog BOMBrowser asking about the possibility to exit is showed. Press yes.
Expected results: The application is ended. No window is showed
Passed: [X]

### Test 1.31 - Menu->edit->copy
Test description: insert code %6% and press ENTER;  select menu->edit->copy
Expected results: Paste the clipboard in an editr and check that there is the same table showed in the BOMBrowser - Codes list. Check that the number of row are the same +1 of the "BOMBrowser - Codes list" widow (there is the header)
Passed: [X]

### Test 1.32 - Ctrl-C (Menu->edit->copy)
Test description: insert code %6% and press ENTER;  press CTRL-C.
Expected result: Paste the clipboard in an editr and check that there is the same table showed in the BOMBrowser - Codes list. Check that the number of row are the same +1 of the "BOMBrowser - Codes list" widow (there is the header)
Passed: [X]

### Test 1.33 - Code gui
Test description: insert code 8200% and press ENTER; Select the first entry
Expected result: the information of the selected code is showed in the right panel
Passed: [X]

### Test 1.34 - Code gui (2)
Test description: insert code 8200% and press ENTER; Select the first entry; then select the 2nd entry.
Expected result: the information of the selected code is showed in the right panel
Passed: [X]


## 2 - 'Code gui'

### Test 2.1 - general
Test description: In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the first entry (820000)
Expected result: on the left panel there are the information of the selected code
Passed: [X]

### Test 2.2 - multiple revision
Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001)
- Select another date in the rightmodt combobox
Expected result: The information on the panel are changed accordly
Passed: [X]

### Test 2.3 - multiple revision (2)
Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001)
Expected result: The right most button, contains all the dates (3)
Passed: [X]

### Test 2.4 - documents
Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001)
Expected result: In the bottom part are showed two buttons with two documens
Passed: [X]

### Test 2.5 - documents (2x)
Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001)
Expected result: Clicking one button document, the related document will be opened
Passed: [X]

### Test 2.6 - Copy info..
Test description:
- In the "BOMBrowser - codes list" window insert code 8200% and press ENTER; Select the 2nd entry (820001); Press copy info
Expected result: Pasting the clipboard content in a editor, the relevant information are showed
Passed: [X]

## 3 - BOMBrowser - Assembly

### Test 3.1 - select date
Test description:
- insert code "820037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Check that it is a modal dialog trying to click in the "parent" window
Expected result: Nothing happens
Passed: [X]

### Test 3.2 - select date (2)
Test description:
- insert code "820037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Press the Cancel button
Expected result: The dialog disappear
Passed: [X]

### Test 3.3 - select date (3)
Test description:
- insert code "820037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item, the press the "Select" button.
Expected result: The "BOMBrowser - Assembly" window appears. Check that the date in the window title is the same that you selected
Passed: [X]

### Test 3.4 - show assembly
Test description:
- insert code "810037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly" command.
- Expected results: The "BOMBrowser" error dialog is showed; this dialog says "The item is not an assembly".
Passed: [X]

### Test 3.6 - show assembly (2)
Test description:
- insert code "820037" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item, and press the "Select button". The Assembly window
  appears
- Select an item with an assembly (e.g electronic board)
- then RMB click and then execute Show Assembly.
Expected result: A new "Select date" window is showed.
Passed: [X]

### Test 3.8 - where used (2)
- insert code "100000" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly" command.
- "The BOMBrowser: Select Date" dialog is showed.
- Select the first item, and press the "Select button". The Assembly window
  appears
- Select a code below the top one(100000); then RMB and then execute "Where used"
Expected result: a where used window appears
Passed: [X]

### Test 3.10 - valid where used (2)
- insert code "100000" in "BOMBrowser - Code list"
- press the right mouse button on the first entry
- select the "Show assembly" command.
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
- insert code 82037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- go back to the "BOMBrowser - code list"; press the right mouse button on the first entry and select the "Where used" command.

Two windows are opened. Select the "Windows menu" in the "BOMBrowser - Assembly" window:

Expected results: in the menu are showed the two windows: "BOMBrowser - Assembly", "BOM Browser - Codes list".
Passed: [X]

### Test 3.13 - menu->file->close
Test description:
- insert code 82037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
 - go back to the "BOMBrowser - Assembly"; press the right mouse button on the first entry and select the "Where used" command.
Two windows are opened. Select the "File->Quit" in the "BOMBrowser - Assembly" window:
Expected results: The "BOMBrowser - Assembly" list is closed. "BOMBrowser - Codes list" is opened.
Passed: [X]

### Test 3.14 -Ctrl-Q  menu->file->close
Test description:
- insert code 82037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
Two windows are opened. Set the focus to the "BOMBrowser - Assembly", then press CTRL-Q
Expected results: The "BOMBrowser - Assembly" is closed. "BOMBrowser - Codes list" is opened.
Passed: [X]

### Test 3.15 - menu->file->exit
Test description:
- insert code 82037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Assembly" window:
Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.
Passed: [X]

### Test 3.16 - menu->file->exit (2)
Test description:
- insert code 82037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Codes list" window:
A dialog BOMBrowser asking about the possibility to exit is showed. Press No
Expected results: Two windows are opened
Passed: [X]

### Test 3.17 - menu->file->exit (3)
Test description:
- insert code 82037 in "BOMBrowser - Codes list"
- press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
Two windows are opened. Select the "File->Exit" in the "BOMBrowser - Assembly" window:
Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.
- Press Yes
Expected results: The application is ended. No window is showed
Passed: [X]

### Test 3.18 - menu->file->exit
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
Two windows are opened. Press CTRL-X
Expected results: a dialog BOMBrowser asking about the possibility to exit is showed.
Passed: [X]

### Test 3.19 - menu->file->exit (2)
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Two windows are opened. Press CTRL-X
A dialog BOMBrowser asking about the possibility to exit is showed. Press No
Expected results: Two windows are opened
Passed: [X]

### Test 3.20 - menu->file->exit (3)
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Two windows are opened. Press CTRL-X
A dialog BOMBrowser asking about the possibility to exit is showed. Press Yes
Expected results: The application is ended. No window is showed
Passed: [X]


### Test 3.21 - menu->file->export as json
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Select File->export as json
- Save the file and reopen it in a editor
Expected results: The file is in a JSON format
Passed: [X]

### Test 3.22 - menu->file->export as CVS
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Select File->export as json
- Save the file and reopen it in a editor
Expected results: The file is in a CVS (tab separated fields) format
Passed: [X]

### Test 3.23 - menu->view->show up level 1
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Select View->show up level 1
Expected results: The bom is collapsed to showing only the first level (top code and its children)
Passed: [X]

### Test 3.24 - menu->view->show up level 2
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Select View->show up level 2
Expected results: The bom is collapsed to showing only the two levels (top code and its children, and their children)
Passed: [X]

### Test 3.25 - menu->view->show all levels
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Select View->show up level 2
Expected results: The bom is showing all levels
Passed: [X]

### Test 3.26 - menu->view->show up level 1 (ctrl-1)
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Press CTRL-1
Expected results: The bom is collapsed to showing only the first level (top code and its children)
Passed: [X]

### Test 3.27 - menu->view->show up level 2 (ctrl-2)
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Press CTRL-2
Expected results: The bom is collapsed to showing only the two levels (top code and its children, and their children)
Passed: [X]

### Test 3.28 - menu->view->show all levels (CTRL-A)
Test description:
- insert code 82037;  press the right mouse button on the first entry and select the "Show assembly" command; select the first date doubleckicking on it.
- Press CTRL-A
Expected results: The bom is showing all levels
Passed: [X]

### Test Set 3.29 - find

Prepratory steps:
- insert code 82037 in the BOMBrowser codes list window
- press the right mouse button on the first entry and select the "Show assembly" command
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
- Press "cancel" button
Expected results: The find dialog is closed
Passed: [X]

#### Test 3.29.4 - find a code
Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" 3 times
Expected results: A different instance of the code 810003 is showed each time
Passed: [X]


#### Test 3.29.5 - find a code
Test description:
- Select Search->Find
- The find dialog is showed
- Insert the code '810003'
- Press "next" 3 times
- Press "prev" 2 times
Expected results: A different instance of the code 810003 is showed each time
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
Expected results: After thelast action a dialog "Data not found" is showed
Passed: [X]

## 4 - BOMBrowser - Valid where used

## 5 - BOMBrowser - Where used

## 6 - BOMBrowser - Select date

## 7 - BOMBrowser - Diff window

## 8 - BOMBrowser - Copy/revise code

### Test 8.1 - date dialog
Test description
- insert code 82040 in the "BOMBrowser codes list" window, then press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
Expected results: A "BOM Browser select date dialog" appears
Passed: [X]

### Test 8.2 - date dialog
Test description
- insert code 82040 in the "BOMBrowser codes list" window, then press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; press cancel
Expected results: The dialog disappears
Passed: [X]

### Test 8.3 - date dialog
Test description
- insert code 82040 in the "BOMBrowser codes list" window, then press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; press select
Expected results: The Revise/copy windows appears
Passed: [X]

### Test 8.4 - date dialog
Test description
- insert code 82040 in the "BOMBrowser codes list" window, then press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the first entry
Expected results: The Revise/copy windows appears
Passed: [X]

### Test 8.5 - Revise/copy code window
Test description
- insert code 82040 in the "BOMBrowser codes list" window, then press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Revise/copy windows appears
Expected results: the "Iter" are the same as the one selected in the "Select date" window
Passed: [X]

### Test 8.6 - Revise/copy code window
Test description
- insert code 82040 in the "BOMBrowser codes list" window, then press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the *second* entry
- The Revise/copy windows appears
Expected results: the "Iter" are the same as the one selected in the "Select date" window
Passed: [X]

### Test set 8.6 - Revise/copy code window

Prepratory steps:
- insert code 82040 in the "BOMBrowser codes list" window, then press search
- press the right mouse button on the first entry and select "Revise/copy code..." command
- A "BOM Browser select date dialog" appears; double click on the *first* entry
- The Revise/copy windows appears

#### Test 8.6.1 - Cancel

Test description: press Cancel button
Expected results: an exit confirmation dialog will appears
Passed: [X]

#### Test 8.6.2 - Cancel (2)
Test description:
- press Cancel button
- an exit confirmation dialog will appears; press yes
Expected results: the "Revise/copy windows" is closed
Passed: [X]

#### Test 8.6.3 - Cancel (3)
Test description:
- press Cancel button
- an exit confirmation dialog will appears; press yes
Expected results: the dialog is closed; the "Revise/copy windows" is opened
Passed: [X]

#### Test 8.6.4 - Revise/copy code window
Test description: check the editability of the following fields: New/Code, New/Iter, New/Description
Expected results: only New/Description is editable
Passed: [X]

#### Test 8.6.5 - Revise/copy code window
Test description: check the field New/Iter
Expected results: The field New/Iter is Old/Iter + 1
Passed: [X]

#### Test 8.6.6 - Revise/copy code window
Test description:
- click on the copy checkbox
- check the editability of the following fields: New/Code, New/Iter, New/Description
Expected results: the field New/Code New/Description are editable
Passed: [X]

#### Test 8.6.7 - Revise/copy code window
Test description:
- click on the copy checkbox
- check the field New/Iter
Expected results: The field New/Iter is 0
Passed: [X]

#### Test 8.6.8 - Copy error
Test description:
- click on the copy checkbox
- press "Copy/Revise button"
Expected results: A confirmation dialog appears
Passed: [X]

#### Test 8.6.9 - Confirmation dialog
Test description:
- click on the copy checkbox
- press "Copy/Revise button"
- A confirmation dialog appears; press no
Expected results: The confirmation dialog disappears
Passed: [X]

#### Test 8.6.10 - Confirmation dialog / error
Test description:
- click on the copy checkbox
- press "Copy/Revise button"
- A confirmation dialog appears; press yes
Expected results: An error dialog appears saying that the code already exists
Passed: [X]



## 9 - BomBrowser - Edit code

## 10 - BomBrowser - Edit date


# RESULTS:
2020-03-07 v0.4.0b1
Failed tests list
