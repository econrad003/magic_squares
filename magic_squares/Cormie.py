"""
Cormie.py - John Cormie's constructions of antimagic squares
Copyright © 2023 by Eric Conrad

DESCRIPTION

    Implemented here are John Cormie's methods for constructing
    antimagic squares. [1]

    These constructions produce antimagic squares of order at least
    five.  The odd ones are generated from scratch.  The even ones
    are produced by framing a smaller even square.
    
    Since there are known examples of order 4 antimagic squares with
    entries 1..16 and step 1, Cormie's results are a constructive
    demonstration that there are step 1 squares of order n with entries
    covering 1..n² for all n≥2.

    The classes implemented here are:

        1) CormieOdd - antimagic squares of odd order (n = 5, 7, 9,
           11, 13, etc.)

        2) 

IMPLEMENTATION NOTES

    The C programs mentioned on the web site were unavailable --
    the algorithms here are based on the descriptions and examples
    provided on the site and not on the source code.

    Details were missing from the description of the construction
    of the n=4k+3 case.  But the examples for 7, 11, and 19 were
    helpful.  (The example for n=15 is missing.)


REFERENCES

    [1] John Cormie.  "The antimagic square project".  Web. Accessed
        25 Nov 2023.
            http://ion.uwinnipeg.ca/~vlinek/jcormie/

MODIFICATIONS

    25 Nov 2023 - EC - initial version
        1) CormieOdd - completed 27 Nov 2023

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
from magic_squares.antimagic_square import AntimagicSquare

    # methods test_band and test_pattern were a big help in
    # debugging!

def test_band(target:MagicSquare, start:tuple,
              direction:tuple, x_start:int, color):
    """fill in a band for testing"""
    i, j = start
    h, k = direction
    x = x_start
    for p in range(target.n):
        target[(i, j)] = color + str(x)
        x += 1
        i = (i+h) % target.n
        j = (j+k) % target.n

def test_pattern(target:MagicSquare):
    """print a test pattern"""
    print("Test Pattern:")
    for i in range(target.n):
        line = []
        for j in range(target.n):
            line.append(target[(i, j)])
        print(line)

        #
        #  The real stuff is all here!
        #

class CormieOdd(AntimagicSquare):
    """John Cormie's construction of antimagic squares of odd order

    The general idea is to create a magic square which provides the
    high order digit and an antimagic square which provides the low
    order digit in a two-digit base n number.  (If we take the digits
    in the wrong order, the step size will go from 1 to n, but the
    result will still be antimagic).

    The details differ for evenly odd and oddly odd, but the overall
    idea is the same.
    """

        # SQUARE 1 - degenerate magic square with magic constant 0
        #       used a a prototype.
        #   It is used to determine the high order digit base n
        #   of the entry in the antimagic square.

    @classmethod
    def make_square1(cls, n:int) -> MagicSquare:
        """Build the first prototype, a magic square of odd order

        The result is a degenerate magic square.
        """
        k = n // 2
        if n != 2*k+1 or n < 0:
            raise ValueError(f'n={n} must be an odd integer.')
        range1 = range(1, k+1)
        range2 = reversed(range1)
        list1 = list(range1) + list(-i for i in range2) + [0]

        table1 = MagicSquare(n, debug=True)

            # here we configure the square:
            #   it is just an addition table for ℤ/nℤ, but it is
            #   arranged in an unusual way.

        for i in range(n):
            for j in range(n):
                x = (i + list1[j]) % n
                if x > n/2:
                    x -= n
                table1[(i, j)] = x

        table1.check()          # make sure it works.
        return table1

    @classmethod
    def band(cls, target:MagicSquare, start:tuple,
                  direction:tuple, x_start:int):
        """fill in a band

        The antimagic prototype is a band matrix.  Each band consists
        of the numbers from -n//2 through n//2 arranged consectively
        from corner to corner, starting from one cell in the band,
        proceeding diagonally in one direction and ending in the 
        diagonal predecessor.

        The bands are parallel to the antidiagonal.  Each band
        has n entries. Except for the antidiagonal itself, the bands
        wrap according to the torus topology on the square.  For
        example, here are the five bands in an order 5 matrix:

                1 2 3 4 5
                2 3 4 5 1
                3 4 5 1 2
                4 5 1 2 3
                5 1 2 3 4

        If we start in band 2 row 0 and number the cells in a
        northeasterly direction, the entries would look like this:

                * -2  *  *  *
                2  *  *  *  *
                *  *  *  *  1
                *  *  *  0  *
                *  * -1  *  *
        """
        i, j = start
        h, k = direction
        x = x_start
        for _ in range(target.n):
            target[(i, j)] = x
            x += 1
            i = (i + h) % target.n
            j = (j + k) % target.n

    @classmethod
    def red_band1(cls, target:MagicSquare):
        """fill in the red band (n=4k+1)"""
        k = target.n // 4
        start = (2*k, 2*k)
        direction = (-1, 1)
        x_start = -2*k
        cls.band(target, start, direction, x_start)

    @classmethod
    def red_bands3(cls, target:MagicSquare):
        """fill in the red bands (n=4k+3)"""
        k = target.n // 4
        x_start = - 2*k - 1
        start = (2*k + 1, 2*k)
        direction = (1, -1)
        cls.band(target, start, direction, x_start)
        start = (2*k + 1, 2*k + 1)
        direction = (-1, 1)
        cls.band(target, start, direction, x_start)
        start = (2*k + 2, 2*k + 1)
        direction = (1, -1)
        cls.band(target, start, direction, x_start)

    @classmethod
    def blue_bands1(cls, target:MagicSquare):
        """fill in the blue bands (n=4k+1)"""
        n = target.n
        k = n // 4
        u, v = n-1, n-1         # SE corner
        x_start = -2*k
        for _ in range(k-1):
            start = (u, v)
            direction = (1, -1)
            cls.band(target, start, direction, x_start)
            u -= 1                  # go up
            start = (u, v)
            direction = (-1, 1)
            cls.band(target, start, direction, x_start)
            v -= 1                  # go west

                # knight SSW of NE corner (S of red -1)
        u, v = 2, n-2
        for _ in range(k-1):
            start = (u, v)
            direction = (1, -1)
            cls.band(target, start, direction, x_start)
                # knight ENE of start
            u, v = (u-1) % n, (v+2) % n
            start = (u, v)
            direction = (-1, 1)
            cls.band(target, start, direction, x_start)
                # (4,3) leaper S⁴W³ of start
            u, v = (u+4) % n, (v-3) % n

    @classmethod
    def blue_bands3(cls, target:MagicSquare):
        """fill in the blue bands (n=4k+3)"""
        n = target.n
        k = n // 4
        u, v = n-4, 1         # (3,1) leaper NNNE of SW corner
        x_start = -2*k-1
        for _ in range(k-1):
            start = (u, v)
            direction = (-1, 1)
            cls.band(target, start, direction, x_start)
            u, v = (u+1) % n, (v-2) % n # knight WWS
            start = (u, v)
            direction = (1, -1)
            cls.band(target, start, direction, x_start)
            u, v = (u-4) % n, (v+3) % n    # (4,3) leaper

                # below NE corner 
        u, v = 1, 0
        for _ in range(k-1):
            start = (u, v)
            direction = (-1, 1)
            cls.band(target, start, direction, x_start)
            u = (u+1) % n                   # down one
            start = (u, v)
            direction = (1, -1)
            cls.band(target, start, direction, x_start)
            v = (v+1) % n                   # east one

    @classmethod
    def green_bands1(cls, target:MagicSquare):
        """fill in the green bands (n=4k+1)"""
        n = target.n
        k = n // 4
        x_start = -2*k
        u, v = 2*k+1, n-1
        start = (u, v)
        direction = (1, -1)
        cls.band(target, start, direction, x_start)
        v -= 1
        start = (u, v)
        cls.band(target, start, direction, x_start)

    @classmethod
    def green_bands3(cls, target:MagicSquare):
        """fill in the green bands (n=4k+3)"""
        n = target.n
        k = n // 4
        x_start = -2*k-1
        u, v = n-2, 2*k+1
        start = (u, v)
        direction = (-1, 1)
        cls.band(target, start, direction, x_start)
        v += 1
        start = (u, v)
        cls.band(target, start, direction, x_start)

    @classmethod
    def turquoise_bands1(cls, target:MagicSquare):
        """fill in the turquoise bands (n=4k+1)

        In my web browser, these appear as a pale blue (sky blue?)
        instead of as turquoise.
        """
        n = target.n
        k = n // 4
        x_start = -2*k
        u, v = 2*k-2, 0
        start = (u, v)
        direction = (-1, 1)
        cls.band(target, start, direction, x_start)
        u, v = 0, 2*k+1
        start = (u, v)
        cls.band(target, start, direction, x_start)

    @classmethod
    def turquoise_bands3(cls, target:MagicSquare):
        """fill in the turquoise bands (n=4k+3)

        In my web browser, these appear as a pale blue (sky blue?)
        instead of as turquoise.
        """
        n = target.n
        k = n // 4
        x_start = -2*k-1
        u, v = 2*k+2, n-1
        start = (u, v)
        direction = (1, -1)
        cls.band(target, start, direction, x_start)
        u, v = 2*k+1, 1
        start = (u, v)
        direction = (-1, 1)
        cls.band(target, start, direction, x_start)

    @classmethod
    def make_square2(cls, n:int) -> AntimagicSquare:
        """make the antimagic prototype (n=4k+1)

        Cormie colors the bands using the colors red, blue, green
        and turquoise (sky blue?).  The coloring depends on order.

                EVENLY ODD CASE

        If n=4k+1, there is one red band (the antidiagonal),
        2 green bands, and two turquoise bands.  The remaining
        n-5 bands are blue.  Half of the blue bands are immediately
        above the red band, and half are immediately below.  The
        two green bands are separated on both sides from the blue bands
        (or red for n=5) by the turquoise bands.  For n=9, the band
        coloring (1 red, 2 each of blue, green and turquoise) looks
        like this:

                B B T G G T B B R
                B T G G T B B R B
                T G G T B B R B B
                G G T B B R B B T
                G T B B R B B T G
                T B B R B B T G G
                B B R B B T G G T
                B R B B T G G T B
                R B B T G G T B B
        """
        k = n // 4
        if n != 4*k + 1:
            raise ValueError(f'n={n}≠4·{k}+1: n must be evenly odd.')

        target = AntimagicSquare(n, debug=True)

            # add the bands
        cls.red_band1(target)
        cls.blue_bands1(target)
        cls.green_bands1(target)
        cls.turquoise_bands1(target)

        target.check()
        return target

    @classmethod
    def make_square3(cls, n:int) -> AntimagicSquare:
        """make the antimagic prototype (n=4k+3)

        Cormie colors the bands using the colors red, blue, green
        and turquoise (sky blue?).  The coloring depends on order.

                ODDLY ODD CASE

        If n=4k+3, there are three red bands (the antidiagonal and
        its immediate neighbors), 2 green bands, and two turquoise
        bands.  The remaining n-7 bands are blue.  Half of the blue
        bands are immediately above the red bands, and half are
        immediately below.  The two turquoise bands are closer to
        the antidiagonal than the two green ones.  For n=11, the band
        coloring (3 red, 2 each of blue, green and turquoise) looks
        like this:

                R B B G G T T B B R R
                B B G G T T B B R R R
                B G G T T B B R R R B
                G G T T B B R R R B B
                G T T B B R R R B B G
                T T B B R R R B B G G
                T B B R R R B B G G T
                B B R R R B B G G T T
                R R R B B G G T T B B
                R R B B G G T T B B R
        """
        k = n // 4
        if n != 4*k + 3:
            raise ValueError(f'n={n}≠4·{k}+3: n must be oddly odd.')

        target = AntimagicSquare(n, debug=True)

            # add the bands
        cls.red_bands3(target)
        cls.blue_bands3(target)
        cls.green_bands3(target)
        cls.turquoise_bands3(target)

        # target.check()
        return target

    def configure(self):
        """create an antimagic square of odd order (n>4, n odd)

        The prototypes are saved as _prototype1 (MagicSquare) and
        _prototype2 (AntimagicSquare).
        """
        n = self.n
        k = n // 4
        m = n % 4
        if n < 4:
            msg = "There are no antimagic squares of order " \
                + "n less than 4 with entries from 1 consecutively " \
                + "through n² and magic difference 1 (except " \
                + "n=0)"
            raise ValueError(msg)
        if n % 2 != 1:
            raise ValueError(f'n={n} must be odd')

        self._prototype1 = square1 = self.make_square1(n)
        self._prototype2 = square2 = self.make_square2(n) if m == 1 \
            else self.make_square3(n)

        for i in range(n):
            for j in range(n):
                    # use the two prototypes to create a number in
                    # base n
                x, y = square1[(i,j)] + 2*k, square2[(i,j)] + 2*k
                self[(i, j)] = n*x + y + 1

        self.name = "John Cormie's odd order construction" \
            + f"n = {n} = 4·{k}+{m}"
        self.cite = "John Cormie (1999)"

if __name__ == "__main__":
        # self-test
    for n in range(5, 20, 2):
        k = n // 4
        m = n % 4
        print(f'n = {n} = 4·{k}+{m} -- Cormie Odd')
        foo = CormieOdd(n)
        print(foo.name)
        print(foo)
        m = foo.magic
        print(f"start: {m.start}  stop:{m.stop}  step: {m.step}")

    print("SUCCESS!")
