import os
import pytest
import shlex

import tabletosvg.main


@pytest.mark.parametrize("filename", (
    "file.txt",
    "output.txt",
))
def test___main___golden_run___no_error_raised(
    filename
):
    # output_filename = os.path.join(test_folder.output, "kingfisher-halfdome", f"halfdome-{resolution}-{depth}.jpg")
    command_line = \
        f" --file {filename}"

    command_line_args = tabletosvg.main.parse_command_line_args(shlex.split(
        command_line,
        posix=os.name == "posix"
    ))
    exitcode = tabletosvg.main.main(**command_line_args)

    assert exitcode == 0
