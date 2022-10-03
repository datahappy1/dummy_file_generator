"""
test performance
"""
import os
import pytest
from datetime import datetime

from dummy_file_generator.__main__ import DummyFileGenerator as Dfg

CONFIG_JSON_PATH = os.sep.join([os.getcwd(), 'tests', 'files', 'test_config.json'])
DATA_FILES_LOCATION = os.sep.join([os.getcwd(), 'tests', 'files'])
GENERATED_FILE_PATH_BASE = os.sep.join(['tests', 'generated_files'])
LOGGING_LEVEL = 'INFO'


# def teardown_module():
#     for filename in os.listdir(GENERATED_FILE_PATH_BASE):
#         file_path = os.path.join(GENERATED_FILE_PATH_BASE, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#         except Exception as e:
#             print('Failed to delete %s. Reason: %s' % (file_path, e))


@pytest.mark.parametrize(
    "test_project, test_file_extension, expected_duration", [
        # ("test_csv", ".csv", 1),
        # ("test_flatfile", ".txt", 1),
        ("test_json", ".json", 1)
    ])
def test_performance_csv(test_project, test_file_extension, expected_duration):
    """
    assuming 1MB csv, 1 MB flat text or 1 MB json file will get written under 1 or in 1 second,
    you can alter the referential value "expected_duration" based on your HW resources
    :return: assertion result
    """
    filename = "test_run_result_performance" + test_file_extension
    generated_file_abs_path = os.sep.join([GENERATED_FILE_PATH_BASE, filename])

    execution_start_time = datetime.now()

    project_scope_kwargs = {
        "project_name": test_project,
        "data_files_location": DATA_FILES_LOCATION,
        "config_json_path": CONFIG_JSON_PATH,
        "default_rowcount": None,
    }

    dfg_obj = Dfg(LOGGING_LEVEL, **project_scope_kwargs)

    file_scope_kwargs = {
        "generated_file_path": generated_file_abs_path,
        "file_size": 1024,
        "row_count": None,
        "file_encoding": None,
        "file_line_ending": None,
    }

    dfg_obj.write_output_file(**file_scope_kwargs)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds

    assert duration <= expected_duration

