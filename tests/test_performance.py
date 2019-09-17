"""
test performance
"""
import os.path
from datetime import datetime
import pytest
from dummy_file_generator.__main__ import DummyFileGenerator as Dfg

@pytest.mark.parametrize(
    "test_project, test_file_extension, expected_duration", [
        ("test_csv", ".csv", 1),
        ("test_flatfile", ".txt", 1)
    ])
def test_performance(test_project, test_file_extension, expected_duration):
    """
    assuming 1MB csv or 1 MB flat text file will get written under 1 or in 1 second,
    you can alter the referential value "expected_duration" based on your HW resources
    :return: assertion result
    """
    filename = "test_run_result_performance" + test_file_extension
    generated_file_path = os.sep.join(['generated_files', 'tests', filename])

    execution_start_time = datetime.now()

    kwargs = {"project_name": test_project, "absolute_path": generated_file_path,
              "file_size": 1024, "row_count": 0, "logging_level": "INFO"}

    obj = Dfg(**kwargs)
    Dfg.main(obj)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds

    os.remove(generated_file_path)

    assert duration <= expected_duration
