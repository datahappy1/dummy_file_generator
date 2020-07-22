"""
test units
"""
import os

from dummy_file_generator.__main__ import DummyFileGenerator as Dfg
from dummy_file_generator.utils import get_data_file_content_list_with_item_count


CONFIG_JSON_PATH = os.sep.join([os.getcwd(), 'files', 'test_config.json'])
DATA_FILES_LOCATION = 'files'
LOGGING_LEVEL = 'INFO'


project_scope_kwargs = {
    "project_name": 'test_csv',
    "data_files_location": DATA_FILES_LOCATION,
    "config_json_path": CONFIG_JSON_PATH,
    "default_rowcount": None,
}

DFG_OBJ = Dfg(LOGGING_LEVEL, **project_scope_kwargs)
DFG_OBJ._set_vars_from_data_files_content(DATA_FILES_LOCATION)


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


class TestUnitClass:
    def test_unit_get_data_file_content(self):
        """
        unit test load_file_to_list
        :return: assert load_file_to_list works as expected
        """
        expected_output = ['test1', 'test2', 'test3']
        actual_output = get_data_file_content_list_with_item_count('test.txt',
                                                                   data_files_location=
                                                                   DATA_FILES_LOCATION)[0]
        assert expected_output == actual_output

    def test_unit_get_data_file_values_from_dfg_instance(self):
        """
        unit test get_data_set
        :return: assert getting a data set works as expected
        """
        expected_output = ['test1', 'test2', 'test3']
        actual_output = DFG_OBJ.__getattribute__('data_file_test')[0]

        assert expected_output == actual_output

    def test_unit_flat_writer_flat_row_header(self):
        """
        unit test flat header
        :return: assert flat header output works as expected
        """
        expected_output = 'test1 test2  test3   '
        actual_output = DFG_OBJ.flat_row_header(['test1', 'test2', 'test3'], [6, 7, 8])

        assert expected_output == actual_output

    def test_unit_csv_writer_csv_row_header(self):
        """
        unit test csv header
        :return: assert csv header output works as expected
        """
        expected_output = 'test1,test2,test3'
        actual_output = DFG_OBJ.csv_row_header('test1, test2, test3')

        assert expected_output == actual_output

    def test_unit_flat_writer_flat_row_output(self):
        """
        unit test flat row output
        :return: assert flat row output works as expected
        """
        expected_output = DFG_OBJ.flat_row_output(['test', 'test', 'test'], [6, 7, 8])
        expected_output = _replace_multiple_str_occurrences_in_str(expected_output, '123', '')
        actual_output = _replace_multiple_str_occurrences_in_str('test1 test2  test3   ', '123', '')

        assert expected_output == actual_output

    def test_unit_csv_writer_csv_row_output(self):
        """
        unit test csv row output
        :return: assert csv row output works as expected
        """
        csv_row_separator = '|'
        expected_output = DFG_OBJ.csv_row_output('test, test, test', csv_row_separator)
        expected_output = _replace_multiple_str_occurrences_in_str(expected_output, '123', '')
        actual_output = _replace_multiple_str_occurrences_in_str('test1|test2|test3', '123', '')

        assert expected_output == actual_output
