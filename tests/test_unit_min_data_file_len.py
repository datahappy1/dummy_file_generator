import sys
import os.path

data_files_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(data_files_dir)

import data_files


# set the correct directory to enable both pytest runs and manual specific test runs
p = os.getcwd().split(os.sep)
if p[(len(p)-1)] == 'tests':
    os.chdir(os.path.dirname(os.getcwd()))
else:
    pass


data_files_path = os.path.abspath(os.curdir), 'data_files.py'
data_files_path = os.sep.join(data_files_path)

utils_path = os.path.abspath(os.curdir), 'utils.py'
utils_path = os.sep.join(utils_path)

# assuming test.txt has len of only 3(rows) and therefore is having less rows then firstnames.txt file
unit_test_eval = data_files.min_data_file_len('["test.txt","firstnames.txt"]')


def test_min_data_file_len():
    assert unit_test_eval == 3
