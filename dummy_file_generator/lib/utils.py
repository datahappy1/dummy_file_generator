""" general utilities library """
import os

def whitespace_generator(i):
    """
    whitespaces generator function
    :param i:
    :return: whitespaces string
    """
    return int(i) * ' '


def list_to_str(columns):
    """
    list to str function
    :param columns: list
    :return: string
    """
    columns = str(columns).strip('[]').split(', ')
    return columns


def load_file_to_list(data_set_name, data_files_path=None):
    """
    load a data file from disk and return as list
    :param data_set_name:
    :param data_files_path:
    :return: list
    """
    if data_files_path:
        data_files_dir_path = os.path.join(data_files_path)
    else:
        data_file_path = os.path.dirname(__file__)
        data_files_dir_path = os.path.join(data_file_path, 'data_files')

    data_set = open(str(data_files_dir_path) + os.sep + data_set_name)
    return data_set.read().split("\n")


def replace_multiple(main_string, to_be_replaced, new_string):
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
