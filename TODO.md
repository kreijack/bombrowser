
- handle the case where the bombrowser.ini file is missing
- make an handler in db.py for showing a error dialog for incorrect SQL
- refresh the properties
- open some window by command line (bombrowser -openassy <code>/<date>)

- todiscuss: add the concept of "prototype" bom/code

- remake the db tests

- rename get_drawings_by_code_id -> get_drawings_by_code_rid
- show every where rid

- BUG: investigating the reason why in the edit dialog, children table
  the first column lost the 'italic' after an insert row
- add a DB.get_last_code_by_code_id function which is more clear
- in edit code add open assy

- advance search (in all fields)
- normalize/standardize the unit (now are a free text)
- replace QMainWindow with BBMainWindow to better handle the windows list/closure

- In the AssemblyWindow track the date and use it in the next Show Assembly

- Implement an extern module to customize some function:
  - code validator
  - revise validator
  - export format
  - repo format (?)

- Ensure that during revise the latest rev_id is not changed
- Ensure that during dates update latest rev_id is not changed,
  and the date are always the same

- add a README

- add move children rows in the edit dialogs

- add refresh in asm

- check for loop when iterating a bom (e.g. exporter)

- add test for template
- add test fro assembly latest