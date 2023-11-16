"""
doubly_even.py - an algorithm for constructing doubly even squares
Copyright © 2023 by Eric Conrad

    See https://en.wikipedia.org/wiki/Magic_square
        article title: Magic square
        topic: Special methods of construction

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
from magic_squares.magic_square import MagicSquare

class DoublyEven(MagicSquare):
    """a type of doubly even magic square"""

    def __init__(self, n:int, debug=False, indexer=None, pattern=None):
        """constructor"""
        if not indexer:
            indexer = lambda i, j, n: n*i + j + 1
        if not pattern:
            pattern = [[1,0,0,1], [0,1,1,0], [0,1,1,0], [1,0,0,1]]
        self.pattern = pattern
        self.indexer = indexer
        super().__init__(4*n, debug=debug)  # multiply by 4

    def configure(self):
        """creation algorithm"""
        n = self.n
        nn = n*n
        f = self.indexer
        pattern = self.pattern
        m = len(pattern)
        for i in range(n):
            for j in range(n):
                p, q = i % m, j % m
                flag = pattern[p][q]
                entry = f(i, j, n)
                if not flag:
                    entry = nn - entry + 1
                self[(i, j)] = entry

if __name__ == "__main__":
        # self-test
    result = DoublyEven(1, debug=True)
    print(result)
    result.check()

    print('*' * 72)
    result = DoublyEven(2, debug=True)
    print(result)
    result.check()

    print('*' * 72)
    result = DoublyEven(3, debug=True)
    print(result)
    result.check()

    print("SUCCESS!")
