import argparse
import json
from src import data_files_handler as data_files, settings, utils as util
import logging
import sys
import os.path
import io
from datetime import datetime


def args():
    ###########################################################################
    # 0: parsing and storing arguments
    ###########################################################################

    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--projectname', type=str, required=True)
    parser.add_argument('-fn', '--filename', type=str, required=True)
    parser.add_argument('-fs', '--filesize', type=int, required=False, default=0)
    parser.add_argument('-rc', '--rowcount', type=int, required=False, default=0)
    parser.add_argument('-gf', '--generated_files_location', type=str, required=False, default='generated_files')
    parsed = parser.parse_args()

    project_name = parsed.projectname
    file_name = parsed.filename
    file_size = parsed.filesize
    row_count = parsed.rowcount
    generated_files_location = parsed.generated_files_location

    main(project_name, file_name, file_size, row_count, generated_files_location)


def main(project_name, file_name, file_size, row_count, generated_files_location=''):
    ###########################################################################
    # 1: reading configuration json for project and file paths setup
    ###########################################################################
    project_path = os.path.abspath(os.curdir).replace('src', '').replace('tests', '') + os.sep

    with open(project_path + 'config.json') as f:
        data = json.load(f)

        column_name_list = []
        column_len_list = []
        data_file_list = []
        column_stmt_first_loop = []
        column_stmt_more_loops = []

    ###########################################################################
    # 2: building statements based off config.json project settings
    ###########################################################################
        for project in data['project']:
            if project['project_name'] == project_name:
                header = project['header']
                file_type = project['file_type']
                file_extension = project['file_extension']

                # csv statements
                if file_type == "csv":
                    for column in project['columns']:

                        column_name_list.append(column['column_name'])
                        data_file_list.append(column['datafile'])

                        column_stmt_first_loop.append('data_files.DataFiles.return_csv_value("' + column['datafile']
                                                      + '",iterator)')
                        column_stmt_more_loops.append('data_files.DataFiles.return_csv_value("' + column['datafile']
                                                      + '",divmod(iterator,data_files.DataFiles.return_count("'
                                                      + column['datafile'] + '"))[1])')

                    header_row_str = util.Headers.return_csv_header(column_list=column_name_list)
                    column_stmt_first_loop_str = util.list_to_stmt(statement=column_stmt_first_loop, add_plus_sign=True, add_comma=True)
                    column_stmt_more_loops_str = util.list_to_stmt(statement=column_stmt_more_loops, add_plus_sign=True, add_comma=True)

                # flat file statements
                elif file_type == "flat":
                    for column in project['columns']:

                        column_name_list.append(column['column_name'])
                        column_len_list.append(column['column_len'])

                        data_file_list.append(column['datafile'])

                        column_stmt_first_loop.append('data_files.DataFiles.return_flat_value("' + column['datafile']
                                                      + '","' + str(column['column_len'])
                                                      + '",iterator)')
                        column_stmt_more_loops.append('data_files.DataFiles.return_flat_value("' + column['datafile']
                                                      + '","' + str(column['column_len'])
                                                      + '",divmod(iterator,data_files.DataFiles.return_count("'
                                                      + column['datafile'] + '"))[1])')

                    header_row_str = util.Headers.return_flat_header(column_name_list=column_name_list, column_len_list=column_len_list)
                    column_stmt_first_loop_str = util.list_to_stmt(statement=column_stmt_first_loop, add_plus_sign=True, add_comma=False)
                    column_stmt_more_loops_str = util.list_to_stmt(statement=column_stmt_more_loops, add_plus_sign=True, add_comma=False)

                else:
                    logging.error(f'No such file type as {file_type} can be used, only csv or flat types are supported!')
                    sys.exit(1)
                break
        else:
            logging.error(f'No such project as {project_name} defined in config.json configuration file!')
            sys.exit(1)

    ###########################################################################
    # 3: preparing variables needed for output file generation
    ###########################################################################
    iterator = 0
    output_file_size = file_size
    output_file_extension = '.' + file_extension
    output_file_name = os.sep.join(['.', generated_files_location, file_name + output_file_extension])

    min_data_file_len = data_files.DataFiles.min_data_file_len(data_file_list)
    file_encoding = settings.file_encoding

    if row_count == 0 and file_size == 0:
        # use default row_count from settings.py in case no row counts and no file size args provided:
        row_count = settings.default_row_count

    ###########################################################################
    # 4: writing the output file
    ###########################################################################
    with io.open(output_file_name, 'w', encoding=file_encoding) as output_file:
        execution_start_time = datetime.now()
        print(f'File {output_file_name} processing started at {execution_start_time}')

        if bool(header):
            output_file.write(header_row_str)

        while output_file.tell() < output_file_size or iterator < row_count:
            if iterator < min_data_file_len:
                output_file.write(eval(column_stmt_first_loop_str)+'\n')
            else:
                output_file.write(eval(column_stmt_more_loops_str)+'\n')

                if divmod(iterator, 10000)[1] == 1:
                    print(f'{iterator-1} rows written')

            iterator = iterator + 1

        output_file.close()

        execution_end_time = datetime.now()
        duration = (execution_end_time - execution_start_time).seconds
        if duration > 1000:
            duration = str(duration / 60) + ' minutes'
        else:
            duration = str(duration) + ' seconds'

        print(f'File {output_file_name} processing finished at {execution_end_time}')
        print(f'{output_file_size/1024} kB file with {iterator} rows was written in {duration}')


if __name__ == "__main__":
    args()
