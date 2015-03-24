x_x: The Dead Guy CLI
=====================

.. image:: https://badge.fury.io/py/x_x.png
    :target: http://badge.fury.io/py/x_x

.. image:: https://pypip.in/d/x_x/badge.png
        :target: https://crate.io/packages/x_x/


x_x is a Microsoft Excel file command line reader.  The purpose of this is to not break
the workflow of people who live on the command line and need to access a
spreadsheet generated using Microsoft Excel.

Install
-------

To install:

::

  $ pip install x_x


Usage
-----

Run using the `x_x` command:

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

For help use:

::

  $ x_x --help
