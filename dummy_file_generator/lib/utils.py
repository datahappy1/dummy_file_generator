""" general utilities library """
import os
from dummy_file_generator.configurables.settings import FILE_LINE_ENDING

class CustomException(Exception):
    pass

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


def read_file_return_content_and_content_list_length(data_set_name, data_files_location) -> tuple:
    """
    load a data file from filesystem and return a tuple with the list of the file content and
    an int with the length minus 1 of the file content list
    :param data_set_name:
    :param data_files_location:
    :return: tuple
    """
    data_files_dir_path = os.path.join(data_files_location)
    data_set = open(os.sep.join((str(data_files_dir_path),data_set_name)))
    data_set = data_set.read().split(FILE_LINE_ENDING)
    return data_set, len(data_set) -1


def replace_multiple(main_string, to_be_replaced, new_string) -> str:
    """
    helper function to iterate over the strings to be replaced
    :param main_string:
    :param to_be_replaced:
    :param new_string:
    :return: string with replacements
    """
    for elem in to_be_replaced:
        if elem in main_string:
            main_string = main_string.replace(elem, new_string)
    return main_string
