import os.path
from datetime import datetime
import sys

main_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(main_dir)

from dummy_file_generator.dummy_file_generator import main


# assuming 1Mb flat file will get written under 30 seconds
# alter this referential value based on your HW resources
def test_integration_flatfile():
    filename = "tests", "test_run_result_performance_test_flatfile"
    filename = os.sep.join(filename)

    execution_start_time = datetime.now()

    main("test_flatfile", filename, 1048576, 'generated_files' + os.sep)

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds

    duration_threshold = 30
    assert duration < duration_threshold
