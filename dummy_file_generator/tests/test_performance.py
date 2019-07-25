"""
test performance
"""
import os.path
from datetime import datetime
import pytest
from dummy_file_generator.main import DummyFileGenerator as Dfg


@pytest.mark.parametrize(
    "test_input, test_file_extension, expected_duration", [
        ("test_csv", ".csv", 2),
        ("test_flatfile", ".txt", 2)
    ])
def test_performance(test_input, test_file_extension, expected_duration):
    """
    assuming 1MB csv or 1 MB flat text file will get written under 2 seconds,
    you can alter the referential value "expected_duration" based on your HW resources
    :return: assertion result
    """
    filename = "test_run_result_performance"
    generated_file_path = os.sep.join(['generated_files', 'tests'])

    execution_start_time = datetime.now()

    kwargs = {"project_name": test_input, "file_name": filename, "file_size": 1024,
              "row_count": 0, "generated_files_location": generated_file_path}

    obj = Dfg(**kwargs)
    Dfg.main(obj)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds

    os.remove(os.sep.join([generated_file_path, 'test_run_result_performance' +
                           test_file_extension]))

    assert duration < expected_duration
