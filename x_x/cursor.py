import itertools
import string


class XCursor(object):

    def __init__(self, sheet, headingrow=None):
        self.headingrow = headingrow
        self.sheet = sheet

    def num_rows(self):
        return self.sheet.nrows

    def num_cols(self):
        if self.headingrow is None:
            return len(self.sheet_row(0))
        else:
            return len(self.sheet_row(self.headingrow))

    def sheet_row(self, n):
        return [c.value for c in self.sheet.row(n)]

    def keys(self):
        if self.headingrow is not None:
            return self.sheet_row(self.headingrow)
        else:
            u = string.ascii_uppercase
            return [''.join(r) for idx, r in
                    enumerate(itertools.chain(u, itertools.product(u, u)))
                    if idx < self.num_cols()]

    def __iter__(self):
        start = self.headingrow + 1 if self.headingrow is not None else 0
        return (self.sheet_row(n) for n in range(start, self.num_rows()))


class CSVCursor(XCursor):

    def sheet_row(self, n):
        return self.sheet[n]

    def num_rows(self):
        return len(self.sheet)
