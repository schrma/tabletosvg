import argparse
import sys
import logging
import csv
import dataclasses

from typing import List
from dataclasses_json import dataclass_json


from tabletosvg import __version__

_logger = logging.getLogger(__name__)


@dataclass_json
@dataclasses.dataclass
class DataBaseItem:
    name: str
    type: str


def read_file(filename):
    """Read file

    Nothing special

    Args:
      filename (str): File to read

    Returns:
      str: content of file
    """
    with open(filename, "r") as file_object:
        # Append 'hello' at the end of file
        content = file_object.read()
    return content


def write_file(filename, content):
    """Write file

    Args:
      filename (string): File to write
      content (string): content which will be written to file

    Returns:
      None: nothing
    """
    with open(filename, "w") as file_object:
        file_object.write(content)

class OutputCreatorTxt:
    def __init__(self, container_name):
        self._content = ""
        self._container_name = container_name

    @property
    def content(self):
        return self._content

    def add_intro(self):
        self.append(self._container_name)

    def add_outro(self):
        self.append("")

    def append(self, text):
        self._content = self.content
        self._content = self.content + text + "\n"

    def print_content(self):
        print(self._content)

    def write(self, filename):
        write_file(filename, self._content)


def create_output(database_input: List[DataBaseItem], table_name, outputfilename=None):
    output_creator_txt = OutputCreatorTxt(table_name)
    output_creator_txt.add_intro()
    for row in database_input:
        output_creator_txt.append("-" + row.name + ": (" + row.type + ")")
    if outputfilename:
        output_creator_txt.write(outputfilename)
    else:
        output_creator_txt.print_content()


def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        database_input = []
        for each_row in reader:
            item = DataBaseItem(each_row[0], each_row[1])
            database_input.append(item)
    return database_input


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = " [%(asctime)s]%(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version="tabletosvg {ver}".format(ver=__version__),
    )
    parser.add_argument("--file", help="Input file", default="input.txt", type=str)
    return parser


def parse_command_line_args(args=None):
    parsed_args = get_parser().parse_args(args)
    return vars(parsed_args)


def main(**kwargs):
    input_file = kwargs["file"]
    setup_logging(logging.DEBUG)
    _logger.debug("Starting main functinon...")
    print(input_file)
    _logger.info("Script ends here")
    return 0


if __name__ == "__main__":
    sys.exit(main(**parse_command_line_args()))