import sys
import os.path

data_files_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(data_files_dir)

import data_files


# assuming test.txt has len of only 3(rows) and therefore is having less rows then firstnames.txt file
def test_min_data_file_len():
    unit_test_eval = data_files.min_data_file_len('["test.txt","firstnames.txt"]')

    assert unit_test_eval == 3
