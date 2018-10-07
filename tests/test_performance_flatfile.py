import os.path
from datetime import datetime
import sys

main_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(main_dir)

from src import dummy_file_generator


# assuming 1Mb flat file will get written under 3 seconds
# alter this referential value based on your HW resources
def test_integration_flatfile():
    filename = "test_run_result_performance_test_flatfile"
    generated_file_path = 'generated_files' + os.sep + 'tests' + os.sep

    execution_start_time = datetime.now()

    dummy_file_generator.main("test_flatfile", filename, 250, generated_file_path)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds

    duration_threshold = 3
    assert duration < duration_threshold
