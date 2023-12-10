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

MODIFICATIONS

    21 Nov 2023 - EC
        1) added attribute "_csvname" for use with the make_examples
           script.
        2) added some examples.
        3) corrected some typos.  Added an alias for Sagrada Familia.

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
Jupiter._csvname = "Jupiter"
_all.append(Jupiter)

Parshavnatha = MS.from_sq(((7, 12, 1, 14), (2, 13, 8, 11),
                          (16, 3, 10, 5), (9, 6, 15, 4)))
Parshavnatha.name = "Parshavnatha/Chautisa Yantra"
Parshavnatha.cite = "Parshvnatha temple, Khajuraho, India. c 10th c CE"
Parshavnatha.keywords = "Chautisa Yantra, 34 song, Parshavnatha temple"
Parshavnatha._csvname = "Parshavnatha"
_all.append(Parshavnatha)

Melencolia1514 = MS.from_sq(((16, 3, 2, 13), (5, 10, 11, 8),
                             (9, 6, 7, 12), (4, 15, 14, 1)))
Melencolia1514.name = "Melencolia I"
Melencolia1514.cite = "Albrecht Dürer, Melencolia I (engraving, 1514)"
Melencolia1514.keywords = "Albrecht Dürer, Melencolia I, 1514"
Melencolia1514._csvname = "Durer_Melencolia"
_all.append(Melencolia1514)

    # this one is "trivial" as the entries 10 and 14 both occur twice.
    # Note: the name has an accent over the i in Familia
SagradaFamília = MS.from_sq(((1, 14, 14, 4), (11, 7, 6, 9),
                             (8, 10, 10, 5), (13, 2, 3, 15)))
SagradaFamília.name = "Sagrada Família"
SagradaFamília.cite = "Passion façade, Sagrada Família church, " \
    + "Barcelona, Spain. (façade design 1917, construction 1954-1976)"
SagradaFamília.keywords = "trivial, 33, Sagrada Família"
SagradaFamília._csvname = "SagradaFamilia"
SagradaFamilia = SagradaFamília     # unaccented alias
_all.append(SagradaFamília)

# EXAMPLES ADDED 21 NOV 2023

    # another trivial example, but very old - it is a combinatorial
    # design related to the manufacture of perfume

Varahamihira = MS.from_sq(((2, 3, 5, 8), (5, 8, 2, 3),
                           (4, 1, 7, 6), (7, 6, 4, 1)))
Varahamihira.name = "Varahamihira"
Varahamihira.cite = "Combinatorial design for perfume manufacture " \
    + "in Brhat Samhita by Varahamihira (c 587 CE)."
Varahamihira.keywords = "trivial, pandiagonal, perfume, Varahamihira," \
    + "Brhat Samhita, combinatorial design"
Varahamihira._csvname = "Varahamihira"
_all.append(Varahamihira)

    # Four perfect magic squares can be derived from this design by
    # adding 8 to two entries in each tier. 

        #   + 0 0 +     0 + + 0     + 0 + 0     0 + 0 +
        #   + 0 0 +     0 + + 0     0 + 0 +     + 0 + 0
        #   0 + + 0     + 0 0 +     0 + 0 +     + 0 + 0
        #   0 + + 0     + 0 0 +     + 0 + 0     0 + 0 +
        
Varahamihira14 = MS.from_sq(((10, 3, 5, 16), (13, 8, 2, 11),
                             (4, 9, 15, 6), (7, 14, 12, 1)))
Varahamihira14.name = "Varahamihira (1, 4)"
Varahamihira14.cite = "< block design for perfume manufacture " \
    + "in Brhat Samhita by Varahamihira (c 587 CE)."
Varahamihira14.keywords = "perfume, Varahamihira, Brhat Samhita"
Varahamihira14._csvname = "Varahamihira_14"
_all.append(Varahamihira14)

Varahamihira23 = MS.from_sq(((2, 11, 13, 8), (5, 16, 10, 3),
                             (12, 1, 7, 14), (15, 6, 4, 9)))
