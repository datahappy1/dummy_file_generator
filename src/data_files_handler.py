import logging
import io
import os.path
import sys
from src import settings, utils as util


def load_file(data_file_name):
    # strip tests from abspath to support pytest running integration and performance tests
    # from /tests folder
    project_path = os.path.abspath(os.curdir).strip('src').strip('tests')
    data_files_path = os.sep.join([project_path, 'data_files', data_file_name])
    file_encoding = settings.file_encoding

    try:
        with io.open(data_files_path, 'r', encoding=file_encoding) as file:
            data = file.read()
            return data.split('\n')
    except IOError:
        logging.error(f'Error when trying to read {data_files_path}!')
        sys.exit(1)


class DataFiles:
    ###############################################################################
    # Load data files into variables and configure data_files related functions
    # Whenever you add a new data_files file, remember to set it up here!
    ###############################################################################

    # integration and perf. tests file load
    test_file = load_file(data_file_name='test.txt')

    # the real data files load
    first_names_file = load_file(data_file_name='firstnames.txt')
    last_names_file = load_file(data_file_name='lastnames.txt')
    dates_file = load_file(data_file_name='dates.txt')
    ids_file = load_file(data_file_name='IDs.txt')

    @staticmethod
    def return_csv_value(data_file_name, iterator):
        # integration and perf. tests
        if data_file_name == 'test.txt':
            return DataFiles.test_file[iterator]

        # the real data files
        elif data_file_name == 'firstnames.txt':
            return DataFiles.first_names_file[iterator]
        elif data_file_name == 'lastnames.txt':
            return DataFiles.last_names_file[iterator]
        elif data_file_name == 'dates.txt':
            return DataFiles.dates_file[iterator]
        elif data_file_name == 'IDs.txt':
            return DataFiles.ids_file[iterator]
        else:
            logging.error(f'Error when calling function return_csv_value with data_file_name: {data_file_name} ,'
                          f'No such data file in data_files dir!')
            sys.exit(1)

    @staticmethod
    def return_flat_value(data_file_name, column_len, iterator):
        # integration and perf. tests
        if data_file_name == 'test.txt':
            return (DataFiles.test_file[iterator] + util.whitespace_generator(int(column_len) - len(DataFiles.test_file[iterator])))[:int(column_len)]

        # the real data files
        elif data_file_name == 'firstnames.txt':
            return (DataFiles.first_names_file[iterator] + util.whitespace_generator(int(column_len) - len(DataFiles.first_names_file[iterator])))[:int(column_len)]
        elif data_file_name == 'lastnames.txt':
            return (DataFiles.last_names_file[iterator] + util.whitespace_generator(int(column_len) - len(DataFiles.last_names_file[iterator])))[:int(column_len)]
        elif data_file_name == 'dates.txt':
            return (DataFiles.dates_file[iterator] + util.whitespace_generator(int(column_len) - len(DataFiles.dates_file[iterator])))[:int(column_len)]
        elif data_file_name == 'IDs.txt':
            return (DataFiles.ids_file[iterator] + util.whitespace_generator(int(column_len) - len(DataFiles.ids_file[iterator])))[:int(column_len)]
        else:
            logging.error(f'Error when calling function return_flat_value with data_file_name: {data_file_name} ,'
                          f'No such data file in data_files dir!')
            sys.exit(1)

    @staticmethod
    def min_data_file_len(data_file_list):
        data_file_len_list = []

        # integration and perf. tests
        if 'test.txt' in data_file_list:
            data_file_len_list.append(eval('len(DataFiles.test_file)'))

        # the real data files
        if 'firstnames.txt' in data_file_list:
            data_file_len_list.append(eval('len(DataFiles.first_names_file)'))
        if 'lastnames.txt' in data_file_list:
            data_file_len_list.append(eval('len(DataFiles.last_names_file)'))
        if 'dates.txt' in data_file_list:
            data_file_len_list.append(eval('len(DataFiles.dates_file)'))
        if 'IDs.txt' in data_file_list:
            data_file_len_list.append(eval('len(DataFiles.ids_file)'))
        if len(data_file_len_list) == 0:
            logging.error(f'Error when calling function min_data_file_len with data_file_list: {data_file_list}')
            sys.exit(1)
        return min(eval(str(data_file_len_list)))

    @staticmethod
    def return_count(data_file_name):
        # integration and perf. tests
        if data_file_name == 'test.txt':
            return len(DataFiles.test_file)

        # the real data files
        elif data_file_name == 'firstnames.txt':
            return len(DataFiles.first_names_file)
        elif data_file_name == 'lastnames.txt':
            return len(DataFiles.last_names_file)
        elif data_file_name == 'dates.txt':
            return len(DataFiles.dates_file)
        elif data_file_name == 'IDs.txt':
            return len(DataFiles.ids_file)
        else:
            logging.error(f'Error when calling function return_count with data_file_name: {data_file_name},'
                          f'No such data file in data_files dir!')
            sys.exit(1)
