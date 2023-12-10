"""
composition.py - a composition algorithm for doubly even magic squares
Copyright © 2023 by Eric Conrad

DESCRIPTION

    Suppose we have an even magic order magic square M of order m with
    enries from 1 through m², inclusive, and a square matrix N of order
    n with entries from 1 through n², inclusive.  We construct a
    square m×n composition matrix C as follows:

        C is a square block matrix consisting of n² blocks of order m
        matrices.  Suppose N[i,j]=p.  Let M(i,j) denote the (i,j) block
        of the result C.  The rules for constructing M(p) are as
        follows:

            1) if M[a,b] ≤ m²/2, then:
                    M(i,j)[a,b] = (p-1)m²/2 + M[a,b]; and
            2) if M[a,b] > m²/2, then:
                    M(i,j)[a,b] = (mn)² - (p+1)m²/2 + M[a,b].

EXAMPLE ONE

    As an example, let M be the magic square from Albrecht Dürer's
    drawing Melencolia I (1514):

            16   3   2  13
             5  10  11   8
             9   6   7  12
             4  15  14   1

    Let N be the identity matrix of order 1:

            1

    Then C has a single block subject to the following rules:
            1) M(1,1)[a,b] = (p-1)m²/2 + M[a,b] = M(a,b); and
            2) M(i,j)[a,b] = (mn)² - (p+1)m²/2 + M[a,b] = M[a,b]

    So C = M.

EXAMPLE TWO

    Let M be the Dürer square again.

    Let N be the 2×2 matrix:

            1  2
            3  4

    Then our blocks are:

            M(1,1)                  M(1,2)
            64   3   2  61          56  11  10  53
             5  58  59   8          13  42  43  16
            57   6   7  60          49  14  15  52
             4  63  62   1          12  55  54  9

            M(2,1)                  M(2,2)
            48  19  18  45          40  27  26  37
            21  42  43  24          29  34  35  32
            41  22  23  44          33  30  31  36
            20  47  46  17          28  39  38  25

    Analyzing our blocks:
    
        (1) The Dürer square has two entries below 9 an two entries
            above 8 on each row, column or diagonal.  The magic
            constant of the Dürer square is 34.

            The magic constant of any block is:
                64 + 3 + 2 + 61 = 125 + 5 = 130.

            Each of the four blocks is a magic square.

        (2) For an arbitrary traditional square M of order m, the magic
            constant is:
                x = m (m² + 1) / 2

            If M is of even order and exactly half of the entries in
            any given tier (row/column/diagonal) are below the median
            value (m+1)/2, then the magic number of a block will be:
                (m/2) ((mn)² - m²) + x = m ((mn)² + 1) / 2

            Evaluating this at m=4, n=2:
                2 (64 + 1) = 130, as expected. 

    Analyzing the large square as a whole, the sum along any tier
    is n times the magic constant of a block.  Then:

        (1) For the example, the magic constant is:

                2 (130) = 260.

        (2) In the general case, assuming that the prototype magic
            square has the same numbers of high and low entries, the
            magic constant is:

                n (m ((mn)² + 1) / 2) = (mn) ((mn)² + 1) / 2.

        (3) The magic constant of an order mn traditional magic square
            is the mn(th) triangular number divided by mn, or

                mn ((mn)² + 1) / 2, as expected.

            Evaluating at m=4, n=2:

                8 (64 + 1) / 2 = 4 (65) = 2 (130) = 260, as expected.

    See https://en.wikipedia.org/wiki/Magic_square
        article title: Magic square
        topic: Special methods of construction

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
import traceback
from fractions import Fraction

from magic_squares import logger
from magic_squares.magic_square import MagicSquare
from magic_squares.listlike2D import listlike2D

class Composite(MagicSquare):
    """a type of doubly even magic square"""

    def __init__(self, even_sq:MagicSquare, template:listlike2D,
                 diagonals:bool=True, debug:bool=False,
                 warnings:bool=True,
                 f:callable=None, g:callable=None):
        """constructor

        REQUIRED ARGUMENTS

            even_sq - a magic square of even order m; in each tier (row,
                column, or diagonal), half the entries should be below
                the median value and half should be above it.

            template - a square matrix of order n containing each of the
                integers from 1 through n² -- list, tuple, listlike2D,
                or MagicSquare are all accepted; this does not need to
                be a magic square.

        KEYWORD ARGUMENTS

            diagonals (default True)
                if False, a semimagic square is acceptable.

            debug (default False)
                if True, the constructor will not check the magic
                property; in this case, the sum of the first row (i.e.
                row 0) is used in lieu of the magic number.

            warnings (default True)
                if False, warning messages will be suppressed.

            f (default None)
            g (default None)
                If even_sq is an even square of order m with entries
                1 through m, then:
                    f(m, n, p, q) = (p-1)m²/2 + q
                    g(m, n, p, q) = (mn)² -  (p+1)m²/2 + q
                The parameters m and n are the orders of the even square
                and the template matrix, respectively.  The parameter
                p is the applicable entry in the pattern matrix.  The
                parameter q is the applicable entry in the even order
                magic square.

                These methods can be used to tweak the algorithm to
                allow for more exotic imputs and/or compositions.
                Unless you are doing something exotic, leave them
                alone.
        """
        self._even_sq = even_sq
        m = even_sq.n
        n = len(template)
        self._pattern = listlike2D(template, n, n) \
            if isinstance(template, (list, tuple)) \
            else template
        self._f = f
        self._g = g
        self.name = f"composition magic square ({m}·{n}×{m}·{n})"
        if getattr(even_sq, "name", None):
            self.name += f" < {even_sq.name}" 
        self._warnings = warnings
        super().__init__(m*n, diagonals=diagonals, debug=debug)

    def configure(self):
        """creation algorithm"""
        warnings = 0
        even = self._even_sq
        m = even.n

        pattern = self._pattern
        n = pattern.n
        f = self._f if callable(self._f) \
            else lambda m, n, p, q: (p-1) * m *m // 2 + q
        g = self._g if callable(self._g) \
            else lambda m, n, p, q: ((m*n)**2) - (p+1) * m * m // 2 + q

        s = 0
        for i in range(m):
            for j in range(m):
                s += even[(i, j)]
        mean = Fraction(s, m*m)

        if self._warnings:
            self.validate_parameters(even, m, pattern, n, mean)

        for a in range(self.n):
            for b in range(self.n):
                i, j = a // m, b // m       # coordinates of the block
                p = pattern[(i, j)]
                i, j = a % m, b % m         # in-block coordinates
                q = even[(i, j)]
                self[(a,b)] = f(m, n, p, q) if q < mean \
                    else g(m, n, p, q)

    def validate_parameters(self, even, m, pattern, n, mean):
        """issue warnings if the parameters are exotic"""
        warnings = 0
        if m % 2 != 0:
            logger.warning("The order of M is {m} which is odd; "
                + "an even integer is expected.")
            warnings += 1

        if callable(self._f) or callable(self._g):
            logger.warning("The functions f and g have been modified")
            warnings += 1

        expected = Fraction((m*m +1), 2)
        if mean != expected:
            logger.warning(f"The mean value for M is {mean}; " \
                + f"expected: {expected}.  The entries of M are not " \
                + "a permutation of 1..m².")
            warnings += 1

        lows = 0
        for i in range(m):
            for j in range(m):
                if even[(i, j)] < mean:
                    lows += 1
        if lows != Fraction(m*m, 2):
            logger.warning(f"The mean value for M is {mean}; " \
                + f"expected: {expected}.  Exactly half the entries " \
                + "of M should be less than the mean.")
            warnings += 1

        foo = set()
        for i in range(n):
            for j in range(n):
                foo.add(pattern[(i, j)])
        if foo != set(range(1, n*n+1)):
            logger.warning("The pattern set N is not " \
                + f"{{1..n²}} where n={n}.")
            warnings += 1

        if warnings:
            logger.warning(f"{warnings} warnings issued. " \
                + "(But you know what you're doing, don't you?)")

def demo1(csvname:str, i:int, insert_i:bool):
    """input from CSV"""
    foo = None
    return foo

def demo2(base:MagicSquare, pattern:listlike2D,
         title:str) -> MagicSquare:
    """create a magic square"""
    try:
        result = Composite(base, pattern)
        if title:
            result.name = title
    except Exception as msg:
        traceback.print_exc()
        print(str(msg))
        result = None
    return result

def check_result(result:MagicSquare):
    """Checks to see whether everything is there"""
    n = result.n
    expected = set(range(1, n*n+1))
    got = set()
    missing = set()
    extraneous = set()
    for i in range(n):
        for j in range(n):
            got.add(result[(i,j)])
    if expected == got:
        result.check = "perfect"
        return missing, extraneous
    missing = expected - got
    extraneout = got - expected
    result.check = f'{len(missing)} missing items, ' \
        + f'{len(extraneous)} extraneous items'
    if len(extraneous) < len(missing):
        result.check += f', at least {len(missing)-len(extraneous)}' \
            + ' duplicate items'
    return missing, extraneous

def main(argv):
    """main routine"""
    import argparse
    from random import shuffle
    import logging
    logger.setLevel(logging.DEBUG)

    from magic_squares.spreadsheet import SpreadsheetManager as SM
    from magic_squares.order4 import Melencolia1514, Jupiter, \
        Parshavnatha
    Sol = [[6, 32, 3, 34, 35, 1], [7, 11, 27, 28, 8, 30],
           [19, 14, 16, 15, 23, 24], [18, 20, 22, 21, 17, 13],
           [25, 29, 10, 9, 26, 12], [36, 5, 33, 4, 2, 31]]
    Sol = MagicSquare.from_sq(Sol)
    Sol.name = "Sol (6×6)"

    DESC = "test the composition module"
    EPILOG = "If an exception is encountered during processing, " \
        + "the program will attempt to continue with subsequent " \
        + "input."
    parser = argparse.ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument("-n", "--dim_pattern", type=int, default=3, \
        metavar="n", \
        help="(default=3) order n of the pattern matrix N.")
    parser.add_argument("-s", "--shuffle", action="store_true", \
        help="shuffle the entries of pattern matrix.  By default " \
        + "the entries are 1 through n² in row major order.")
    parser.add_argument("-p", "--set_pattern", type=str, \
        metavar="string", \
        help="use the integers in the string as a pattern. " \
        + "The quoted string must contain the integers 1 through n² " \
        + "in some order, separated by spaces.  These will be " \
        + "entered into the pattern in row major order.")
    parser.add_argument("-q", "--quiet", action="store_true", \
        help="don't display the pattern.")
    parser.add_argument("-o", "--output", type=str, default=None, \
        help="an optional csv filename for the output magic square.")
    parser.add_argument("-d", "--description", type=str, default=None, \
        metavar="title", \
        help="an optional description for the output magic square")
    parser.add_argument("input", type=str, nargs="*", \
        help="a mix of reserved magic square names or csv pathmames " \
        + "to be used as input.  The following names are reserved: " \
        + "durer: Dürer's magic square; song34: the Chautisa Yantra; " \
        + "jove: Jupiter, sol: Sol.  If no inputs are entered, " \
        + "Dürer's magic square will be used.  Inputs must be even in" \
        + "order.")

    args = parser.parse_args(argv)
    n = args.dim_pattern

    default = list(range(1, n*n+1))
    if args.set_pattern:
        pattern = list(map(int, args.set_pattern.split()))
        assert sorted(pattern) == default
    else:
        pattern = default
        if args.shuffle:
            shuffle(pattern)
    pattern = [pattern[i:i+n] for i in range(0, len(pattern), n)]
    if not args.quiet:
        print("Pattern:", pattern)

    if not args.input:
        args.input = ["durer"]
    if args.output:
        last4 = args.output[-4:]
        if last4 == ".csv":
            output = args.output[:-4]
        else:
            output = args.output
            last4 = ".csv"
    item_num = 0
    num_items = len(args.input)

    # print(args)
    for item in args.input:
        item_num += 1
        print("Processing:", item, f'({item_num} of {num_items})')
            # determine the magic square input M
        reserved = {"durer": Melencolia1514, "song34": Parshavnatha,
                    "jove": Jupiter, "sol": Sol}
        if item in reserved:
            base = reserved[item]
        else:
            base = demo1(item, item_num, len(args.input)>1)
        if not base:
            continue
        foo = demo2(base, pattern, args.description)
        if not foo:
            print("\tFAILED!")
            continue
        missing, extraneous = check_result(foo)
        if missing:
            print("Missing entries:", missing)
        if extraneous:
            print("Extraneous entries", extraneous)
        if len(args.input) > 1:
            foo.name += f' [{item_num}]'
        if not args.output:
            print(foo.name)
            print(foo)
        csvname = output
        if len(args.input) > 1:
            csvname += f'({item_num})'
        csvname += last4
        print(f"Saving: {csvname}")
        SM.csv_writer(foo, csvname)

if __name__ == "__main__":
        # self-test
    import sys
    main(sys.argv[1:])

    print("SUCCESS!")
