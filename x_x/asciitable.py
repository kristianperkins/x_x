# -*- coding: utf-8 -*-
# asciitable.py taken from ipydb: https://github.com/jaysw/ipydb

"""Draw ascii tables."""
import itertools
import sys


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
    return itertools.izip_longest(*[iter(l)] * n)


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
            out.write('+' + '-' * (size + 2))
        out.write('+\n')

    def draw_headings(headings, sizes):
        heading_line(sizes)
        for idx, size in enumerate(sizes):
            fmt = '| %%-%is ' % size
            out.write((fmt % headings[idx]))
        out.write('|\n')
        heading_line(sizes)

    cols, lines = termsize()
    headings = cursor.keys()
    heading_sizes = map(lambda x: len(str(x)), headings)
    if paginate:
        cursor = isublists(cursor, lines - 4)
        # else we assume cursor arrive here pre-paginated
    for screenrows in cursor:
        sizes = heading_sizes[:]
        for row in screenrows:
            if row is None:
                break
            for idx, value in enumerate(row):
                if not isinstance(value, basestring):
                    value = str(value)
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
                    if not isinstance(value, basestring):
                        value = str(value)
                    if len(value) > max_fieldsize:
                        value = value[:max_fieldsize - 5] + '[...]'
                    value = value.replace('\n', '^')
                    value = value.replace('\r', '^').replace('\t', ' ')
                    value = fmt % value
                    try:
                        value = value.encode('utf-8', 'replace')
                    except UnicodeDecodeError:
                        value = fmt % '?'
                    out.write(value)
            out.write('|\n')
        if not paginate:
            heading_line(sizes)
            out.write('\n')
