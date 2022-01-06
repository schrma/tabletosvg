import os
import pytest
import shlex

from tabletosvg.main import read_csv, create_output, read_file


@pytest.fixture(name="default_data_from_csv")
def path_to_general_fixture(test_folder):
    file_csv = os.path.join(test_folder.input, "default_data.csv")
    return read_csv(file_csv)


def test___read_csv___no_error_raised(
        default_data_from_csv
):
    test = default_data_from_csv

def test___create_output___with_default_file___no_error_raised(
        test_folder,
        default_data_from_csv
):
    reference_filenmae = os.path.join(test_folder.input, "result_default_data.txt")
    outputfilename = os.path.join(test_folder.output, "output_default_data.txt")
    create_output(default_data_from_csv, "input", outputfilename=outputfilename)

    output_content = read_file(outputfilename)
    result_content = read_file(reference_filenmae)

    assert output_content == result_content




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
