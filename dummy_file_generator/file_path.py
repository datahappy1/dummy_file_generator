import os

from dummy_file_generator.exceptions import DummyFileGeneratorException


def get_path_from_project_sub_folder(sub_folder: str, filename: str = "") -> str:
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


def create_target_folder_if_not_exists(absolute_path: str) -> None:
    """
    function creating the target folder if it does not exist
    :param absolute_path:
    :return:
    """
    if not os.path.exists(os.path.dirname(absolute_path)):
        try:
            os.makedirs(os.path.dirname(absolute_path))
        except OSError as os_err:
            raise DummyFileGeneratorException(
                f"Cannot create target folder, " f"OSError: {os_err}"
            )
        except TypeError as type_err:
            raise DummyFileGeneratorException(
                f"Cannot create target folder, " f"TypeError: {type_err}"
            )
