"""
leaper_demo.py - create a magic squares using leaper moves
Copyright © 2023 by Eric Conrad

USAGE

    python leaper_demo.py [-h] [-o OUTPUT] [-s y x] n p q
    create a magic squares using leaper moves

    POSITIONAL ARGUMENTS
        n                     magic square order (odd)
        p                     leaper parameter p
        q                     leaper parameter q

    OPTIONS
        -h, --help            show this help message and exit
        -o OUTPUT, --output OUTPUT
                output csvfile path (default: console)
        -s y x, --start y x   
            start position for the leaper (default: t m).
            Row number y:
                an integer or "t", "m", "b" for top, middle, bottom,
                or "[t/m/b][+/-][integer]" for a relative row.
            Column number x
                an integer or "l", "m", "r" for left middle right, or 
                "[t/m/b][+/-][integer]" for a relative column.
            These values are reduced modulo n, so (for example) "t-2"
            and "b-1" are the same row."

        (p,q) = fairy chess leaper move (a knight is a (2,1) leaper).
        Necessary, but not sufficientn are that n>p>q and these three
        values must be relatively prime.

        Suggestion: try n=7, p=3, q=1. Then experiment.

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
from math import gcd
from magic_squares import logger

from magic_squares.magic_square import MagicSquare, SiameseMagicSquare
from magic_squares.spreadsheet import SpreadsheetManager as SM
from magic_squares.line_bundle import BundledMagicSquare

def get_base_square(n:int) -> MagicSquare:
    """create a magic square of given order from scratch"""

    def odd_square(n:int) -> MagicSquare:
        """returns a magic square of odd order"""
        return SiameseMagicSquare(n)

    def evenly_even_square(n:int) -> MagicSquare:
        """returns a magic square of evenly even order"""
        from magic_squares.doubly_even import DoublyEven

        k = n // 4
        return DoublyEven(k)

    def oddly_even_square(n:int) -> MagicSquare:
        """returns a magic square of oddly even order"""
        from magic_squares.al_Antaki import alAntakiOddlyEven

        k = n // 4
        return alAntakiOddlyEven(evenly_even_square(4*k))

    if n % 2 == 1:
        return odd_square(n)
    if n % 4 == 0:
        return evenly_even_square(n)
    return oddly_even_square(n)

def validate_source(source):
    """validate the source magic square"""
    n = source.n
    source_set = set(source.matrix.values())
    target_set = set(list(range(1,n*n+1)))
    if source_set != target_set:
        print("  Missing:", target_set - source_set)
        print("Extraneous:", source_set - target_set)
        raise ValueError("Entries of the matrix to frame must be 1..n")

def main(argv):
    """main routine"""
    import argparse

    DESC = "create a magic square using line bundles"
    EPILOG = ""
        
    parser = argparse.ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument("-o", "--output", type=str, default=None, \
        help="output csvfile path (default: console)")
    parser.add_argument("-n", "--order", type=int, default=4, \
        metavar="n", \
        help="order of the magic square to be framed. Ignored if" \
        + " the input is from a spreadsheet.")
    parser.add_argument("-i", "--input", type=str, default=None, \
        help="input file (CSV).")
    parser.add_argument("-e", "--echo", action="store_true", \
        help="echo the input square")
    parser.add_argument("-f", "--reflect", type=str, default=None, \
        help="an optional reflection.  Possibilities are horizontal" \
        + ", vertical, diagonal or antidiagonal.  Only the first " \
        + "letter is significant: h-horizontal, v-vertical, " \
        + "d-diagonal, a-antidiagonal. Omit for no flip.  Rotations" \
        + " take place after the flip.")
    parser.add_argument("-r", "--rotate", type=int, default=0, \
        help="number of counterclockwise right angle rotations to " \
        + "apply to the input.  Negative is clockwise.")
    parser.add_argument("-a", "--algorithm", type=int, default=0, \
        help="algorithm for framing (default 0)")
    parser.add_argument("-R", "--randomize", action="store_true", \
        help="make random choices")
    parser.add_argument("-T", "--trace", action="store_true", \
        help="display the line bundle activity")
#    parser.add_argument("-c", "--corners", nargs=2, type=int, \
#        default=None, metavar=("TL", "BL"), \
#        help="the respective values to be placed in the top left " \
#        + "and bottom left corners.  These can be drawn from 1 " \
#        + "through 2n+2 or from n²-2n-1 through n².  Their sum cannot" \
#        + "be n²+1.  Some pairs may yield no solutions.")

    args = parser.parse_args(argv)
    if args.input:
        pass
    elif args.order:
        source = get_base_square(args.order)
    else:
        raise ValueError("Either a source file or an order must be" \
            + " specified")
    if args.echo:
        print("Input:")
        print("\tName:", getattr(source, "name", "--unknown--"))
        print("\tOrder:", source.n)
        print(source)
    validate_source(source)
    if args.reflect:
        flip = args.reflect[0]
        source = source.reflect(flip)
        if args.echo:
            print(f"Reflect({flip}):")
            print(source)
    rotate = args.rotate % 4
    if rotate:
        source = source.rotate(rotate)
        if args.echo:
            print(f"Rotate({rotate}):")
            print(source)
    result = BundledMagicSquare(source, algorithm=args.algorithm,
                                randomize=args.randomize,
                                trace=args.trace)
    print("Result:")
    print(result)
    result.check()
    assert result.magic == result.n * (result.n ** 2 + 1) // 2

if __name__ == "__main__":
    import sys
    import logging
    logger.setLevel(logging.DEBUG)
    main(sys.argv[1:])

