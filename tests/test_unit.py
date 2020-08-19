"""
test units
"""
import os
import io
import pytest

from dummy_file_generator.__main__ import DummyFileGenerator as Dfg
from dummy_file_generator.writer import Writer
from dummy_file_generator.rowdatagenerator import RowDataGenerator

TEST_FILE_HANDLER_PATH = os.sep.join([os.getcwd(), 'tests', 'files', 'testfile'])
CONFIG_JSON_PATH = os.sep.join([os.getcwd(), 'tests', 'files', 'test_config.json'])
DATA_FILES_LOCATION = os.sep.join([os.getcwd(), 'tests', 'files'])

LOGGING_LEVEL = 'INFO'

PROJECT_SCOPE_KWARGS_CSV = {
    "project_name": 'test_csv',
    "data_files_location": DATA_FILES_LOCATION,
    "config_json_path": CONFIG_JSON_PATH,
    "default_rowcount": None,
}

DFG_OBJ_CSV = Dfg(LOGGING_LEVEL, **PROJECT_SCOPE_KWARGS_CSV)
COLUMNS_CSV = DFG_OBJ_CSV.columns

PROJECT_SCOPE_KWARGS_FLAT = {
    "project_name": 'test_flatfile',
    "data_files_location": DATA_FILES_LOCATION,
    "config_json_path": CONFIG_JSON_PATH,
    "default_rowcount": None,
}

DFG_OBJ_FLAT = Dfg(LOGGING_LEVEL, **PROJECT_SCOPE_KWARGS_FLAT)
COLUMNS_FLAT = DFG_OBJ_FLAT.columns

DATA_FILES_CONTENTS = DFG_OBJ_CSV.load_data_files_content(DATA_FILES_LOCATION)


def _replace_multiple_str_occurrences_in_str(string, old_value, new_value) -> str:
    """
    helper function to replace all occurrences of a string in another string
    :param string:
    :param old_value:
    :param new_value:
    :return: string with replacements
    """
    for elem in old_value:
        if elem in string:
            string = string.replace(elem, new_value)
    return string


class TestUnitWriter:
    @pytest.mark.parametrize("file_type", ["csv", "flat"])
    def test_init_writer(self, file_type):
        with io.open(TEST_FILE_HANDLER_PATH, mode="w") as output_file_handler:
            writer = Writer(file_type=file_type,
                            file_handler=output_file_handler,
                            **{"csv_value_separator": ",",
                               "csv_quoting": "NONE",
                               "csv_quote_char": "",
                               "file_line_ending": "\n"}
                            )

            assert isinstance(writer, Writer)

    @pytest.mark.parametrize("file_type, test_input, expected",
                             [("csv", ["test row"], "test row\n"),
                              ("flat", "test row", "test row\n")])
    def test_write_row(self, file_type, test_input, expected):
        with io.open(TEST_FILE_HANDLER_PATH, mode="w") as write_output_file_handler:
            writer = Writer(file_type=file_type,
                            file_handler=write_output_file_handler,
                            **{"csv_value_separator": ",",
                               "csv_quoting": "NONE",
                               "csv_quote_char": "",
                               "file_line_ending": "\n"}
                            )

            assert writer.write_row(test_input) is None

        assert open(TEST_FILE_HANDLER_PATH).readline() == expected

        os.remove(TEST_FILE_HANDLER_PATH)


class TestUnitRowGenerator:
    @pytest.mark.parametrize("file_type, columns",
                             [("csv", COLUMNS_CSV),
                              ("flat", COLUMNS_FLAT)])
    def test_init_generator(self, file_type, columns):
        generator = RowDataGenerator(file_type=file_type,
                                     data_files_contents=DATA_FILES_CONTENTS,
                                     columns=columns)

        assert isinstance(generator, RowDataGenerator)

    @pytest.mark.parametrize("file_type, columns, expected",
                             [("csv", COLUMNS_CSV, ['testcol1', 'testcol2', 'testcol3']),
                              ("flat", COLUMNS_FLAT, "testcol1  testcol2      testcol3    ")])
    def test_generator_header_row(self, file_type, columns, expected):
        generator = RowDataGenerator(file_type=file_type,
                                     data_files_contents=DATA_FILES_CONTENTS,
                                     columns=columns)

        assert generator.generate_header_row() == expected

    @pytest.mark.parametrize("file_type, columns, expected",
                             [("csv", COLUMNS_CSV, ['test', 'test', 'test']),
                              ("flat", COLUMNS_FLAT, "test     test         test       ")])
    def test_generator_body_row(self, file_type, columns, expected):
        generator = RowDataGenerator(file_type=file_type,
                                     data_files_contents=DATA_FILES_CONTENTS,
                                     columns=columns)

        _actual = generator.generate_body_row()
        actual = _replace_multiple_str_occurrences_in_str(str(_actual), '123', '')

        assert actual == str(expected)
