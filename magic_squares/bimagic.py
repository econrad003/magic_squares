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

    In addition, there are procedures ("example1" through "example6") which
    return specific examples.  The main routine displays the results from the
    example in a somewhat user-friendly fashion.

    Examples 1 through 4 are all mentioned in the NumberPhile video [1] and,
    except for Example 4, were copied here from the video.  Example 4 was
    lifted from MathWorld [2].  Example 5, a solution to a problem from Martin
    Gardner, was given in the Wikipedia article [3].  Example 6 was copied
    from the MathWorld article [4].  References [5] and [6] are mentioned in the
    documentation of Example 6 in connection with an order 128 trimagic
    square (128×128=16,384 entries!) that was constructed in 1906, without
    the use of digital computers.

REFERENCES

    [1] "Magic square breakthrough" in Wikipedia.  Web.  Accessed 18 February 2025.
        https://www.numberphile.com/videos/magic-square-breakthrough

    [2] "Bimagic square" in MathWorld.  Web.  Accessed 18 February 2025.
        https://mathworld.wolfram.com/BimagicSquare.html

    [3] "Magic square" in Wikipedia.  Web.  Accessed 20 February 2025.
        https://en.wikipedia.org/wiki/Magic_square

    [4] "Trimagic square" in MathWorld.  Web.  Accessed 20 February 2025.
        https://mathworld.wolfram.com/TrimagicSquare.html

    [5] "Jacquard machine" in Wikipedia.  Web.  Accessed 20 February 2023.
        https://en.wikipedia.org/wiki/Jacquard_machine

    [6] "Analytical engine" in Wikipedia.  Web.  Accessed 20 February 2023.
        https://en.wikipedia.org/wiki/Analytical_engine

MODIFICATIONS

    19 Feb 2025 - EC - initial version
    20 Feb 2025 - EC
        (1) Added Martin Gardner's semimagic square of squares
        (2) Added a few references
        (3) Added Walter Trump's order 12 perfect trimagic square

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
    """first example (Parker square)

    See the NumberPhile video [1].
    """
    square = [[222, 381, 6], [291, 174, 282], [246, 138, 339]]
    powermagic(square, warnings=True)
    return square, powermagic(square, diagonals=False, warnings=True)

def example2():
    """second example (Matt Parker - degenerate Parker square)

    See the NumberPhile video [1].
    """
    square = [[29, 1, 47], [41, 37, 1], [23, 41, 29]]
    powermagic(square, warnings=True)
    return square, powermagic(square, diagonals=False, warnings=True)

def example3():
    """third example (Leonhard Euler - square of squares is magic)

    See the NumberPhile video [1].
    """
    square = [[68, 29, 41, 37], [17, 31, 79, 32], [59, 28, 23, 61], [11, 77, 8, 49]]
    return square, powermagic(square, warnings=True)

def example4():
    """fourth example (Georges Pfefferman []1890] - bimagic)

    See the NumberPhile video [1] and the MathWorld article [2] on bimagic
    squares.
    """
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

def example5():
    """fifth example (Martin Gardner square)

    See the Wikipedia article [3].
    """
    square = [[127, 46, 58], [2, 113, 94], [74, 82, 97]]
    powermagic(square, warnings=True)
    return square, powermagic(square, diagonals=False, warnings=True)

def example6():
    """sixth example (Walter Trump [2002] - trimagic)

    See the MathWorld article [4] on trimagic squares.

    This is a smallest possible perfect trimagic square.  (Perfect here means
    that the square's entries are consecutive.  Smallest refers to the order.
    Note that there are eight congruent magic squares -- the dihedral group
    acting on the matrix by rotation and reflection -- so there are necessarily
    at least eight order 12 trimagic squares.)

    The earliest trimagic known square was an order 128 magic square constructed
    by G Tarry in 1906 -- about 35 to 50 years before the advent of practical
    digital computers.  (The NumberPhile video [1] mentions the feat and briefly
    displays a spreadsheet which contains Tarry's trimagic square.)

    The first digital computers were weaving looms that used punched cards.
    (See the Wikipedia article [5] on Jacquard looms.)  Inspired by the looms,
    Charles Babbage designed and patented the first digital computer in 1837,
    but failed to build it because of conflicts with the chief engineer and
    insufficient funds.  (See also [6] for more information.)
    """
    square = [[  1,  22,  33,  41,  62,  66,  79,  83, 104, 112, 123, 144], # 1
              [  9, 119,  45, 115, 107,  93,  52,  38,  30, 100,  26, 136], # 2
              [ 75, 141,  35,  48,  57,  14, 131,  88,  97, 110,   4,  70], # 3
              [ 74,   8, 106,  49,  12,  43, 102, 133,  96,  39, 137,  71], # 4
              [140, 101, 124,  42,  60,  37, 108,  85, 103,  21,  44,   5], # 5
              [122,  76, 142,  86,  67, 126,  19,  78,  59,   3,  69,  23], # 6
              [ 55,  27,  95, 135, 130,  89,  56,  15,  10,  50, 118,  90], # 7
              [132, 117,  68,  91,  11,  99,  46, 134,  54,  77,  28,  13], # 8
              [ 73,  64,   2, 121, 109,  32, 113,  36,  24, 143,  81,  72], # 9
              [ 58,  98,  84, 116, 138,  16, 129,   7,  29,  61,  47,  87], # 10
              [ 80,  34, 105,   6,  92, 127,  18,  53, 139,  40, 111,  65], # 11
              [ 51,  63,  31,  20,  25, 128,  17, 120, 125, 114,  82,  94]] # 12
    MagicSquare.from_sq(square)     # this verifies that we have a magic square
    return square, powermagic(square, warnings=True), \
           powermagic(square, warnings=True, d=3)

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

    print("-"*72)
    print("Example 5 (Gardner square):")
    square, power = example5()
    print("Not magic:", square)
    print("Square of squares is semimagic!")

    print("-"*72)
    print("Example 6 (Walter Trump's 12x12 trimagic square):")
    square, power, cube = example6()
    magic = MagicSquare.from_sq(square)
    print(f"Magic: (order={len(magic)}, magic number={magic.magic})")
    for i in range(12):
        print("\t", end="")
        for j in range(12):
            print("%4d" % square[i][j], end="")
        print()
    print(f"Square of squares is magic! (magic number={power.magic})")
    print(f"Square of cubes is also magic! (magic number={cube.magic})")

