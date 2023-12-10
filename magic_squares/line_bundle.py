"""
line_bundle.py - a tool for framing magic and antimagic squares
Copyright © 2023 by Eric Conrad

DESCRIPTION

    This particular type of line bundle is described in connection
    with extending antimagic squares of even order by adding a frame.
    (See reference [1].)

REFERENCES

    [1] John Cormie.  "The antimagic square project".  Web. Accessed
        25 Nov 2023.
            http://ion.uwinnipeg.ca/~vlinek/jcormie/

MODIFICATIONS

    29 Nov 2023 - EC - initial version

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
from random import random, shuffle
from fractions import Fraction

import logging
from magic_squares import logger
logger.setLevel(logging.DEBUG)

from magic_squares.magic_square import MagicSquare, SiameseMagicSquare
from magic_squares.bordering import FramedMagicSquare
from magic_squares.decorators import Tier

class _LineBundle(object):
    """bipartite graph for finding a border for a square

    The vertices in the left set are the numbers from 1 through 2n+2,
    and in the right set, their complements with respect to (n+2)²+1.
    Each vertex shares an implied edge with its complement.  The
    remaining edges are between a left set element and a right set
    element.

    The goal is to identify the four corner nodes and the nodes which
    which make up each orthogonal frame piece.  To do that, we have
    two kinds of edges which connect a vertex on the left with some
    vertex on the right, other than its complement.  These are the
    green edges and the purple edges.

    A left node is in the top row of a frame if its complement is on a
    green edge, the bottom row if it is on a green edge, the left
    column if its complement is on a purple edge, and the right column
    if it is on a purple edge.

    The four corner nodes are the four nodes which lie in both a row and
    a column.  We will construct a frame for a 4x4 magic square as an
    example.  Here n=4, so our line bundle consists of two strands:

            1   2   3   4   5   6   7   8   9   10
            36  35  34  33  32  31  30  29  28  27

    Our corner nodes of choice are 1, 6 and their complements 36, 31.
    The top and bottom left are 1 and 6, respectively, and to
    preserve the magic property, we have 31 and 36 at top right and
    bottom right.  Since 1 and 31 are the top corners, we have the
    following green edge:
                (6, 31, green)
    which moves 6 to the bottom and keeps 1 at the top.  Since 1 and
    6 are on the left, we will need to connect 36 and 31 with purple
    edges.

    Before we proceed, let us define the slope of an edge:

            (6,36,G)                        (8,27,P)
            1---36                          8---29
               G                             P
              G     Slope: 6-1=+5             P         Slope: 8-10=-2
             G                                 P
            6---31                         10---27
            
                Figure 1: Calculating slope.

    We place the nodes vertically from least left value to largest left
    value..  If the edge rises from left to right, as it does here, the
    slope is positive.  If the edged falls, the slope is negative.  The
    absolute value of the slope is just the difference between the two
    left values.

    For a magic frame, we need to satisfy the following conditions:
        1) Each row and column must sum to the magic constant;
        2) Each node must be paired with its complement in the same
           diagonal (for a corner node) or row (for a side node) or
           column (for a row node).

    These conditions are equivalent to the following conditions on the
    line bundle:
        1) Each row and column contains (n+2)/2 left nodes and (n+2)/2
           right nodes;
        2) The sum of the green slopes is zero; and
        3) The sum of the purple slopes is zero.

    A solution with 1 and 6 as corners is given by the following edge
    set:
        (3,33,green), (5,28,green), (6,36,green)
        (2,36,purple), (7,31,purple), (8,27,purple)

    This corresponds to the following frame:

            1   34  4   32  9   31      magic number 111
            35                  2
            30                  7
            29                  8
            10                  27
            6   3   33  5   28  36

    Drawing the line bundle using colored pencils will verify that
    the bundle satisfies all three conditions.  For example, the green
    edge (3,33) places 3 and and 33 on the bottom and their complements
    34 and 4 on top.  The slope is negative since (3,34) is above (4,33)
    in the bundle.  Hence the slope is -1.  In the order given, the
    green slopes are -1, -4 and +5, and sum to 0.  The purple slopes,
    respectively 1, 1 and -2 also sum to 0.

    Note that the bundle condition (1) means that this method must be
    modified for finding frames of odd degree.  The modification
    involves calculating the slope of an unpaired entry.

    Consider the entries (a, b) and (c, d) in the bundle.  Suppose we
    wish to have a on the top and c on the bottom.  Then we link these
    two entries with a green edge from c to b.  The slope is given by:
                            (b+c) - (a+d)
        m = c - a = b - d = -------------
                                  2
    If the two entries are the same, this expression makes the slope 0.
    On the other hand, suppose we have un unpaired entry (e, f) which
    we want to use to compensate for the pairing c→b.  For example,
    consider the following al-Buzjani border for a 3x3 magic square:

             4  19  21   1  20          magic constant
            24               2              5(5²+1)/2 = 5·13 = 65
            23               3
             8              18
             6   7   5  25  22

    It is easily verified that both rows and both columns individually
    sum to the magic constant and the each pair of complementary
    entries sums to 5²+1=26.  Note that 4 and 1 are on top and that
    6, 7 and 5 are on the bottom.  We can bundle 1, 4, 6 and 7 with
    the green links:
        6 → 22  leaving 4 and 20 on top     slope 6-4 = 22-20 = 2
        7 → 25  leaving 1 and 19 on top     slope 7-1 = 25-19 = 6
                                                    net slope = 8
    Adding the two slopes we have a green net slope of 8.  To balance
    the system, we need a compensating slope of -8 for the remaining
    green edge 5→21 which moves 5 to the bottom and 21 to the top.
    Our compensating slope is:
        (e - f) / 2 = (5 - 21) / 2 = -8

    One objection is that we might instead just bundle 4 and 6.  But
    that is not a problem:
        6 → 22  leaving 4 and 20 on top     slope 6-4 = 22-20 =   2
        7 → 19  moving 7 to the bottom      slope    (7-19)/2 =  -6
        5 → 21  moving 5 to the bottom      slope    (5-21)/2 =  -8
        25 → 1  moving 25 to the bottom     slope    (25-1)/2 =  12
                                                    net slope =   0

    We can thus replace a linked pair with two linked complements.  In
    this case we replaced the edge 7→25 (slope 6) with two edges
    7→19 (slope -6) and 25→1 (slope 12).  The net slope is the same in
    both cases.

    NOTE
        This class _LineBundle contains the necessary tools for
        handling even order frames only.  It does not contain the tools
        for odd order frames.  Use class LineBundle instead, or, better
        yet, class BundledMagicSquare.
    """

    def __init__(self, n:int, debug:bool=False):
        """constructor"""
        self.validate(n)
        self.n = n
        self.sigma = (n+2)**2 + 1
        self.green = {}
        self.purple = {}
        self.debug = debug
        self.initialize()           # additional initializations

    def initialize(self):
        """additional initialization"""
        pass

    def validate(self, n):
        """make sure n is valid"""
        if not isinstance(n, int):
            raise TypeError(f"n={n}: n must be an integer.")
        if n < 4 or n % 2 == 1:
            raise ValueError(f"{n}: n must be even and larger than 3.")

    def complement(self, node:int) -> int:
        """return the complement of a node"""
        return self.sigma - node

    def is_source_node(self, node:int) -> bool:
        """return True if node is a left node"""
        return isinstance(node, int) and node > 0 and node < 2*self.n+3

    def is_target_node(self, node:int) -> bool:
        """return True if n is a right node"""
        return self.is_source_node(self.complement(node))

    def is_node(self, node:int) -> bool:
        """return True if n is a node"""
        return self.is_source_node(node) or self.is_target_node(node)

    def is_top_node(self, node:int) -> bool:
        """return True if the node is in the top row"""
        opposite = self.complement(node)
        return opposite in self.green

    def is_bottom_node(self, node:int) -> bool:
        """return True if the node is in the bottom row"""
        return node in self.green

    def is_left_node(self, node:int) -> bool:
        """return True if the node is in the left column"""
        opposite = self.complement(node)
        return opposite in self.purple

    def is_right_node(self, node:int) -> bool:
        """return True if the node is in the right column"""
        return node in self.purple

    @property
    def green_degree(self):
        """return the number of green nodes"""
        return len(self.green)

    @property
    def green_sum(self):
        """return the sum of the green slopes"""
        s = 0
        t = 0
        for node in self.green:
            partner = self.complement(self.green[node])
            if self.is_source_node(node):
                s += node - partner
            else:
                t += node - partner
        assert s == t
        return s

    @property
    def purple_degree(self):
        """return the number of purple nodes"""
        return len(self.purple)

    @property
    def purple_sum(self):
        """return the sum of the green slopes"""
        s = 0
        t = 0
        for node in self.purple:
            partner = self.complement(self.purple[node])
            if self.is_source_node(node):
                s += node - partner
            else:
                t += node - partner
        assert s == t
        return s

    def link_green(self, source:int, target:int):
        """make a green edge"""
        if not self.is_source_node(source):
            raise ValueError(f"{source}: arg1 must be a source node")
        if not self.is_target_node(target):
            raise ValueError(f"{target}: arg2 must be a target node")
        if source == self.complement(target):
            raise ValueError(f"{source},{target}: slope may not be 0")

        if source in self.green:
            self.unlink_green(source)
        if target in self.green:
            self.unlink_green(target)

        if self.debug:
            msg = f"Link {source} --GREEN--> {target}"
            msg += f" ({source-self.complement(target)})"
            logger.info(msg)
        self.green[source] = target
        self.green[target] = source

    def link_purple(self, source:int, target:int):
        """make a purple edge"""
        if not self.is_source_node(source):
            raise ValueError(f"{source}: arg1 must be a source node")
        if not self.is_target_node(target):
            raise ValueError(f"{target}: arg2 must be a target node")
        if source == self.complement(target):
            raise ValueError(f"{source},{target}: slope may not be 0")

        if source in self.purple:
            self.unlink_purple(source)
        if target in self.purple:
            self.unlink_purple(target)

        if self.debug:
            msg = f"Link {source} --PURPLE--> {target}"
            msg += f" ({source-self.complement(target)})"
            logger.info(msg)
        self.purple[source] = target
        self.purple[target] = source

    def unlink_green(self, node:int):
        """remove a green edge"""
        partner = self.green[node]      # IndexError if does not exist
        if self.debug:
            logger.info(f"Unlink {node} --GREEN--> {partner}")
        if node in self.green:
            del self.green[node]
        if partner in self.green:
            del self.green[partner]

    def unlink_purple(self, node:int):
        """remove a purple edge"""
        partner = self.purple[node]     # IndexError if does not exist
        if self.debug:
            logger.info(f"Unlink {node} --PURPLE--> {partner}")
        if node in self.purple:
            del self.purple[node]
        if partner in self.purple:
            del self.purple[partner]

    @property
    def framing(self):
        """construct the frame"""
        top = []
        bottom = []
        left = []
        right = []
        corners = {0:[], 1:[], 2:[], 3:[]}
        unknown = []
        for node in range(1, 2*self.n+3):
            partner = self.complement(node)
            if self.is_top_node(node):
                if self.is_left_node(node):
                    corners[0].append(node)
                    corners[2].append(partner)
                elif self.is_right_node(node):
                    corners[1].append(node)
                    corners[3].append(partner)
                else:
                    top.append(node)
                    bottom.append(partner)
                continue
            if self.is_bottom_node(node):
                if self.is_left_node(node):
                    corners[3].append(node)
                    corners[1].append(partner)
                elif self.is_right_node(node):
                    corners[2].append(node)
                    corners[0].append(partner)
                else:
                    bottom.append(node)
                    top.append(partner)
                continue
            if self.is_left_node(node):
                left.append(node)
                right.append(partner)
                continue
            if self.is_right_node(node):
                right.append(node)
                left.append(partner)
                continue
            unknown.append(node)
        status = 0                      # tentative success
        for corner in corners:
            if len(corners[corner]) != 1:
                status += 1<<corner         # 1, 2, 4, 8
        if len(unknown):
            status += 16                # 16 == 2**4 == 1<<4
        return status, (top, right, bottom, left), corners

class LineBundle(_LineBundle):
    """includes complementary links

    This class provides a minimalistic extension to class _LineBundle
    for handling frames of odd order.  In addition, there may be
    frames of even order which are only accessible through this class
    as the _LineBundle class only allows (source, target) links where
    both the source and the complement of the target are both less than
    2n+3.  This requirement mean that the _LineBumdle class only
    produces frames for which, on each side of the frame, the number
    of nodes less than 2n+3 is equal to the number of nodes whose
    complements are less than 2n+3.  (An odd order frame breaks this
    symmetry.)  Class LineBundle provides a new class of link which
    break this symmetry.
    """

    def validate(self, n):
        """make sure n is valid"""
            # note: don't call super().validate(n)
        if not isinstance(n, int):
            raise TypeError(f"n={n}: n must be an integer.")
        if n < 1 or n == 2:
            raise ValueError(f"{n}: n must be positive but not 2.")

    @property
    def green_sum(self):
        """return the sum of the green slopes"""
        s = 0
        t = 0
        u = 0
        for node in self.green:
            target = self.green[node]
            partner = self.complement(target)
            if node == partner:
                    # complementary link
                u += Fraction(node - target, 2)
            elif self.is_source_node(node):
                s += node - partner
            else:
                t += node - partner
        assert s == t
        if u.denominator == 1:
            u = u.numerator
        return s + u

    @property
    def green_sum(self):
        """return the sum of the purple slopes"""
        s = 0
        t = 0
        u = 0
        for node in self.purple:
            target = self.purple[node]
            partner = self.complement(target)
            if node == partner:
                    # complementary link
                u += Fraction(node - target, 2)
            elif self.is_source_node(node):
                s += node - partner
            else:
                t += node - partner
        assert s == t
        if u.denominator == 1:
            u = u.numerator
        return s + u

    def clink_green(self, source:int):
        """make a complementary green edge"""
        if not self.is_node(source):
            raise ValueError(f"{source}: arg1 must be a valid node")
        target = self.complement(source)

        if source in self.green:
            self.unlink_green(source)
        if target in self.green:
            self.unlink_green(target)

        if self.debug:
            msg = f"Link {source} --GREEN--> {target} (complementary:"
            msg += f" {Fraction(source-target, 2)})"
            logger.info(msg)
        self.green[source] = target

    def clink_purple(self, source:int):
        """make a complementary purple edge"""
        if not self.is_node(source):
            raise ValueError(f"{source}: arg1 must be a valid node")
        target = self.complement(source)

        if source in self.purple:
            self.unlink_purple(source)
        if target in self.purple:
            self.unlink_purple(target)

        if self.debug:
            msg = f"Link {source} --PURPLE--> {target} (complementary:"
            msg += f" {Fraction(source-target, 2)})"
            logger.info(msg)
        self.purple[source] = target

def parse_status(status:int):
    """parse the status returned by LineBundle.framing()"""
    if status == 0:
        return                              # SUCCESS
    if error < 0 or error >= 32:
        raise ValueError("Undefined error")
    if status & 16:
        raise ValueError("Some nodes are unclassified")
    if status & 1:
        raise ValueError("Top left corner error")
    if status & 2:
        raise ValueError("Top right corner error")
    if status & 4:
        raise ValueError("Bottom right corner error")
    if status & 8:
        raise ValueError("Bottom left corner error")
    raise NotImplementedError("Something weird has happened!")

class BundledMagicSquare(FramedMagicSquare):
    """a more automated version for framing magic squares

    The test program is "separately bundled" (so to speak) as:
        bundle_demo.py
    """

    DISPATCH_TABLE = {}

    def __init__(self, picture:MagicSquare, algorithm:int=0,
                 randomize:bool=True, trace:bool=False):
        """constructor

        ARGUMENTS
            picture - the magic square to be framed.
            algorithm - an integer indicating the algorithm to be
                used.  The value is used during configuration.  If
                there is no configuration associated with the
                supplied value, then the magic check will be bypassed.
                (default: zero)
            randomize - if this is set (default), certain arbitrary
                choices will be replaced by coin flips.  If unset,
                the result is pre-determined.
            trace - if true, show the line bundle linkages as they form.
                (default: False)
        """
        if not self.DISPATCH_TABLE:
            self.initialize_algorithm_table()
        self.algorithm = algorithm
        self.randomize = randomize
        self.bundle = LineBundle(picture.n, debug=trace)
        super().__init__(picture, magic_zero=False, debug=True)

    def configure(self):
        """configuration"""
        n = self.source.n
        h = 2*n+2
                # center the picture in the frame
        for i in range(n):
            for j in range(n):
                self[(i+1, j+1)] = self.source[(i, j)] + h

                # frame
        n = self.n
        self._top = Tier(self, "row", 0)
        self._bottom = Tier(self, "row", n-1)
        self._left = Tier(self, "column", 0)
        self._right = Tier(self, "column", n-1)
        self.configure_frame()

                # build the frame
        if self.algorithm in self.DISPATCH_TABLE:
            self.DISPATCH_TABLE[self.algorithm](self)

    def my_random(self):
        """random or not..."""
        if self.randomize:
            return 1 if random() < 0.5 else 0
        return 1

    def my_shuffle(self, foo:list):
        """random or not..."""
        if self.randomize:
            shuffle(foo)

    def initialize_algorithm_table(self):
        """set up the dispatch table for bundling algorithms

        The values in the table are static methods which take a
        class instance as their only argument.  (It's a static method
        which behaves almost exactly like a class instance method.
        If it walks like a duck and talks like a duck, then ...)
        As such, they can be implemented as standalone functions.

        The indices or keys are the algorithm numbers.

        To emphasize that these are static methods, we write them
        using 'this' instead of self.
        """
        cls = self.__class__
        cls.DISPATCH_TABLE[0] = cls.default_configure

    @staticmethod
    def default_configure(this:object):
        """the default configuration method

        A special method is invoked for n=4.  Otherwise, there are three
        cases: (a) n is odd, (b) n divisible by 4 or (c) n congruent to
        2 modulo 4.  (The value n is the order of the magic square to be
        framed.)
        """
        n = this.source.n
        if n % 2 == 1 and n > 0:    # odd
            this.frame0_odd()
        elif n <= 2:                # impossible
            return
        elif n == 4:             # special
            this.frame0_4()
        elif n % 4 == 0:            # divisible by 4
            this.frame0_evenly_even()
        else:                       # 2 modulo 4
            this.frame0_oddly_even()
        this.framing()

    def frame0_4(self):
        """a frame for order 4 magic squares

        The top left corner is 1 and the bottom left corner is 6, the
        order of the resulting magic square.  There is no freedom here,
        so randomize does nothing.
        """
        bundle = self.bundle
        bundle.link_purple(2, 36)       # 2 to right, 1 to left*
        bundle.link_purple(7, 31)       # 7 to right, 6 to bottom left+
        bundle.link_green(6, 36)        # 6 to bottom+, 1 to top left*

            # the remaining links are forced
        bundle.link_green(3, 33)        # 3 to bottom, 4 to top
        bundle.link_green(5, 28)        # 5 to bottom, 9 to top
        bundle.link_purple(8, 27)       # 8 to right, 10 to left

    def frame0_oddly_even(self):
        """a frame for magic squares of oddly even order

        The top left corner is n+1 and the bottom left corner is n+2.
        There is some freedom of choice here.
        """
        n = self.source.n
        bundle = self.bundle
            # set up the corners
        bundle.link_green(n+2, bundle.complement(n+1))
        bundle.link_purple(n+3, bundle.complement(n+1))
        bundle.link_purple(n+4, bundle.complement(n+2))

            # we have some free play with green links
        foo = list(range(1, n, 2))
        self.my_shuffle(foo)
        ascents, descents = foo[:n//4], foo[n//4:]
        for node in ascents:
            bundle.link_green(node+1, bundle.complement(node))
        for node in descents:
            bundle.link_green(node, bundle.complement(node+1))

            # not as much for purple links
        bundle.link_purple(n+5, bundle.complement(n+7))
        bundle.link_purple(n+6, bundle.complement(n+8))
        foo = list(range(n+9, 2*n+2, 2))
        self.my_shuffle(foo)
        ascents, descents = foo[:(n-6)//4], foo[(n-6)//4:]
        for node in ascents:
            bundle.link_purple(node+1, bundle.complement(node))
        for node in descents:
            bundle.link_purple(node, bundle.complement(node+1))

    def frame0_evenly_even(self):
        """a frame for magic squares of evenly even order n>4

        The top left corner is n+1 and the bottom left corner is n+2.
        There is some freedom of choice here.
        """
        n = self.source.n
        bundle = self.bundle
            # set up the corners
            # the horizontals include 1, 2, ..., n-1, n+3
            # the verticals include n, n+4, n+5, ... 2n+2
        bundle.link_green(n+2, bundle.complement(n+1))
        bundle.link_purple(n, bundle.complement(n+1))
        bundle.link_purple(n+4, bundle.complement(n+2))

            # first green-only link has slope -4
        bundle.link_green(n-1, bundle.complement(n+3))          # (*)
        foo = list(range(1, n-2, 2))
        self.my_shuffle(foo)
            # three green links are needed to compensate for (*)
        ascents, rest = foo[:3], foo[3:]
        for node in ascents:
            bundle.link_green(node+1, bundle.complement(node))
            # the rest divide nicely (note: len(rest)==0 when n=8)
        ascents, descents = rest[:len(rest)//2], rest[len(rest)//2:]
        for node in ascents:
            bundle.link_green(node+1, bundle.complement(node))
        for node in descents:
            bundle.link_green(node, bundle.complement(node+1))

            # more freedom for purple links
        foo = list(range(n+5, 2*n+2, 2))
        self.my_shuffle(foo)
        descents, ascents = foo[:n//4], foo[n//4:]  # 1 extra descent
        for node in ascents:
            bundle.link_purple(node+1, bundle.complement(node))
        for node in descents:
            bundle.link_purple(node, bundle.complement(node+1))

    def frame0_odd(self):
        """unrandomized, this is al-Buzjani's method

        Top left and bottom left are n+1 and n+3, respectively.
        Node n goes to middle right and node n+2 goes to middle
        bottom.

        The remaining even nodes and odd nodes are, by default,
        respectively horizontal and vertical.  Apart from the choice
        of direction, there is no free play here.  The randomize
        option gives just two permutations.
        """
        n = self.source.n
        bundle = self.bundle
                # set up the middle items n through n+3
            # n+2 moves to the bottom while n moves to the right
        bundle.clink_green(n+2)
        bundle.clink_purple(n)
            # top left is n+1, bottom left is n+3
        bundle.link_green(n+3, bundle.complement(n+1))      # n+3 bottom
        bundle.clink_purple(bundle.complement(n+1))         # n+1 left
        bundle.clink_purple(bundle.complement(n+3))         # n+3 left

        links = (n - 1) // 2
        node = 1
        if self.my_random():        # heads -- the default
                # low evens to right, high odds to bottom
            for _ in range(links):
                bundle.link_green(node+n+3, bundle.complement(node))
                node += 1
                bundle.link_purple(node, bundle.complement(node+n+3))
                node += 1
        else:
                # low odds to right, high evens to bottom
            for _ in range(links):
                bundle.link_purple(node, bundle.complement(node+n+3))
                node += 1
                bundle.link_green(node+n+3, bundle.complement(node))
                node += 1

    def framing(self):
        """build the frame"""
        bundle = self.bundle
        if self.bundle.debug:
            msg = f"Sums: green={bundle.green_sum}, " \
                + f"purple={bundle.purple_sum}"
            logger.info(msg)
            msg = f"Degrees: green={bundle.green_degree}, " \
                + f"purple={bundle.purple_degree}"
            logger.info(msg)

        status, frame, corners = bundle.framing
        try:
            parse_status(status)
        except ValueError as msg:
            print("Framing failure:", str(msg))
            return status

        top, right, bottom, left = frame
        top = corners[0] + top + corners[1]
        right = corners[1] + right + corners[2]
        bottom = corners[3] + bottom + corners[2]
        left = corners[0] + left + corners[3]
        for i in range(self.n):
            self._top[i] = top[i]
            self._right[i] = right[i]
            self._bottom[i] = bottom[i]
            self._left[i] = left[i]
        self.debug = False          # ready for check
        return status

if __name__ == "__main__":
        # self-test

    from magic_squares.order4 import Melencolia1514

            # attempt to frame an order 3 magic square
    logger.info("Attempting order 3 frame")
    square = BundledMagicSquare(SiameseMagicSquare(3), trace=True)
    print(square)
    square.check()

            # attempt to frame an order 5 magic square
    logger.info("Attempting order 5 frame")
    assert square.n == 5
    square = BundledMagicSquare(square, trace=True)
    print(square)
    square.check()

            # attempt to frame an order 7 magic square
    logger.info("Attempting order 7 frame")
    assert square.n == 7
    square = BundledMagicSquare(square, trace=True)
    print(square)
    square.check()

            # attempt to frame an order 9 magic square
    logger.info("Attempting order 9 frame")
    assert square.n == 9
    square = BundledMagicSquare(square, trace=True)
    print(square)
    square.check()
    assert square.n == 11

            # attempt to frame an order 4 magic square
    print("-"*72)
    logger.info("Attempting order 4 frame")
    square = BundledMagicSquare(Melencolia1514, trace=True)
    print(square)
    square.check()

            # attempt to frame an oddly even magic square
    print("-"*72)
    assert square.n == 6
    logger.info("Attempting order 6 frame")
    square = BundledMagicSquare(square, trace=True)
    print(square)
    square.check()

            # attempt to frame an evenly even magic square
    print("-"*72)
    assert square.n == 8
    logger.info("Attempting order 8 frame")
    square = BundledMagicSquare(square, trace=True)
    print(square)
    square.check()

            # attempt to frame another oddly even magic square
    print("-"*72)
    assert square.n == 10
    logger.info("Attempting order 10 frame")
    square = BundledMagicSquare(square, trace=True)
    print(square)
    square.check()

            # attempt to frame another evenly even magic square
    print("-"*72)
    assert square.n == 12
    logger.info("Attempting order 12 frame")
    square = BundledMagicSquare(square, trace=True)
    print(square)
    square.check()

    print("-"*72)
    assert square.n == 14
    print("SUCCESS!")
