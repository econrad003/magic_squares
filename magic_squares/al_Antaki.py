"""
al_Antaki.py - extend even order magic squares by bordering
Copyright © 2023 by Eric Conrad

DESCRIPTION

    Implemented here are al-Antaki's methods for bordering a even order
    magic squares  See the Wikipedia article on magic squares for a
    summary or read the documentation for each of the classed for
    more extensive details.

    Two classes are implemented here:

        1) alAntakiEvenlyEven - a border for oddly even magic squares;
           the resulting square is evenly even.

        1) alAntakiOddlyEven - a border for evenly even magic squares;
           the resulting square is oddly even.

TERMINOLOGY

    The phrase "evenly even" means "divisibly by 4", or equivalently,
    "congruent to 0 modulo 4".   An evenly even number is an integer
    multiple of 4.  The phrase "doubly even" is equivalent to "evenly
    even".

    The phrase "oddly even" means "with remainder 2 after dividing by
    4", or equivalently, "congruent to 2 modulo 4", or, also
    equivalently, "even but not a multiple of 4".

REFERENCES

    [1] "Magic squares" in Wikipedia. Web.

        The two methods are described under the heading "Continuous
        enumeration methods".

    [2] John Grogono.  "The 10x10 magic squares, a method for creating
        creating 10x10 and larger 4p+2 Magic Squares" in Grogono Magic
        Squares.  Web, March 2010.  Accessed 17 November 2023.
            URL: https://www.grogono.com/magic/10x10.php

    [3] Inder Taneja. "Different Types of Magic Squares of Order 14".
        Web, 26 September 2023.  Accessed 17 November 2023.
                URL: https://numbers-magic.com/?p=2640

MODIFICATIONS

    17 Nov 2023 - EC - initial version

LICENSE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see
        <https://www.gnu.org/licenses/>.
"""
from magic_squares.magic_square import MagicSquare
from magic_squares.bordering import FramedMagicSquare
from magic_squares.decorators import Tier

