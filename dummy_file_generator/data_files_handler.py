""" data files handler module """
import os
from os import listdir
from os.path import isfile, join


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


data_files = [f for f in listdir("C:\dummy_file_generator\dummy_file_generator\data_files")
              if isfile(join("C:\dummy_file_generator\dummy_file_generator\data_files", f)) and
              str(f).endswith('.txt')]

class DataSets():
    """
    class for data sets handling
    """
    pass

def get_data_set(data_set_name):
    """
    function for dynamic data_set list retrieval
    :param data_set_name:
    :return: data_set
    """
    data_set = DataSets()

    for data_file in data_files:
        setattr(data_set, data_file.replace('.txt', ''), load_file_to_list(data_file))

    return getattr(data_set, data_set_name)