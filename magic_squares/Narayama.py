"""
Narayama.py - the Narayama-de la Hire algorithm for magic squares
Copyright © 2023 by Eric Conrad

    The algorithm is discussed briefly in the documentation for class
    NarayamaMagic.  The discussion presumes familiarity with Euler's
    method.

    See also: https://en.wikipedia.org/wiki/Magic_square
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
import sys
from magic_squares import logger
from magic_squares.listlike2D import listlike2D
from magic_squares.Euler import GraecoLatinMagic

class NarayamaMagic(GraecoLatinMagic):
    """a magic square built from 'criss-cross' squares

    The Narayama de la Hire method involves a weakening of the rules
    for Euler's method when the order n is even.  For odd orders,
    the two methods are identical.

    EULER'S RULES FOR EVEN ORDER

        1.  In the Greek square, in each row, in each column and in
            each of the two diagonals, each letter appears exactly once.

        2.  In the Latin square, in each row, in each column and in
            each of the two diagonals, each letter appears exactly once.

        3.  In the Graeco-Latin square, each entry is unique.

    NARAYAMA'S OPTIONS

        4.  In place of (1) and (2):

            (a) In the Greek square, in each row and on each diagonal,
                each letter appears exactly once, while in each column
                just two letters appear, each in exactly half of the
                entries in the column.

            (b) In the Latin square, in each column and on each
                diagonal, each letter appears exactly once, while in
                each row just two letters appear, each in exactly
                half of the entries in the row.

        4'. As an alternative to 4, in place of (1) and (2), we can
            interchange the Greek and the Latin squares in 4(a)
            and 4(b).

    Rule 3 still applies to the merged Graeco-Latin square.

    Because rows and columns have duplicate entries, there are some
    necessary restrictions on permutations of {0, 1, ..., n-1) which
    can be used as substitions.  For example, if n=4 and the letters
    a and d appear in the same column, then we require that a+d=3,
    limiting (a,d) to (0,3), (3,0), (1,2) or (2,1).
    """

    def init_Latin_square(self, latin:listlike2D,
                          n:int, name:str) -> listlike2D:
        """wrapper for the initializing the Latin squares"""
        if isinstance(latin, (tuple, list)):
            latin = listlike2D(latin, n, n)         # wrapper

        msg = self.criss_cross_type(latin, name)
        if msg:
            msg = self.__class__.__name__ + "(" + name + ")" + msg
            logger.warning(msg)

        if "latin" in self.settings:
            p1, q1 = self.settings["greek"]
            p2, q2 = self.settings["latin"]
            if p1 != q2 or p2 != q1:
                msg = f'greek {p1},{q1}, latin {p2}, {q2}:'
                msg += 'p1 != q2 or p2 != q1'
                logger.warning(msg)

        return latin

    def criss_cross_type(self, latin, name) -> str:
        """determine whether this is a criss-cross square"""
        n = self.n
        row0 = set()
        col0 = set()
        for i in range(n):
            row0.add(latin[(0,i)])
            col0.add(latin[(i,0)])
        p, q = len(row0), len(col0)
        self.settings[name] = (p, q)
        if max(p,q) != n:
            return f'({name}) max({p},{q}) != {n}'
        items = row0 | col0
        if len(items) != n:
            return f'|{name}[{0},*]∪{name}[*,{0}]|={len(items)}' \
                + f' (exp: {n})'
        if n % p != 0 or n % q != 0:
            return f'p={p}, q={q} but n={n} -- orbit error'

            # check rows and columns and domain
        for i in range(1, n):
            row = set()
            col = set()
            for j in range(n):
                item = latin[(i, j)]
                if not item in items:   # domain check
                    return f'unexpected item at {name}[{i},{j}]'
                row.add(item)
                item = latin[(j, i)]
                col.add(item)
            if len(row) != p:
                return f'|{name}[{i},*]| != {p}'
            if len(col) != q:
                return f'|{name}[*,{i}]| != {q}'

            # check diagonals
        diag1 = set()
        diag2 = set()
        for i in range(n):
            diag1.add(latin[(i, i)])
            diag2.add(latin[(n-i-1, n-i-1)])
        diag1 = len(diag1)
        diag2 = len(diag2)
        if not diag1 in {1, n}:
            return f'{name} main diagonal has {diag1} distinct items'
        if not diag2 in {1, n}:
            return f'{name} antidiagonal has {diag2} distinct items'
        if max(diag1, diag2) != n:
            return f'{name} diagonals max({diag1},{diag2}) != {n}'

            # two checks logged as info rather than warning
            #   (They violate the algorithm requirements as given
            #   in the Wikipedia article, but if there is a problem.
            #   the orthogonality check will probably scream.)

        if n // p > 2:
            logger.info(f'{name} n={n} p={p} n//p>2')
        if n // q > 2:
            logger.info(f'{name} n={n} p={q} n//q>2')

        return ""           # nothing notewothy

def test_4_by_4(quiet=True):
    """run tests using 4x4 orthogonal Latin squares

    If no exceptions are raised, then the test is successful
    """
    from random import choice

    class Foo(object):
        """mapping class"""

        def __init__(self, alpha, beta, gamma, delta, a, b, c, d):
            """set up the mapping as a dictionary"""
            self.bar = {'α':alpha, 'β':beta, 'γ':gamma, 'δ':delta,
                        'a':a,     'b':b,    'c':c,     'd':d}

        def foobar(self, gee, ell, n):
            """a little-endian mapper"""
            x = self.bar[gee]
            y = self.bar[ell]
            return n*x + y + 1

        def foobaz(self, gee, ell, n):
            """a big-endian mapper"""
            x = self.bar[gee]
            y = self.bar[ell]
            return x + n*y + 1

    def print4(greek, latin):
        """display a 4x4 Graeco-Latin square"""
        print("Graeco-Latin square:")
        for i in range(4):
            s = ""
            for j in range(4):
                s += "   " + greek[i][j] + latin[i][j]
            print(s)

    def test(alpha, beta, gamma, delta, a, b, c, d):
        """run two tests"""
        fmt = f"Narayama({alpha}{beta}{gamma}{delta}|{a}{b}{c}{d})" \
            + "/(%s) > 4x4 magic square:"
        foo = Foo(alpha, beta, gamma, delta, a, b, c, d)
        print(fmt % "HL")           # "little endian" - high-low
        magic = NarayamaMagic(n, greek, latin, mapping=foo.foobar)
        print(magic)
        print(fmt % "LH")           # "big endian" - low-high
        magic = NarayamaMagic(n, greek, latin, mapping=foo.foobaz)
        print(magic)

    #     GREEK SQUARE    LATIN SQUARE      GRAECO-LATIN
    #     ============    ============      ============
    #       α β γ δ         b c a d         αb βc γa δd
    #       δ γ β α         a d b c         δa γd βb  αc
    #       β α δ γ         d a c b         βd αa δc γb
    #       γ δ α β         c b d a         γc δb αd βa

    n = 4
        # Create a 4x4 semi-Greek square (rows excepted)
    alpha, beta, gamma, delta = 'α', 'β', 'γ', 'δ'
    greek = [[alpha, delta, delta, alpha],
             [gamma, beta, beta, gamma],
             [beta, gamma, gamma, beta],
             [delta, alpha, alpha, delta]]

        # Create a 4x4 semi-Latin square (columns excepted)
    a, b, c, d = 'a', 'b', 'c', 'd'
    latin = [[a, c, b, d],
             [d, b, c, a],
             [d, b, c, a],
             [a, c, b, d]]

        # Check orthogonality
    msg = GraecoLatinMagic.are_orthogonal(greek, latin, 4)
    if msg:
        raise ValueError("(greek ⟂ latin) " + msg)
    print4(greek, latin)

    print("There are 4 choices for α from the set {0,1,2,3}...")
    print("With α chosen, there are 2 available choices for β...")
    print("That gives 4·2=8 choices for α and β, likewise for a and b.")
    print("Square that: 8²=64 for two independent permutations")
    print("Double that: 2·64=128 for base-4 digit ordering...")
    print("128 magic squares can be generated by this procedure.")
    print("We will choose just five pairs of permutations,",
          "with four chosen randomly,")
    print("  to produce just ten of these magic squares")

    permutations = set()
    permutations.add((0,1,2,3, 0,1,2,3))    # a=α=0, b=β=1, etc.
        # first choose a in 4 ways, then b in 2.  Then c=3-b, d=3-a
    choices = [[0,1,2,3], [0,2,1,3], [1,0,3,2], [1,3,0,2],
               [2,0,3,1], [2,3,0,1], [3,1,2,0], [3,2,1,0]]
    while len(permutations) < 5:
        sigma1 = choice(choices)
        sigma2 = choice(choices)
        sigma = tuple(sigma1 + sigma2)
        permutations.add(sigma)
    permutations = list(permutations)
    permutations.sort()
    # print(permutations)

    for sigma in permutations:
        test(*sigma)

    if not quiet:
        print("4x4 test", \
            "(10 magic squares from 1 Graeco-Latin square)" \
            + "... passed!")


def main(argv:list) -> int:
    """parse exguments"""
    import argparse

    DESCRIPTION = 'Create a magic square "á la méthode Eulerienne".'
    EPILOG = "Narayama's method uses pseudo-Graeco-Latin squares."
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     epilog=EPILOG)
    parser.add_argument("-4", "--magic4", action="store_true", \
        help="run the 3x3 matrix test (eight magic squares)")
    parser.add_argument("-v", "--verbose", action="store_true", \
        help="include commentary")
    args = parser.parse_args()

    if args.verbose:
        print(__doc__)
        print("\n\nclass GraecoLatinMagic(MagicSquare):")
        print(GraecoLatinMagic.__doc__)

    tests = 0
    if args.magic4:
        tests += 1
        test_4_by_4(not args.verbose)

    if tests:
        print(f'{tests} test modules attempted and passed')
    else:
        if not args.verbose:
            print("No tests were attempted.  For help, run with '-h'.")
            return 0
    
    print("SUCCESS!")
    return 0

if __name__ == "__main__":
        # testing
    sys.exit(main(sys.argv[1:]))