class alAntakiEvenlyEven(FramedMagicSquare):
    """al-Buzjani's frame around oddly even order magic squares:
    The result is an evenly even magic square.

    This is a fast way of extending an oddly even (4m-2)x(4m-2) order
    square to an evenly even (4m)x(4m) square -- fast but not very
    general.  We are assuming that the inout is a traditional magic
    square with entries in some order having each of the values from 1
    through (4m-2)², and the output from 1 through (4m)².  As
    off-diagonal elements in the frame can be permuted in vertical or
    horizontal pairs along the edges, there are large number of
    symmetries.

    Basically one starts along the top and bottom and fills these in
    with the numbers from 1 through n=4m-2 and their complements.
    the corners are n+1 and n+2 in the same row (either top or bottom)
    and their complements in the opposite row. The magic square maker
    then fills in the sides with the remaining low numbers from n+3 to
    2n+2 and their complements.  There are some constraints on the
    chices in these processes.

    There are no nontrivial magic squares of order 2, so we require
    m≥2.

    Fortunately the algorithm is much simpler than the analysis which
    follows here.

    DETAILED AND PAINFUL ANALYSIS

        Although this is somewhat painful, we work out the details for
        the benefit of anyone who wishes or needs to generalize the
        method.  In addition to the smallest example (m=2), we give
        polynomials which can be evaluated for any m>2.  Remember that
        n=2m-2.

        The goal here is to establish the constraints on placement and
        to show that there is a (general) solution.

        For our example, consider the case where m=2 (i.e. n=6).  Then
        the low numbers run from 1 to 2n+2=14.  The complements or
        corresponding high numbers run from (n+2)²=64 down to:
            (n+2)² - (2n+1) = n² + 4n + 4 - 2n - 1
                            = n² + 2n + 3 = (n+1)² + 2
                            = 51.

        The complement of an entry k is k'=(n+2)²+1-k=65-k. In other
        words:
            k + k' = (n+2)² + 1 = 65.

        The magic number of the order n=6 square to be framed is:
            n (n² + 1) / 2 = 6 ᐧ  37  /  2  =  111.

        This square is translated forward h=2n+2=14 to accommonate the
        low numbers in the frame.  After translation, every entry is
        increased by h, so, since each row sum is increased by n times
        h, the magic number of the picture (or translate) is (ugh!):
            n (n² + 1) / 2 + nh = n (n² + 1) / 2 + n (2n + 2)
                                = ((n³ + n) + (4n² + 4n)) / 2
                                = (n³ + 4n² + 5n) / 2
                                = n (n² + 4n + 5) / 2
                                = n ((n+2)² + 1) / 2
                                                                            = 6 ᐧ 65 / 2 = 195.

        The magic number of the resulting square is:
            (n+2) ((n+2)² + 1) / 2 = 8 ᐧ  65  /  2 = 260.

        The difference between the two magic numbers is simply:
             (n+2) ((n+2)² + 1) / 2 - n ((n+2)² + 1) / 2
                = ((n+2) - n) ((n+2)² + 1) / 2
                = (n+2)² + 1 = 65, as expected.

        If we place n+1=7 and n+2=8 in the top corners, then the numbers
        1 through n=6 and their complements are placed in the top and
        bottom.  The top corners are accompanied by their complements
        on opposite ends of the diagonals.  The remaining values and
        their complements are placed in the same columns.  If we sum all
        the entries top and bottom:
            1 + 2 + ... + n + (n+1) + (n+2) + 1' + 2' + ... + (n+2)'
                = (1 + 1') + (2 + 2') + ... + ((n+2) + (n+2)')
                = ((n+2)² + 1) + ... + ((n+2)² + 1)    [(n+2) copies]
                = (n+2) ((n+2)² + 1)
        which is twice the magic number of the framed square (i.e. twice
        260 or 520).

        Summing along the left side and the right side will give the
        same result.

    ANALYSIS: THE TOP AND BOTTOM ROWS

        We want the top row to sum to the magic number given that it
        contains corners n+1=7 and n+2=8.  We are missing two high
        values at the corner, suggesting that we compensate by using
        two fewer low numbers in the top than in the bottom.  Here
        we can work with our example and try to generalize.  Suppose we
        place low values a and b on the top and c, d, e and f on the
        bottom.  On top, we have:
            7 + a + b + c' + d' + e' + f' + 8
                = 15 + a + b + (65-c) + (65-d) + (65-e) + (65-f)
                                       = 4 ᐧ 65 + 15 + a + b - c - d - e -f
        Then, since the magic number is 4 ᐧ 65:
            15 + a + b - c - d - e -f = 0
        There is a unique solution {a,b}={1,2} and {c,d,e,f}={3,4,5,6}.

        To generalize this, al-Antaki worked from left from right in
        groups of four until six cells remained.  Here, of course, is
        the trivial case, as six cells immediately remain:
            RULE 1: when six cells remain, put the first two on the
                bottom and the remaining four on top.
        Letting N=(n+2)²+1=65, sum of these four values is:
            (N-n) + (N-(n-1)) + (N-(n-2)) + (N-(n-3))
                = 4N - 4n + 1 + 2 + 3 = 4N - 4N + 6
                = 260 - 24 + 6 = 260 - 18
        That 18 is significant as for n=6, the two corner cells plus
        the two low cells sum to 7+8+1+2=18.  The net sum on the top,
        then, is the magic number 260.

        For the cells before the last six, he set down a different
        rule:
            RULE 2: when ten or more cells remain, put the first and
                fourth on top and the second and third on the bottom.
        In this case, the four numbers are k, k+1, k+2 and k+3 and
        the sum along the top is:
            k + (N-(k+1)) + (N-(k+2)) + (k+3) = 2N.
        This rule does not apply when n=6 (i.e. m=2).

        We have m-2 blocks of 4 plus our remaining block of six.  So
        the blocks of 4 contribute:
            (m-2)(2N) = (2m-2)N
        to the row sum on top.  The magic number is:
            (n+2)N / 2 = (4m)N / 2 = 2mN
        So RULE 2 undershoots the top row sum by 4N.

        The remainding part of the row consists of the two corners and
        the last six columns above the picture:
            (n-5) + (n-4) + (n-3)' + (n-2)' + (n-1)' + n' + (2n+3) 
                = (4N - 4n + 3 + 2 + 1) + (4n - 5 - 4 + 3)
                = 4N.
        This is exactly what we need!

    ANALYSIS: THE LEFT AND RIGHT COLUMNS

        The situation here is a bit different as the corner elements
        are complementary.  But we still have an asymmetry.  But this
        is easily fixed.

        We can use blocks of four in the same way, but stop when just
        two rows are left.  We assume her that the left side has n+1
        in the top corner and the right side accordingly has n+2.

        The rules adopted by al-Antaki are:

            RULE 3: on the left side, starting below the top corner,
                consectively by row, in groups of 4 rows, place the
                complements in the first and fourth cell an low values
                in the second and third cell.

            RULE 4: on the left side in the two cells that remain,
                place the complement of the penultimate ("next-to-last")
                value in the fist cell and the ultimate) or last
                low value in the second.

        RULE 4 restores symmetry by forming a group of four rows with
        the top and bottom rows.
    """

    def __init__(self, traditional_sq:MagicSquare):
        """constructor

        We suppress the magic_zero check since the input must be
        a traditional magic square with entries running from 1
        through n².  Instead we check that the input is evenly even in
        order and has magic number n(n²+1)/2. We then shift the input
        so that the values are properly centered.

        The shift value h=2n+2 can be obtaining by subtracting the
        median element in the input, i.e. (n²+1)/2, from the median
        element in the output, i.e. ((n+2)²+1)/2.  The difference h
        is given by h=2n+2.

        The real work is done in method configure_frame.
        """
        n = traditional_sq.n
        assert n % 4 == 2, "require oddly even order"
        assert traditional_sq.magic == n*(n*n+1)//2, "traditional"

        self.picture = traditional_sq.translate(2*n + 2)

        super().__init__(self.picture, magic_zero=False)
        self.name = f"{self.__class__.__name__}: framed picture"
        self.name += f" / order {n} -> order{n+2}"

    def configure_frame(self):
        """configure the frame"""
        picture = self.picture
        n = self.picture.n                  # order of the picture
        entry_limit = (n+2)**2 + 1
        prime = lambda i: entry_limit - i   # the complement
        top, bottom = self.top, self.bottom
        left, right = self.left, self.right

            # fill in the corner entries
        top[0] = n+1
        top[n+1] = n+2
        bottom[n+1] = prime(n+1)
        bottom[0] = prime(n+2)
        base = n+2
        
        for i in range(1, n+1):
                # decide on placement of i
            if i < n-5:         # RULE 2 - group of four
                top[i], bottom[i] = (i, prime(i)) if i%4 < 2 \
                    else (prime(i), i)
            else:               # RULE 1 - last six cells
                j = i - (n-6)
                top[i], bottom[i] = (i, prime(i)) if j%6 in {1, 2} \
                    else (prime(i), i)

                # decide on placement of base+i
            j = base + i
            if i < n-1:         # RULE 2 - group of four
                right[i], left[i] = (j, prime(j)) if i%4 < 2 \
                    else (prime(j), j)
            else:               # RULE 1 - last two cells
                right[i], left[i] = (j, prime(j)) if i%2 == 1 \
                    else (prime(j), j)

        #   for testing
        #print("Output:")
        #print(self)
        #print("Magic:", self.row_sum(0))

