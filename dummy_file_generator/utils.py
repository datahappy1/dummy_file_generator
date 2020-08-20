""" general utilities library """
import os

from dummy_file_generator.exceptions import DummyFileGeneratorException


def get_path_from_project_sub_folder(sub_folder, filename='') -> str:
    """
    returns file path or folder path based on the provided args
    from the dummy_file_generator/dummy_file_generator location
    :param sub_folder:
    :param filename:
    :return:
    """
    current_dir = os.path.dirname(__file__)
    current_dir_path = os.path.join(current_dir)
    return os.sep.join([current_dir_path, sub_folder, filename])


def create_target_folder_if_not_exists(absolute_path) -> None:
    """
    function creating the target folder if it does not exist
    :param absolute_path:
    :return:
    """
    if not os.path.exists(os.path.dirname(absolute_path)):
        try:
            os.makedirs(os.path.dirname(absolute_path))
        except OSError as os_err:
            raise DummyFileGeneratorException(f'Cannot create target folder, '
                                              f'OSError: {os_err}')
        except TypeError as type_err:
            raise DummyFileGeneratorException(f'Cannot create target folder, '
                                              f'TypeError: {type_err}')


def get_data_file_content_list_with_item_count(data_set_name, data_files_location) -> tuple:
    """
    load a data file from filesystem and return a tuple with the list of the file content and
    an int with the length of the file content list
    :param data_set_name:
    :param data_files_location:
    :return:
    """
    data_files_dir_path = os.path.join(data_files_location)
    data_set_file_stream = open(os.sep.join((str(data_files_dir_path), data_set_name)))
    data_set = data_set_file_stream.read().split('\n')
    return data_set, len(data_set)


def list_data_files(data_files_location) -> list:
    """
    list data files function
    :param data_files_location:
    :return:
    """
    try:
        data_files_list = [f for f in os.listdir(data_files_location) if
                           os.path.isfile(os.path.join(data_files_location, f))
                           and str(f).endswith('.txt')]
    except OSError as os_err:
        raise DummyFileGeneratorException(f'Cannot list data_files, '
                                          f'OSError: {os_err}')

    if not data_files_list:
        raise DummyFileGeneratorException(f'No data_files in {data_files_location}')

    return data_files_list


def load_data_files_content(data_files_location) -> dict:
    """
    load data files content function
    :param data_files_location:
    :return:
    """
    data_files_list = list_data_files(data_files_location=data_files_location)

    data_files_content = dict()
    for data_file in data_files_list:
        data_files_content[data_file] = \
            get_data_file_content_list_with_item_count(data_file,
                                                       data_files_location=data_files_location)

    return data_files_content


def get_map_value(map_dict, key):
    """
    function returning value by key from a mapping dict
    :param map_dict:
    :param key:
    :return:
    """
    try:
        return map_dict[key]
    except KeyError as key_err:
        raise DummyFileGeneratorException(f'KeyError {key_err} for provided '
                                          f'map_dict: {map_dict} and key: {key}')
