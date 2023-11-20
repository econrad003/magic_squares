"""
leaper_demo.py - create a magic squares using leaper moves
Copyright © 2023 by Eric Conrad

USAGE

    python leaper_demo.py [-h] [-o OUTPUT] [-s y x] n p q
    create a magic squares using leaper moves

    POSITIONAL ARGUMENTS
        n                     magic square order (odd)
        p                     leaper parameter p
        q                     leaper parameter q

    OPTIONS
        -h, --help            show this help message and exit
        -o OUTPUT, --output OUTPUT
                output csvfile path (default: console)
        -s y x, --start y x   
            start position for the leaper (default: t m).
            Row number y:
                an integer or "t", "m", "b" for top, middle, bottom,
                or "[t/m/b][+/-][integer]" for a relative row.
            Column number x
                an integer or "l", "m", "r" for left middle right, or 
                "[t/m/b][+/-][integer]" for a relative column.
            These values are reduced modulo n, so (for example) "t-2"
            and "b-1" are the same row."

        (p,q) = fairy chess leaper move (a knight is a (2,1) leaper).
        Necessary, but not sufficientn are that n>p>q and these three
        values must be relatively prime.

        Suggestion: try n=7, p=3, q=1. Then experiment.

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
from math import gcd
from magic_squares import logger

from magic_squares.Moschopoulos import PQLeaperSquare
from magic_squares.spreadsheet import SpreadsheetManager as SM

def validate_parameters(n:int, p:int, q:int, start:tuple) -> tuple:
    """check the numerical inputs"""
    for item in (n, p, q):
        if not isinstance(item, int):
            msg = f"(n, p, q)={(n,p,q)}: Integers required"
            raise TypeError(msg)
    if n <= p or p <= q or q<=0:
        msg = f"(n, p, q)={(n,p,q)}: Require n>p>q>0."
        raise ValueError(msg)
    if max(gcd(n, p), gcd(p, q), gcd(n,q)) != 1:
        msg = f"(n, p, q)={(n,p,q)}: Require pairwise relatively prime"
        raise ValueError(msg)

    y, x = start
    to_int = lambda s: int(s) if len(s) else 0
    if not isinstance(y, int):
        if isinstance(y, str):
            f = {"t":0, "m":n//2, "b":n-1}
            y = f[y[0]] + to_int(y[1:]) if y[0] in f else int(y)
        else:
            raise TypeError(f"y=row={y}: String or int required")

    if not isinstance(x, int):
        if isinstance(x, str):
            f = {"l":0, "m":n//2, "r":n-1}
            x = f[x[0]] + to_int(x[1:]) if x[0] in f else int(x)
        else:
            raise TypeError(f"x=column={x}: String or int required")

    return y, x

def demo(n:int, p:int, q:int, start:tuple, output:str=None):
    """leaper magic square simulation"""
    start = validate_parameters(n, p, q, start)
    logger.info(f'demo: PQLeaper({n},{p},{q},{start})')
    foo = PQLeaperSquare(n, p, q, start, debug=True)    # defer check
    try:
        foo.check()             # run the check
    except Warning as msg:
        msg = str(msg)
        logger.warning(f'({p,q} leaper/order={n} @{start}: ' + msg)
        foo.diagonals = False   # try semimagic
    foo.check()             # run the check for real

    if output:
        SM.csv_writer(foo, output)
    else:
        print(foo)

def main(argv):
    """main routine"""
    import argparse

    DESC = "create a magic squares using leaper moves"
    EPILOG = "(p,q) = fairy chess leaper move (a knight is a " \
        + "(2,1) leaper).  Necessary: n>p>q and these three values " \
        + "must be relatively prime.  This is necessary but not " \
        + "sufficient.  Suggestion: try n=7, p=3, q=1.  Then " \
        + "experiment."
        
    parser = argparse.ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument("-o", "--output", type=str, default=None, \
        help="output csvfile path (default: console)")
    parser.add_argument("-s", "--start", type=str, nargs=2, \
        default=("t","m"), metavar=("y", "x"), \
        help="start position for the leaper (default: t m). " \
        + 'Row number y -- an integer or "t", "m", "b" for top, ' \
        + 'middle, bottom, or "[t/m/b][+/-][integer]" for  a ' \
        + 'relative row. Column number x -- an integer or ' \
        + '"l", "m", "r" for left middle right, or  ' \
        + '"[t/m/b][+/-][integer]" for a relative column.  These ' \
        + 'values are reduced modulo n, so (for example) "t-2" and ' \
        + '"b-1" are the same row."')
    parser.add_argument("n", type=int, help="magic square order (odd)")
    parser.add_argument("p", type=int, help="leaper parameter p")
    parser.add_argument("q", type=int, help="leaper parameter q")

    args = parser.parse_args(argv)
    demo(args.n, args.p, args.q, args.start, args.output)

if __name__ == "__main__":
    import sys
    import logging
    logger.setLevel(logging.DEBUG)
    main(sys.argv[1:])

