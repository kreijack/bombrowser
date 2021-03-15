# TODO LIST:

## UI

- [ ] add move children rows in the edit dialogs
- [ ] add refresh in asm
- [ ] show every where rid
- [ ] in edit code add open assy

## GENERAL

- [ ] refresh the properties
- [ ] todiscuss: add the concept of "prototype" bom/code
- [ ] advance search (in all fields)
- [ ] normalize/standardize the unit (now are a free text)
- [ ] gval: create a listbox menu
- [ ] In the AssemblyWindow track the date and use it in the next Show Assembly
- [ ] Implement an extern module to customize some function:
  - code validator
  - revise validator
- [ ] add a README
- [ ] check for loop when iterating a bom (e.g. exporter)
- [ ] refactor the codegui in order to minimize the use of db

## Database

- [ ] add a DB.get_last_code_by_code_id function which is more clear
- [ ] remake the db tests (partially done)
- [ ] Ensure that during revise the latest rev_id is not changed
- [ ] Ensure that during dates update latest rev_id is not changed, and the date are always the same
- [ ] add test for updating function

## BUGS

- [ ] BUG: investigating the reason why in the edit dialog, children table the first column lost the 'italic' after an insert row
- [ ] make an handler in db.py for showing a error dialog for incorrect SQL
- [ ] rename get_drawings_by_code_id -> get_drawings_by_code_rid
- [ ] If the dates are changed, then the codegui in "codes list" window may be confused

## TESTS

- [ ] add test for template
- [ ] add test for assembly latest

# DONE

2021/03/14
- [X] handle the case where the bombrowser.ini file is missing
- [X] replace QMainWindow with BBMainWindow to better handle the windows list/closure

2021/03/12
- [X] open some window by command line (bombrowser -openassy *code/date*)

2021/03/11
- [X] Implement a modular export format
