import argparse
import json
import data_files as data_files
import utils as util
import logging
import sys
import os.path
from datetime import datetime


def main():
    ###########################################################################
    # 0: parsing and storing arguments
    ###########################################################################

    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--projectname', type=str, required=True)
    parser.add_argument('-fn', '--filename', type=str, required=True)
    parser.add_argument('-fs', '--filesize', type=int, required=True)
    parser.add_argument('-gf', '--generated_files_location', type=str, required=False, default='generated_files/')
    parsed = parser.parse_args()

    project_name = parsed.projectname
    file_name = parsed.filename
    file_size = parsed.filesize
    generated_files_location = parsed.generated_files_location

    ###########################################################################
    # 1: reading configuration json for project and file paths setup
    ###########################################################################

    project_path = os.path.join(os.sep, os.path.abspath(os.curdir) + os.sep)

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

                        column_stmt_first_loop.append('data_files.return_csv_value("' + column['datafile']
                                                      + '",iterator)')
                        column_stmt_more_loops.append('data_files.return_csv_value("' + column['datafile']
                                                      + '",divmod(iterator,data_files.return_count("'
                                                      + column['datafile'] + '"))[1])')

                    header_row_str = util.return_csv_header(column_list=column_name_list)

                # flat file statements
                elif file_type == "flat":
                    for column in project['columns']:

                        column_name_list.append(column['column_name'])
                        column_len_list.append(column['column_len'])

                        data_file_list.append(column['datafile'])

                        column_stmt_first_loop.append('data_files.return_flat_value("' + column['datafile']
                                                      + '","' + str(column['column_len'])
                                                      + '",iterator)')
                        column_stmt_more_loops.append('data_files.return_flat_value("' + column['datafile']
                                                      + '","' + str(column['column_len'])
                                                      + '",divmod(iterator,data_files.return_count("'
                                                      + column['datafile'] + '"))[1])')

                    header_row_str = util.return_flat_header(column_name_list=column_name_list,
                                                             column_len_list=column_len_list)

                else:
                    logging.error(f'No such file type as {file_type} can be used, only csv or flat types are supported!')
                    sys.exit(1)

                column_stmt_first_loop_str = util.list_to_stmt(statement=column_stmt_first_loop, add_plus_sign=True)
                column_stmt_more_loops_str = util.list_to_stmt(statement=column_stmt_more_loops, add_plus_sign=True)

                break
        else:
            logging.error(f'No such project as {project_name} defined in config.json configuration file!')
            sys.exit(1)

    ###########################################################################
    # 3: preparing variables needed for output file generation
    ###########################################################################
    iterator = 0
    output_file_size = file_size
    output_file_extension = file_extension
    output_file_name = generated_files_location + file_name + '.' + output_file_extension
    min_data_file_len = data_files.min_data_file_len(data_file_list)

    ###########################################################################
    # 4: writing the output file
    ###########################################################################
    with open(output_file_name, 'w') as output_file:
        execution_start_time = datetime.now()
        print(f'File {output_file_name} processing started at {execution_start_time}')

        if bool(header):
            output_file.write(header_row_str)

        while output_file.tell() < output_file_size:
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
    main()
