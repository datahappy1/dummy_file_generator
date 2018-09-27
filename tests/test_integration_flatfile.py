import os.path


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

    filename = "tests", "test_run_result_integration_test_flatfile"
    filename = os.sep.join(filename)

    os.system(main_file_path + " -pn test_flatfile -fn " + filename + " -fs 256")

    generated_files = str(os.path.abspath(os.curdir))
    generated_files = generated_files, 'generated_files', (filename + '.txt')
    generated_files = os.sep.join(generated_files)

    with open(generated_files, 'r') as test_run_file:
        test_run_data_var = test_run_file.read()
        return test_run_data_var


def referential_result_loader():
    ref_test_file_path = str(os.path.abspath(os.curdir)).strip('tests')
    ref_test_file_path = ref_test_file_path, 'generated_files', 'tests', 'referential_result_integration_test_flatfile.txt'
    ref_test_file_path = os.sep.join(ref_test_file_path)

    with open(ref_test_file_path, 'r') as referential_result_file:
        referential_result_data_var = referential_result_file.read()
        return referential_result_data_var


def test_integration_flatfile():
    test_run_data_var = test_runner()
    referential_result_data_var = referential_result_loader()
    assert test_run_data_var == referential_result_data_var
