from __future__ import print_function
import codecs
from six import PY3
from contextlib import contextmanager
from subprocess import Popen, PIPE

if PY3:
    import csv
else:
    import unicodecsv as csv


def open_file(filename, encoding):
    """For opening files for reading with a specified encoding (usually UTF-8)"""
    if PY3:
        return open(filename, encoding=encoding)
    else:
        return codecs.open(filename, "r", encoding)


def write_out(s, out, encoding="utf-8"):
    """Provides 2 vs 3 compatibility for writing to ``out``"""
    try:
        if PY3:
            if isinstance(s, bytes):
                out.stdin.write(s)
            else:
                out.stdin.write(bytes(s, encoding))
        else:
            out.stdin.write(s)
    except IOError:
        exit()


@contextmanager
def out_py2():
    """Wrapping our call to ``less`` via ``Popen`` into a basic context manager for Python 2"""
    out = Popen('less -FXRiS', shell=True, bufsize=0, stdin=PIPE)
    yield out
    out.wait()


def out_proc():
    """A context-enabled call to Popen"""
    if PY3:
        return Popen('less -FXRiS', shell=True, bufsize=0, stdin=PIPE)
    else:
        return out_py2()
