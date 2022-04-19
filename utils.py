"""
BOM Browser - tool to browse a bom
Copyright (C) 2020,2021 Goffredo Baroncelli <kreijack@inwind.it>

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

import sys, traceback

from PySide2.QtWidgets import QMessageBox

from version import version

def __show_exception(exc_type, exc_value, exc_traceback,
        title, msg):

    if hasattr(exc_value, "_orig_traceback"):
        msg = "Query:\n"
        msg += exc_value._orig_query + "\n"
        msg += "-" * 30 + "\n"
        msg += "Exception:\n%r\n"%(exc_value)
        msg += "-" * 30 + "\n"
        msg += "Traceback:\n%s\n"%(exc_value._orig_traceback)
    else:
        excs = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                    '{0}: {1}'.format(exc_type.__name__, exc_value)])
        msg = msg + "\n" + "-" * 30 + "\n" + excs + "\n" + "-" * 30 + "\n"

    QMessageBox.critical(None, title, msg)

def _show_exception(exc_type, exc_value, exc_traceback):
    __show_exception(exc_type, exc_value, exc_traceback,
        "BOMBrowser - %s"%(version),
        "Catch 'uncautch' exception:")

def show_exception(title = "BOMBrowser - %s"%(version),
                   msg = "BOMBrowser - got exception"):
    __show_exception(*sys.exc_info(), title, msg)

class Callable:
    def __init__(self, f, *args, **kwargs):
        self._f = f
        self._args = args
        self._kwargs = kwargs
    def __call__(self, *args, **kwargs):
        return self._f(*args, *self._args, **kwargs, **self._kwargs)

def catch_exception(f):
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            QMessageBox.critical(None, "BOMBrowser",
                "During call of function '%r' an exception occurred:"%(f) +
                "-"*30 + "\n" +
                '\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb)) +
                "-"*30 + "\n")

            print('\n'.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
            raise

    return wrapper

def split_with_escape(s, delimiter, escape_symbol='\\', quote=None):

    ret = []
    i = 0
    escape=False
    item = ""
    quoted = False

    while i < len(s):
        if escape_symbol and s[i] == escape_symbol:
            escape = True
            i += 1
            continue

        if escape:
            if s[i] == 'n':
                item += '\n'
            elif s[i] == 't':
                item += '\t'
            elif s[i] == 'b':
                item += '\b'
            elif s[i] == 'r':
                item += '\r'
            else:
                item += s[i]

            i += 1
            escape = False
            continue

        if quote and (s[i] == quote):
            quoted = not quoted
            i += 1
            continue

        if s[i] == delimiter and not quoted:
            ret.append(item)
            item = ""
            i += 1
            continue

        item += s[i]
        i += 1


    ret.append(item)

    return ret

#
#   Table of conversion
#       '\n'    '\\n'
#       '\t'    '\\t'
#       '\\'    '\\\\'
#       None    '\\None'    <- None is not a string, is None !
#
# Be aware that above are python strings so '\\' means single backslash

_escape_conversion_table = [("\\", "\\"), ("\n", "n"), ("\t", "t")]

def xescape(s):
    if s is None:
        return "\\None"

    s = str(s)
    for i, k in _escape_conversion_table:
        j = 0
        while True:
            j = s.find(i, j)
            if j < 0:
                break
            s = s[:j] + "\\" + k + s[j+1:]
            j += 2

    return s

def xunescape(s):

    if s == "\\None":
        return None

    j = 0
    while True:
        j = s.find("\\", j)
        if j < 0:
            break
        # last character is a single \, leave as is
        if j + 1 >= len(s):
            break
        
        for a,b in _escape_conversion_table:
            if s[j+1] == b:
                s = s[:j] + a + s[j+2:]
                j += 1
                break
        else:
            # unknown sequence ignore it
            j += 1
                
    return s        

def test_xescape():
    assert(xescape("abc") == "abc")
    assert(xescape("a\0bc") == "a\0bc")
    assert(xescape("ab\ncxx") == "ab\\ncxx")
    assert(xescape("ab\tcxx") == "ab\\tcxx")
    assert(xescape("ab\\cxx") == "ab\\\\cxx")
    assert(xescape("ab\\\ncxx") == "ab\\\\\\ncxx")
    assert(xescape(None) == "\\None")
    assert(xescape("\\n") == "\\\\n")
    assert(xescape("\\") == "\\\\")

def test_xunescape():
    assert("abc" == xunescape("abc"))
    assert("ab\0c" == xunescape("ab\0c"))
    assert("ab\ncxx" == xunescape("ab\\ncxx"))
    assert("ab\tcxx" == xunescape("ab\\tcxx"))
    assert("ab\\cxx" == xunescape("ab\\\\cxx"))
    assert("ab\\\ncxx" == xunescape("ab\\\\\\ncxx"))
    assert(None is xunescape("\\None"))
    assert("\\n" == xunescape("\\\\n"))
    assert("\\" == xunescape("\\\\"))
    
    # unammisible sequences
    assert("abcd\\" == xunescape("abcd\\"))
    assert("ab\\cd\\" == xunescape("ab\\cd\\"))

def test_split_with_escape_escape():
    r = split_with_escape(r"abcd\,efg", ",")
    assert(r == ["abcd,efg"])

    r = split_with_escape("abc\\ndefg", ",")
    assert(r == ["abc\ndefg"])

    r = split_with_escape(r"abc\bdefg", ",")
    assert(r == ["abc\bdefg"])

    r = split_with_escape(r"abc\tdefg", ",")
    assert(r == ["abc\tdefg"])

def test_split_with_escape_quote():
    r = split_with_escape(r'"abcdefg"', ",", quote='"')
    assert(r == ['abcdefg'])

    r = split_with_escape(r'"abcdefg"', ",", quote='')
    assert(r == ['"abcdefg"'])

    r = split_with_escape('"abc","defg"', ",", quote='"')
    assert(r == ["abc", "defg"])

def test_split_with_escape_quote():
    r = split_with_escape(r'"abcdefg"', ",", quote='"')
    assert(r == ['abcdefg'])

    r = split_with_escape(r'"abcdefg"', ",", quote='')
    assert(r == ['"abcdefg"'])

    r = split_with_escape('"ab, c","defg"', ",", quote='"')
    assert(r == ["ab, c", "defg"])

    r = split_with_escape('"ab\\" c","defg"', ",", quote='"')
    assert(r == ["ab\" c", "defg"])

def test_split_with_escape_simple():
    r = split_with_escape("abcd,efg", ",")
    assert(r == ["abcd", "efg"])

    r = split_with_escape("abcdefg", ",")
    assert(r == ["abcdefg"])

    r = split_with_escape("", ",")
    assert(r == [""])

    r = split_with_escape("abcd,", ",")
    assert(r == ["abcd", ""])

    r = split_with_escape("abcd,,,,", ",")
    assert(r == ["abcd", "", "", "", ""])

    r = split_with_escape(",,abcd,,,,", ",")
    assert(r == ["", "", "abcd", "", "", "", ""])
    
def test_callable_simple():

    def effe():
        return True
    
    c = Callable(effe)
    assert(c)

def test_callable_with_args_1():

    def effe(n):
        return n
    
    c = Callable(effe, True)
    assert(c())

def test_callable_with_args_2():
    def effe(n):
        return n
    
    c = Callable(effe)
    assert(c(True))

def test_callable_with_args_3():
    def effe(n, n1=False):
        return n != n1
    
    c = Callable(effe , n1=True)
    assert(c(False))

def test_callable_with_args_4():
    def effe(n, n1=False):
        return n != n1
    
    c = Callable(effe , False, n1=True)
    assert(c())
    
def test_callable_with_args_5():
    def effe(n, n2, n3=7):
        return n - n2 + n3
    
    c = Callable(effe , 2, n3=8)
    assert(c(3) == (3 - 2 + 8))

def test_callable_with_args_6():
    def effe(n, n2, n3=7, n4=22):
        return n - n2 + n3 / n4
    
    c = Callable(effe , 3, n3=8)
    
    # check that a different order would give a different results
    assert((2 - 3 + 8 / 77) != (3 - 2 + 8 / 77))
    assert((2 - 3 + 8 / 77) != (2 - 3 + 77 / 8))
    
    assert(c(2, n4=77) == (2 - 3 + 8 / 77))

if __name__ == "__main__":
    last = 1
    import test_db, sys
    test_db.run_test(sys.argv[last:], sys.modules[__name__])
