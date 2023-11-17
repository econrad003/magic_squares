# magic_squares
algorithms and tools for creating and playing with magic squares

## 1 DESCRIPTION

The algorithms and other tools are implemented as a Python package named "magic squares".  The package contains an initialization file *\_\_init\_\_.py* which sets up a logger which I occasionally use for warning and informational messages.  There is also a main module *\_\_main\_\_.py* which, at the moment, just prints its docstring.

To use the package:

1) Download the *magic_squares* folder as an archive (*e.g* zip, tar, gzipped tar).
2) Unpack the archive into the working directory or somewhere where it can be accessed through your Python path.
3) Check -- you should see a folder called *magic_squares* and inside that folder you should see some Python scripts, including *\_\_init\_\_.py*, *magic_square.py*, *bordering.py*, *etc.*
4) Test -- in a console shell, from your working directory, run the script *magic_square.py*:
  ```
  python3 -m magic_squares.magic_square
  ```
5) (Unless you have Python 2, you can use the command ``python`` instead of ``python3``.  But don't forget the ``-m`` flag, and since this is a module, the syntax is ``[package].[module]`` with a period separating the package name from the module name!) You should see some odd order magic squares displayed in your console.
6) Have fun.

## 2 Modules

(Apart from the first three, the modules are listed in alphabetic order.  The first *magic_square.py* provides the base clas and is used throughout the package.  The second and third are support packages to simplify some of the coding.)

### 2.1 Base and support modules

*magic_square.py* (base class and a standard example class)

* Implements the base class *MagicSquare* and some basic transformations such as translation, scaling, reflection and rotations.  The class also provides methods for inputting magic squares from lists and tuples.
* Also provided is a class *SiameseMagicSquare* (the name is traditional and not historically accurate) which produces a basic sequence of magic squares of odd order.

*decorators.py* (decorators and related support tools)

* Where I plan to put any decorators that I write for use in the package.

*listlike2D.py* (a support class)

* Implements a class *listlike2D* which is basically a tool for manipulating two-dimensional lists like square matrices.  It's mainly used to simplify input processing.

### 2.2 Implementation modules

*al_Buzjani.py*

* Implements a class *alBuzjaniBorder* which uses a particular framing algorithm to embed a magic in a larger magic square.

*bordering.py*

* Implements a class *FramedMagicSquare* used as a base for bordering algorithms.

*doubly_even.py*

* Implements a class *DoublyEven* which builds a sequence of magic squares of order divisible by 4. ("doubly even" and "evenly even" are synonyms for "divisible by 4".

*Euler.py*

* Implements a class *GraecoLatinMagic* which takes produces a magic square using an algorithm that Leonhard Euler liked.  The only difficulty is finding the Latin squares to make it work.

*Moschopoulos.py*

* Implements four algorithms for creating magic squares (two for odd order squares -- one is equivalent to the "Siamese" algorithm; and two algorithms for creating evenly even squares.  These are from a treatise by Manuel Moschopoulos from about 1315.
* Class *MoschopoulosOdd* - the method of "twos and threes" for odd order squares -- essentially the Siamese algorithm with a checkers flavour.  The square is basically constructed by moving diagonally 1 space, like a piece on a checkerboard.
* Class *Moschopoulos3s5s* - the method of "threes and fives", also for odd order squares -- this is not equivalent to the Siamese algorithm.  Instead of checker moves, the construction used knight's moves from chess.
* Class *MoschopoulosEvenlyEven* - a method for creating magic squares of evenly even order (yes, divisible by 4) using a simple pattern and some interchanges.
* Class *MoschopoulosArchetype* - another method for creating magic squares of evenly even order using an archetype 4x4 magic square as a seed.
* Bonus class *PQLeaperSquare* - a generalization of the two odd order methods which uses a piece called a leaper from "fairy chess".  The checker move is a special case called a (1,1)-leaper.  The knight is another special case -- a (2,1)-leaper.  You can try other leapers with various initial conditions -- sometimes they work and sometimes they don't.  They do seem to work much of the time.  File *leapers.txt" shows a few successes and some failures as well.  (The failures that I encountered were all semi-magic squares.)

*Narayama.py*

* Similar to Euler's algorithm using Latin squares, but for even order, the conditions are weaker.  (Weaker conditions are a good thing -- it means you can do a bit more starting with a bit less!)

*order4.py*

* a small menagerie of order 4 magic squares.
