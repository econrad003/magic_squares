"""
order4.py - some magic squares of order4
Copyright © 2023 by Eric Conrad

DESCRIPTION

    This is just a collection of some 4x4 magic squares of
    historical importance.  Unless otherwise noted, these
    may be found in the Wikipedia article on Magic squares.

REFERENCES

    [1] "Magic squares" in Wikipedia.  Web.  Accessed 11 November 2023.
        URL: https://en.wikipedia.org/w/index.php?title=Magic_square

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
from magic_squares.magic_square import MagicSquare as MS

_all = list()

    # Jupiter from Krakow MS of the Picatrix
    #   Picatrix = Ghāyat al-Ḥakīm, (Arabic, c 11th c CE)
Jupiter = MS.from_sq(((4, 14, 15, 1), (9, 7, 6, 12),
                      (5, 11, 10, 8), (16, 2, 3, 13)))
Jupiter.name = "Jupiter"
Jupiter.cite = "Picatrix/Ghāyat al-Ḥakīm c 11th c CE (Krakow MS)"
Jupiter.keywords = "Jupiter, Picatrix"
_all.append(Jupiter)

Parshavnatha = MS.from_sq(((7, 12, 1, 14), (2, 13, 8, 11),
                          (16, 3, 10, 5), (9, 6, 15, 4)))
Parshavnatha.name = "Parshvanatha/Chautisa Yantra"
Parshavnatha.cite = "Parshvanatha temple, Khajuraho, India. c 10th c CE"
Parshavnatha.keywords = "Chautisa Yantra, 34 song, Parshvanatha temple"
_all.append(Parshavnatha)

Melencolia1514 = MS.from_sq(((16, 3, 2, 13), (5, 10, 11, 8),
                             (9, 6, 7, 12), (4, 15, 14, 1)))
Melencolia1514.name = "Melencolia I"
Melencolia1514.cite = "Albrecht Dürer, Melencolia I (engraving, 1514)"
Melencolia1514.keywords = "Albrecht Dürer, Melencolia I, 1514"
_all.append(Melencolia1514)

    # this one is "trivial" as the entries 10 and 14 both occur twice.
SagradaFamília = MS.from_sq(((1, 14, 14, 4), (11, 7, 6, 9),
                             (8, 10, 10, 5), (13, 2, 3, 15)))
SagradaFamília.name = "Sagrada Família"
SagradaFamília.cite = "Passion façade, Sagrada Família church, " \
    "Barcelona, Spain. (façade design 1917, construction 1954-1976)"
SagradaFamília.keywords = "trivial, 33, Sagrada Família"
_all.append(SagradaFamília)

if __name__ == "__main__":
        # self-test

    for item in _all:
        print(item.name)
        print(item.cite)
        if item.keywords:
            print("keywords:", item.keywords)
        print(item)

    print("SUCCESS!")
