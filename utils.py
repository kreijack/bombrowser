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

    exc_info = (exc_type, exc_value, exc_traceback)
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
    def __call__(self):
        return self._f(*self._args, **self._kwargs)

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

if __name__ == "__main__":
    last = 1
    import test_db, sys
    test_db.run_test(sys.argv[last:], sys.modules[__name__])