class alAntakiOddlyEven(FramedMagicSquare):
    """al-Buzjani's frame around evenly even order magic squares:
    The result is an oddly even magic square.

    NOTE ON THE DISCUSSION

        Placement of entries on the left side in the implementation
        is from top to bottom.  In the discussion, it is bottom to
        top.  The discussion ordering can be obtained by applying
        a permutation to the left and right side:

            n = insq.n                          # get the order
            outsq = alAntakiOddlyEven(insq)
            bwd = list(reversed(range(1, n+1)))
            outsq2 = output_square.vertical_permutation(bwd)            

    THE ALGORITHM

        We will illustrate the process for inputs of order n=4 and n=8.

        STEP 1:
            Starting in the bottom, avoiding corners, place the numbers
            1 through 3 alternately in the bottom and top rows.  The
            complements are placed opposite these values:

                n=4 -> n+2=6             n=8 -> n+2=10
                 * 36  2 34  *  *        * 100  2 98  *  *  *  *  *  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  1 35  3  *  *        *   X  X  X  X  X  X  X  X  *
                    ^  ^  ^              *   X  X  X  X  X  X  X  X  *
                                         *   X  X  X  X  X  X  X  X  *
                                         *   X  X  X  X  X  X  X  X  *
                                         *   1 99  3  *  *  *  *  *  *
                                             ^  ^  ^

        STEP 2:
            In a counterclockwise direction, rotate and, avoiding
            corners, place the next number in an available slot,
            and its complement opposite.  Repeat this step until the
            number n has been placed:

                n=4 -> n+2=6             n=8 -> n+2=10
                 * 36  2 34  *  *        * 100  2 98  5 94  *  *  *  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
              > 33  X  X  X  X  4        *   X  X  X  X  X  X  X  X  *
                 *  1 35  3  *  *        *   X  X  X  X  X  X  X  X  *
                                      > 93   X  X  X  X  X  X  X  X  8
                                      >  6   X  X  X  X  X  X  X  X 95
                                      > 97   X  X  X  X  X  X  X  X  4
                                         *   1 99  3 96  7  *  *  *  *
                                                      ^  ^

        STEP 3:
            Fill in the corners starting top left with n+1, top right
            with n+2, and their complements diagonally opposite:

                n=4 -> n+2=6             n=8 -> n+2=10
                 5 36  2 34  *  6        9 100  2 98  5 94  *  *  * 10
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
                33  X  X  X  X  4        *   X  X  X  X  X  X  X  X  *
                31  1 35  3  * 32        *   X  X  X  X  X  X  X  X  *
                                        93   X  X  X  X  X  X  X  X  8
                                         6   X  X  X  X  X  X  X  X 95
                                        97   X  X  X  X  X  X  X  X  4
                                        91   1 99  3 96  7  *  *  * 92

        STEP 4:
            The next two numbers (n+3 and n+4) are placed on the left
            side...:

                n=4 -> n+2=6             n=8 -> n+2=10
                 5 36  2 34  *  6        9 100  2 98  5 94  *  *  * 10
                 *  X  X  X  X  *        *   X  X  X  X  X  X  X  X  *
               > 8  X  X  X  X 29        *   X  X  X  X  X  X  X  X  *
               > 7  X  X  X  X 30        *   X  X  X  X  X  X  X  X  *
                33  X  X  X  X  4     > 12   X  X  X  X  X  X  X  X 89
                31  1 35  3  * 32     > 11   X  X  X  X  X  X  X  X 90
                                        93   X  X  X  X  X  X  X  X  8
                                         6   X  X  X  X  X  X  X  X 95
                                        97   X  X  X  X  X  X  X  X  4
                                        91   1 99  3 96  7  *  *  * 92

        STEP 5:
            Place the remaining numbers as in step 2, starting with the
            bottom of the frame.
    
                n=4 -> n+2=6             n=8 -> n+2=10
                 5 36  2 34 28  6        9 100  2 98  5 94 88 15 84 10
              > 27  X  X  X  X 10     > 83   X  X  X  X  X  X  X  X 18
                 8  X  X  X  X 29     > 16   X  X  X  X  X  X  X  X 85
                 7  X  X  X  X 30     > 87   X  X  X  X  X  X  X  X 14
                33  X  X  X  X  4       12   X  X  X  X  X  X  X  X 89
                31  1 35  3  9 32       11   X  X  X  X  X  X  X  X 90
                             ^          93   X  X  X  X  X  X  X  X  8
                                         6   X  X  X  X  X  X  X  X 95
                                        97   X  X  X  X  X  X  X  X  4
                                        91   1 99  3 96  7 13 86 17 92
                                                            ^  ^  ^

        CHECKS

            1) Numbers opposite each other in the frame should sum
               to (n+2)²+1 as the order of the output is n+2.

            2) The top row should sum to (n+2)((n+2)²+1) / 2.

                a)  5+36+2+34+28+6 = 111
                    6 (37) / 2 = 111                    Check!
                b)  9+100+2+98+5+94+88+15+84+10 = 505
                    10 (101) / 2 = 505                  Check!

            3) The left side should sum to (n+2)((n+2)²+1) / 2.

                a) 5+27+8+7+33+31 = 111                 Check!
                b) 9+83+16+87+12+11+93+6+97+91 = 505    Check!

            (The magic number is (n+2)((n+2)²+1) / 2.)
    """
    def __init__(self, traditional_sq:MagicSquare):
        """constructor

        We suppress the magic_zero check since the input must be
        a traditional magic square with entries running from 1
        through n².  Instead we check that the input is oddly eve in norder
        and has magic number n(n²+1)/2. We then shift the input so
        that the values are properly centered.

        The shift value h=2n+2 can be obtaining by subtracting the
        median element in the input, i.e. (n²+1)/2, from the median
        element in the output, i.e. ((n+2)²+1)/2.  The difference h
        is given by h=2n+2.

        The real work is done in configure frame.
        """
        n = traditional_sq.n
        assert n % 4 == 0, "require evenly even order"
        assert traditional_sq.magic == n*(n*n+1)//2, "traditional"

        self.picture = traditional_sq.translate(2*n + 2)

        super().__init__(self.picture, magic_zero=False)
        self.name = f"{self.__class__.__name__}: framed picture"
        self.name += f" / order {n} -> order{n+2}"

    def configure_frame(self):
        """configure the frame"""
        picture = self.picture
        n = self.picture.n                  # order of the picture
        entry_limit = (n+2)**2 + 1
        prime = lambda k: entry_limit - k   # the complement
        top, bottom = self.top, self.bottom
        left, right = self.left, self.right

        ccw = {bottom:right, right:top, top:left, left:bottom}
        state = {top:0, left:0}             # MRU
        key = {top:top, bottom:top, left:left, right:left}
        opp = {top:bottom, bottom:top, left:right, right:left}
        prime = lambda i: entry_limit - i

        k = 0                               # most recent placed

            # STEP ONE
        here = top
        while k < 3:                        # place 1, 2 and 3
            k += 1
            there, here = here, opp[here]       # swap
            state[top] += 1
            i = state[top]                      # get next index
            here[i], there[i] = (k, prime(k))   # update

            # STEP TWO
        here = bottom
        while k < n:
            k += 1
            here = ccw[here]                    # rotate
            there = opp[here]
            state[key[here]] += 1
            i = state[key[here]]
            here[i], there[i] = k, prime(k)

            # STEP THREE
        top[0], top[n+1] = n+1, n+2
        bottom[n+1], bottom[0] = prime(n+1), prime(n+2)
        k = n+2

            # STEP FOUR
        here, there = left, right
        while k < n+4:
            k += 1
            state[left] += 1
            i = state[left]                    # get next index
            here[i], there[i] = (k, prime(k))   # update

            # STEP FIVE
        while k < 2*n+2:
            k += 1
            here = ccw[here]                    # rotate
            there = opp[here]
            state[key[here]] += 1
            i = state[key[here]]
            here[i], there[i] = k, prime(k)

        #   for testing
        #print("Output:")
        #print(self)
        #print("Magic:", self.row_sum(0))

