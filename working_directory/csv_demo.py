# tests the spreadsheet module
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
