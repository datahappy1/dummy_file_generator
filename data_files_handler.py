""" data files handler module """
import os
import logging
from random import randint


def whitespace_generator(i):
    """
    whitespaces generator function
    :param i:
    :return: whitespaces string
    """
    return int(i) * ' '


def load_file_to_list(data_set_name):
    """
    load a data file from disk and return as list
    :param data_set_name:
    :return: list
    """
    data_files_dir_path = os.path.join(os.path.dirname(__file__), 'data_files')
    data_set = open(str(data_files_dir_path) + os.sep + data_set_name)
    return data_set.read().split("\n")


class DataSets:
    """
    class for data sets handling
    """
    IDs = load_file_to_list('IDs.txt')
    firstnames = load_file_to_list('firstnames.txt')
    lastnames = load_file_to_list('lastnames.txt')
    dates = load_file_to_list('dates.txt')


def get_data_set(data_set_name):
    """
    function for dynamic data_set list retrieval
    :param data_set_name:
    :return: data_set
    """
    data_set = DataSets()
    return getattr(data_set, data_set_name)


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
    columns = str(columns).strip('[]')
    columns = columns.split(', ')
    column_lengths = str(column_lengths).strip('[]')
    whitespaces = column_lengths.split(', ')
    row = []

    for index, column in enumerate(columns):
        column = column.strip("'")
        whitespace = int(whitespaces[index])
        value = get_data_set(column)[randint(0, len(get_data_set(column))-1)]
        value = value + whitespace_generator(whitespace - len(value))
        row.append(value)
    row = ''.join(row)
    return row


def csv_row_header(columns, csv_value_separator):
    """
    csv row header
    :param columns:
    :param csv_value_separator:
    :return: csv row header
    """
    header_row = []

    columns = str(columns).strip('[]')
    columns = columns.split(', ')

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
    columns = str(columns).strip('[]')
    columns = columns.split(', ')
    row = []

    for column in columns:
        column = column.strip("'")
        value = get_data_set(column)[randint(0, len(get_data_set(column))-1)]
        row.append(value)
    row = csv_value_separator.join(row) + csv_value_separator
    return row