if __name__ == "__main__":
        # self-test

    from magic_squares.order4 import Melencolia1514

    def test1(square):
        """self test"""
        n = square.n
        print("Input:", square.name, "/ order:", n)
        print(square)
        new_square = alAntakiEvenlyEven(square)
        print("Output:", new_square.name, "/ order:", new_square.n)
        print(new_square)
        expect = (n+2)*((n+2)**2 + 1) // 2
        print("Magic number:", new_square.magic, "/ expected:", expect)
        assert new_square.magic == expect
        return new_square

    def test2(square):
        """self test"""
        n = square.n
        print("Input:", square.name, "/ order:", n)
        print(square)
        new_square = alAntakiOddlyEven(square)
        print("Output:", new_square.name, "/ order:", new_square.n)
        print(new_square)
        expect = (n+2)*((n+2)**2 + 1) // 2
        print("Magic number:", new_square.magic, "/ expected:", expect)
        assert new_square.magic == expect
        return new_square

        #   to start, we need a magic square of order 6.  Fortunately
        # one is given in [1].

    Sol = MagicSquare.from_sq([[ 6, 32,  3, 34, 35,  1],
                               [ 7, 11, 27, 28,  8, 30],
                               [19, 14, 16, 15, 23, 24],
                               [18, 20, 22, 21, 17, 13],
                               [25, 29, 10,  9, 26, 12],
                               [36,  5, 33,  4,  2, 31]])
    Sol.name = "Sol"
    test1(Sol)

        #   To test the next case, we need a magic square of order 10.
        # An internet search found this one at [2].

    data = """25 26 15 14 83 82 69 68 57 56
              27 24 12 13 80 81 70 71 58 59
              61 62 50 51 38 39  4  5 92 93
              63 60 48 49 36 37  6  7 94 95
              16 19 86 87 74 75 40 41 28 29
              18 17 84 85 72 73 42 43 30 31
              52 55 23 22 11 10 97 96 65 64
              54 53 21 20  9  8 99 98 67 66
              88 89 77 76 47 46 35 34  3  0
              91 90 79 78 45 44 33 32  1  2
              """
    data = list(map(int, data.split()))
    order10 = []
    for i in range(10):
        order10.append(data[10*i:10*i+10])
    order10 = MagicSquare.from_sq(order10)
    order10 = order10.translate(1)
    order10.name = "Grogono's order 10 magic square"
    test1(order10)

        #   And to test the next case, we need a magic square of order
        # 14. An internet search found this one (and many others) at
        # [3].

    data = """1 95 191 112 138 78 58 32 17 159 146 178 125 49
            147 16 110 176 188 127 87 117 4 53 70 83 38 163
            126 162 31 137 172 63 80 6 47 26 97 99 149 184
            190 111 150 46 155 115 5 77 34 170 23 96 140 67
            164 84 55 12 121 86 29 101 133 62 173 25 186 148
            104 10 89 37 21 166 179 154 195 74 44 134 59 113
            19 35 132 57 3 153 196 165 180 92 122 51 72 102
            45 65 71 90 36 193 152 181 168 119 130 2 103 24
            30 43 60 73 94 182 167 194 151 107 7 118 22 131
            68 144 156 27 75 48 105 93 120 136 183 42 11 171
            81 187 175 114 69 18 135 52 85 14 106 143 160 40
            139 174 8 161 142 108 116 15 79 185 39 61 54 98
            177 129 123 192 56 33 20 64 100 141 82 158 91 13
            88 124 28 145 109 9 50 128 66 41 157 189 169 76 
           """
    data = list(map(int, data.split()))
    order14 = []
    for i in range(14):
        order14.append(data[14*i:14*i+14])
    order14 = MagicSquare.from_sq(order14)
    order14.name = "Taneja's order 14 magic square"
    test1(order14)
    
        # Now we test the oddly even module.  For this we will start
        # with Albrecht Dürer's square

    sq2 = test2(Melencolia1514)
    sq3 = test1(sq2)
    sq4 = test2(sq3)
    sq5 = test1(sq4)
    sq6 = test2(sq5)

    print("SUCCESS!")
