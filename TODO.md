# TODO LIST:

## UI

- [ ] add move children rows in the edit dialogs
- [ ] show every where rid
- [ ] in edit code add open assy

## GENERAL

- [ ] refresh the properties
- [ ] normalize/standardize the unit (now are a free text)
- [ ] In the AssemblyWindow record the date and use it in the next Show Assembly
- [ ] Implement an extern module to customize some function:
  - code validator
  - revise validator
- [ ] check for loop when iterating a bom (e.g. exporter)
- [ ] add import from external source (cad, excel...) [partially]
- [ ] for each command in code list window and in assembly window check that the code exists and it is not an artifact of a deleted one
- [ ] add an exception handler for each database update [partially]
- [ ] in the "edit dialog", handle the case when the dates are changed by another user returning from "edit dates dialog"

## Database

- [ ] add a DB.get_last_code_by_code_id function which is more clear
- [ ] Ensure that during revise the latest rev_id is not changed
- [ ] Ensure that during dates update latest rev_id is not changed, and the date are always the same
- [ ] add test for updating function

## BUGS

- [ ] BUG: investigating the reason why in the edit dialog, children table the first column lost the 'italic' after an insert row
- [ ] make an handler in db.py for showing a error dialog for incorrect SQL
- [ ] rename get_drawings_by_code_id -> get_drawings_by_code_rid
- [ ] If the dates are changed, then the codegui in "codes list" window may be confused
- [ ] in the "Edit dates" dialog, when a prototype is enterd (or removed), change the iter accordling

## TESTS

- [ ] add test for template
- [ ] add test for assembly latest

# DONE

2021/03/21
- [ ] add refresh in asm

2021/03/29:
- [X] remake the db tests

2021/03/27:
- [X] gval: create a listbox menu

2021/03/26:
- [X] advance search (in all fields)

2021/03/25:
- [X] "select date dialog" -> swap the buttons "select" and "cancel"

2021/03/20
- [X] todiscuss: add the concept of "prototype" bom/code
- [X] add a README
- [X] refactor the codegui in order to minimize the use of db

2021/03/14
- [X] handle the case where the bombrowser.ini file is missing
- [X] replace QMainWindow with BBMainWindow to better handle the windows list/closure

2021/03/12
- [X] open some window by command line (bombrowser -openassy *code/date*)

2021/03/11
- [X] Implement a modular export format
