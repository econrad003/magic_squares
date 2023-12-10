"""
examples2.py - creates spreadsheets for standard examples
Copyright © 2023 by Eric Conrad

DESCRIPTION

    The magic squares represented in this script were named for planets
    in the Ptolemaic system (i.e., the sun, the moon, and the planets
    from Mercury through Saturn).  They were in the past used in
    divination, specifically in the pseudosciences of astrology and
    numerology. Practitioners would give special meaning to the order
    (n), the largest entry (n²), the magic constant (n(n²+1)/2) and the
    sum of the entries (n²(n²+1)/2, a triangular number), as well as
    to particular placements of numbers in the squares.  (Disclaimer:
    These applications of magic squares are, in the words of magicians
    Penn and Teller, just bullshit.)

    These are simply presented here as examples.  Jupiter and Saturn
    appear in "examples1.py" as Jupiter and Siam_03, respectively,
    and are not repeated here.

REFERENCE

    The squares here all appear in the Wikipedia article on magic
    squares.

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
from magic_squares.magic_square import MagicSquare as MS
from magic_squares.spreadsheet import SpreadsheetManager as sm

prefix = "spreadsheets/"
extension = ".csv"

CITE = "Picatrix/Ghāyat al-Ḥakīm c 11th c CE (Krakow MS)"

print("Making standard magic squares examples...")
print("Folder:", prefix)

print()
print("1. Saturn (3x3) - see Siam_03 in examples1.py - omitted here")
print("2. Jupiter (4x4) - see Jupiter in examples1.py - omitted here")
print("3. Mars (5x5)")
Mars = MS.from_sq([[11, 24, 7, 20, 3], [4, 12, 25, 8, 16],
                   [17, 5, 13, 21, 9], [10, 18, 1, 14, 22],
                   [23, 6, 19, 2, 15]])
Mars.name = "Mars"
Mars.keywords = "Mars, Ares"

print("4. Sol (6x6)")
Sol = MS.from_sq([[ 6, 32,  3, 34, 35,  1],
                  [ 7, 11, 27, 28,  8, 30],
                  [19, 14, 16, 15, 23, 24],
                  [18, 20, 22, 21, 17, 13],
                  [25, 29, 10,  9, 26, 12],
                  [36,  5, 33,  4,  2, 31]])
Sol.name = "Sol"
Sol.keywords = "Sol, Helios, Apollo, Shamash, Ra, Sun"

print("5. Venus (7x7)")
Venus = MS.from_sq([[22, 47, 16, 41, 10, 35, 4],
                    [5, 23, 48, 17, 42, 11, 29],
                    [30, 6, 24, 49, 18, 36, 12],
                    [13, 31, 7, 25, 43, 19, 37],
                    [38, 14, 32, 1, 26, 44, 20],
                    [21, 39, 8, 33, 2,27, 45],
                    [46, 15, 40, 9, 34, 3, 28]])
Venus.name = "Venus"
Venus.keywords = "Venus, Aphrodite, Morning Star, Evening Star"
Venus.keywords += "Ninsi'anna, Tioumoutiri, Ouaiti"

print("6. Mercury (8x8)")
Mercury = MS.from_sq([[8, 58, 59, 5, 4, 62, 63, 1],
                      [49, 15, 14, 52, 53, 11, 10, 56],
                      [41, 23, 22, 44, 45, 19, 18, 48],
                      [32, 34, 35, 29, 28, 38, 39, 25],
                      [40, 26, 27, 37, 36, 30, 31, 33],
                      [17, 47, 46, 20, 21, 43, 42, 24],
                      [9, 55, 54, 12, 13, 51, 50, 16],
                      [64, 2, 3, 61, 60, 6, 7, 57]])
Mercury.name = "Mercury"
Mercury.keywords = "Mercury, Hermes, Quicksilver"

print("7. Luna (9x9)")
Luna = MS.from_sq([[37, 78, 29, 70, 21, 62, 13, 54, 5],
                   [6, 38, 79, 30, 71, 22, 63, 14, 46],
                   [47, 7, 39, 80, 31, 72, 23, 55, 15],
                   [16, 48, 8, 40, 81, 32, 64, 24, 56],
                   [57, 17, 49, 9, 41, 73, 33, 65, 25],
                   [26, 58, 18, 50, 1, 42, 74, 34, 66],
                   [67, 27, 59, 10, 51, 2, 43, 75, 35],
                   [36, 68, 19, 60, 11, 52, 3, 44, 76],
                   [77, 28, 69, 20, 61, 12, 53, 4, 45]])
Luna.name = "Luna"
Luna.keywords = "Luna, Selene, Diana, Artemis, Sin, Khonsu"

print("Making the spreadsheets...")
for foo in {Mars, Sol, Venus, Mercury, Luna}:
    foo.cite = CITE
    foo.keywords = foo.keywords + ", Picatrix"
    csvname = foo.name
    print("\t", foo.name, "\t", foo.n)
    print("\t", foo.keywords)
    sm.csv_writer(foo, prefix + csvname + extension)

print("SUCCESS!")
