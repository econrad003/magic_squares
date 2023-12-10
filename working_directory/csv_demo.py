"""
csv_demo.py - tests the spreadsheet module
Copyright © 2023 by Eric Conrad

LICENSE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see
        <https://www.gnu.org/licenses/>.
"""

import logging
from magic_squares import logger
from magic_squares.spreadsheet import SpreadsheetManager as sm
from magic_squares.order4 import Melencolia1514

logger.setLevel(logging.DEBUG)

SAMPLE_INPUT = "spreadsheets/test.csv"
TEST_OUTPUT = "spreadsheets/output.csv"

foo = sm.csv_reader(SAMPLE_INPUT, True)
print(foo.name)
print(foo.comment)
print(foo)

sm.csv_writer(Melencolia1514, TEST_OUTPUT)

print("Checking output")
foo = sm.csv_reader(TEST_OUTPUT, True)
print(foo.name)
print(foo.cite)
print(foo.keywords)
print(foo)


print("SUCCESS!")
