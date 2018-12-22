""" dummy file generator main runner """
import argparse
import json
import os.path
import io
import logging
from datetime import datetime
import data_files_handler as data_files
from configurables.settings import DEFAULT_ROW_COUNT, FILE_ENCODING, FILE_LINE_ENDING, \
    CSV_VALUE_SEPARATOR


def args():
    """
    argparse based argument parsing function
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--projectname', type=str, required=True)
    parser.add_argument('-fn', '--filename', type=str, required=True)
    parser.add_argument('-fs', '--filesize', type=int, required=False, default=0)
    parser.add_argument('-rc', '--rowcount', type=int, required=False, default=0)
    parser.add_argument('-gf', '--generated_files_location', type=str,
                        required=False, default='generated_files')
    parsed = parser.parse_args()

    project_name = parsed.projectname
    file_name = parsed.filename
    file_size = parsed.filesize
    row_count = parsed.rowcount
    generated_files_location = parsed.generated_files_location

    obj = DummyFileGenerator(project_name, file_name, file_size, row_count,
                             generated_files_location)
    DummyFileGenerator.main(obj)


class DummyFileGenerator:
    """
    main project class
    """
    def __init__(self, project_name, file_name, file_size, row_count,
                 generated_files_location):
        self.project_name = project_name
        self.config_path = os.sep.join([os.path.join(os.path.dirname(__file__)), 'configurables'])
        self.file_name = file_name
        self.file_size = file_size
        self.row_count = row_count
        self.generated_files_location = generated_files_location
        self.column_name_list = []
        self.column_len_list = []
        self.data_file_list = []
        self.header = None
        self.file_type = None
        self.file_extension = None

    def read_config(self):
        """
        read config json file function
        :return:
        """
        project_name = self.project_name
        config_path = self.config_path

        with open(config_path + os.sep + 'config.json') as file:
            data = json.load(file)

            for project in data['project']:
                if project['project_name'] == project_name:
                    self.header = project['header']
                    self.file_type = project['file_type']
                    self.file_extension = project['file_extension']
                    for column in project['columns']:
                        self.column_name_list.append(column['column_name'])
                        self.data_file_list.append(str(column['datafile']).replace('.txt', ''))
                        if self.file_type == "flat":
                            self.column_len_list.append(column['column_len'])

    def write_output(self):
        """
        write output function
        :return:
        """
        column_name_list = self.column_name_list
        column_len_list = self.column_len_list
        data_file_list = self.data_file_list

        output_file_size = self.file_size
        row_count = self.row_count
        output_file_extension = '.' + self.file_extension
        output_file_name = os.sep.join(['.', self.generated_files_location,
                                        self.file_name + output_file_extension])

        file_line_ending = FILE_LINE_ENDING
        file_encoding = FILE_ENCODING
        csv_value_separator = CSV_VALUE_SEPARATOR

        if row_count == 0 and output_file_size == 0:
            # use default row_count from settings.py in case no row counts
            # and no file size args provided:
            row_count = DEFAULT_ROW_COUNT

        with io.open(output_file_name, 'w', encoding=file_encoding) as output_file:
            execution_start_time = datetime.now()
            logging.info('File %s processing started at %s', output_file_name,
                         execution_start_time)

            if bool(self.header):
                if self.file_type == "csv":
                    output_file.write(data_files.csv_row_header(column_name_list,
                                                                csv_value_separator)
                                      + file_line_ending)
                elif self.file_type == "flat":
                    output_file.write(data_files.flat_row_header(column_name_list,
                                                                 column_len_list)
                                      + file_line_ending)

            iterator = 1
            while output_file.tell() < output_file_size or iterator < row_count:
                if self.file_type == "csv":
                    row = data_files.csv_row_output(data_file_list, csv_value_separator)
                elif self.file_type == "flat":
                    row = data_files.flat_row_output(data_file_list, column_len_list)

                output_file.write(row + file_line_ending)
                iterator = iterator + 1

                if divmod(iterator, 10000)[1] == 1:
                    logging.info('%s rows written', iterator-1)

            output_file.close()

            execution_end_time = datetime.now()
            duration = (execution_end_time - execution_start_time).seconds

            if duration > 1000:
                duration = str(duration / 60) + ' minutes'
            else:
                duration = str(duration) + ' seconds'

            logging.info('File %s processing finished at %s\n '
                         '%s kB file with %s rows written in %s',
                         output_file_name, execution_end_time,
                         output_file_size/1024, iterator, duration)

    def main(self):
        """
        main function
        :return:
        """
        # set logging levels for main function console output
        logging.getLogger().setLevel(logging.INFO)

        DummyFileGenerator.read_config(self)
        DummyFileGenerator.write_output(self)


if __name__ == "__main__":
    args()
