"""
bordering.py - extend a magic square by bordering
Copyright © 2023 by Eric Conrad

DISCUSSION

    In this setting we envision starting with a magic square (which we
    will refer to as the picture) and adding a 1-cell border (which we
    will call the frame).  For reference, consider the following 3x3
    magic square with magic constant 0 and a possible 5x5 extension:

                                          U  a  b  c  V
              1  2 -3                     x  1  2 -3 -x
             -4  0  4        --->         y -4  0  4 -y
              3 -2 -1                     z  3 -2 -1 -z
                                         -V -a -b -c -U

    To preserve the magic property, each frame cell C and its opposite
    cell (labelled -C) along a row, column or diagonal passing though
    the picture must sum to a constant M.  In addition, each row and
    each column of the frame must sum to M+m where m is the magic
    constant of the picture.  If M=m=0, then along the frame, we need

             U + a + b + c + V = 0          (1)     top
            -V - a - b - c - U = 0          (1')    bottom
             U + x + y + z - V = 0          (2)     left
             V - x - y - z - U = 0          (2')    right

    Note that Equations (1) and (1') are equivalent, and that Equations
    (2) and (2') are also equivalent.

    If M is arbitrary, we should relabel the cells named -* as *'.  In
    this case we have: 

             U  + a  + b  + c  + V  = M      (3)     top
             V' + a' + b' + c' + U' = M      (3')    bottom
             U  + x  + y  + z  + V' = M      (4)     left
             V  + x' + y' + z' + U' = M      (4')    right

    For each cell C, C + C' = M, so the left hand side of Equation (3')
    can be rewritten as:

            (M - V) + (M - a) + (M - b) + (M - c) + (M - U)
                = 5M - (U + a + b + c - V) = 5M - M = 4M

    But that implies that 4M = M and thus M = 0, assuming that m = 0.
    (If the picture is an nxn magic square, the same argument reduces
    to (n+1)M = M, or M = 0, whenever the magic constant m is 0.)

    If the picture's magic constant m ≠ 0, we can sum along the second
    row of the framed picture:

             x + * + * + * + x' = M + m      (5)     second row

    Here the asterisks are placeholders for the picture cells.
    The top and bottom equations become:

             U  + a  + b  + c  + V  = M + m  (6)     top
             V' + a' + b' + c' + U' = M + m  (6')    bottom

    Reducing the left hand side of Equation (6'):

             M + m
                 = (M - V) + (M - a) + (M - b) + (M - c) + (M - U)
                 = (n+2)M - (U - V) + (a + b + c)
                 = (n+2)M - M - m
                 = (n+1)M - m

    This implies:

             2m = nM

    For a traditional magic square with cells numbered from 1 through
    n², the sum of the cells is the triangular number △(n²):

            △(n²) = n² (n² + 1) / 2           (7)    triangular sum

    Dividing by n gives the row sum or magic number m:

             m = n (n² + 1) / 2                (7')   traditional m

    So for a traditional magic square, we can write M as a function
    of m:

             M = 2m / n = n² + 1               (7'')  bordering

ODD ORDER (when M=m=0)

    The M=m=0 setting works well for squares of odd order with entries
    consecutive from - (n² - 1) / 2 through (n² - 1) / 2 (as in our
    example for n=3 with entries from -4 through 4, consecutively).

    In this case, we can extend the square using consecutive values
    ranging from  - ((n+2)² - 1) / 2 through - (n² + 1) / 2 on the
    negative side and from (n² + 1) / 2 through ((n+2)² - 1) / 2 on the
    positive side.

    There are a number of solutions for our example:

                                          U  a  b  c  V
              1  2 -3                     x  1  2 -3 -x
             -4  0  4        --->         y -4  0  4 -y
              3 -2 -1                     z  3 -2 -1 -z
                                         -V -a -b -c -U

    The available positive constants are {5, 6, 7, 8, 9, 10, 11, 12},
    with 4 odd and 4 even.  Each of these is paired with its negative
    in an opposite position on the frame.  We need only consider how
    to fill the top and left sides of the frame.

    If U and V have opposite parity, then we are left with three odd
    pairs and three even pairs.  Since U+V and U-V are both odd, we
    need a+b+c and x+y+z to be odd to arrive at the vanishing sums (1)
    and (2) along the top and left sides of the frame.  With three odd
    pairs, we have no way of picking 3 odd numbers and 3 even numbers
    so that a+b+c and x+y+z are both odd.  Thus U and V must have the
    same parity, both even or both odd.  At this point we can simply
    use trial and error to find some solutions...  Here are two
    solutions...

            U   V   U+V     U-V     a   b   c       x   y   z
            7   9    16      -2     6 -10 -12       5   8 -11  (8)
            6  10    16      -4   -12 -11   7       8  -9   5  (9)

    In solution (8), we can permute the cells a, b and c on the left,
    and the cells x, y and z on the top.  Under these two permutations,
    Solution (8) encapsulates (6)(6)=36 solutions.  Interchanging U
    and V changes the sign of U-V, and thus the signs of x, y and z,
    doubling to 72 the number of simple transformations.  Changing the
    sign of V interchanges U+V with U-V and thus abc with xyz, again
    doubling to 144 the number of transformation.  (Changing the sign
    of U is the same as swapping U and V, changing the sign, and
    swapping back, so this transformation is already covered.)

    In a likewise manner, there are 144 easy transformations of
    Solution (9).

                 Solution (8)              Solution (9)
               7  6 -10 -12  9           6 -12 -11  7  10
               5  1   2  -3 -5           8   1   2 -3  -8
               8 -4   0   4 -8          -9  -4   0  4   9
             -11  3  -2  -1 11           5   3  -2 -1  -5
              -9 -6  10  12 -7         -10  12  11 -7  -6

    We can obtain traditional magic squares from these by translation.
    The mean of 25 and 1 is 13, so we add 13 to all entries:

              20 19  3  1 22             19  1  2 20 23
              18 14 15 10  8             21 14 15 10  5
              21  9 13 17  5              4  9 13 17 22
               2 16 11 12 24             18 16 11 12  8
               4  7 23 25  6              3 25 24  6  7

EVEN ORDER (when M=m=0)

    First we note that there are no non-trivial magic squares of
    order 2:

            a  b        a+b = a+c = a+d  implies b=c=d
            d  c        d+a = d+b implies a=b=c=d

    Apart from the trivial magic squares of orders 0 and 2, the lowest
    even order is 4.

    Here we have another problem.  For example, if we are working with
    traditional squares of order 4 with cells numbered from 1 through
    16, then the magic number is:

            m' = △(n²)/n = △(16)/4 = 4(17)/2 = 34

    To translate this to a square with m = 0, we need a shift of

            h = -m' / n = -34 / 4 = -17/2 = -8.5

    This is not an integer, but it is a half-integer.

    Perhaps the most famous magic square of order four in Western
    Civilization* is the magic square in Albrecht Dürer's drawing
    Melencolia (1514):

            16  2  3 13                      7.5 -6.5 -5.5  4.5
             5 10 11  8   === h=-8.5 ===>   -3.5  1.5  2.5 -0.5
             9  6  7 12                      0.5 -2.5 -1.5  3.5
             4 15 14  1                     -4.5  6.5  5.5 -7.5

    (The revival of interest in mathematics and sciences in Western
    Europe was heavily influenced by Arabic mathematics, in turn
    influenced by then contemporary mathematics in India as well as
    ancient Greek language mathematics from the Hellenistic period.)

    To extend this by bordering to a 6x6 square which translates
    to a traditional square with entries from 1 through 36, our
    frame constants are the half-integers in the set:
            {k+0.5, -k-0.5: 8 ≤ k ≤ 18, k ∈ ℤ}          (10)

    Similar considerations apply to framing about any traditional
    magic square of even order.

REFERENCES

    [1] "Magic squares" in Wikipedia.  Web.  Accessed 11 November 2023.

MODIFICATIONS

    16 Nov 2023 - EC
        1) added reference.
        2) moved class alBuzjaniBorder into a separate module.

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
from magic_squares.magic_square import MagicSquare, SiameseMagicSquare
from magic_squares.decorators import Tier

def translate_to_zero(square:MagicSquare, n:int=None) -> MagicSquare:
    """return a shift-equivalent magic square with magic constant 0

    The optional argument n is only valid if argument square is a
    dictionary.  It is ignored in all other cases.
    """
        # convert if necessary

    if not isinstance(square, MagicSquare):
        square = MagicSquare.from_sq(square, n)

    m = square.magic
    n = square.n

    if m == 0:
        square.tzinfo = (m, 0, "exact")        # history
        return square           # nothing to do

    if m % n == 0:
        h = m // n              # exact: hn = m
        square = square.translate(-h)
        square.tzinfo = (m, -h, "exact")       # history
        return square

    h = Fraction(m, n)
    square = square.translate(-h)
    square.tzinfo = (m, -h, "fraction")     # history
    return square

    # VISUALIZATION OF THE FRAME
    #        top
    #   U + a + b + V                   U + a + b + V = 0
    #   c          -c                   U + c + d - V = 0
    #   d          -d    right
    #  -V - a - b - U
    #
    # NOTES
    #   If the bones are all integers:      <-- n odd
    #       -- If U and V have the same parity, then the frame pieces
    #       must all have an even number of odd bones
    #       -- If U and V had opposite parity, then the frame pieces
    #       must all have an odd number of odd bones
    #   If the bones are half integers:     <-- n even
    #       -- We need to consider congruence classes p modulo 4 where
    #       the bone is p/2:
    #           1) p:1
    #           2) p:2 (p/2 is an odd integer)
    #           3) p:3
    #           4) p:0 (p/2 is an even integer)

class FramedMagicSquare(MagicSquare):
    """a base class for framing algorithms

    CONSTRUCTOR ARGUMENTS

        picture - the magic square to be framed

        magic_zero (default True)
            if True, the input must have magic constant zero
    """
    def __init__(self, picture:MagicSquare, magic_zero:bool=True,
                 debug:bool=False):
        """constructor"""
        self.source = MagicSquare.from_sq(picture)
        if bool(magic_zero):
            assert picture.magic == 0
        super().__init__(picture.n+2, debug=debug)

    def configure(self):
        """here we mount the picture and then configure the frame"""
                # picture
        picture = self.source
        n = picture.n
        for i in range(n):
            for j in range(n):
                self[(i+1, j+1)] = picture[(i,j)]       # picture

                # frame
        n = self.n
        self._top = Tier(self, "row", 0)
        self._bottom = Tier(self, "row", n-1)
        self._left = Tier(self, "column", 0)
        self._right = Tier(self, "column", n-1)
        self.configure_frame()

    def configure_frame(self):
        """subclasses may redefine this

        As long as the picture is a magic square, this method will
        retain the magic property
        """
        n = self.n
        for i in range(n):
            self.top[i] = self.bottom[i] = 0
            self.left[i] = self.right[i] = 0

    @property
    def top(self):
        """the topmost row -- top of the frame"""
        return self._top

    @property
    def bottom(self):
        """the bottommost row -- bottom of the frame"""
        return self._bottom

    @property
    def left(self):
        """the leftmost column -- left side of the frame"""
        return self._left

    @property
    def right(self):
        """the rightmost column -- right side of the frame"""
        return self._right

    @staticmethod
    def _sigma_list(full_range:range, sigma:list) -> dict:
        """process a full permutation"""
                # validation
        full_list = list(full_range)
        if sorted(sigma) != full_list:
            raise ValueError("not a permutation")

                # transformation
        new_sigma = {}
        for i in full_range:
            target = sigma[i-full_range.start]
            if i != target:
                new_sigma[i] = target
        return new_sigma

    @staticmethod
    def _sigma_tuple(full_range:range, sigma:tuple) -> dict:
        """process a cycle"""
                # validation
        full_set = set(full_range)
        sigma_set = set(sigma)
        if not (sigma_set <= full_set):
            raise ValueError("invalid entries in cycle")
        if len(sigma) < 2:
            return dict()           # trivial cycle
        if len(sigma_set) != len(sigma):
            raise ValueError("duplicate entries in cycle")

                # transformation
        new_sigma = dict()
        for i in range(len(sigma)):
            source = sigma[i]
            target = sigma[i+1 if i<len(sigma)-1 else 0]
            new_sigma[source] = target
        return new_sigma

    @staticmethod
    def _sigma_dict(full_range:range, sigma:tuple) -> dict:
        """process a dictionary permutation"""
                # validation
        full_set = set(full_range)
        sigma_keyset = set(sigma.keys())
        sigma_valueset = set(sigma.values())
        if not (sigma_keyset <= full_set):
            raise ValueError("invalid key entries in permutation")
        if not (sigma_valueset <= full_set):
            raise ValueError("invalid value entries in permutation")
        if sigma_keyset != sigma_valueset:
            raise ValueError("not a bijection (not one-to-one)")
        return sigma

    @classmethod
    def _sigma(cls, full_range:range,
               sigma:(tuple, list, dict)) -> dict:
        """validate a permutation"""
        if isinstance(sigma, list):
            return cls._sigma_list(full_range, sigma)
        if isinstance(sigma, tuple):
            return cls._sigma_tuple(full_range, sigma)
        if isinstance(sigma, dict):
            return cls._sigma_dict(full_range, sigma)
        raise TypeError("Permutation must be list, tuple or dict")

    def vertical_permutation(self, sigma:(tuple, list, dict)):
        """permute entries on the left and right sides

        REQUIRED ARGUMENTS

            sigma - a permutation of (1...n-2).  The corner entries
                must stay fixed.

                The permuation may be written in one of three ways:

                    list - each of the values 1 through n-2 appears
                        exactly once, with position base 1 indicating
                        the source and the corresponding entry the
                        destination.

                    tuple - a cyclic permutation

                    dict - a permutation, fixed elements may be
                        omitted

                Examples for n=5:
                    [1, 3, 2] -> 1 2 3      1 is fixed, 2 and 3 are
                                 1 3 2      swapped

                    (3, 2)                  same (cycle notation)

                    {3:2, 2:3}              same

                    (1, 2, 3) -> 1 2 3      1 -> 2 -> 3 -> 1
                                 2 3 1      another cycle
        """
        sigma = self._sigma(range(1,self.n-1), sigma)
        mapping = {}
        for key in sigma:
            item = sigma[key]
            mapping[item] = (self.left[key], self.right[key])
        for item in mapping:
            target1, target2 = mapping[item]
            self.left[item], self.right[item] = target1, target2
        self.check()

    def horizontal_permutation(self, sigma:list):
        """permute entries on the top and on the bottom

        REQUIRED ARGUMENTS

            sigma - a permutation of (1...n-2).  The corner entries
                must stay fixed.  For more information on writing
                permutations, see vertical permutations (above).
        """
        sigma = self._sigma(range(1,self.n-1), sigma)
        mapping = {}
        for key in sigma:
            item = sigma[key]
            mapping[item] = (self.top[key], self.bottom[key])
        for item in mapping:
            target1, target2 = mapping[item]
            self.top[item], self.bottom[item] = target1, target2
        self.check()

if __name__ == "__main__":
        # self-test
    from random import shuffle
    from magic_squares.al_Buzjani import alBuzjaniBorder

    def test(foo):
        """self test"""
        n = foo.n
        print(f'Input for n={n}:')
        print(foo)
        print(f'Output for n={n}:')
        bar = alBuzjaniBorder(foo)
        print(bar)
        return bar

    foo = test(SiameseMagicSquare(1))
    foo = test(foo.rotate(1))
    foo = test(foo.rotate(1))

    sigma = list(range(1, len(foo)-1))
    shuffle(sigma)
    foo.vertical_permutation(sigma)
    print(f"After vertical shuffle {sigma}:")
    print(foo)

    foo = test(foo.rotate(1))

    sigma = (1, 2, 3)
    foo.horizontal_permutation(sigma)
    print(f"After horizontal cycle {sigma}:")
    print(foo)

    foo = test(foo.rotate(1))

    sigma = {1:2, 2:1, 3:4, 4:3}
    foo.horizontal_permutation(sigma)
    print(f"After horizontal permutation {sigma}=(1 2)(3 4):")
    print(foo)

    foo = test(foo.rotate(1))

    print("SUCCESS!")
