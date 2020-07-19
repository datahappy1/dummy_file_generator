"""
test performance
"""
import os
import pytest
from datetime import datetime

from dummy_file_generator.__main__ import DummyFileGenerator as Dfg

CONFIG_JSON_PATH = os.sep.join([os.getcwd(), 'files', 'test_config.json'])
LOGGING_LEVEL = 'INFO'
DATA_FILES_LOCATION = 'files'


@pytest.mark.parametrize(
    "test_project, test_file_extension, expected_duration", [
        ("test_csv", ".csv", 1),
        ("test_flatfile", ".txt", 1)
    ])
def test_performance_csv(test_project, test_file_extension, expected_duration):
    """
    assuming 1MB csv or 1 MB flat text file will get written under 1 or in 1 second,
    you can alter the referential value "expected_duration" based on your HW resources
    :return: assertion result
    """
    filename = "test_run_result_performance" + test_file_extension
    generated_file_path = os.sep.join(['generated_files', 'tests', filename])

    execution_start_time = datetime.now()

    project_scope_kwargs = {
        "project_name": test_project,
        "data_files_location": DATA_FILES_LOCATION,
        "config_json_path": CONFIG_JSON_PATH,
        "default_rowcount": None,
    }

    dfg_obj = Dfg(LOGGING_LEVEL, **project_scope_kwargs)

    file_scope_kwargs = {
        "absolute_path": generated_file_path,
        "file_size": 1024,
        "row_count": None,
        "file_encoding": None,
        "file_line_ending": None,
        "csv_value_separator": None,
    }

    dfg_obj.write_output_file(**file_scope_kwargs)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds

    os.remove(generated_file_path)

    assert duration <= expected_duration
