"""
examples1.py - creates spreadsheets for standard examples
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
from magic_squares.magic_square import SiameseMagicSquare
import magic_squares.order4 as o4

prefix = "spreadsheets/"
extension = ".csv"

print("Making standard magic squares examples...")
print("Folder:", prefix)

print()
print("1. Using the method described by French diplomat Simon de la")
print("   Loubère in Du Royaume de Siam (1691).  The method was")
print("   already known in India and China, but is sometimes called")
print("   the Siamese method.")
for i in range(3, 20, 2):
    foo = SiameseMagicSquare(i)
    csvname = f"Siam_{i:02}"
    foo.cite = "Du Royaume de Siam (1691) by Simon de la Loubère"
    foo.keywords = "odd order, ancient"
    print("\t", foo.name, "\t", csvname)
    
    sm.csv_writer(foo, prefix + csvname + extension)

print("2. Making some well-known order 4 magic squares...")
for foo in o4._all:
    csvname = foo._csvname
    print("\t", foo.name, "\t", csvname)
    sm.csv_writer(foo, prefix + csvname + extension)
    


print("SUCCESS!")
