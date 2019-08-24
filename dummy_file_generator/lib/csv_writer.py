""" csv writer library """
from random import randint
from dummy_file_generator.lib.utils import list_to_str
from dummy_file_generator.data_files_handler import get_data_set


def csv_row_header(columns, csv_value_separator):
    """
    csv row header
    :param columns:
    :param csv_value_separator:
    :return: csv row header
    """
    columns = list_to_str(columns)
    header_row = []

    for column in columns:
        column = column.strip("'")
        header_row.append(column)
    header_row = csv_value_separator.join(header_row) + csv_value_separator
    return header_row


def csv_row_output(columns, csv_value_separator):
    """
    function for generating csv output data row
    :param columns:
    :param csv_value_separator:
    :return: output csv data row
    """
    columns = list_to_str(columns)
    row = []

    for column in columns:
        column = column.strip("'")
        value = get_data_set(column)[randint(0, len(get_data_set(column))-1)]
        row.append(value)
    row = csv_value_separator.join(row)
    return row
