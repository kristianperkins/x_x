import itertools
import string
import os
import subprocess
import sys
import click
import xlrd
import jsonpickle

from . import asciitable

class XCursor(object):

    def __init__(self, sheet, headingrow=None):
        self.headingrow = headingrow
        self.sheet = sheet

    def keys(self):
        if self.headingrow is not None:
            return [c.value for c in self.sheet.row(self.headingrow)]
        else:
            u = string.ascii_uppercase
            cols = len(self.sheet.row(0))
            return [''.join(r) for idx, r in
                    enumerate(itertools.chain(u, itertools.product(u, u)))
                    if idx < cols]

    def __iter__(self):
        start = self.headingrow + 1 if self.headingrow is not None else 0
        return ([c.value for c in self.sheet.row(n)] for n in range(start, self.sheet.nrows))


@click.command()
@click.option('--heading', '-h', type=int, help='[Required for JSON] Row number containing the headings.')
@click.option('--json/--no-json', '-J/-j', default=False, help="[Optional] Flag for enabling JSON output.")
@click.option('--less/--no-less', '-L/-l', default=False, help="[Optional] Flag for automatically routing table(s) to less.")
@click.argument('filename')
@click.argument('pages')

def cli(filename, heading, pages, json, less):
    
    """ x_x is a Microsoft Excel file command line reader. 
    The purpose of this is to not break the workflow of people who live 
    on the command line and need to access a spreadsheet 
    generated using Microsoft Excel. Ex: x_x [options] [filename] [pages(comma-separated)]
    """
    
    # Grab a reference to the workbook passed by the filename argument
    workbook = xlrd.open_workbook(filename)
    
    # If using less, point stdin to a subprocess' stdin, otherwise route to this applications stdout
    if (less):
        stdin = subprocess.Popen('less -FXRiS', shell=True, bufsize=0, stdin=subprocess.PIPE).stdin
    else: 
        stdin = sys.stdout

    # If JSON, render out the content of the sheet(s) as JSON kvps
    if (json): 
        json_result = []
        for i in pages.split(','):
            sheet = workbook.sheet_by_index(int(i))
            result = { 'name': sheet.name, 'values': [] }
            header = sheet._cell_values[int(heading)]
            sheet._cell_values.pop(int(heading));
            for j in sheet._cell_values:
                row = {}
                for k,l in enumerate(j):
                    row[header[k] if header[k] != "" else GetExcelColumn(k)] = l
                result['values'].append(row)
            json_result.append(result)
        print(jsonpickle.encode(json_result))

    # Otherwise, render out using asciitable
    else: 
        for i in pages.split(','):
            asciitable.draw(XCursor(workbook.sheet_by_index(int(i)), heading), out=stdin)

# http://stackoverflow.com/a/19576446/1760344
def GetExcelColumn(index):
    quotient = int(index / 26)
    if quotient > 0:
        return GetExcelColumn(quotient) + str(chr((index % 26) + 64))
    else:
        return str(chr(index + 64))