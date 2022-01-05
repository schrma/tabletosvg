import argparse
import sys
import logging

from tabletosvg import __version__

_logger = logging.getLogger(__name__)


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