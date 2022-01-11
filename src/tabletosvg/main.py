import os
import argparse
import sys
from typing import List
import logging
import csv
import dataclasses
import pyperclip

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
    with open(filename, "r", encoding='UTF-8') as file_object:
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
    with open(filename, "w", encoding='UTF-8') as file_object:
        file_object.write(content)


def split_path(fullfilename):
    path = os.path.dirname(fullfilename)
    filename_with_extension = os.path.basename(fullfilename)
    base_filename, extension = os.path.splitext(filename_with_extension)
    return path, base_filename, extension


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


def copy_to_clip(text):
    pyperclip.copy(text)


def create_output(database_input: List[DataBaseItem], table_name, outputfilename=None):
    if not database_input:
        return
    _logger.debug("Table name: %s", table_name)
    output_creator_txt = OutputCreatorTxt(table_name)
    output_creator_txt.add_intro()
    for row in database_input:
        output_creator_txt.append("-" + row.name + ": (" + row.type + ")")
    if outputfilename:
        output_creator_txt.write(outputfilename)
    else:
        output_creator_txt.print_content()
    copy_to_clip(output_creator_txt.content)


def read_csv(filename):
    database_input = None
    try:
        file_handler = open(filename, 'r', encoding='UTF-8')
        with file_handler:
            reader = csv.reader(file_handler, delimiter=";")
            database_input = []
            for each_row in reader:
                item = DataBaseItem(each_row[0], each_row[1])
                database_input.append(item)
    except FileNotFoundError as fnf_error:
        _logger.error(fnf_error)
    return database_input


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = " [%(asctime)s]%(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel.upper(), stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='input_file', help="CSV-File from database", type=str)
    parser.add_argument("-out", "--output_file", help="File to save result", default="output.txt", type=str)
    parser.add_argument(
        '-log',
        '--loglevel',
        default='info',
        help='Provide logging level. Example --log debug, default=info'
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"tabletosvg {__version__}",
    )
    return parser


def parse_command_line_args(args=None):
    parsed_args = get_parser().parse_args(args)
    return vars(parsed_args)


def main(**kwargs):
    full_input_file = kwargs["input_file"]
    outputfilename = kwargs["output_file"]
    setup_logging(kwargs["loglevel"])
    _logger.debug("Starting main function...")
    _logger.info("Input file: %s", full_input_file)
    _logger.info("Output file: %s", outputfilename)
    data_from_csv = read_csv(full_input_file)
    _, table_name, _ = split_path(full_input_file)
    create_output(data_from_csv, table_name, outputfilename=None)
    _logger.debug("Ending ...")
    return 0


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    return main(**parse_command_line_args())


if __name__ == "__main__":
    sys.exit(run())
