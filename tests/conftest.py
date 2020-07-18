import os
import pytest

from dummy_file_generator.__main__ import DummyFileGenerator as Dfg


@pytest.fixture(scope="session", autouse=True)
def tests_setup_dfg_instance():
    CONFIG_JSON_PATH = os.sep.join([os.getcwd(), 'files', 'test_config.json'])
    LOGGING_LEVEL = 'INFO'
    DATA_FILES_LOCATION = 'files'
    PROJECT_SCOPE_KWARGS = {
        "project_name": 'test_csv',
        "data_files_location": DATA_FILES_LOCATION,
        "config_json_path": CONFIG_JSON_PATH,
        "default_rowcount": None,
    }

    dfg_obj = Dfg(LOGGING_LEVEL, **PROJECT_SCOPE_KWARGS)
    return dfg_obj
