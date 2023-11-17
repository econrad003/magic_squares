"""
al_Buzjani.py - extend an odd order magic square by bordering
Copyright © 2023 by Eric Conrad

DESCRIPTION

    Implemented here is al-Buzjani's method for bordering a magic
    square of odd order.  See the Wikipedia article on magic squares
    or read the source code for more details.

REFERENCES

    [1] "Magic squares" in Wikipedia.  Web.  Accessed 11 November 2023.

MODIFICATIONS

    16 Nov 2023 - EC
        1) added reference.
        2) move class alBuzjaniBorder from module bordering here
           as a separate module.

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
from magic_squares.bordering import FramedMagicSquare
from magic_squares.decorators import Tier

class alBuzjaniBorder(FramedMagicSquare):
    """al-Buzjani's frame for odd order squares

    This is a fast way of extending an odd order (nxn) square to an
    (n+2)x(n+2) square -- fast but not very general.  As off-diagonal
    elements in the frame can be permuted in vertical or horizontail
    pairs along the edges, there are large number of symmetries.
    """

    def __init__(self, traditional_sq:MagicSquare):
        """constructor

        We suppress the magic_zero check since the input must be
        a traditional magic square with entries running from 1
        through n².  Instead we check that the input is odd in order
        and has magic number n(n²+1)/2. We then shift the input so
        that the values are properly centered.

        The shift value h=2n+2 can be obtaining by subtracting the
        median element in the input, i.e. (n²+1)/2, from the median
        element in the output, i.e. ((n+2)²+1)/2.  The difference h
        is given by h=2n+2.

        The real work is done in configure frame.
        """
        n = traditional_sq.n
        assert n % 2 == 1, "require odd order"
        assert traditional_sq.magic == n*(n*n+1)//2, "traditional"

        picture = traditional_sq.translate(2*n + 2)

        super().__init__(picture, magic_zero=False)

    def configure_frame(self):
        """configure the frame"""
        n = self.n                  # order
        bmax = n*n+1                # range stop for entries
            # lower left and points opposite where high value go
            #       3
            #       1
            #       x 2 4 
        m = 1
        i, j = n-2, 1
        while m < n-2:
            self.left[i] = m
            self.right[i] = bmax - m
            # print("LR", i, m, bmax-m)  
            i -= 1
            m += 1
            self.bottom[j] = m
            self.top[j] = bmax - m
            # print("BT", j,  m, bmax-m)  
            j += 1
            m += 1
        self.bottom[j] = m              # this is the picture order!
        self.top[j] = bmax - m
        # print("BT", j,  m, bmax-m)  
        j += 1
        m += 1
        self.top[0] = m                 # top left
        self.bottom[n-1] = bmax - m     # botton right
        # print("D1", "-",  m, bmax-m)  
        m += 1
        self.right[i] = m               # middle row (framed pic order)
        self.left[i] = bmax - m
        # print("RL", i,  m, bmax-m)  
        i -= 1
        m += 1
        self.top[n-1] = m               # top right
        self.bottom[0] = bmax - m       # botton left
        # print("D2", "-",  m, bmax-m)  
        m += 1
            # upper right and points opposite
            #       12 14 16 10     (here framed for n=9)
            #                15
            #                13
            #                11
            #                 9 <-- order n, middle row
        while i > 0:
            self.right[i] = m
            self.left[i] = bmax - m
            # print("RL", i,  m, bmax-m)  
            i -= 1
            m += 1
            self.top[j] = m
            self.bottom[j] = bmax - m
            # print("TB", j,  m, bmax-m)  
            j += 1
            m += 1

if __name__ == "__main__":
        # self-test
    from random import shuffle

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
    foo = test(SiameseMagicSquare(3))
    foo = test(SiameseMagicSquare(5))
    foo = test(SiameseMagicSquare(7))
    foo = test(foo)

    print("SUCCESS!")
