"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021,2022,2023 Goffredo Baroncelli <kreijack@inwind.it>

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

def database_password(pwd):
    return pwd

def get_edit_window_importer_list():
    """
        it should return a list of a pair (menuname, function)
    """
    return []

def get_bom_checker_list():
    """
        return a list of methods that check a pair (rootnode, bom)
    """
    return []

def get_asm_tool_menu_list():
    """
        return a list of pairs (menuname, function(root, data)) to show
        in the asmgui window (asm mode)
    """
    return []

# ----

try:
    import customize_ext
    found = True
except ImportError:
    found = False

if found:
    import customize_ext

    if hasattr(customize_ext, 'database_password'):
        database_password = customize_ext.database_password

    if hasattr(customize_ext, 'get_edit_window_importer_list'):
        get_edit_window_importer_list = customize_ext.get_edit_window_importer_list

    if hasattr(customize_ext, 'get_bom_checker_list'):
        get_bom_checker_list = customize_ext.get_bom_checker_list

    if hasattr(customize_ext, 'get_bom_checker_list'):
        get_bom_checker_list = customize_ext.get_bom_checker_list

    if hasattr(customize_ext, 'get_asm_tool_menu_list'):
        get_asm_tool_menu_list = customize_ext.get_asm_tool_menu_list
