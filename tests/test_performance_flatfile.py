import os.path
from datetime import datetime


# set the correct directory to enable both pytest runs and manual specific test runs
p = os.getcwd().split(os.sep)
if p[(len(p)-1)] == 'tests':
    os.chdir(os.path.dirname(os.getcwd()))
else:
    pass


def test_runner():
    main_file_path = str(os.path.abspath(os.curdir)).strip('tests')
    main_file_path = main_file_path, '__main__.py'
    main_file_path = os.sep.join(main_file_path)

    filename = "tests", "test_run_result_performance_test_flatfile"
    filename = os.sep.join(filename)

    execution_start_time = datetime.now()

    os.system(main_file_path + " -pn test_flatfile -fn " + filename + " -fs 1048576")

    execution_end_time = datetime.now()
    duration = (execution_end_time - execution_start_time).seconds
    return duration


duration_test_run = test_runner()


# assuming 1Mb file will get written under 30 seconds
def test_integration_csv():
    duration_threshold = 30

    assert duration_test_run < duration_threshold

