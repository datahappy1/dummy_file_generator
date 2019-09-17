"""
test units
"""
from dummy_file_generator.lib.utils import replace_multiple, load_file_to_list
from dummy_file_generator import * #flat_row_header, flat_row_output, csv_row_header, csv_row_output


def test_unit_data_files_handler_load_file_to_list():
    """
    unit test load_file_to_list
    :return: assert load_file_to_list works as expected
    """
    output = load_file_to_list('test.txt')
    assert output == ['test1', 'test2', 'test3']


def test_unit_data_files_handler_get_data_set():
    """
    unit test get_data_set
    :return: assert get_data_set works as expected
    """
    output = get_data_set('test')
    assert output == ['test1', 'test2', 'test3']


def test_unit_flat_writer_flat_row_header():
    """
    unit test flat header
    :return: assert flat header output works as expected
    """
    output = flat_row_header(['test1', 'test2', 'test3'], [6, 7, 8])
    assert output == 'test1 test2  test3   '


def test_unit_csv_writer_csv_row_header():
    """
    unit test csv header
    :return: assert csv header output works as expected
    """
    csv_row_separator = '|'
    output = csv_row_header('test1, test2, test3', csv_row_separator)
    assert output == 'test1|test2|test3|'


def test_unit_flat_writer_flat_row_output():
    """
    unit test flat row output
    :return: assert flat row output works as expected
    """
    l_output = flat_row_output(['test', 'test', 'test'], [6, 7, 8])
    l_output = replace_multiple(l_output, '123', '')

    r_output = replace_multiple('test1 test2  test3   ', '123', '')

    assert l_output == r_output


def test_unit_csv_writer_csv_row_output():
    """
    unit test csv row output
    :return: assert csv row output works as expected
    """
    csv_row_separator = '|'
    l_output = csv_row_output('test, test, test', csv_row_separator)
    l_output = replace_multiple(l_output, '123', '')

    r_output = replace_multiple('test1|test2|test3', '123', '')

    assert l_output == r_output
