import sys
import os.path

main_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(main_dir)

from src import dummy_file_generator


# assuming the referential_result_integration_test_flatfile.txt file and
# the file generated in this test with test.txt data_file loaded in is having the same content
def test_integration_csv():
    filename = "test_run_result_integration_test_flatfile"

    dummy_file_generator.main("test_flatfile", filename, 250, 'generated_files' + os.sep + 'tests' + os.sep)

    generated_file_path = str(os.path.abspath(os.curdir)).strip('tests')
    generated_file_path = generated_file_path + 'generated_files' + os.sep +'tests' + os.sep + (filename + '.txt')
    #generated_file_path = os.sep.join(generated_file_path)


    with open(generated_file_path, 'r') as test_run_file:
        test_run_data_var = test_run_file.read()

    ref_test_file_path = str(os.path.abspath(os.curdir)).strip('tests')
    ref_test_file_path = ref_test_file_path, 'generated_files', 'tests', 'referential_result_integration_test_flatfile.txt'
    ref_test_file_path = os.sep.join(ref_test_file_path)

    with open(ref_test_file_path, 'r') as referential_result_file:
        referential_result_data_var = referential_result_file.read()

    assert test_run_data_var == referential_result_data_var
