import os
from typing import Tuple, List, Dict

from dummy_file_generator.exceptions import DummyFileGeneratorException

DataFileContentListWithItemCount = Tuple[list, int]


def _list_data_files(data_files_location: str) -> List[str]:
    """
    list data files function
    :param data_files_location:
    :return:
    """
    try:
        data_files_list = [
            f
            for f in os.listdir(data_files_location)
            if os.path.isfile(os.path.join(data_files_location, f))
            and str(f).endswith(".txt")
        ]
    except OSError as os_err:
        raise DummyFileGeneratorException(
            f"Cannot list data_files, " f"OSError: {os_err}"
        )

    if not data_files_list:
        raise DummyFileGeneratorException(f"No data_files in {data_files_location}")

    return data_files_list


def _get_data_file_content_list_with_item_count(
    data_set_file_path: str,
) -> DataFileContentListWithItemCount:
    """
    load a data file from filesystem and return a tuple with the list of the file content and
    an int with the length of the file content list
    :param data_set_file_path:
    :return:
    """
    data_set = open(data_set_file_path).read().split("\n")
    return data_set, len(data_set)


def load_data_files_content(
    data_files_location: str,
) -> Dict[str, DataFileContentListWithItemCount]:
    """
    load data files content function
    :param data_files_location:
    :return:
    """
    data_files_list = _list_data_files(data_files_location=data_files_location)

    data_files_content = dict()
    for data_file in data_files_list:

        data_set_file_path = os.sep.join((os.path.join(data_files_location), data_file))

        data_files_content[data_file] = _get_data_file_content_list_with_item_count(
            data_set_file_path=data_set_file_path
        )

    return data_files_content
