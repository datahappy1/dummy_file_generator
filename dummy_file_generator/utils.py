""" general utilities library """
import os


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
    data_files_dir_path = os.path.join(data_files_location)
    data_set_file_stream = open(os.sep.join((str(data_files_dir_path), data_set_name)))
    data_set = data_set_file_stream.read().split('\n')
    return data_set, len(data_set)
