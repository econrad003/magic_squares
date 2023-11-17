"""
magic_square.py - magic square tools
Copyright © 2023 by Eric Conrad

DESCRIPTION

    Implemented here are two classes:

        MagicSquare - a base class for magic squares
        SiameseMagicSquare - an ancient algorithm for constructing
            magic squares of odd order.  The name is one of several
            customary names and is probably historically inaccurate
            as the earlist manuscript evidence comes from China.

REFERENCES

    [1] "Magic squares" in Wikipedia.  Web.  Accessed 11 November 2023.

MODIFICATIONS

    16 Nov 2023 - EC
        1) added reference.
        2) corrected the handling of n=1 in class SiameseMagicSquare
           method configure.
        3) added a few notes.

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
from math import sqrt, ceil
from magic_squares.listlike2D import listlike2D

class MagicSquare(object):
    """a base class for magic squares"""

    def __init__(self, n:int, diagonals=True, debug=False):
        """constructor"""
        if not isinstance(n, int):
            raise TypeError
        if n < 0:
            raise ValueError
        self.n = n          # number of rows and of columns
        self.diagonals = diagonals
        self._magic = None
        self.matrix = {}
        self.initialize()
        self.configure()
        if debug:
                # provide a possible magic number
            self._magic = self.row_sum(0)
        else:
                # check that the square is magic
            self.check()

    def initialize(self):
        """prepare an empty matrix"""
        for i in range(self.n):
            for j in range(self.n):
                self.matrix[(i, j)] = float('inf')

    def configure(self):
        """stub for the creation algorithm"""
        pass

    def check(self):
        """check that the matrix is a magic square"""
        self._magic = self.row_sum(0)
        for j in range(1, self.n):
            if self.row_sum(j) != self._magic:
                raise Warning(f'Row {j} sum != {self._magic}')
        for i in range(self.n):
            if self.column_sum(i) != self.magic:
                raise Warning(f'Column {i} sum != {self._magic}')
        if self.diagonals:
            if self.main_diagonal_sum() != self.magic:
                raise Warning(f'Main diagonal sum != {self._magic}')
            if self.back_diagonal_sum() != self.magic:
                raise Warning(f'Back diagonal sum != {self._magic}')
        return self._magic

    def row_sum(self, i:int) -> int:
        """sum the entries in row i"""
        total = 0
        for j in range(self.n):
            total += self.matrix[(i, j)]
        return total

    def column_sum(self, j:int) -> int:
        """sum the entries in row j"""
        total = 0
        for i in range(self.n):
            total += self.matrix[(i, j)]
        return total

    def main_diagonal_sum(self) -> int:
        """sum the entries on the main diagonal"""
        total = 0
        for i in range(self.n):
            total += self.matrix[(i, i)]
        return total

    def back_diagonal_sum(self) -> int:
        """sum the entries on the secondary diagonal"""
        total = 0
        for i in range(self.n):
            total += self.matrix[(i, self.n-i-1)]
        return total

    @property
    def magic(self):
        """return the most recent magic number without checking"""
        return self._magic

    def __getitem__(self, index:tuple) -> int:
        """get the (i, j) entry"""
        return self.matrix[index]

    def __setitem__(self, index:tuple, value) -> int:
        """set the (i,j) entry

        As this may cause the magic property to fail, the magic
        value is reset to None.  Run a check to set the value.
        """
        if not index in self.matrix:
            raise IndexError(f'Index {index} is not valid')
        self.matrix[index] = value
        self._magic = None

    def __str__(self):
        """to string"""
        s = ""
        for i in range(self.n):
            if i > 0:
                s += "\n"
            for j in range(self.n):
                s += " %4d" % self.matrix[(i, j)]
        return s

    def __len__(self):
        """number of rows"""
        return self.n

    @staticmethod
    def from_sq(source:object, n:int=None) -> object:
        """copy the magic square from a a magic square

        The keyword argument n is ignored if the source is a magic
        square (class MagicSquare) or listlike (class listlike2D)
        or a list or a tuple.  It is optional if the source is a
        dictionary.

        If the source is a dictionary and the order n is not supplied,
        then the floor of the square root of the dictionary length will
        be used.
        """
        if isinstance(source, (MagicSquare, listlike2D)):
            n = source.n
        elif isinstance(source, (tuple, list)):
            n = len(source)
            source = listlike2D(source, n, n)
        elif isinstance(source, dict):
            if not n:
                nn = len(source)
                n = int(ceil(sqrt(nn)))+1           # paranoid floor!
                while(n*n > nn):                    #
                    n -= 1                          #
        else:
            raise TypeError
        target = MagicSquare(n, debug=True)
        for i in range(n):
            for j in range(n):
                target[(i,j)] = source[(i,j)]
        target.check()
        return target

    @property
    def to_copy(self) -> object:
        """photocopy"""
        return self.from_sq(self)

    def reflect(self, axis="h") -> object:
        """reflect (or flip) about the given axis (default: "h")

        The possible axes are:
            "h" - the center row (horizontal)
            "v" - the center column (vertical)
            "d" - the main diagonal
            "a" - the antidiagonal
        """
        axis = axis.lower()
        if not axis in {"h", "v", "d", "a"}:
            raise ValueError(f'Bad axis "{axis}" of reflection')
        n = self.n
        target = MagicSquare(n, debug=False)
        if axis == "h":
            for i in range(n):
                for j in range(n):
                    target[(i, j)] = self[(n-i-1, j)]
        elif axis == "v":
            for i in range(n):
                for j in range(n):
                    target[(i, j)] = self[(i, n-j-1)]
        elif axis == "d":               # matrix transpose
            for i in range(n):
                for j in range(n):
                    target[(i, j)] = self[(j, i)]
        else:                           # matrix antitranspose
            for i in range(n):
                for j in range(n):
                    target[(i, j)] = self[(n-j-1, n-i-1)]
        target.check()
        return target

    def rotate(self, right_angles:int=1) -> object:
        """rotate counterclockwise through a number of right angles

        Each of the four distinct rotations including the identity can
        be written as the product of two reflections.  It's not the
        most efficient way, as it requires one intermediate matrix,
        but it is easy.
        """
        right_angles = right_angles % 4
        axes = ["h", "a", "v", "d"]     # e.g. a(h(A)) = rot(A,90)
        axis2 = axes[right_angles]
        temp = self.reflect()           # A -> h(A)
        return temp.reflect(axis=axis2) # h(A) -> rot(A, *)

    def translate(self, h:int, debug=False) -> object:
        """create a magic square by translation (adding a constant)"""
        n = self.n
        target = MagicSquare(n, debug=True)
        for i in range(n):
            for j in range(n):
                target[(i,j)] = self[(i,j)] + h
        if debug:
            self._magic = self.row_sum(0)
        else:
            target.check()
        return target

    def __add__(self, h:int):       # translation M+h
        """translation by constant on right"""
        if not isinstance(h, int):
            raise NotImplementedError
        return self.translate(h)

    def __radd__(self, h:int):      # translate h+M
        """translation by constant on left"""
        if not isinstance(h, int):
            raise NotImplementedError
        return self.translate(h)

    def scale(self, m:int, debug=False) -> object:
        """multiply by a constant"""
        n = self.n
        target = MagicSquare(n, debug=True)
        for i in range(n):
            for j in range(n):
                target[(i,j)] = self[(i,j)] * m
        if debug:
            self._magic = self.row_sum(0)
        else:
            target.check()
        return target

    def __mul__(self, m:int):       # right scalar multiply Mm
        """scaling by constant on right"""
        if not isinstance(m, int):
            raise NotImplementedError
        return self.scale(m)

    def __rmul__(self, m:int):      # left scalar multiply mM
        """translation by constant on left"""
        if not isinstance(m, int):
            raise NotImplementedError
        return self.scale(m)

    def affine(self, m:int, b:int, debug=False) -> object:
        """affine transformation: Y = mX + b

        This combines a scale and translate into a single tranform
        and does not create an intermediate matrix.
        """
        n = self.n
        target = MagicSquare(n, debug=True)
        for i in range(n):
            for j in range(n):
                target[(i,j)] = self[(i,j)] * m + b
        if debug:
            self._magic = self.row_sum(0)
        else:
            target.check()
        return target
        

class SiameseMagicSquare(MagicSquare):
    """magic square of odd order using Kurushima's algorithm"""

    def configure(self):
        """configure the magic square using Kurushima's algorithm"""
        n = self.n
        if n % 2 != 1:
            raise ValueError("Kurushima's algorithm requires odd order")
        self.name = f"Kurushima n={n}"

        if n == 1:              #                  [16 Nov 2023]
            self[(0, 0)] = 1
            return              # fast exit

            # fill in the center
        modulus = n * n
        c = n // 2              # center ordinate
        self[(c-1, c)] = n*n
        self[(c, c-1)] = n
        self[(c,   c)] = (n*n + 1) // 2
        self[(c, c+1)] = n*n + 1 - n
        self[(c+1, c)] = 1

        def sw(this, n):
            """southwest coordinates and update rule"""
            i, j = this
            return (i+1, j-1), n

        def ne(this, n):
            """southwest coordinates and update rule"""
            i, j = this
            return (i-1, j+1), -n

        def se(this, n):
            """southwest coordinates and update rule"""
            i, j = this
            nbr = (i+1, j+1)
            update = 1-n if i + j == n-2 else 1
            return nbr, update

        def nw(this, n):
            """southwest coordinates and update rule"""
            i, j = this
            nbr = (i-1, j-1)
            update = n-1 if i + j == n else -1
            return nbr, update

        def updater(unvisited, stack, this, nbr, update, modulus):
            """update the southwest neighbor"""
            if not nbr in unvisited:
                return
            stack.append(nbr)
            if self.matrix[nbr] < float('inf'):
                return
            self.matrix[nbr] = (self.matrix[this] + update) % modulus

        unvisited = set()
        for i in range(n):
            for j in range(n):
                unvisited.add((i,j))
        stack = [(c-1, c), (c, c-1), (c, c+1), (c+1, c), (c, c)]
        while unvisited:
            i, j = this = stack.pop()
            if not this in unvisited:
                continue
            unvisited.remove(this)
                    # check southwest neighbor
            nbr, update = sw(this, n)
            updater(unvisited, stack, this, nbr, update, modulus)
                    # check northeast neighbor
            nbr, update = ne(this, n)
            updater(unvisited, stack, this, nbr, update, modulus)
                    # check southeast neighbor
            nbr, update = se(this, n)
            updater(unvisited, stack, this, nbr, update, modulus)
                    # check northwest neighbor
            nbr, update = nw(this, n)
            updater(unvisited, stack, this, nbr, update, modulus)

