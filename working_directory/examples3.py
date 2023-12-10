"""
examples2.py - creates spreadsheets for antimagic examples
Copyright © 2023 by Eric Conrad

The squares here are from the references.

REFERENCES

    [1] "Antimagic square" in Wikipedia. 8 Nov. 2023.  Web.
        Accessed 25 November 2023.
            https://en.wikipedia.org/wiki/Antimagic_square

    [2] "Antimagic squares" in MathWorld.  Web.  Accessed 25 Nov 2023.
            https://mathworld.wolfram.com/AntimagicSquare.html

    [3] Johm Cormie.  "The antimagic square project". Web.  Accessed
        25 Nov 2023.
            http://ion.uwinnipeg.ca/~vlinek/jcormie/

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
from magic_squares.antimagic_square import AntimagicSquare
from magic_squares.spreadsheet import SpreadsheetManager as sm

prefix = "spreadsheets/"
extension = ".csv"

CITE1 = "antimagicsquares.net (dead domain) via Wikipedia"
CITE2 = 'Eric Weisstein. "Antimagic square" in Mathworld.'
CITE3 = 'John Cormie. "The Antimagic square project".' \
    + " http://ion.uwinnipeg.ca/~vlinek/jcormie/"

print("Making antimagic squares examples...")
print("Folder:", prefix)

print()
foobar = set()

x = [[2, 15, 5, 13], [16, 3, 7, 12], [9, 8, 14, 1], [6, 4, 11, 10]]
x = AntimagicSquare.from_sq(x)
x.name = "order 4 antimagic square (antimagic-4-001)"
x.keywords = "antimagic"
x.cite = CITE1
x._csvname = "antimagic-4-001"
foobar.add(x)

x = [[1, 13, 3, 12], [15, 9, 4, 10], [7, 2, 16, 8], [14, 6, 11, 5]]
x = AntimagicSquare.from_sq(x)
x.name = "order 4 antimagic square (antimagic-4-002)"
x.keywords = "antimagic"
x.cite = CITE1
x._csvname = "antimagic-4-002"
foobar.add(x)

x = [[15, 2, 12, 4], [1, 14, 10, 5], [8, 9, 3, 16], [11, 13, 6, 7]]
x = AntimagicSquare.from_sq(x)
x.name = "order 4 antimagic square (antimagic-4-003)"
x.keywords = "antimagic"
x.cite = CITE2
x._csvname = "antimagic-4-003"
foobar.add(x)

x = [[5, 8, 20, 9, 22], [19, 23, 13, 10, 2], [21, 6, 3, 15, 25],
     [11, 18, 7, 24, 1], [12, 14, 17, 4, 16]]
x = AntimagicSquare.from_sq(x)
x.name = "order 5 antimagic square (antimagic-5-001)"
x.keywords = "antimagic"
x.cite = CITE1
x._csvname = "antimagic-5-001"
foobar.add(x)

x = [[21, 18, 6, 17, 4], [7, 3, 13, 16, 24], [5, 20, 23, 11, 1],
     [15, 8, 19, 2, 25], [14, 12, 9, 22, 10]]
x = AntimagicSquare.from_sq(x)
x.name = "order 5 antimagic square (antimagic-5-002)"
x.keywords = "antimagic"
x.cite = CITE2
x._csvname = "antimagic-5-002"
foobar.add(x)

x = [[10, 25, 32, 13, 16, 9], [22, 7, 3, 24, 21, 30],
     [20, 27, 18, 26, 11, 6], [1, 31, 23, 33, 17, 8],
     [19, 5, 36, 12, 15, 29], [34, 14, 2, 4, 35, 28]]
x = AntimagicSquare.from_sq(x)
x.name = "order 6 antimagic square (antimagic-6-001)"
x.keywords = "antimagic"
x.cite = CITE2
x._csvname = "antimagic-6-001"
foobar.add(x)

x = [[14, 3, 34, 21, 47, 29, 22], [43, 16, 13, 25, 6, 26, 44],
     [30, 48, 24, 8, 12, 9, 45], [10, 5, 11, 38, 49, 46, 19],
     [4, 41, 37, 36, 33, 27, 1], [39, 17, 40, 20, 7, 35, 23],
     [31, 42, 18, 32, 28, 2, 15]]
x = AntimagicSquare.from_sq(x)
x.name = "order 7 antimagic square (antimagic-7-001)"
x.keywords = "antimagic"
x.cite = CITE2
x._csvname = "antimagic-7-001"
foobar.add(x)

x = [[49, 16, 50, 10, 19, 28, 24, 56], [42, 43, 11, 15, 44, 38, 55, 5],
     [25, 21, 48, 46, 9, 37, 6, 63], [29, 47, 8, 40, 51, 30, 52, 1],
     [45, 22, 54, 23, 20, 34, 2, 62], [14, 59, 18, 33, 41, 26, 61, 13],
     [36, 12, 58, 32, 27, 64, 3, 35], [17, 39, 7, 57, 53, 4, 60, 31]]
x = AntimagicSquare.from_sq(x)
x.name = "order 8 antimagic square (antimagic-8-001)"
x.keywords = "antimagic, John Cormie"
x.cite = CITE3
x._csvname = "antimagic-8-001"
foobar.add(x)

x = [[52, 19, 81, 22, 29, 15, 42, 31, 76],
     [61, 10, 67, 23, 54, 79, 25, 33, 16],
     [57, 9, 71, 24, 38, 1, 51, 47, 75],
     [26, 78, 7, 69, 66, 77, 13, 27, 12],
     [39, 21, 74, 20, 37, 17, 49, 55, 64],
     [8, 65, 4, 62, 50, 34, 73, 41, 40],
     [56, 68, 2, 63, 14, 72, 35, 44, 6],
     [53, 30, 60, 32, 36, 3, 46, 43, 58],
     [11, 70, 5, 59, 48, 80, 28, 45, 18]]
x = AntimagicSquare.from_sq(x)
x.name = "order 9 antimagic square (antimagic-9-001)"
x.keywords = "antimagic"
x.cite = CITE2
x._csvname = "antimagic-9-001"
foobar.add(x)


print("Making the spreadsheets...")
for foo in foobar:
    bar = foo.magic
    csvname = foo._csvname
    print("\t", foo.name, "\t", foo.n, [bar.start, bar.stop, bar.step])
    print("\t", foo.keywords)
    sm.csv_writer(foo, prefix + csvname + extension)

print("SUCCESS!")
