"""
test units
"""
from dummy_file_generator.utils import get_data_file_content_list_with_item_count
from tests.conftest import tests_setup_dfg_instance

DATA_FILES_LOCATION = 'files'

DFG = tests_setup_dfg_instance()
DFG._set_vars_from_data_files_content(DATA_FILES_LOCATION)


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


class Test:
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
        actual_output = DFG.__getattribute__('data_file_test')[0]

        assert expected_output == actual_output

    def test_unit_flat_writer_flat_row_header(self):
        """
        unit test flat header
        :return: assert flat header output works as expected
        """
        expected_output = 'test1 test2  test3   '
        actual_output = DFG.flat_row_header(['test1', 'test2', 'test3'], [6, 7, 8])

        assert expected_output == actual_output

    def test_unit_csv_writer_csv_row_header(self):
        """
        unit test csv header
        :return: assert csv header output works as expected
        """
        csv_row_separator = '|'
        expected_output = 'test1|test2|test3'
        actual_output = DFG.csv_row_header('test1, test2, test3', csv_row_separator)

        assert expected_output == actual_output

    def test_unit_flat_writer_flat_row_output(self):
        """
        unit test flat row output
        :return: assert flat row output works as expected
        """
        expected_output = DFG.flat_row_output(['data_file_test', 'data_file_test', 'data_file_test'], [6, 7, 8])
        expected_output = _replace_multiple_str_occurrences_in_str(expected_output, '123', '')
        actual_output = _replace_multiple_str_occurrences_in_str('test1 test2  test3   ', '123', '')

        assert expected_output == actual_output

    def test_unit_csv_writer_csv_row_output(self):
        """
        unit test csv row output
        :return: assert csv row output works as expected
        """
        csv_row_separator = '|'
        expected_output = DFG.csv_row_output('test, test, test', csv_row_separator)
        expected_output = _replace_multiple_str_occurrences_in_str(expected_output, '123', '')
        actual_output = _replace_multiple_str_occurrences_in_str('test1|test2|test3', '123', '')

        assert expected_output == actual_output
