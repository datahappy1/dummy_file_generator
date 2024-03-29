"""
test units
"""
import io
import os

import pytest

from dummy_file_generator import DummyFileGeneratorException
from dummy_file_generator.__main__ import DummyFileGenerator as Dfg
from dummy_file_generator.data_files import load_data_files_content
from dummy_file_generator.rowdatagenerator import RowDataGenerator
from dummy_file_generator.writer import Writer

TEST_FILE_HANDLER_ABS_PATH = os.sep.join([os.getcwd(), 'tests', 'files', 'testfile.dummy'])
CONFIG_JSON_PATH = os.sep.join([os.getcwd(), 'tests', 'files', 'test_config.json'])
DATA_FILES_LOCATION = os.sep.join([os.getcwd(), 'tests', 'files'])
DATA_FILES_CONTENTS = load_data_files_content(DATA_FILES_LOCATION)
LOGGING_LEVEL = 'INFO'

PROJECT_SCOPE_KWARGS_CSV = {
    "project_name": 'test_csv',
    "data_files_location": DATA_FILES_LOCATION,
    "config_json_path": CONFIG_JSON_PATH,
    "default_rowcount": None,
}

DFG_OBJ_CSV = Dfg(LOGGING_LEVEL, **PROJECT_SCOPE_KWARGS_CSV)
COLUMNS_CSV = DFG_OBJ_CSV.properties.columns

PROJECT_SCOPE_KWARGS_FLAT = {
    "project_name": 'test_flatfile',
    "data_files_location": DATA_FILES_LOCATION,
    "config_json_path": CONFIG_JSON_PATH,
    "default_rowcount": None,
}

DFG_OBJ_FLAT = Dfg(LOGGING_LEVEL, **PROJECT_SCOPE_KWARGS_FLAT)
COLUMNS_FLAT = DFG_OBJ_FLAT.properties.columns

PROJECT_SCOPE_KWARGS_JSON_SIMPLE = {
    "project_name": 'test_json_simple',
    "data_files_location": DATA_FILES_LOCATION,
    "config_json_path": CONFIG_JSON_PATH,
    "default_rowcount": None,
}

DFG_OBJ_JSON_SIMPLE = Dfg(LOGGING_LEVEL, **PROJECT_SCOPE_KWARGS_JSON_SIMPLE)
COLUMNS_JSON_SIMPLE = DFG_OBJ_JSON_SIMPLE.properties.columns

PROJECT_SCOPE_KWARGS_JSON_COMPLEX = {
    "project_name": 'test_json_complex',
    "data_files_location": DATA_FILES_LOCATION,
    "config_json_path": CONFIG_JSON_PATH,
    "default_rowcount": None,
}

DFG_OBJ_JSON_COMPLEX = Dfg(LOGGING_LEVEL, **PROJECT_SCOPE_KWARGS_JSON_COMPLEX)
COLUMNS_JSON_COMPLEX = DFG_OBJ_JSON_COMPLEX.properties.columns


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


def teardown_module():
    try:
        os.remove(TEST_FILE_HANDLER_ABS_PATH)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (TEST_FILE_HANDLER_ABS_PATH, e))


class TestUnitWriter:
    @pytest.mark.parametrize("file_type", ["csv", "flat", "json"])
    def test_init_writer(self, file_type):
        with io.open(TEST_FILE_HANDLER_ABS_PATH, mode="w") as output_file_handler:
            writer = Writer(file_type=file_type,
                            file_handler=output_file_handler,
                            **{"csv_value_separator": ",",
                               "csv_quoting": "NONE",
                               "csv_quote_char": None,
                               "csv_escape_char": None,
                               "file_line_ending": "\n"}
                            )

            assert isinstance(writer, Writer)

    @pytest.mark.parametrize("file_type, test_input, expected",
                             [("csv", ["test row"], "test row\n"),
                              ("flat", "test row", "test row\n"),
                              ("json", "test row", '"test row",\n')])
    def test_write_row(self, file_type, test_input, expected):
        with io.open(TEST_FILE_HANDLER_ABS_PATH, mode="w") as write_output_file_handler:
            writer = Writer(file_type=file_type,
                            file_handler=write_output_file_handler,
                            **{"csv_value_separator": ",",
                               "csv_quoting": "NONE",
                               "csv_quote_char": None,
                               "csv_escape_char": None,
                               "file_line_ending": "\n"}
                            )

            assert writer.write_row(test_input) is None

        assert open(TEST_FILE_HANDLER_ABS_PATH).readline() == expected


class TestUnitRowGenerator:
    @pytest.mark.parametrize("file_type, columns",
                             [("csv", COLUMNS_CSV),
                              ("flat", COLUMNS_FLAT),
                              ("json", COLUMNS_JSON_SIMPLE),
                              ("json", COLUMNS_JSON_COMPLEX)])
    def test_init_generator(self, file_type, columns):
        generator = RowDataGenerator(file_type=file_type,
                                     data_files_contents=DATA_FILES_CONTENTS,
                                     columns=columns)

        assert isinstance(generator, RowDataGenerator)

    @pytest.mark.parametrize("file_type, columns, expected",
                             [("csv", COLUMNS_CSV, ['testcol_a', 'testcol_b', 'testcol_c']),
                              ("flat", COLUMNS_FLAT, "testcol_a testcol_b     testcol_c   ")])
    def test_generator_header_row(self, file_type, columns, expected):
        generator = RowDataGenerator(file_type=file_type,
                                     data_files_contents=DATA_FILES_CONTENTS,
                                     columns=columns)

        assert generator.generate_header_row() == expected

    @pytest.mark.parametrize("file_type, columns",
                             [("json", COLUMNS_JSON_SIMPLE),
                              ("json", COLUMNS_JSON_COMPLEX)])
    def test_generator_header_row_raises_error(self, file_type, columns):
        generator = RowDataGenerator(file_type=file_type,
                                     data_files_contents=DATA_FILES_CONTENTS,
                                     columns=columns)
        with pytest.raises(DummyFileGeneratorException):
            generator.generate_header_row()

    @pytest.mark.parametrize("file_type, columns, expected",
                             [("csv", COLUMNS_CSV, ['test', 'test', 'test']),
                              ("flat", COLUMNS_FLAT, "test     test         test       "),
                              ("json", COLUMNS_JSON_SIMPLE, "{'testcol_a': 'test', 'testcol_b': 'test', 'testcol_c': 'test'}"),
                              ("json", COLUMNS_JSON_COMPLEX, "{'testcol_a': 'test', 'testcol_b': 'test', 'testcol_c': 'test', "
                                                             "'arrayColumnExample_a': ['test', {'testcol_ad': 'test', 'testcol_ab': "
                                                             "'test', 'testcol_ac': 'test'}, 'test', 'test', 'test', {'testcol_ad': "
                                                             "'test', 'testcol_ae': 'test'}, 'test'], 'testcol_d': 'test', "
                                                             "'arrayColumnExample_b': [{'testcol_ba': 'test', 'testcol_bb': 'test', "
                                                             "'testcol_bc': 'test'}, 'test', 'test']}")])
    def test_generator_body_row(self, file_type, columns, expected):
        generator = RowDataGenerator(file_type=file_type,
                                     data_files_contents=DATA_FILES_CONTENTS,
                                     columns=columns)

        _actual = generator.generate_body_row()
        # replace occurrences of 1,2 or 3 as the generated values from the test.txt are randomly picked
        actual = _replace_multiple_str_occurrences_in_str(str(_actual), '123', '')

        assert actual == str(expected)
