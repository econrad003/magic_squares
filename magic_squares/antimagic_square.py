"""
antimagic_square.py - antmagic square tools
Copyright © 2023 by Eric Conrad

DESCRIPTION

    An antimagic square is a square matrix with integer entries
    whose rows, columns, and diagonals all add up to a set of distinct
    integers which, in some order, form an arithmetic progression.
    (Generally the entries are expected to be from 1 to n² and the
    progression to be consecutive.)

    Implemented here are the following classes:

        AntimagicSquare - a class derived from the magic squares
            class.

REFERENCES

    [1] "Antimagic square" in Wikipedia. 8 Nov. 2023.  Web.
        Accessed 25 November 2023.

MODIFICATIONS

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
from fractions import Fraction
from magic_squares.listlike2D import listlike2D
from magic_squares.magic_square import MagicSquare

class AntimagicSquare(MagicSquare):
    """a base class for antimagic squares

    The main difference between magic squares and antimagic squares is
    in the check for the magic property.

    We leave the option for diagonals in place -- so semiantimagic
    squares are certainly a possibility.

    We also need to change the "new_target" class method..
    """

    def __init__(self, *args, **kwargs):
        """initialization"""
        self.name = "antimagic square"
        super().__init__(*args, **kwargs)

    def check(self):
        """check that the matrix is an anti magic square

        DESCRIPTION

            This replaces the magic check.  A key difference here is
            that the attribute "magic" is a range object.  (If the
            check is omitted (via debug=True), then the attribute
            "magic" be a row sum.)

        NOTE ON WARNING EXCEPTIONS

            It is very easy to make a mistake when entering a matrix
            manually.  Two lines are displayed before the Warning
            exception is raised.  The first displays the sums in the
            order received: (row 0, column 0, row 1, column 1, ...,
            row n, column n, main diagonal, back diagonal).  The
            second line displays the same values in sorted order.
            Use the second line to find a value that fits poorly
            with the others.  Then use the first line to find the row
            or column that contains that sums to that value.  Good luck!
        """
        magic = []
        for i in range(self.n):
            magic.append(self.row_sum(i))
            magic.append(self.column_sum(i))
        if self.diagonals:
            magic.append(self.main_diagonal_sum())
            magic.append(self.back_diagonal_sum())
        magic2 = sorted(magic)

        delta = magic2[1] - magic2[0]       # candidate difference
        if delta == 0:
            print("Row/col/diag:", magic)
            print(" Progression:", magic2)
            raise Warning('The values of the sums must be distinct')
        for i in range(2, len(magic)):
            if magic2[i] - magic2[i-1] != delta:
                print("Row/col/diag:", magic)
                print(" Progression:", magic2)
                raise Warning('Not an arithmetic progression')

        self._magic = range(magic2[0], magic2[-1]+delta, delta)
        return self._magic

    @classmethod
    def new_target(cls, *args, use_my_class=False, **kwargs) -> object:
        """create a new target

        We normally want AntimagicSquare, not cls!  
        """
        if use_my_class:
            return cls(*args, **kwargs)
        else:
            return AntimagicSquare(*args, **kwargs)

if __name__ == "__main__":
        # self-test
    x = [[2, 15, 5, 13], [16, 3, 7, 12], [9, 8, 14, 1], [6, 4, 11, 10]]
    x = AntimagicSquare.from_sq(x)
    print(x.name)
    print(x)
    print("antimagic progression:", list(x.magic))
    print("                delta:", x.magic.step)
    assert x.magic == range(29, 39)

    print("SUCCESS!")
