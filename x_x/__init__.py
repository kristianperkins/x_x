import itertools
import string

import xlrd

import asciitable


class XCursor(object):

    def __init__(self, sheet, headingrow=None):
        self.headingrow = headingrow
        self.sheet = sheet

    def keys(self):
        if self.headingrow is not None:
            return [c.value for c in self.sheet.row(self.headingrow)]
        else:
            u = string.uppercase
            cols = len(sheet.row(0))
            return [''.join(r) for idx, r in
                    enumerate(itertools.chain(u, itertools.product(u, u)))
                    if idx < cols]

    def __iter__(self):
        start = self.headingrow + 1 if self.headingrow is not None else 0
        return ([c.value for c in self.sheet.row(n)] for n in xrange(start, self.sheet.nrows))



if __name__ == "__main__":
    workbook = xlrd.open_workbook('example.xlsx')
    sheet = workbook.sheet_by_index(0)
    asciitable.draw(XCursor(sheet, 0))
