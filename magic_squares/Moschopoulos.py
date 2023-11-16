"""
Moschopoulos.py - algorithms for creating magic squares
Copyright © 2023 by Eric Conrad

DESCRIPTION

    Here we implement several algorithmm that were described by Manuel
    Moschopoulos, the nephew of a Byzantine bishop, that he wrote
    down probably around 1315 [1, §2 (biographical details)]

THE ALGORITHMS

    MoschopoulosOdd - the method of "twos and threes"
        a method for constructing a square of odd order.

    Moschopoulos3s5s - the method of "threes and fives"
        another method for constructing a square of odd order.

    MoschopoulosEvenlyEven - the method of interchanges
        a method for constructing a magic square of evenly even order.
        (The phrase "evenly even" means "divisible by four".)

    MoschopoulosArchetype - the method of archetypes
        another method for constructing a magic square of evenly even
        order, this one using a magic square of order 4 as its seed.
        For order 4, the result is a copy of the archetype square 
 
COMMAND LINE USAGE

    python -m magic_squares.Moschopoulos [-h] [-a [n ...]] [-b [n ...]]
            [-c [n ...]] [-d [n ...]]
            [-l p q] [-y y] [-x x] [-L [n ...]]

    magic square algorithms from Manuel Moschopoulos (c 1315)

    OPTIONS

        -h, --help
            show this help message and exit

        -a [n ...], --alg1 [n ...]
            Moschopoulos' "twos and threes" algorithm for creating
            magic squares of any odd order. This algorithm uses
            unit diagonal moves on a toroidal lattice.

        -b [n ...], --alg2 [n ...]
            Moschopoulos' "threes and five" algorithm for creating
            magic squares of any odd order. This algorithm uses
            knight moves on a toroidal lattice.

        -c [n ...], --alg3 [n ...]
            Moschopoulos' diagonal interchange algorithm for
            creating magic squares of any evenly even order.

        -d [n ...], --alg4 [n ...]
            Moschopoulos' archetype algorithm for creating magic
            squares of any evenly even order.

        -L [n ...], --leaper [n ...]
            the experimental Leaper algorithm for magic squares of
            odd order. Note that while this algorithm does produce
            some very interesting magic squares, it does sometimes
            produce squares that are not magic  Tweak some of the
            parameters below.

                LEAPER PARAMETERS

        -l p q, --leaperpq p q
            (default: p=3, q=1) specify leaper parameters for the
            experimental Leaper algorithm. Preconditions: n>p>q and
            all three pairwise relatively prime.

        -y y, --leapery y
            (default: y=0) a row where the leaper should start.
            Integers are accepted, as are the names "m", "t" or
            "b" (for "middle", "top" and "bottom"), or expressions
            like "m+3" or "m-3" for three rows above and below the
            middle.

        -x x, --leaperx x
            (default: x="m") a column where the leaper should start.
            Naming rules are as for y.

REFERENCES

    [1] Peter G. Brown, "The Magic Squares of Manuel Moschopoulos"
        in Convergence. Mathematical Association of America. July 2012.
            URL: https://maa.org/press/periodicals/convergence/
                + the-magic-squares-of-manuel-moschopoulos-
                + the-mathematics-of-the-methods-odd-squares

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

_all = []

class MoschopoulosOdd(MagicSquare):
    """Moschopoulos' twos and threes method for odd order magic squares

    BACKGROUND

        These are the same squares referred to as "Siamese magic
        squares", and the means of construction are probably quite old,
        possibly (and probably) Chinese in origin.  The oldest of these
        is certainly the Luo Shu Magic square of order 3:

                            4  9  2
                            3  5  7
                            8  1  6

        Probably the most obvious feature of this magic square is the
        median progression 4,5,6 along the main diagonal.  The maximum
        entry 3²=9 appears immediately above the median entry (9+1)/2=5,
        and the minimum entry 1 appears directly below.  The order 3
        appears to the left of the median.

        As described in [1], here is a general algorithm.  (A
        simplification follows this discussion, and actual code, a small
        double loop, can be found in the method "configure"). We use an
        order n=5 square as an illustrative example.  Bracketed comments
        refer to this example.

            Given: an odd positive integer n [e.g. n=5].

            1. Start with an empty order 2n-1 square grid [2n-1=9],
               with rows and columns labelled from -(n-1)/2 to (3n-3)/2
              [for order 5: -2 through 6, see Figure 1].  The middle
              column is labelled (n-1)/2 [ex: 2] and the top row is
              labelled -n(n-1)/2 [ex: -2].

            2. Starting in the top middle entry [ex: (-2,2) in
               Figure 1], and moving down and right, fill in the
               numbers from 1 through n [Figure 1: 1 through 5].

                             *  *  *  *  *
                      -2 -1  0  1  2  3  4  5  6
                  -2               1
                  -1            6     2
                 * 0        11     7     3
                 * 1     16    12     8     4
                 * 2  21    17    13     9     5
                 * 3     22    18    14    10
                 * 4        23    19    15
                   5           24    20
                   6              25
                 
                    Figure 1: the basic grid

            3. Diagonally below and left the entered numbers, in the
               same order, continue the progression with the next n
               consecutive entries.  Repeat the process until the full
               progression from 1 through n² has been entered.  [The
               completed grid is in Figure 1.]

            4. The entries in rows and in columns labelled from 0
               through n-1 are all in their proper place.  The middle n
               values in the progression appear in place in the diagonal
               running from (0,0) through (n-1,n-1).  [See Figure 2.
               The starred rows and columns in Figure 1 mark the in
               place entries and are the basis for Figure 2.]

               At this point, it is worth noting that the coordinates
               of the filled out entries sum to even numbers.  The
               remaining slots are empty.  [For example, slot (1,3) has
               entry 8 -- the sum of the coordinate is 4, which is even.
               Slot (0,3) with sum 3, odd, is empty.]

                        0  1  2  3  4
                      ---------------
                  0 |  11     7     3
                  1 |     12     8          Figure 2.  The starred
                  2 |  17    13     9         rows and columns from
                  3 |     18    14            Figure 1.
                  4 |  23    19    15

            5. The remaining entries [rows or columns without stars] are
               moved into the magic square using the Division Algorithm.
               The smallest non-negative (!) remainder is used for the
               out-of-bounds coordinate.  [For example, take entry 1
               in slot (-2, 2).  The smallest positive remainders** of
               -2 and 2 are respectively 3 and 2, so 1 goes in slot
               (3, 2).  The completed magic square appears in Figure 3.]

                        0  1  2  3  4
                      ---------------
                  0 |  11 25  7 20  3
                  1 |   4 12 25  8 16       Figure 3.  The result.
                  2 |  17  5 13 21  9
                  3 |  10 18  1 14 22
                  4 |  23  6 19  2 15

    THE DIVISION ALGORITHM

        The standard form of the Division Algorithm (or Division Lemma)
        for integers is:

            For all pairs of integers a and b, if b ≠ 0, there is a
            unique pair of integers q and r such that:
                (i) a = bq + r; and
                (ii) 0 ≤ r < |b|.

        The numbers a, b, q and r are respectively the dividend, the
        divisor, the quotient and the remainder.

        Point (i) basically says what it means when we say that
        division is an inverse of multiplication.  Point (ii) puts
        a constraint on the remainder.  For the integers, this
        particular constraint not only guarantees existence of
        quotients, but also uniqueness.

    ** A NOTE ON DIVISION
    
        With regard to the coordinates (-2, 2), note that:

            (i) -2 = 4(-1) + 2      and     (ii) 0 ≤ 2 < |4|.
                quotient q=-1
                remainder r=2

        This is not saying that customary division is wrong.  We just
        happen to need a small non-negative remainder.  With customary
        division, we have, since a=-2<0 and b=4>0:

            (i) -2 = 4(0) - 2      and     (ii) -4 < -2 ≤ 0
                                   and     (iii) sgn r = sgn a.
                quotient q=0
                remainder r=2

        It's not wrong and it's a perfectly fine way of defining
        division -- but it gives an out of range index -- so it is
        unsuitable for our purposes.

        Fortunately, for b>0, Python implements integer division
        (quotient) and modulus (remainder) in the same way as 
        formulated above.  (For b<0, Python's formulation is a bit
        different, but that doesn't affect us here.)

    SIMPLIFYING THE CONSTRUCTION

        It is not actually necessary to actually construct the larger
        grid as we can simply transform the coordinates and place
        entries into the magic square in essentially one step:

            Coordinates
                in the larger grid      in the magic square
                    (x, y)                  (x % n, y % n)

    GENERALIZATION

        The diagonal move is like a move in checkers.  In fairy chess,
        we call a piece that normally moves diagonally one space a
        (1,1) leaper.
    """

    def __init__(self, n:int):
        """constructor"""
        super().__init__(n)
        self.name = f"Moschopoulos n={n}=2m+1 (first method)"

    def configure(self):
        """configuration"""
        n = self.n
        if n % 2 != 1:
            raise ValueError("Order {n} must be odd")
        median = (n-1) // 2
        z = 1                       # the starting entry
        start = (-median, median)   # starting row and column
        for x in range(n):
            i, j = start                # unpack the start point
            for y in range(n):
                self[i % n, j % n] = z      # store the entry
                z += 1                      # prepare the next entry
                i += 1
                j += 1
            i, j = start                # unpack previous start point
            i += 1                      # down
            j -= 1                      # left
            start = (i, j)              # pack the next start point  

_all.append(MoschopoulosOdd)

class Moschopoulos3s5s(MagicSquare):
    """a method for creating odd order squares using a knight's move

    DESCRIPTION

        In this method, the progressions of length n follow a knight's
        move in chess, down two cells and right 1 cell.  When the knight
        leaves the board on the bottom or on the left, it continues
        respectively at the top or at the right.  The moves start from
        the top.  The first progression starts at the top center cell.
        The starting progression is illustrated in Figure 4:

           v  x  x  1  x  x
           >  4  x  v  x  x         Figure 4.  Starting the second
              v  x  >  2  x             method for odd orders.
              >  5  x  v  x                 v = down 2
              x  x  x  >  3                 > = right
                          v

        The next progression start a knight's move down 2 units and
        left 1 below the start position.

             10  x  1  x  x
              4  x  V  8  x         Figure 5.  The second progression.
              x (6) <  2  x
              x  5  x  x  9         Note: knight's move down 2, then
              x  x  7  x  3            left to start.
                    v

        The third progression follows the same pattern. In the
        illustration, 11 is a knight's move down and left 6 to start
        the third progression.  To place the 12, we go "down" 2 to
        reach the 4, and right 1 to place the 12 above the 6.

             10 18  1 14 22
              4 12 25  8 16         Figure 6.  The result.
             23  6 19  2 15
             17  5 13 21  9
             11 24  7 20  3

        The remaining progressions follow the same pattern: a knight's
        move down 2 and right from the preceeding start to start and a
        knight's move down 2 and left to continue.
    
        Moschopoulos called this the method of threes and fives.  The
        implementation of the threes and fives method involves a couple
        of minor changes to the code in the double loop of the first method.

        The nice median sequence along the main diagonal that appears
        in the method of twos and threes does not show up in the method
        of threes and fives (except when n=1 or n=3).

    GENERALIZATIONS

        In fairy chess (chess variations that use non-standard pieces or
        non-standard boards or non-standard rules), the knight is a
        special case of a piece called a leaper.  In particular, a
        knight is a (2,1)-leaper: it moves two units orthogonally, then
        one unit in a perpendicular direction.

        The PQLeaper class is a class to experiment with more general
        leapers.

    """
    def __init__(self, n:int):
        """constructor"""
        super().__init__(n)
        self.name = f"Moschopoulos n={n}=2m+1 (second method)"

    def configure(self):
        """configuration"""
        n = self.n
        if n % 2 != 1:
            raise ValueError("Order {n} must be odd")
        median = (n-1) // 2
        z = 1                       # the starting entry
        start = (0, median)         # starting row and column
        for x in range(n):
            i, j = start                # unpack the start point
            for y in range(n):
                self[i % n, j % n] = z      # store the entry
                z += 1                      # prepare the next entry
                i += 2                      # down 2
                j += 1                      # right 1
            i, j = start                # unpack previous start point
            i += 2                      # down 2
            j -= 1                      # left 1
            start = (i, j)              # pack the next start point  

_all.append(Moschopoulos3s5s)

class MoschopoulosEvenlyEven(MagicSquare):
    """a method for constructing evenly even magic squares

    DESCRIPTION

        This method is based on a 4x4 prototype:

               0  1  2  3
            0  D        A
            1     D  A
            2     A  D
            3  A        D

        The main diagonal and the antidiagonal are marked in the
        prototype.  The target 4mx4m square is covered by copies of the
        prototype.

        Squares in the target are numbered consectively in row major
        order from 1 to 16m² and in reverse from 16m² to 1.  The entry
        in a marked cell is its forward number, in an unmarked cell
        its backward number.

    ILLUSTRATION

        The algorithm is easily illustrated with a 4x4 example:

            Prototype        Forward F      Backward B
             1 0 0 1         1  2  3  4     16 15 14 13
             0 1 1 0         5  6  7  8     12 11 10  9
             0 1 1 0         9 10 11 12      8  7  6  5
             1 0 0 1        13 14 15 16      4  3  2  1

            Marked=1           Result           Example
            Unmarked=0       1 15 14  4     cell 6 is marked:
                            12  6  7  9         so cell 6 is F(6)=6
                             8 10 11  5     cell 8 is unmarked:
                            13  3  2 16         so cell 8 is B(8)=9

        For an 8x8 matrix, the prototype is the same.  The numbers
        in F run in rows from 1 through 8, from 9 through 16, etc.
        The numbers in B run from 64 down through 57, from 52 down
        through 49, etc.  The prototype divides the result into
        four quadrants, each with its own copy of the prototype.
        The procedure is the same.

    ANALYSIS

        Note that this can be represented compactly as:
            B(i,j) = n² + 1 - F(i,j)        0 ≤ i, j < n
            F(i,j) = ni + j
            P(i,j) = (i-j)%4 == 0 or (i+j)%4 == 3   (Prototype)
            R(i,j) = F(i,j) if P(i,j) else B(i,j)
    """

    def __init__(self, n:int):
        """constructor"""
        super().__init__(n)
        self.name = f"Moschopoulos n={n}=4m (method of interchange)"

    def configure(self):
        """configuration"""
        n = self.n
        if n % 4 != 0:
            raise ValueError("Order {n} must be divisible by 4")

            #     0 1 2 3
            #   0 =     ║           =:  (i-j)%4 == 0
            #   1   = ║             ║:  (i+j)%4 == 3
            #   2   ║ =
            #   3 ║     =

        p, q = 1, n*n
        for i in range(n):
            for j in range(n):
                self[(i,j)] = p if (i-j)%4 == 0 or (i+j)%4 == 3 else q
                p += 1
                q -= 1

class MoschopoulosArchetype(MagicSquare):
    """a method for constructing evenly even magic squares

    DESCRIPTION

        That this method is trickier to write up is no surprise.
        The author of [1] notes this, and the translation of the
        manuscript is difficult to decipher. As in the previous
        algorithm, we have a prototype.  In addition, we have an
        archetype and its counterpart, which for lack of a better
        word, we'll call the deuterotype.

               P                 A                  D    
           Prototype         Archetype          Deuterotype
            1 0 0 1          1 14 11  8         49 62 59 56
            0 1 1 0         12  7  2 13         60 55 50 61
            1 0 0 1          6  9 16  3         54 57 64 51
            0 1 1 0         15  4  5 10         63 52 53 58

                    Figure 1.  The 4x4 prototypes

        The archetype A is a 4x4 matrix with entries ranging from 1
        consecutively through 16, in other words, A is a traditional
        magic square.  Both the prototype P and the deuterotype D
        depend on the  archetype A.  The prototype simply expresses
        a True/False relation (with False=0 and True=1).  The
        dependencies are as follows:

                P[i,j] = bool(A[i,j] < 9)               0 ≤ i, j < 4
                D[i,j] = A[i,j] + n² - 16               0 ≤ i, j < 4

        Since the deuterotype is a translate of the archetype A,
        the deuterotype is a magic square, albeit not a traditional
        one (unless n=4). Its entries cover the highest sixteen values
        in the the result.  The illustrated deuterotype is for n=8.

        The illustrated prototype is actually a magic square.  (I
        don't know whether that is a prerequisite.)
                
        For n=4m, the grid is covered by an mxm grid of prototypes,
        numbered in row major order.  (Column majoring would also
        work.) If n=8, then m=2, so the covering consists of 4
        quadrants:

                Q0  |  Q1                 0 |  8
                ----+----               ----+----   base = 8Q
                Q2  |  Q3                16 | 24
        
                QUADRANTS                  BASE

        Moschopoulos's rule basically says that the (i,j) entry of the
        result R is:

                     +--
                     |   A[i,j] + base, if P[i,j] is true
            R[i,j] = |
                     |   D[i,j] - base, if P[i,j] is false
                     +--

        Happy magicking!
    """

    def __init__(self, n:int, archetype=None):
        """constructor

        USAGE

            The order of the result is n.  The value of n must be
            a multiple of 4.

            If given, the archetype must be a 4x4 array (tuple/list)
            that will form a magic square.  The default archetype is
            the following magic square:

                    1  14  11   8
                   12   7   2  13
                    6   9  16   3
                   15   4   5  10
        """
        if not archetype:
            archetype = [[1, 14, 11, 8], [12, 7, 2, 13],
                         [6, 9, 16, 3], [15, 4, 5, 10]]
        self.archetype = MagicSquare.from_sq(archetype)
        if len(self.archetype) != 4:
            raise ValueError("The archetype must be order 4")
        super().__init__(n)
        self.name = f"Moschopoulos n={n}=4m (method of archetypes)"

    def configure(self):
        """configuration"""
        n = self.n
        m = n // 4

        if n % 4 != 0:
            raise ValueError("Order {n} must be divisible by 4")
        archetype = self.archetype

        #print("Archetype")
        #print(archetype)

        prototype = {}
        for i in range(4):
            for j in range(4):
                prototype[(i,j)] = archetype[(i,j)] < 9

        deuterotype = archetype.translate(n*n - 16)
        #print("Deuterotype")
        #print(deuterotype)

        first_base = 0              # upper left left quadrant
        for i in range(n):
            base = first_base       # first quadrant in row
            for j in range(n):
                p = archetype[(i%4, j%4)] + base
                q = deuterotype[(i%4, j%4)] - base
                self[(i,j)] = p if prototype[(i%4,j%4)] else q
                if j % 4 == 3:      # are we entering a new quadrant?
                    base += 8           # yes!
            if i % 4 == 3:      # will next row start a new quadrant?
                first_base = base   # yes!
        #print("Result")
        #print(self)

_all.append(MoschopoulosEvenlyEven)

class PQLeaperSquare(MagicSquare):
    """a method for creating odd order magic squares using leapers

    LEAPERS

        In fairy chess (chess variations that use non-standard pieces or
        non-standard boards or non-standard rules), the knight is a
        special case of a piece called a leaper.  In particular, a
        knight is a (2,1)-leaper: it moves two units orthogonally, then
        one unit in a perpendicular direction.  The method of threes
        and fives uses a knight starting at the top middle position
        to generate an odd order magic square.  The method of twos and
        threes uses a checker piece (i.e. a (1,1)-leaper) starting two
        cells above the top middle position to generate an odd order
        magic square.  A natural question is can other leapers be used
        to produce magic squares of odd order.  The answer is yes, but
        not all leapers will work, and there are conditions of the
        starting position.

        (It is called a leaper, because it is not blocked by
        intermediate pieces.)  In the method of twos and threes,
        Moschopoulos used a (1,1)-leaper.  In the second method, he
        used a (2,1)-leaper.  Could other leapers be used?   (Yes!)
        Presumably for a (p,q)-leaper, we would need p and q to be
        relatively prime to each other and to n.  Also, the choice of
        starting position will make a difference.

        The PQLeaper class is a class to experiment with more general
        leapers.

    QUESTIONS

        For a given leaper, which cells can be used as starting cells?

        Are there other fairy chess moves that might produce interesting
        variations on this theme?
    """

    FIRST_USE_WARNING = True

    def __init__(self, n:int, p:int, q:int=1, start:tuple=None,
                 debug=False, warn_unsafe=True):
        """constructor"""
        if warn_unsafe and not self.FIRST_USE_WARNING:
            msg = f"{__file__}::PQLeaperSquare: "
            msg += "This class seems to be pretty good at "
            msg += "producing magic squares when n is prime..."
            logger.warning(msg)
            msg = "  -- it doesn't seem to work as well when "
            msg += "n is composite..."
            logger.warning(msg)
            msg = "  -- in any case, it is known to fail on some "
            msg += "inputs...  Caveat emptor!"
            logger.warning(msg)
            self.__class__.FIRST_USE_WARNING = False
        for v in (p, q):
            if not isinstance(v, int):
                raise TypeError("p and q must be integers")
        if n > 1:
            if gcd(p, n) != 1 or gcd(q, n) != 1 or gcd(p, q) != 1:
                msg = "p, q and n must be pairwise relatively prime"
                raise ValueError(msg)
        self.leaper = (p, q)
        median = (n-1) // 2
        start = start if start else (0, median)
        self.leaper_start = start
        super().__init__(n, debug=debug)
        self.name = f"({p},{q})-Leaper n={n}, start={start}"

    def configure(self):
        """stub for the creation algorithm"""
        n = self.n
        p, q = self.leaper
        if n % 2 != 1:
            raise ValueError("Order {n} must be odd")
        z = 1                       # the starting entry
        start = self.leaper_start
        for x in range(n):
            i, j = start                # unpack the start point
            for y in range(n):
                self[i % n, j % n] = z      # store the entry
                z += 1                      # prepare the next entry
                i += p                      # down p
                j += q                      # right q
            i, j = start                # unpack previous start point
            i += p                      # down p
            j -= q                      # left q
            start = (i, j)              # pack the next start point  

_all.append(PQLeaperSquare)

def test_class(n, clsid):
    """simple test of the basic algorithms"""
    foo = clsid(n)                      # generate a magic square
    print(foo.name)
    print(foo)
    magic = foo.magic
    expected = n*(n*n + 1) // 2        # triangular number / n
    print("Magic number:", magic, f"(expected: {expected})")
    if magic != expected:
        print("ERROR: wrong magic number")

def test_leaper(n, p, q, y, x):
    """a test of the leaper algorithm"""
    def translate(yx):
        """translate a row or column coordinate"""
        values = {"t":0, "m":(n-1)//2, "b":n-1}
        if yx[0] in values:
            yx1 = values[yx[0]]
            yx = yx[1:]
            if not yx:
                return yx1
            yx2 = yx[0]
            yx3 = int(yx[1:])
            if yx2 == "+":
                return yx1 + yx3
            if yx2 == "-":
                return yx1 - yx3
            raise ValueError("Expected '+' or '-'")
        return int(yx)

    y = translate(y)
    x = translate(x)
    foo = PQLeaperSquare(n, p, q, (y, x), debug=True)
    print(foo.name)
    ok = True
    msg = "ok!"
    try:
        foo.check()
    except Warning as err:
        msg = str(err)
        words = set(msg.split())
        ok = False
    print(foo)
    if ok:
        print("  (The leaper algorithm was successful!)")
    else:
        print("  ERROR: " + msg)
        if "diagonal" in words:
            print("  (semimagic but not magic)")
        else:
            print("  (neither magic nor semimagic)")

def main(argv):
    """main routine"""
    import argparse

    DESC = 'magic square algorithms from Manuel Moschopoulos (c 1315)'
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-a', '--alg1', type=int, nargs='*', \
        metavar='n', default=[], \
        help='Moschopoulos\' "twos and threes" algorithm for ' \
        + 'creating magic squares of any odd order. This ' \
        + 'algorithm uses unit diagonal moves on a toroidal ' \
        + 'lattice.')
    parser.add_argument('-b', '--alg2', type=int, nargs='*', \
        metavar='n', default=[], \
        help='Moschopoulos\' "threes and five" algorithm for ' \
        + 'creating magic squares of any odd order.  This ' \
        + 'algorithm uses knight moves on a toroidal lattice.')
    parser.add_argument('-c', '--alg3', type=int, nargs='*', \
        metavar='n', default=[], \
        help='Moschopoulos\' diagonal interchange algorithm for ' \
        + 'creating magic squares of any evenly even order.')
    parser.add_argument('-d', '--alg4', type=int, nargs='*', \
        metavar='n', default=[], \
        help='Moschopoulos\' archetype algorithm for ' \
        + 'creating magic squares of any evenly even order.')
    parser.add_argument('-L', '--leaper', type=int, nargs='*', \
        metavar='n', default=[], \
        help='the experimental Leaper algorithm for magic squares of ' \
        + ' odd order.  Note that while this algorithm does produce ' \
        + 'some very interesting magic squares, it does sometimes ' \
        + 'produce squares that are not magic.  Tweak some of the ' \
        + 'parameters below.')
    parser.add_argument('-l', '--leaperpq', type=int, nargs=2, \
        metavar = ('p', 'q'), default=(3, 1), \
        help='(default: p=3, q=1) specify leaper parameters for the ' \
        + 'experimental Leaper algorithm.  Preconditions n>p>q and ' \
        + 'all three pairwise relatively prime.')
    parser.add_argument('-y', '--leapery', type=str, \
        metavar='y', default="t", \
        help='(default: y=0) a row where the leaper should start. ' \
        + 'Integers are accepted, as are the names "m", "t" or "b" ' \
        + '(for "middle", "top" and "bottom"), or expressions like ' \
        + '"m+3" or "m-3" for three rows above and below the middle.')
    parser.add_argument('-x', '--leaperx', type=str, \
        metavar='x', default="m", \
        help='(default: x="m") a column where the leaper should ' \
        + 'start.  Naming rules are as for y.')
    args = parser.parse_args(argv)

    for n in args.alg1:
        name = "MoschopoulosOdd"
        print("*** Manuel Moschopoulos -- method of twos and threes")
        if n<1:
            print(f"{name}:ERROR n={n} is not positive.")
            continue
        if n%2 == 0:
            print(f"{name}:ERROR n={n} is not odd.")
            continue
        test_class(n, MoschopoulosOdd)

    for n in args.alg2:
        name = "Moschopoulos3s5s"
        print("*** Manuel Moschopoulos -- method of threes and fives")
        if n<1:
            print(f"{name}:ERROR n={n} is not positive.")
            continue
        if n%2 == 0:
            print(f"{name}:ERROR n={n} is not odd.")
            continue
        test_class(n, Moschopoulos3s5s)

    for n in args.alg3:
        name = "MoschopoulosEvenlyEven"
        print("*** Manuel Moschopoulos -- method of interchanges")
        if n<1:
            print(f"{name}:ERROR n={n} is not positive.")
            continue
        if n%4 != 0:
            print(f"{name}:ERROR n={n} is not divisible by 4.")
            continue
        test_class(n, MoschopoulosEvenlyEven)

    for n in args.alg4:
        name = "MoschopoulosArchetype"
        print("*** Manuel Moschopoulos -- method of archetypes")
        if n<1:
            print(f"{name}:ERROR n={n} is not positive.")
            continue
        if n%4 != 0:
            print(f"{name}:ERROR n={n} is not divisible by 4.")
            continue
        test_class(n, MoschopoulosArchetype)

    y = args.leapery
    x = args.leaperx
    for n in args.leaper:
        p, q = args.leaperpq
        if n<1:
            print(f"PQLeaperSquare:ERROR n={n} is not positive.")
            continue
        p, q = p % n, q % n         # reduce modulo n
        if n%2 == 0:
            print(f"PQLeaperSquare:ERROR n={n} is not odd.")
            continue
        if gcd(n, p) != 1 or gcd(n, p) != 1 or gcd(p, q) != 1:
            print(f"PQLeaperSquare:ERROR n={n}, p={p}, q={q} " \
                + "are not pairwise relatively prime")
            continue
        if p < q:
            print(f"PQLeaperSquare:ERROR n={n}, p={p}, q={q} " \
                + "with p<q")
            continue
        test_leaper(n, p, q, y, x)

if __name__ == "__main__":
        # self-test
    import sys
    main(sys.argv[1:])

    print("SUCCESS!")
