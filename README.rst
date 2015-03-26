x_x: The Dead Guy CLI
=====================

.. image:: https://badge.fury.io/py/x_x.png
    :target: http://badge.fury.io/py/x_x

.. image:: https://pypip.in/d/x_x/badge.png
        :target: https://crate.io/packages/x_x/


x_x is a command line reader that displays either Excel files or CSVs in your terminal. The purpose of this is to not break the workflow of people who live on the command line and need to access a spreadsheet generated using Microsoft Excel.

Install
-------

The easy way:

::

    $ pip install x_x


Or the hard way:

::

    $ git clone https://github.com/krockode/x_x.git && cd x_x && python setup.py install

Usage
-----

Installing this package gives you an ``x_x`` CLI executable.

::

    $ x_x --help
    Usage: x_x [OPTIONS] FILENAME

      Display Excel or CSV files directly on your terminal. The file type is
      guessed from file extensions, but can be overridden with the --file-type
      option.

    Options:
      -h, --heading INTEGER        Row number containing the headings.
      -f, --file-type [csv|excel]  Force parsing of the file to the chosen format.
      -d, --delimiter TEXT         Delimiter (only applicable to CSV files)
                                   [default: ',']
      -q, --quotechar TEXT         Quote character (only applicable to CSV files)
                                   [default: '"']
      -e, --encoding TEXT          Encoding [default: UTF-8]
      --version                    Show the version and exit.
      --help                       Show this message and exit.

So, for example:

::

  $ x_x dead_guys.xlsx
  +---------------+--------------+
  | A             | B            |
  +---------------+--------------+
  | Person        | Age at Death |
  | Harrold Holt  | 59.0         |
  | Harry Houdini | 52.0         |
  | Howard Hughes | 70.0         |

Or to specify a specific row as the header which will be visible on each page:

::

  $ x_x -h 0 dead_guys.xlsx
  +---------------+--------------+
  | Person        | Age at Death |
  +---------------+--------------+
  | Harrold Holt  | 59.0         |
  | Harry Houdini | 52.0         |
  | Howard Hughes | 70.0         |

Weird CSVs? No problem!

::

    $ cat dead_guys.csv
    person;age_at_death
    Harrold Holt;59
    Harry Houdini;52
    Howard Hughes;70
    |Not some guy, but just a string with ; in it|;0

::

    $ x_x -h 0 --delimiter=';' --quotechar='|' dead_guys.csv
    +----------------------------------------------+--------------+
    | person                                       | age_at_death |
    +----------------------------------------------+--------------+
    | Harrold Holt                                 | 59           |
    | Harry Houdini                                | 52           |
    | Howard Hughes                                | 70           |
    | Not some guy, but just a string with ; in it | 0            |

Does your CSV file not end in "csv"? Again, no problem:

::

    $ mv dead_guys.csv dead_guys.some_other_extension
    $ x_x -h 0 --file-type=csv --delimiter=';' --quotechar='|' dead_guys.some_other_extension
    +----------------------------------------------+--------------+
    | person                                       | age_at_death |
    +----------------------------------------------+--------------+
    | Harrold Holt                                 | 59           |
    | Harry Houdini                                | 52           |
    | Howard Hughes                                | 70           |
    | Not some guy, but just a string with ; in it | 0            |
