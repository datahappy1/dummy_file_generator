""" general utilities library """
import os
from dummy_file_generator.settings import FILE_LINE_ENDING


def whitespace_generator(i) -> str:
    """
    whitespaces generator function
    :param i:
    :return: whitespaces string
    """
    return int(i) * ' '


def add_quotes_to_list_items(columns) -> list:
    """
    list to quoted item list function
    :param columns: list
    :return: list of strings
    """
    columns = str(columns).strip('[]').split(', ')
    return columns


def get_data_file_content_list_with_item_count(data_set_name, data_files_location) -> tuple:
    """
    load a data file from filesystem and return a tuple with the list of the file content and
    an int with the length minus 1 of the file content list
    :param data_set_name:
    :param data_files_location:
    :return: tuple
    """
    def _get_data_set_item_count(data_set) -> int:
        return len(data_set) - 1

    data_files_dir_path = os.path.join(data_files_location)
    data_set = open(os.sep.join((str(data_files_dir_path), data_set_name)))
    data_set = data_set.read().split(FILE_LINE_ENDING)
    data_set_len = _get_data_set_item_count(data_set)
    return data_set, data_set_len
