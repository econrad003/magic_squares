"""
decorators.py - decorators and metaclasses
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
    # decorators

def combine_args(function):
    """combine the optional arguments into a single tuple

    Keyword arguments are not affected.

    Examples:
        @combine_args(f)(1, 2, 3, foo="bar")
            -> f((1, 2, 3), foo="bar")
    """
    def wrapper(*args, **kwargs):
        """the combine_args wrapper"""
        result = function(args, **kwargs)
        return result
    return wrapper

    # metaclasses

class Tier(object):
    """a row, a column or a diagonal

    The class provides the indexing dunder operators __getitem__ and
    __setitem__ and the length dunder operator __len__, so that tiers
    behave like fixed-length arrays.  Entries can the tier may be
    accessed or modified, but deletions are not permitted.

    The use of a λ-expression to preprocess indices gives this class
    a metaclass-like flavor.
    """

    def __init__(self, square_matrix, tier_type:str, tier_number:int=0):
        """constructor

        REQUIRED ARGUMENTS

            square_matrix - an nxn square matrix with indices running
                from 0 through n-1

            tier_type - a string describing type type of tier.  Values
                can be any of:
                    a) "row" - a row in the matrix;
                    b) "column" - a column in the matrix;
                    c) "diagonal" - the main diagonal; and
                    d) "antidiagonal" - the antidiagonal

        OPTIONAL ARGUMENTS

            tier_number (default 0) - identifies the tier.  Values
                by type are:
                    a) row number for "row" type;
                    b) column number for "column" type;
                    c) ignored for "diagonal" type;
                    d) 0 for "antidiagonal" type, to index from
                        top right to bottom left; and
                    e) 1 for "antidiagonal" type, to index from
                        bottom left to top right.

        EXCEPTIONS

            TypeError is raised if the tier_type is not one of the
            four given types, or when the tier_type is "antidiagonal",
            if the tier_number is not 0 or 1.
        """
        n = len(square_matrix) - 1              # last column
        self._matrix = square_matrix
        if tier_type == "row":
            self._tier = lambda j: (tier_number, j)
        elif tier_type == "column":
            self._tier = lambda i: (i, tier_number)
        elif tier_type == "diagonal":
            self._tier = lambda i: (i, i)
        elif tier_type == "antidiagonal" and tier_number == 0:
            self._tier = lambda i: (i, n-i)     # NE to SW
        elif tier_type == "antidiagonal" and tier_number == 1:
            self._tier = lambda i: (n-i, i)     # SW to NE
        else:
            raise TypeError("Unknown tier type")

    def __getitem__(self, index):
        """access an element"""
        return self._matrix[self._tier(index)]

    def __setitem__(self, index, value):
        """set an element"""
        self._matrix[self._tier(index)] = value
        return value

    def __len__(self):
        """get the order"""
        return len(self.matrix)

if __name__ == "__main__":
        # self-test
    from magic_squares.magic_square import SiameseMagicSquare

    @combine_args
    def f1(*args, **kwargs):
        """test"""
        assert len(args) == 1
        return args[0]
    assert f1() == ()
    assert f1(1,2,3,foo="bar") == (1,2,3)

    foo = SiameseMagicSquare(3)
    bar = Tier(foo, "row", 0)
    baz = tuple(bar[i] for i in range(3))
    assert baz == (4, 9, 2)
    assert len(baz) == 3
    bar = Tier(foo, "row", 1)
    baz = tuple(bar[i] for i in range(3))
    assert baz == (3, 5, 7)
    bar = Tier(foo, "row", 2)
    baz = tuple(bar[i] for i in range(3))
    assert baz == (8, 1, 6)
    bar = Tier(foo, "column", 0)
    baz = tuple(bar[i] for i in range(3))
    assert baz == (4, 3, 8)
    bar = Tier(foo, "column", 1)
    baz = tuple(bar[i] for i in range(3))
    assert len(baz) == 3
    assert baz == (9, 5, 1)
    bar = Tier(foo, "column", 2)
    baz = tuple(bar[i] for i in range(3))
    assert baz == (2, 7, 6)
    bar = Tier(foo, "diagonal")
    baz = tuple(bar[i] for i in range(3))
    assert len(baz) == 3
    assert baz == (4, 5, 6)
    bar = Tier(foo, "antidiagonal")
    baz = tuple(bar[i] for i in range(3))
    assert baz == (2, 5, 8)
    assert len(baz) == 3
    bar = Tier(foo, "antidiagonal", 1)
    baz = tuple(bar[i] for i in range(3))
    assert baz == (8, 5, 2)
    assert len(baz) == 3

    print("SUCCESS!")
