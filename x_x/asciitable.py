# -*- coding: utf-8 -*-
# asciitable.py taken from ipydb: https://github.com/jaysw/ipydb

"""Draw ascii tables."""
import itertools
import sys

from six import string_types, PY3
from six.moves import zip, zip_longest


def write_bytes(s, out, encoding="utf-8"):
    """Provides 2 vs 3 compatibility for writing to ``out``"""
    try:
        if PY3:
            if isinstance(s, bytes):
                out.write(s)
            else:
                out.write(bytes(s, encoding))
        else:
            out.write(s.encode(encoding, 'replace'))
    except IOError as bpe:
        exit()

def termsize():
    """Try to figure out the size of the current terminal.

    Returns:
        Size of the terminal as a tuple: (height, width).
    """
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])


class FakedResult(object):

    """Utility for making an iterable look like an sqlalchemy ResultProxy."""

    def __init__(self, items, headings):
        self.items = items
        self.headings = headings

    def __iter__(self):
        return iter(self.items)

    def keys(self):
        return self.headings


class PivotResultSet(object):

    """Pivot a result set into an iterable of (fieldname, value)."""

    def __init__(self, rs):
        self.rs = rs

    def __iter__(self):
        # Note: here we 'ovewrite' ambiguous / duplicate keys
        # is this a bad thing? probably not?
        # r.items() throws exceptions from SA if there are ambiguous
        # columns in the select statement.
        return (zip(r.keys(), r.values()) for r in self.rs)

    def keys(self):
        return ['Field', 'Value']


def isublists(l, n):
    return zip_longest(*[iter(l)] * n)


def draw(cursor, out=sys.stdout, paginate=True, max_fieldsize=100):
    """Render an result set as an ascii-table.

    Renders an SQL result set to `out`, some file-like object.
    Assumes that we can determine the current terminal height and
    width via the termsize module.

    Args:
        cursor: An iterable of rows. Each row is a list or tuple
                with index access to each cell. The cursor
                has a list/tuple of headings via cursor.keys().
        out: File-like object.
    """

    def heading_line(sizes):
        for size in sizes:
            write_bytes('+' + '-' * (size + 2), out)
        write_bytes('+\n', out)

    def draw_headings(headings, sizes):
        heading_line(sizes)
        for idx, size in enumerate(sizes):
            fmt = '| %%-%is ' % size
            write_bytes((fmt % headings[idx]), out)
        write_bytes('|\n', out)
        heading_line(sizes)

    cols, lines = termsize()
    headings = list(cursor.keys())
    if PY3:
        heading_sizes = [len(str(x)) for x in headings]
    else:
        heading_sizes = [len(unicode(x)) for x in headings]
    if paginate:
        cursor = isublists(cursor, lines - 4)
        # else we assume cursor arrive here pre-paginated
    for screenrows in cursor:
        sizes = heading_sizes[:]
        for row in screenrows:
            if row is None:
                break
            for idx, value in enumerate(row):
                if not isinstance(value, string_types):
                    if PY3:
                        value = str(value)
                    else:
                        value = unicode(value)
                size = max(sizes[idx], len(value))
                sizes[idx] = min(size, max_fieldsize)
        draw_headings(headings, sizes)
        for rw in screenrows:
            if rw is None:
                break  # from isublists impl
            for idx, size in enumerate(sizes):
                fmt = '| %%-%is ' % size
                if idx < len(rw):
                    value = rw[idx]
                    if not isinstance(value, string_types):
                        if PY3:
                            value = str(value)
                        else:
                            value = unicode(value)
                    if len(value) > max_fieldsize:
                        value = value[:max_fieldsize - 5] + '[...]'
                    value = value.replace('\n', '^')
                    value = value.replace('\r', '^').replace('\t', ' ')
                    value = fmt % value
                    write_bytes(value, out)
            write_bytes('|\n', out)
        if not paginate:
            heading_line(sizes)
            write_bytes('|\n', out)
