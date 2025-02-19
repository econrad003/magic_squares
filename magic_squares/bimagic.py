"""
bimagic.py - does a square matrix become a magic square when its entries are squared?
Copyright © 2025 by Eric Conrad

DESCRIPTION

    A Parker magic square is a semi-magic square whose entries, when squared,
    form a magic square.  The name was apparently coined in a numberphile
    video after Matt Parker who found a 3x3 example.

    A bimagic square is a Parker magic square which is also a magic square.
    Georges Pfeffermann apparently found the first example in 1890.

    A p-multimagic square is a square matrix for which the entries raised to
    each of the powers d=1, 2, ..., p all form magic squares.  So a bimagic
    square is a 2-multimagic square, and conversely.  Similarly, a trimagic
    square is 3-multimagic, and so on for prefixes like tetra-, penta-, hexa-
    and hepta-.

    Leonhard Euler found a 3x3 example of a square matrix whose entries, when
    squared, form a magic square.  (His example is not a Parker square.)

    Implemented here is a function:

        powermagic - test whether a given square matrix forms a magic square
            when its entries are raised to a given power.

    In addition, there are procedures (example1, example2, example3, example4) which
    return specific examples.  The main routine displays the results from the
    example in a somewhat user-friendly fashion.

REFERENCES

    [1] "Magic square breakthrough" in Wikipedia.  Web.  Accessed 18 February 2025.
        https://www.numberphile.com/videos/magic-square-breakthrough

    [2] "Bimagic square" in MathWorld.  Web.  Accessed 18 February 2025.
        https://mathworld.wolfram.com/BimagicSquare.html

MODIFICATIONS

    19 Feb 2025 - EC - initial version

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
from magic_squares.magic_square import MagicSquare
from magic_squares.listlike2D import listlike2D

def powermagic(square:(list, tuple, MagicSquare), d:int=2,
               diagonals:bool=True, warnings:bool=False):
    """does a square matrix become a magic square when its entries are squared?

    REQUIRED ARGUMENTS

        square - a square matrix

    OPTIONAL ARGUMENTS

        d - the power to be tested; the default is 2 to square the entries.

        diagonals - if False, then the test is for a semi-magic square; the
            default is True.

        warnings - if this is True, then a message is also displayed when the
            test fails; the default is False.

    RETURN VALUE

        If the test succeeds, the resulting magic (or semi-magic) square is
        returned.  If the test fails, the value False is returned.
    """
    n = len(square)
    if isinstance(square, (list, tuple)):
        square = listlike2D(square, n, n)
    magic = list()
    for i in range(n):
        row = list()
        for j in range(n):
            row.append(square[i,j] ** d)
        magic.append(row)
    result = False                  # assume failure
    try:
        result = MagicSquare.from_sq(magic, diagonals=diagonals)
    except Warning as why:          # failure
        if warnings:
            print(why)
    return result

def example1():
    """first example (Parker square)"""
    square = [[222, 381, 6], [291, 174, 282], [246, 138, 339]]
    powermagic(square, warnings=True)
    return square, powermagic(square, diagonals=False, warnings=True)

def example2():
    """second example (degenerate Parker square)"""
    square = [[29, 1, 47], [41, 37, 1], [23, 41, 29]]
    powermagic(square, warnings=True)
    return square, powermagic(square, diagonals=False, warnings=True)

def example3():
    """third example (Euler - square of squares is magic)"""
    square = [[68, 29, 41, 37], [17, 31, 79, 32], [59, 28, 23, 61], [11, 77, 8, 49]]
    return square, powermagic(square, warnings=True)

def example4():
    """fourth example (Pfefferman - bimagic)"""
    square = [[56, 34,  8, 57, 18, 47,  9, 31],
              [33, 20, 54, 48,  7, 29, 59, 10],
              [26, 43, 13, 23, 64, 38,  4, 49],
              [19,  5, 35, 30, 53, 12, 46, 60],
              [15, 25, 63,  2, 41, 24, 50, 40],
              [ 6, 55, 17, 11, 36, 58, 32, 45],
              [61, 16, 42, 52, 27,  1, 39, 22],
              [44, 62, 28, 37, 14, 51, 21,  3]]
    MagicSquare.from_sq(square)     # this verifies that we have a magic square
    return square, powermagic(square, warnings=True)

if __name__ == "__main__":
    print("-"*72)
    print("Example 1 (Parker square):")
    square, power = example1()
    print("Not magic:", square)
    print("Square of squares is semimagic!")

    print("-"*72)
    print("Example 2 (degenerate Parker square):")
    square, power = example2()
    print("Not magic:", square)
    print("Square of squares is semimagic!")

    print("-"*72)
    print("Example 3 (Euler - square of squares is magic):")
    square, power = example3()
    print("Not magic:", square)
    print("Square of squares is magic!")

    print("-"*72)
    print("Example 4 (Pfeffermann - bimagic):")
    square, power = example4()
    print("Magic:", square)
    print("Square of squares is also magic!")

