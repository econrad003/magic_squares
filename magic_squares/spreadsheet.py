"""
spreadsheet.py - a CSV class for uploading and downloading magic squares
Copyright © 2023 by Eric Conrad

DESCRIPTION

    The consists has two methods, csv_reader and csv_writer.  The
    writer takes a magic square and writes it to a CSV file. The
    writer can also output metadata to a second CSV file.  The reader
    reads the CSV and optionally the metadata into a MagicSquare
    object.

    The methods are packaged as class methods in the SpreadsheetManager
    class. 

FORMAT

    The magic square format consists of a simple header line followed
    by the magic square in row major order.  The header consists of
    two cells.  The first cell in the header is the string "MS: without
    quotes.  The second cell is the order of the magic square.  The
    output looks something like this:

            MS, 3
            4, 9, 2
            3, 5, 7
            8, 1, 6

    The optional metadata CSV consists of a header line followed by
    some detail lines.  Each detail consists of a name and a value.
    The name is a string which must contain a syntactically valid
    Python variable name.  The value may be a string or an integer.
    The header line consists of the words "name", "value", and
    "comments".  The comments field is available for editing.  The
    metadata for the magic square CSV would look something like this:

            name, value, comments
            order, 3,
            name, Siamese (3),

MODIFICATIONS

    19 Nov 2023 EC - added a couple of checks to csv_writer.

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
import csv

from magic_squares import logger
from magic_squares.magic_square import MagicSquare

class SpreadsheetManager(object):

    FILE_IDS = {"MS", "SM"}

    @classmethod
    def csv_reader(cls, magic_sq_path:str, metadata_path:str=None,
                   **kwargs):
        """upload the csv and optional metadata into a magic square

        If metadata_path has the value True, the metadata path will
        be built using magic_sq_path.

        Keyword arguments in kwargs are passed to csv.reader.
        """
        logger.debug(f"csv_reader({magic_sq_path}, {metadata_path})")
        with open(magic_sq_path, newline="") as csvfile:
            lines = list(csv.reader(csvfile, **kwargs))
        fileID, order = cls.validate_header(lines)
        diagonals = fileID != "SM"          # SM - semimagic
        lines = cls.extract_square(order, lines)
        sq = MagicSquare.from_sq(lines, diagonals=diagonals)
        if not metadata_path:
            return sq

        if metadata_path == True:
            metadata_path = cls.auto_metadata(magic_sq_path)
        with open(metadata_path, newline="") as csvfile:
            lines = list(csv.reader(csvfile, **kwargs))
        lines.pop(0)
        for line in lines:
            name, value = line[:2]
            name = name.strip()
            value = value.strip()
            cls.process_nvp(sq, name, value)
        return sq

    @classmethod
    def csv_writer(cls, sq:MagicSquare, magic_sq_path:str,
                   metadata:list=[], **kwargs):
        """download from a magic square into a csv

        The path magic_sq_path should end in ".csv".  The default
        metadata path (replacing ".csv" with ".metadata.csv") will be
        used.  (This is more restrictive than the reader policy.)

        The metadata list is a list of name-value pairs to write to the
        metadata file.  The names should be valid python identifiers
        that do not start with underscores.
        """
        logger.debug(f"csv_writer(--sq--, {magic_sq_path})")
        metadata_path = cls.auto_metadata(magic_sq_path)
        with open(magic_sq_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            if sq.diagonals:                        # 19 Nov 2023 / add
                writer.writerow(["MS", sq.n])           # '' / indent
            else:                                       # '' / add
                writer.writerow(["SM", sq.n])           # '' / add
            for i in range(sq.n):
                line = []
                for j in range(sq.n):
                    line.append(sq[(i, j)])
                writer.writerow(line)
        directory = dir(sq)
        nvps = list()
        for item in directory:
            if item == "__class__":
                if not getattr(sq, "class_name", None):
                    continue
                value = getattr(sq.__class__, "__name__", None)
                if isinstance(value, str):
                    nvps.append(["class_name", value])
                continue
            elif item[0] == "_":
                continue
            elif item == "n":
                nvps.append(["order", sq.n])
            elif item == "magic":
                nvps.append(["*magic_number", sq.magic])
            elif isinstance(getattr(type(sq), item, None), property):
                    # added: 19 Nov 2023 -- reason, copy_to method
                    # we want to avoid properties
                continue
            elif not isinstance(getattr(sq, item), (str, int)):
                continue
            else:
                if item == "diagonals":
                    value = "magic" if sq.diagonals else "semimagic"
                    nvps.append(["*type", value])
                else:
                    nvps.append([item, getattr(sq, item)])
        nvps += metadata
        with open(metadata_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["name", "value", "comments"])
            for item in nvps:
                line = map(str, item)
                writer.writerow(line)
                
        return

    @classmethod
    def validate_header(cls,lines:list) -> (str, int):
        """checks the header and returns the order"""
        fileID, order = lines[0][:2]
        fileID = fileID.strip()
        lines.pop(0)
        if not fileID in cls.FILE_IDS:
            msg = f"{fileID} is not a recognized ID"
            logger.error(msg)
            raise ValueError("The header is not valid")
        return fileID, int(order.strip())

    @staticmethod
    def extract_square(order:int, lines:list) -> list:
        """retrieve the magic square data"""
        sq = list()
        for i in range(order):
            sqi = list()
            for j in range(order):
                entry = int(lines[i][j].strip())
                sqi.append(entry)
            sq.append(sqi)
        return sq

    @staticmethod
    def auto_metadata(from_path:str) -> str:
        """build a metadata pathname"""
        if from_path[-4:] != '.csv':
            msg = f"{from_path}: extension {from_path[-4:]}!='.csv'"
            logger.error(msg)
            raise ValueError('Cannot build a metadata path')
        return from_path[:-4] + ".metadata.csv"

    @staticmethod
    def process_nvp(sq:MagicSquare, name, value):
        """process a name-value pair"""
        if name and name[0] == "*":      # info from csv_writer
            logger.info(f'metadata info: {name} = {value}')
            return
        if not name.isidentifier():
            logger.warning(f"name='{name}' is not a valid identifier")
            return
        if name[0] == "_":
            logger.warning(f"name='{name}' is reserved")
            return
        if name == "order":
            return
        if name == "name":
            sq.name = value
            logger.info(f"'name' -> {value}")
            return
        try:
            getattr(sq, name)
            logger.warning(f"name='{name}' is already used")
        except AttributeError:
            setattr(sq, name, value)
            logger.info(f"'{name}' -> '{value}'")
        return
            

if __name__ == "__main__":
    print("To test this, use the demo script csv_demo.py.")
    print("SUCCESS!")
