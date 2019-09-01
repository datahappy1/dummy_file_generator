""" data files handler module """
import os


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


class DataSets:
    """
    class for data sets handling
    """
    test = load_file_to_list('test.txt')
    ids = load_file_to_list('ids.txt')
    first_names = load_file_to_list('first_names.txt')
    last_names = load_file_to_list('last_names.txt')
    dates = load_file_to_list('dates.txt')


def get_data_set(data_set_name):
    """
    function for dynamic data_set list retrieval
    :param data_set_name:
    :return: data_set
    """
    data_set = DataSets()
    return getattr(data_set, data_set_name)
