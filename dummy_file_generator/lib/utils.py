""" general utilities library """
import os
from dummy_file_generator.configurables.settings import FILE_LINE_ENDING

def whitespace_generator(i) -> str:
    """
    whitespaces generator function
    :param i:
    :return: whitespaces string
    """
    return int(i) * ' '


def list_to_str(columns) -> list:
    #TODO rename,not list to str as it returns list
    """
    list to str function
    :param columns: list
    :return: string
    """
    columns = str(columns).strip('[]').split(', ')
    return columns


def load_file_to_list(data_set_name, data_files_location) -> list:
    """
    load a data file from disk and return as a list
    :param data_set_name:
    :param data_files_location:
    :return: list
    """
    data_files_dir_path = os.path.join(data_files_location)
    data_set = open(os.sep.join((str(data_files_dir_path),data_set_name)))
    data_set = data_set.read().split(FILE_LINE_ENDING)
    return data_set


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
