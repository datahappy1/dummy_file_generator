"""
test performance
"""
import os.path
from datetime import datetime
from dummy_file_generator import DummyFileGenerator as dfg


def test_performance_csv():
    """
    assuming 1MB csv file will get written under 3 seconds
    alter this referential value based on your HW resources
    :return: assertion result
    """
    filename = "test_run_result_performance"
    generated_file_path = os.sep.join(['generated_files', 'tests'])

    execution_start_time = datetime.now()

    obj = dfg("test_csv", filename, 1048576, 0, generated_file_path)
    dfg.main(obj)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds
    duration_threshold = 3

    assert duration < duration_threshold


def test_performance_flat():
    """
    assuming 1MB flat txt file will get written under 3 seconds
    alter this referential value based on your HW resources
    :return: assertion result
    """
    filename = "test_run_result_performance"
    generated_file_path = os.sep.join(['generated_files', 'tests'])

    execution_start_time = datetime.now()

    obj = dfg("test_flatfile", filename, 1048576, 0, generated_file_path)
    dfg.main(obj)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds
    duration_threshold = 3

    assert duration < duration_threshold
