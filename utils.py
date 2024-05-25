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

import sys, traceback, re, os

from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QUrl, QByteArray
from PySide2.QtGui import QDesktopServices

from version import version
import db, cfg

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

def bb_match(s, exp, conv2=None, case_sensitive=True):
    """
        bb_match(s, exp, conv)

        return True if 's' match the 'exp' expression.

        The 'exp' expression is in the form:
        <exp1>[;<exp2>[...]]

        where

        exp support the following special chareacters (derived by SQL extension)
        % -> means any characters sequence of any length
        _ -> means any character
        [abc] is any character in the range "abc"
    """

    if exp[0] == '=':
        exps = [exp]
    else:
        exps = exp.split(";")

    if conv2 is None:
        conv2 = lambda x : x

    if isinstance(s, str) and not case_sensitive:
        conv = lambda y : conv2(y).upper()
        s = s.upper()
    else:
        conv = conv2

    for exp in exps:
        if len(exp) == 0:
            continue

        if exp[0] == '=':
            if conv(exp[1:]) == s:
                return True

        elif exp[0] == '>':
            if s > conv(exp[1:]):
                return True

        elif exp[0] == '<':
            if s < conv(exp[1:]):
                return True

        elif exp[0] == '!':
            if s != conv(exp[1:]):
                return True

        elif not ('%' in exp or '_' in exp or '[' in exp or ']' in exp):
            # no special char
            if isinstance(s, str):
                if conv(exp) in s:
                    return True
            else:
                if conv(exp) == s:
                    return True

        elif isinstance(s, str):
            # special char
            exp = exp.replace("\\", r"\\").replace("*", r"\*")
            exp = exp.replace(".", r"\.").replace("%", ".*").replace("_", ".")
            if re.match("^"+exp+"$", s):
                return True

        else:
            # contains [, % ... but it is not a string ?!?!?!?
            assert(0)

    return False

def find_filename(filename):
    if os.path.dirname(filename) != '':
        return filename

    default_dirs = cfg.config()["FILES_UPLOAD"].get("default_dirs", "")
    default_dirs = [ x.strip()
                     for x in default_dirs.split("\n")
                     if (len(x.strip()) > 0 and
                         os.path.exists(x.strip()) and
                         os.path.isdir(x.strip())) ]

    for dd in default_dirs:
        fp = os.path.join(dd, filename)
        if os.path.exists(fp):
            return fp

    return filename

def reload_config_or_warn():
    ret = cfg.reload_and_check_cfg()
    if len(ret) != 1 or ret[0][0] != "OK":
        message = "ERROR in bombrowser.ini\n"
        for type_, msg in ret:
            if type_ == "MORE":
                message += "WARNING: " + msg + "\n"
            else:
                message += "CRITICAL: " + msg + "\n"
        message += "Abort\n"
        QMessageBox.critical(None, "BOMBrowser - %s"%(version),
            message)
        return

class OverrideCursor:
    def __init__(self, cursor=Qt.WaitCursor):
        self._cursor = cursor
    def __enter__(self):
        QApplication.setOverrideCursor(self._cursor)
    def __exit__(self, type_, value, traceback):
        QApplication.restoreOverrideCursor()

def is_url(url):
    return  (url.lower().startswith("ftp://") or
             url.lower().startswith("http://") or
             url.lower().startswith("https://"))

def copy_file_to_clipboard(fn, md):
    # the life is sometime very complicated !

    # windows
    md.setUrls([QUrl.fromLocalFile(fn)])
    # mate
    md.setData("x-special/mate-copied-files",
        QByteArray(("copy\nfile://"+fn).encode("utf-8")))
    # nautilus
    md.setText("x-special/nautilus-clipboard\ncopy\nfile://"+
        fn+"\n")
    # gnome
    md.setData("x-special/gnome-copied-files",
        QByteArray(("copy\nfile://"+fn).encode("utf-8")))
    # dolphin
    md.setData("text/uri-list",
        QByteArray(("file:"+fn).encode("utf-8")))


def open_file_or_url(url):
    if is_url(url):
        QDesktopServices.openUrl(QUrl(url))
    else:
        QDesktopServices.openUrl(QUrl.fromLocalFile(url))

def test_bb_match_simple():
    assert(bb_match("abc", "a"))
    assert(bb_match("abc", "a%"))
    assert(not bb_match("abc", "%a"))

    assert(not bb_match("abc", "c%"))
    assert(bb_match("abc", "%c"))

    assert(not bb_match("abc", "d"))
    assert(not bb_match("abc", "%d"))
    assert(not bb_match("abc", "d%"))

    assert(not bb_match("abc", "=a"))
    assert(not bb_match("abc", "=d"))
    assert(bb_match("abc", "=abc"))

    assert(bb_match("bcd", ">a"))
    assert(bb_match("abc", "<z"))

    assert(bb_match("abc", "!a"))
    assert(bb_match("abc", "!z"))

    assert(not bb_match("abc", "[bfg]"))

    assert(bb_match("abc", "%[bfg]%"))

def test_bb_match_special():
    assert(not bb_match("abc", "a.c"))
    assert(bb_match("abc", "a_c"))
    assert(not bb_match("aac", "a*c"))
    assert(bb_match("aac", "a%c"))
    assert(not bb_match("aac", ".*c"))
    assert(bb_match("aac", "%c"))

def test_bb_match_list():
    assert(bb_match("abc", "a;k"))
    assert(bb_match("abc", "k;a"))

    assert(not bb_match("abc", "k;e"))
    assert(bb_match("abc", "k;=abc"))

    assert(not bb_match("abc", "=k;a"))
    assert(not bb_match("a;c", "=a;b"))

    assert(bb_match("abc", ";=k;a"))

    assert(not bb_match("bcd", ";=k;>fa"))
    assert(bb_match("bcd", ";=k;>a"))

    assert(not bb_match("bcd", ";=k;<a"))
    assert(bb_match("bcd", ";=k;<z"))

    assert(bb_match("bcd", ";=k;!b"))
    assert(not bb_match("bcd", ";=k;!bcd"))

    assert(bb_match("bcd", ";=k;b%"))
    assert(not bb_match("bcd", ";=k;%b"))
    assert(bb_match("bcd", ";=k;%d"))
    assert(not bb_match("bcd", ";=k;d%"))
    assert(bb_match("bcd", ";=k;%d%"))

    assert(bb_match("bcd", ";=k;%c%"))
    assert(not bb_match("bcd", ";=k;%c"))
    assert(not bb_match("bcd", ";=k;c%"))

    assert(not bb_match(11, "9;10", int))
    assert(bb_match(10, "9;10", int))
    assert(not bb_match(10, "20;>10", int))
    assert(bb_match(10, "<20;>10", int))


def test_bb_match_conv():
    assert(not bb_match(10, ">10", int))
    assert(bb_match(10, ">7", int))
    assert(bb_match(10, "<157", int))
    assert(not bb_match(10, "<1", int))

    assert(not bb_match(10, "=11", int))
    assert(bb_match(10, "=10", int))

    assert(not bb_match(10, "!10", int))
    assert(bb_match(10, "!11", int))

    assert(not bb_match(10, "11", int))
    assert(not bb_match(10, "1", int))
    assert(bb_match(10, "10", int))

    assert(not bb_match(10, "1", int))

def test_bb_match_icase():
    assert(not bb_match("abc", "A", case_sensitive=True))
    assert(bb_match("abc", "A", case_sensitive=False))

    assert(bb_match("abc", "%A%", case_sensitive=False))


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

def test_split_with_escape_quote_2():
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