Varahamihira23.name = "Varahamihira (2, 3)"
Varahamihira23.cite = "< block design for perfume manufacture " \
    + "in Brhat Samhita by Varahamihira (c 587 CE)."
Varahamihira23.keywords = "perfume, Varahamihira, Brhat Samhita"
Varahamihira23._csvname = "Varahamihira_23"
_all.append(Varahamihira23)

Varahamihira13 = MS.from_sq(((10, 3, 13, 8), (5, 16, 2, 11),
                             (4, 9, 7, 14), (15, 6, 12, 1)))
Varahamihira13.name = "Varahamihira (1, 3)"
Varahamihira13.cite = "< block design for perfume manufacture " \
    + "in Brhat Samhita by Varahamihira (c 587 CE)."
Varahamihira13.keywords = "perfume, Varahamihira, Brhat Samhita"
Varahamihira13._csvname = "Varahamihira13"
_all.append(Varahamihira13)

Varahamihira24 = MS.from_sq(((2, 11, 5, 16), (13, 8, 10, 3),
                             (12, 1, 15, 6), (7, 14, 4, 9)))
Varahamihira24.name = "Varahamihira (2, 4)"
Varahamihira24.cite = "< block design for perfume manufacture " \
    + "in Brhat Samhita by Varahamihira (c 587 CE)."
Varahamihira24.keywords = "perfume, Varahamihira, Brhat Samhita"
Varahamihira24._csvname = "Varahamihira_24"
_all.append(Varahamihira24)

    # Not perfect (i.e not 1..n*n, but used to generate some perfect
    # squares

Nagarjuniya = MS.from_sq(((30, 16, 18, 36), (10, 44, 22, 24),
                          (32, 14, 20, 34), (28, 26, 40, 6)))
Nagarjuniya.name = "Nagarjuniya"
Nagarjuniya.cite = "Nagarjuniya pandiagonal square (10th century CE)."
Nagarjuniya.keywords = "pandiagonal, imperfect, Nagarjuniya"
Nagarjuniya._csvname = "Nagarjuniya"
_all.append(Nagarjuniya)

    # compare the following design with Varahamihira's design!

Nagarjuniya_r = MS.from_sq(((7, 1, 4, 6), (2, 8, 5, 3),
                            (5, 3, 2, 8), (4, 6, 7, 1)))
Nagarjuniya_r.name = "Nagarjuniya (reduced)"
Nagarjuniya_r.cite = "Nagarjuniya reduced square (10th century CE)."
Nagarjuniya_r.keywords = "trivial, Nagarjuniya"
Nagarjuniya_r._csvname = "Nagarjuniya_r"
_all.append(Nagarjuniya_r)

    # Two perfect magic squares can be derived from this design by
    # adding 8 to two entries in each tier. 

        #   + 0 + 0     0 + 0 +
        #   + 0 + 0     0 + 0 +
        #   0 + 0 +     + 0 + 0
        #   0 + 0 +     + 0 + 0

Nagarjuniya13 = MS.from_sq(((15, 1, 12, 6), (10, 8, 13, 3),
                            (5, 11, 2, 16), (4, 14, 7, 9)))
Nagarjuniya13.name = "Nagarjuniya (1, 3)"
Nagarjuniya13.cite = "Nagarjuniya (10th century CE)."
Nagarjuniya13.keywords = "perfect, Nagarjuniya"
Nagarjuniya13._csvname = "Nagarjuniya_13"
_all.append(Nagarjuniya13)

Nagarjuniya24 = MS.from_sq(((7, 9, 4, 14), (2, 16, 5, 11),
                            (13, 3, 10, 8), (12, 6, 15, 1)))
Nagarjuniya24.name = "Nagarjuniya (2, 4)"
Nagarjuniya24.cite = "Nagarjuniya (10th century CE)."
Nagarjuniya24.keywords = "perfect, Nagarjuniya"
Nagarjuniya24._csvname = "Nagarjuniya_24"
_all.append(Nagarjuniya24)

if __name__ == "__main__":
        # self-test

    for item in _all:
        print(item.name)
        print(item.cite)
        if item.keywords:
            print("keywords:", item.keywords)
        print(item)

    print("SUCCESS!")
