""" flat file writer library """
import logging
from random import randint
from lib.utils import whitespace_generator, list_to_str
from data_files_handler import get_data_set


def flat_row_header(columns, column_lengths):
    """
    flat row header
    :param columns:
    :param column_lengths:
    :return: flat row header
    """
    header_row = []

    for i, j in zip(columns, column_lengths):
        if len(i) > j:
            logging.error('Header value for %s is longer then expected column length '
                          'set in config.json file (%s)!', i, j)
        else:
            header_row.append(str(i) + whitespace_generator(j - len(i)))
    header_row = "".join(header_row)
    return header_row


def flat_row_output(columns, column_lengths):
    """
    function for generating flat output data row
    :param columns:
    :param column_lengths:
    :return: output flat data row
    """
    columns = list_to_str(columns)
    column_lengths = list_to_str(column_lengths)
    row = []

    for index, column in enumerate(columns):
        column = column.strip("'")
        whitespace = int(column_lengths[index])
        value = get_data_set(column)[randint(0, len(get_data_set(column))-1)]
        value = value + whitespace_generator(whitespace - len(value))
        row.append(value)
    row = ''.join(row)
    return row