if __name__ == "__main__":
        # self-test
    LuoShu = SiameseMagicSquare(3, debug=True)
    print(LuoShu.name)
    print(LuoShu)
    LuoShu.check()

    print('*' * 72)
    copy = MagicSquare.from_sq([[6, 1, 8], [7, 5, 3], [2, 9, 4]])
    print(copy)

    print('*' * 72)
    high_five = SiameseMagicSquare(5)
    print(high_five.name)
    print(high_five)

    print('*' * 72)
    super_seven = SiameseMagicSquare(7)
    print(super_seven.name)
    print(super_seven)
    assert super_seven[(0, 0)] == 22
    assert super_seven[(1, 0)] == 5
    assert super_seven[(0, 1)] == 47
    assert super_seven[(6, 6)] == 28
    assert super_seven[(5, 6)] == 45
    assert super_seven[(6, 5)] == 3

    print('*' * 72)
    copy = super_seven.to_copy
    print("Carbon copy")
    print(copy)

    hflip = LuoShu.reflect()
        # check axis
    assert hflip[(1, 0)] == LuoShu[(1, 0)], "hflip (1,0)"
    assert hflip[(1, 1)] == LuoShu[(1, 1)], "hflip (1,1)"
    assert hflip[(1, 2)] == LuoShu[(1, 2)], "hflip (1,2)"
        # check corners
    assert hflip[(0, 0)] == LuoShu[(2, 0)], "hflip NW--SW"
    assert hflip[(2, 2)] == LuoShu[(0, 2)], "hflip SE--NE"

    vflip = LuoShu.reflect(axis="v")
        # check axis
    assert vflip[(0, 1)] == LuoShu[(0, 1)], "vflip (0,1)"
    assert vflip[(1, 1)] == LuoShu[(1, 1)], "vflip (1,1)"
    assert vflip[(2, 1)] == LuoShu[(2, 1)], "vflip (2,1)"
        # check corners
    assert vflip[(0, 0)] == LuoShu[(0, 2)], "vflip NW--NE"
    assert vflip[(2, 2)] == LuoShu[(2, 0)], "vflip SE--SW"

    dflip = LuoShu.reflect(axis="d")
        # check axis
    assert dflip[(0, 0)] == LuoShu[(0, 0)], "dflip (0,0)"
    assert dflip[(1, 1)] == LuoShu[(1, 1)], "dflip (1,1)"
    assert dflip[(2, 2)] == LuoShu[(2, 2)], "dflip (2,2)"
        # check remaining corners
    assert dflip[(2, 0)] == LuoShu[(0, 2)], "dflip SW--NE"
    assert dflip[(0, 2)] == LuoShu[(2, 0)], "dflip NE--SW"

    aflip = LuoShu.reflect(axis="a")
        # check axis
    assert aflip[(0, 2)] == LuoShu[(0, 2)], "aflip (0,2)"
    assert aflip[(1, 1)] == LuoShu[(1, 1)], "aflip (1,1)"
    assert aflip[(2, 0)] == LuoShu[(2, 0)], "aflip (2,0)"
        # check remaining corners
    assert aflip[(0, 0)] == LuoShu[(2, 2)], "aflip NW--SE"
    assert aflip[(2, 2)] == LuoShu[(0, 0)], "aflip SE--NW"

    print(LuoShu.name, "(again)")
    print(LuoShu)
    print("-- rotate 0")
    print(LuoShu.rotate(-44))
    print("-- rotate 90 degrees")
    print(LuoShu.rotate(1))
    print("-- rotate 180 degrees")
    print(LuoShu.rotate(42))
    print("-- rotate 270 degrees")
    print(LuoShu.rotate(3))
    print("-- translate h=1")
    print(LuoShu.translate(1))
    print("-- scale m=-1")
    print(LuoShu.translate(1))
    print("-- affine Y=-X+10")
    print(LuoShu.affine(-1, 10))

    print(high_five.name, "(again)")
    print(high_five)
    b = high_five.n**2+1
    print(f"-- affine Y=-X+{b}")
    print(high_five.affine(-1, b))

    print("SUCCESS!")
