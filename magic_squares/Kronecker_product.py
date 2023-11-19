"""
Kronecker_product.py - take the Kronecker product of two magic squares
Copyright © 2023 by Eric Conrad

DESCRIPTION

    The Kronecker product of two matrices A and B is a block
    matrix with blocks of the form [a[i,j]B] where a[i,j] is
    a typical entry in A.

    For example, given:

            +-     -+           +-           -+
            | 4 9 2 |           | 16  3  2 13 |
        A = | 3 5 7 |       B = |  5 10 11  8 |
            | 8 1 6 |           |  9  6  7 12 |
            +-     -+           |  4 15 14  1 |
                                +-           -+
    Then:
                +-        -+
                | 4B 9B 2B |
        A ⦻ B = | 3B 5B 7B |
                | 8B  B 6B |
                +-        -+
            
                +-                                                   -+
                |  64  12   8  52 | 144  27  18 117 |  32   6   4  26 |
                |  20  40  44  32 |  45  90  99  72 |  10  20  22  16 |
                |  36  24  28  48 |  81  54  63 108 |  18  12  14  24 |
                |  16  60  56   4 |  36 135 126   9 |   8  30  28   2 |
                +-----------------------------------------------------+
                |  48   9   6  26 |  80  15  10  65 | 112  21  14  91 |
              = |  15  30  33  24 |  25  50  55  40 |  35  70  77  56 |
                |  27  18  21  36 |  45  30  35  60 |  63  42  49  84 |
                |  12  15  42   3 |  20  75  70   5 |  28 105  98   7 |
                +-----------------------------------------------------+
                | 128  24  16 104 |  16   3   2  13 |  96  18  12  78 |
                |  40  80  88  64 |   5  10  11   8 |  30  60  66  48 |
                |  72  48  56  96 |   9   6   7  12 |  54  36  42  72 |
                |  32 120 112   8 |   4  15  14   1 |  24  90  84   6 |
                +-                                                   -+

    The Kronecker product is not commutative.  The implementation here
    requires requires square matrices of any order. The Kronecker
    product, however, is defined for any pair of matrices.

    The Kronecker product of two magic squares is itself a magic
    square.  But note in the example that the first row second column
    and the eighth row first column are both 12.  The result will
    generally NOT consist of entries in some order with consecutive
    values ranging from 1 through the square of the order.

REFERENCES

    [1] "Magic squares" in Wikipedia.  Web.  Accessed 11 November 2023.
            URL https://en.wikipedia.org/wiki/Magic_square

    [2] "Kronecker product" in Wikipedia. 15 November 2023. Web. 
        Accessed 18 November 2023.
            URL https://en.wikipedia.org/wiki/Kronecker_product

MODIFICATIONS

    18 Nov 2023 - EC - first version

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

def KroneckerProduct(a:MagicSquare, b:MagicSquare,
                     debug=False) -> MagicSquare:
    """evaluate the Kronecker product"""
    c = list()
    for i in range(a.n):
        for p in range(b.n):
            d = list()
            for j in range(a.n):
                for q in range(b.n):
                    d.append(a[(i,j)] * b[(p,q)])
            c.append(d)
    c = MagicSquare.from_sq(c)
    c.name = "Kronecker product"
    return c

if __name__ == "__main__":
        # self-test
    from magic_squares.order4 import Melencolia1514

    a = SiameseMagicSquare(3)
    print("A:", a.name)
    print(a)

    b = Melencolia1514
    print("B:", b.name)
    print(b)
    
    c = KroneckerProduct(a,b)
    print("A ⦻ B:", c.name)
    print(c)

    d = KroneckerProduct(b,a)
    print("B ⦻ A:", d.name)
    print(d)
    
    print("SUCCESS!")
