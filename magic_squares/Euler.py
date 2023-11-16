"""
Euler.py - an Eulerian algorithm for constructing magic squares
Copyright © 2023 by Eric Conrad

    The algorithm is discussed at length in the documentation for
    class GraecoLatinMagic.  Examples are included.

    See also: https://en.wikipedia.org/wiki/Magic_square
        article title: Magic square
        topic: Special methods of construction

USAGE FOR TESTING

    python -m magic_squares.Euler [-h] [-T] [-3] [-4] [-v]
    Create a magic square "á la méthode Eulerienne".

    OPTIONS

        -h, --help       show this help message and exit
        -T, --self_test  run the self-test to check basic functionality
        -3, --trad3      run the 3x3 matrix test (eight magic squares)
        -4, --magic4     run the 3x3 matrix test (eight magic squares)
        -v, --verbose    include commentary

    Euler's method uses Graeco-Latin squares.

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
from magic_squares.magic_square import MagicSquare

class GraecoLatinMagic(MagicSquare):
    """a magic square built from a Graeco-Latin square

    A Latin square is an nxn square matrix whose entries are the first
    n letters of the Latin alphabet. (For values of n larger than 26
    [if we are using the English alphabet] or 23 [where as in Latin i=j,
    u=v, and there is no w], we can use subscripts or superscripts or
    other markings.  And, of course, any set of n distinguishable
    objects can be used in place of letters.)  Latin squares obey one
    of two orthogonality rules:

        A.  In each row, in each column, and in each of the two
            diagonals, every available letter appears exactly once.

        M.  For odd n only, in each row, in each column, and in one of
            the two diagonals, every available letter appears exactly
            once, and in the other diagonal, the median letter appears
            in each entry.

    For example, here are three isomorphic 3x3 Latin squares:

        0 2 1           a c b           α γ β
        2 1 0           c b a           γ β α
        1 0 2           b a c           β α γ

    In these examples, the middle symbol appears on the antidiagonal
    (running from SW to NE).  The top row contains, in order, the
    first, third, and second symbols in the square's alphabet.

    This is a Rule M Latin square,  In the numeric example, we choose
    consecutive base-n digits from 0 through n-1, in this case we
    are using ternary or base-3, so the digits are 0, 1 and 2.  The
    median value is (n-1)/2, in this case (3-1)/2=1.  We can transpose
    0 and 2 in the first example to obtain an isomorphic Latin square,
    but this is the only permissible permutation of 0, 1 and 2 as the
    median 1 must remain fixed.

    Here are three isomorphic 4x4 Latin squares:

        0 1 2 3         a b c d         α β γ δ
        3 2 1 0         d c b a         δ γ β α
        1 0 3 2         b a d c         β α δ γ
        2 3 0 1         c d a b         γ δ α β

    A Greek square is a Latin square where the Greek alphabet is used
    instead of the Latin alphabet.  Again, any set of distinguishable
    objects may be used in place of Greek letters.  This is a rule A
    Latin square, so we can apply any permutation of the digits 0, 1,
    2 and 3 to the first example to yield an isomorphic Latin square.

    A Graeco-Latin square is an nxn square matrix whose entries are
    ordered pairs.  There are three orthogonality conditions:

        1) The abscissae form a Greek square;
        2) The ordinates form a Latin square; and
        3) Each ordered pair appears exactly once.

    For a 3x3 Graeco-Latin Square, we need a Greek square and a Latin
    square of order 3, but the third condition implies that these
    two squares must not be isomorphic.  Let us try forming a Greek
    square where the main diagonal is constant... Then adjoin the
    3x3 Latin square above, and merge them:

        β α γ       a c b       βa αc γb
        γ β α       c b a       γc βb αa
        α γ β       b a c       αb γa βc

    Conditions (1) and (2) are satisfied by construction.  But what of
    condition (3)?

        Occurrences:
        Pair            αa  αb  αc  βa  βb  βc  γa  γb  γc
        Location        23  31  12  11  22  33  32  13  21
        Occurrences      1   1   1   1   1   1   1   1   1   Total=9

    In the first row of the table, we have listed all nine possible
    ordered pairs.  In the second row, we have given the row and column
    where that pair is located.  In the third row we have counted the
    number of observed occurrences of the pair.  But have we missed
    some occurrence?  We know that each pair occurs at least once.
    There are nine ones for a total of nine entries.  Since each
    pigeonhole (table entry) can hold exactly one pigeon (ordered
    pair), there is no place for another pigeon.  Thus the 3x3 matrix
    of ordered pairs is a Graeco-Latin square.

    Now how do we turn this into a magic square?  Bijectively map the
    ternary digits 0, 1 and 2 each of the two sets of letters.  For
    a square of odd order, we also need to make sure that the middle
    digit is mapped to the each of middle letters, so β=b=1.  Now
    interpret the entry as a base n number -- since n=3, this will
    be ternary.  By convention, finish by adding 1 to each entry.
    Depending on the map and our interpretation of ternary notation
    (i.e. is the most significant digit on the right or on the left?),
    we get an answer...

        Digit map:  α=a=0, β=b=1, and γ=c=2.
                                Little-endian       Big-endian
        βa αc γb    10 02 21    3 2 7   4 3 8       1 6 5   2 7 6
        γc βb αa    22 11 00    8 4 0   9 5 1       8 4 0   9 5 1
        αb γa βc    01 20 12    1 6 5   2 7 6       3 2 7   4 3 8

        Digit map:  α=a=2, β=b=1, and γ=c=0.
                                Little-endian       Big-endian
        βa αc γb    12 20 01    5 6 1   6 7 2       7 2 3   8 3 4
        γc βb αa    00 11 22    0 4 8   1 5 9       0 4 8   1 5 9
        αb γa βc    21 02 10    7 2 3   8 3 4       5 6 1   6 7 2

    SYMMETRIES

        In the 3x3 case, we end up with four of the eight possible
        traditional 3x3 magic squares with entries from 1 through 9.
        Using big-endian ternary instead of little-endian ternary
        amounts to a reflection through the second row.  Notice that
        the second mapping produced 180-degree rotations about the
        center.  Composing the mapping change and the ternary digit
        order produces a reflection through the the second column.
        (Making no change in mapping or in digit order results in no
        change in the magic square -- this is the identity
        transformation.)
    
        Note that we omitted two additional mappings:

            Digit map:  α=c=0, β=b=1, and γ=a=2.
            Digit map:  α=c=2, β=b=1, and γ=a=0.
    
        These will give the four remaining Luo Shu 3x3 squares as well
        as the four missing symmetries (90-degree and 270-degree
        rotations and reflections through the diagonals) in the
        dihedral group D(4) on a square.

        With a larger order, there will be more symmetries associated
        with a single Graeco-Latin square as there are more degrees of
        freedom in assigning the digits. (The symmetry group in this
        case will contain the dihedral group D(4) as a proper
        subgroup.)
    """

    def __init__(self, n:int, greek:listlike2D, latin:listlike2D,
                 mapping=None, debug=False):
        """constructor

        REQUIRED ARGUMENTS

            n - the order of the magic square to be produced

            greek - a Greek square with integer entries (see below)

            latin - a Latin square with integer entries (see below)

        KEYWORD ARGUMENTS

            mapping (default: f(x,y,n) = n*x + y + 1)
                a pure function with three arguments which transforms
                entries of the two input squares into entries of the
                resulting magic squares.  The arguments are an entry
                of the Greek square, an entry of the latin square
                and the order (n) of the resulting magic square.

                If the entries of the input squares are integers, then
                this must be a function which takes three integers as
                its arguments.

            debug (default: False)
                if True, the check for validity will be suppressed

        INPUT GREEK and LATIN SQUARES

            The input squares may be either lists or tuples or matrices
            that are duck-type-compatible with listlike2D structures.
            Lists and tuples will be incorporated into listlike2D
            structures so that they can be accessed by 2-tuple indices.

            There are static methods which can be used to check a
            priori that the input squares are valid and orthogonal.
        """
                    # wrap lists and tuples
        self.n = n
        self.settings = {}                  # subclass hook
        self.greek = self.init_Latin_square(greek, n, "greek")
        self.latin = self.init_Latin_square(latin, n, "latin")
        msg = self.are_orthogonal(greek, latin, n)
        if msg:
            logger.warning(self.__class__.__name__ + msg)

        if not bool(mapping):
            mapping = lambda gee, ell, n: n*gee + ell + 1
        self.mapping = mapping

        super().__init__(n, debug=debug)

    def init_Latin_square(self, latin:listlike2D,
                          n:int, name:str) -> listlike2D:
        """wrapper for the initializing the Latin squares"""
        if isinstance(latin, (tuple, list)):
            latin = listlike2D(latin, n, n)

        msg = self.is_Latin(latin, n)
        if msg:
            msg = self.__class__.__name__ + "(" + name + ")" + msg
            logger.warning(msg)

        return latin

    @staticmethod
    def is_Latin(latin:listlike2D, n:int=None) -> str:
        """test whether a square matrix is a Latin square

        DESCRIPTION

            If n is zero or none, then the len function will be used to
            determine the order.  The  input may be a tuple or a list.

            The return value is a string which reports the first
            detected failure.  If no errors are detected, the empty
            string is returned.

        EXCEPTIONS

            IndexError is raised if there is an attempt to access an
            undefined location.

            Badly formatted data may raise other exceptions.
        """
        if not bool(n):
            n = len(latin)
        if n <= 0:
            return "Invalid length"

        if isinstance(latin, (tuple, list)):
            latin = listlike2D(latin, n, n)     # assume square

            # determine the allow
        items = set()
        for j in range(n):
            items.add(latin[(0,j)])
        if len(items) != n:
            return "Duplicate entry in row 0"

            # check the remaining rows
        for i in range(1, n):
            objs = set()
            for j in range(n):
                objs.add(latin[(i,j)])
            if objs != items:
                return f"Invalid or duplicate entry in row {i}"

            # check the columns
        for j in range(n):
            objs = set()
            for i in range(n):
                objs.add(latin[(i,j)])
            if objs != items:
                return f"Invalid or duplicate entry in column {j}"

            # if we get here, then every entry is a member of the
            # set of entries in the first row.

            # check the diagonals
        diag1 = set()
        diag2 = set()
        for i in range(n):
            diag1.add(latin[(i,i)])             # main diagonal
            diag2.add(latin[(i,n-i-1)])         # antidiagonal

        diag1 = len(diag1)      # all we need are the number of members
        diag2 = len(diag2)

        if diag1 == n and diag2 == n:
            return ""                           # SUCCESS!

        if n % 2 == 0:                  # even order failure
            if diag1 != n:
                return f"Duplicate entry in main diagonal"
            return  f"Duplicate entry in antidiagonal"

                # odd order
        if diag1 == n:
            if diag2 == 1:
                return ""                       # SUCCESS!
            return f"More than one element in antidiagonal"

        if diag2 == n:
            if diag1 == 1:
                return ""                       # SUCCESS!
            return f"More than one element in main diagonal"

        return "Neither diagonal is full"

    @staticmethod
    def are_orthogonal(greek:listlike2D, latin:listlike2D,
                       n:int=None) -> str:
        """check to see if the Latin squares are orthogonal"""
        if not bool(n):
            n = len(greek)
        if isinstance(greek, (list, tuple)):
            greek = listlike2D(greek, n, n)
        if isinstance(latin, (list, tuple)):
            latin = listlike2D(latin, n, n)
        pairs = set()
        for i in range(n):
            for j in range(n):
                pair = (greek[(i,j)], latin[(i,j)])
                pairs.add(pair)
        if len(pairs) == n * n:
            return ""                           # SUCCESS!
        return f'(orthonality) {len(pairs)} pairs, expected {n*n}'

    def configure(self):
        """creation algorithm"""
        greek = self.greek
        latin = self.latin
        f = self.mapping
        n = self.n

        for i in range(n):
            for j in range(n):
                x = greek[(i, j)]
                y = latin[(i, j)]
                z = f(x, y, n)
                self[(i, j)] = z

def self_test(quiet=True):
    """test some basic stuff"""
            #   GREEK       LATIN     GRAECO-LATIN
            #   =====       =====     ============
            #   β α γ       a c b       βa αc γb
            #   γ β α       c b a       γc βb αa
            #   α γ β       b a c       αb γa βc

        # Create a 3x3 Greek square
    alpha, beta, gamma = 'α', 'β', 'γ'
    greek = [[beta, alpha, gamma],
             [gamma, beta, alpha],
             [alpha, gamma, beta]]

    msg = GraecoLatinMagic.is_Latin(greek)
    if msg:
        raise ValueError("(greek) " + msg)

        # Create a 3x3 Latin square
    a, b, c = 'a', 'b', 'c'
    latin = [[a, c, b],
             [c, b, a],
             [b, a, c]]

    msg = GraecoLatinMagic.is_Latin(latin)
    if msg:
        raise ValueError("(latin) " + msg)

    msg = GraecoLatinMagic.are_orthogonal(greek, latin, 3)
    if msg:
        raise ValueError("(greek ⟂ latin) " + msg)

        # test some non-Latin squares
    foo = [[1,1,1],[1,1,1],[1,1,1]]  # first row
    msg = GraecoLatinMagic.is_Latin(foo)
    if not msg:
        raise ValueError("111/111/111 is NOT a Latin square!")

    foo = [[1,2,3],[2,1,4],[1,1,1]]  # second row
    msg = GraecoLatinMagic.is_Latin(foo)
    if not msg:
        raise ValueError("123/214/111 is NOT a Latin square!")

    foo = [[1,2,3],[2,3,1],[3,2,1]]  # second column
    msg = GraecoLatinMagic.is_Latin(foo)
    if not msg:
        raise ValueError("123/231/321 is NOT a Latin square!")

    msg = GraecoLatinMagic.are_orthogonal(greek, latin)
    if msg:
        raise ValueError("(greek⟂latin) " + msg)

    if not quiet:
        print("Self-test passed!")

def test_3_by_3(quiet=True):
    """run tests using 3x3 orthogonal Latin squares

    If no exceptions are raised, then the test is successful
    """
    class Foo(object):
        """mapping class"""

        def __init__(self, alpha, beta, gamma, a, b, c):
            """set up the mapping as a dictionary"""
            self.bar = {'α':alpha, 'β':beta, 'γ':gamma,
                        'a':a,     'b':b,    'c':c}

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

    def print3(greek, latin):
        """display a 3x3 Graeco-Latin square"""
        print("Graeco-Latin square:")
        for i in range(3):
            s = ""
            for j in range(3):
                s += "   " + greek[i][j] + latin[i][j]
            print(s)

    def test(alpha, beta, gamma, a, b, c):
        """run two tests"""
        fmt = f"Euler({alpha}{beta}{gamma}|{a}{b}{c})/(%s) >" \
            + " 3x3 magic square:"
        foo = Foo(alpha, beta, gamma, a, b, c)
        print(fmt % "HL")           # "little endian" - high-low
        magic = GraecoLatinMagic(n, greek, latin, mapping=foo.foobar)
        print(magic)
        print(fmt % "LH")           # "big endian" - low-high
        magic = GraecoLatinMagic(n, greek, latin, mapping=foo.foobaz)
        print(magic)

        # Latin squares
    n = 3
    alpha, beta, gamma = 'α', 'β', 'γ'
    greek = [[beta, alpha, gamma],
             [gamma, beta, alpha],
             [alpha, gamma, beta]]
    msg = GraecoLatinMagic.is_Latin(greek)
    if msg:
        raise ValueError("(greek) " + msg)

    a, b, c = 'a', 'b', 'c'
    latin = [[a, c, b],
             [c, b, a],
             [b, a, c]]

    print3(greek, latin)
    msg = GraecoLatinMagic.is_Latin(latin)
    if msg:
        raise ValueError("(latin) " + msg)

    msg = GraecoLatinMagic.are_orthogonal(greek, latin, 3)
    if msg:
        raise ValueError("(greek ⟂ latin) " + msg)

        # run 8 tests
    test(1,2,3,1,2,3)
    test(3,2,1,1,2,3)
    test(3,2,1,3,2,1)
    test(1,2,3,3,2,1)

    if not quiet:
        print("3x3 test (8 magic squares from 1 Graeco-Latin square)" \
            + "... passed!")

def test_4_by_4(quiet=True):
    """run tests using 4x4 orthogonal Latin squares

    If no exceptions are raised, then the test is successful
    """
    from random import shuffle

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
        fmt = f"Euler({alpha}{beta}{gamma}{delta}|{a}{b}{c}{d})" \
            + "/(%s) > 4x4 magic square:"
        foo = Foo(alpha, beta, gamma, delta, a, b, c, d)
        print(fmt % "HL")           # "little endian" - high-low
        magic = GraecoLatinMagic(n, greek, latin, mapping=foo.foobar)
        print(magic)
        print(fmt % "LH")           # "big endian" - low-high
        magic = GraecoLatinMagic(n, greek, latin, mapping=foo.foobaz)
        print(magic)

    #     GREEK SQUARE    LATIN SQUARE      GRAECO-LATIN
    #     ============    ============      ============
    #       α β γ δ         b c a d         αb βc γa δd
    #       δ γ β α         a d b c         δa γd βb  αc
    #       β α δ γ         d a c b         βd αa δc γb
    #       γ δ α β         c b d a         γc δb αd βa

    n = 4
        # Create a 4x4 Greek square
    alpha, beta, gamma, delta = 'α', 'β', 'γ', 'δ'
    greek = [[alpha, beta, gamma, delta],
             [delta, gamma, beta, alpha],
             [beta, alpha, delta, gamma],
             [gamma, delta, alpha, beta]]
    msg = GraecoLatinMagic.is_Latin(greek)
    if msg:
        raise ValueError("(greek) " + msg)

        # Create a 4x4 Latin square
    a, b, c, d = 'a', 'b', 'c', 'd'
    latin = [[b, c, a, d],
             [a, d, b, c],
             [d, a, c, b],
             [c, b, d, a]]
    msg = GraecoLatinMagic.is_Latin(latin)
    if msg:
        raise ValueError("(latin) " + msg)

        # Check orthogonality
    msg = GraecoLatinMagic.are_orthogonal(greek, latin, 4)
    if msg:
        raise ValueError("(greek ⟂ latin) " + msg)
    print4(greek, latin)

    print("There are 24 permutations of the set {0,1,2,3}...")
    print("Square that: 24²=576 for two independent permutations")
    print("Double that: 2·576=1152 for base-4 digit ordering...")
    print("1152 magic squares can be generated by this procedure.")
    print("We will choose just five pairs of permutations,",
          "with four chosen randomly,")
    print("  to produce just ten of these magic squares")

    permutations = set()
    permutations.add((0,1,2,3, 0,1,2,3))    # a=α=0, b=β=1, etc.
    while len(permutations) < 5:
        sigma1 = [0,1,2,3]
        shuffle(sigma1)
        sigma2 = [0,1,2,3]
        shuffle(sigma2)
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
    EPILOG = "Euler's method uses Graeco-Latin squares."
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     epilog=EPILOG)
    parser.add_argument("-T", "--self_test", action="store_true", \
        help="run the self-test to check basic functionality")
    parser.add_argument("-3", "--trad3", action="store_true", \
        help="run the 3x3 matrix test (eight magic squares)")
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
    if args.self_test:
        tests += 1
        self_test(not args.verbose)

    if args.trad3:
        tests += 1
        test_3_by_3(not args.verbose)

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
