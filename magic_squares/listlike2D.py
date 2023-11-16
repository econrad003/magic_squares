"""
listlike2D.py - wrapper for lists/tuples to model rectangular matrices
Copyright © 2023 by Eric Conrad

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

class listlike2D(object):
    """use two-dimensional indexing on a listlike object

    This is just a simple wrapper.  If the underlying object is
    immutable, then __setitem__ will fail.  Rudimentary boundary
    checking is performed in __getitem__ and __setitem__.
    """

    def __init__(self, obj:list, m:int, n:int):
        """constructor"""
        self.obj = obj          # e.g.: list or a tuple
        self.m = m              # number of rows
        self.n = n              # number of columns

    def __getitem__(self, index):
        """access an entry -- convert the indices"""
        i, j = index
        if i < 0 or j < 0 or i >= self.m or j >= self.n:
            raise IndexError(f'Indices {index} boundary error')
        return self.obj[i][j]

    def __setitem__(self, index, value):
        """replace an entry -- convert the indices"""
        i, j = index
        if i < 0 or j < 0 or i >= self.m or j >= self.n:
            raise IndexError(f'Indices {index} boundary error')
        self.obj[i][j] = value      # exception if obj is immutable
        return value

    def __len__(self):
        """number of rows"""
        return self.m

    @property
    def rows(self):
        """number of rows"""
        return self.m

    @property
    def columns(self):
        """number of columns"""
        return self.n

    @property
    def dim(self):
        """array dimensions"""
        return (self.m, self.n)

class Block(listlike2D):
    """a rectangular block in a matrix-like object"""

    def __init__(self, obj:listlike2D, m1:int, m2:int, n1:int, n2:int):
        """constructor"""
        self.obj = obj
        self.m1, self.m2 = m1, m2               # bounds on rows
        self.m = m2 - m1
        self.n1, self.n2 = n1, n2               # bounda on columns
        self.n = n2 - n1

    def __getitem__(self, index):
        """access an entry -- convert the indices"""
        i, j = index
        ndx2 = p, q = i + self.m1, j + self.n1
        if p < self.m1 or q < self.n1 or p >= self.m2 or q >= self.n2:
            raise IndexError(f'Indices {index}->{ndx2} boundary error')
        return self.obj[ndx2]

    def __setitem__(self, index, value):
        """replace an entry -- convert the indices"""
        i, j = index
        ndx2 = p, q = i + self.m1, j + self.n1
        if p < self.m1 or q < self.n1 or p >= self.m2 or q >= self.n2:
            raise IndexError(f'Indices {index}->{ndx2} boundary error')
        self.obj[ndx2] = value
        return value

if __name__ == "__main__":
        # self-test
    LuoShu = ((4, 9, 2), (3, 5, 7), (8, 1, 6))  # famous magic square
    LuoShu = listlike2D(LuoShu, 3, 3)           # wrapped
    assert len(LuoShu) == len(LuoShu.obj)
    assert LuoShu.rows == 3
    assert LuoShu.columns == 3
    assert LuoShu.dim == (3, 3)
    assert LuoShu[(0,2)] == 2
    assert LuoShu[(2,0)] == 8

    LuoShu = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]  # famous magic square
    LuoShu = listlike2D(LuoShu, 3, 3)           # wrapped
    assert len(LuoShu) == len(LuoShu.obj)
    assert LuoShu[(0,2)] == 2
    assert LuoShu[(2,0)] == 8

    block = Block(LuoShu, 1, 2, 1, 3)
    assert block.rows == 1
    assert block.columns == 2
    assert block.dim == (1, 2)
    assert block[(0, 0)] == 5
    assert block[(0, 1)] == 7
    block[(0, 1)] = 8
    assert LuoShu[(1, 2)] == 8

    try:
        LuoShu[(3, 1)]
        assert False, "IndexError failure 1"
    except IndexError as message:
        print("IndexError (ok!):", message)

    try:
        block[(1, 1)]
        assert False, "IndexError failure 2"
    except IndexError as message:
        print("IndexError (ok!):", message)

    print("SUCCESS!")
