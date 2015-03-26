from __future__ import unicode_literals

import string
import itertools
import click
import xlrd
import os

from . import asciitable, __version__
from .compat import open_file, csv, out_proc
from .cursor import XCursor, CSVCursor
from six import PY3
from subprocess import Popen, PIPE


@click.command()
@click.option('--heading',
              '-h',
              type=int,
              help='Row number containing the headings.')
@click.option("--file-type", "-f", type=click.Choice(["csv", "excel"]),
              help="Force parsing of the file to the chosen format.")
@click.option("--delimiter", "-d", type=str, default=",",
              help="Delimiter (only applicable to CSV files) [default: ',']")
@click.option("--quotechar", "-q", type=str, default='"',
              help="Quote character (only applicable to CSV files) [default: '\"']")
@click.option("--encoding", "-e", type=str, default="utf-8",
              help="Encoding [default: UTF-8]")
@click.version_option(version=__version__)
@click.argument('filename')
def cli(filename, heading, file_type, delimiter, quotechar, encoding):
    """Display Excel or CSV files directly on your terminal.
    The file type is guessed from file extensions, but can be overridden with the --file-type option.
    """
    if file_type is None:
        if filename.endswith(".csv"):
            file_type = "csv"
        else:
            file_type = "excel"

    if file_type == "csv":

        csv_rows = []

        if not PY3:
            delimiter = str(unicode(delimiter))
            quotechar = str(unicode(quotechar))

        with open_file(filename, encoding) as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                csv_rows.append(row)

        cursor = CSVCursor(csv_rows, heading)

    else:
        # As per https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966
        # encodings in Excel are usually UTF-8. So, we only override the encoding
        # if an encoding is specified by the user.
        if encoding.lower() != "utf-8":
            workbook = xlrd.open_workbook(filename, encoding_override=encoding)
        else:
            workbook = xlrd.open_workbook(filename)

        sheet = workbook.sheet_by_index(0)

        cursor = XCursor(sheet, heading)

    with out_proc() as out:

        asciitable.draw(cursor, out=out)
