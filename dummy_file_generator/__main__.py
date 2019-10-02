""" dummy file generator main runner """
import argparse
import json
import io
import os
import sys
import logging

from random import randint
from datetime import datetime

from dummy_file_generator.lib.utils import add_quotes_to_list_items, \
    whitespace_generator, read_file_return_content_and_content_list_length
from dummy_file_generator.configurables.settings import DEFAULT_ROW_COUNT, FILE_ENCODING, \
    FILE_LINE_ENDING, CSV_VALUE_SEPARATOR


class DummyFileGenerator:
    """
    main project class
    """
    def __init__(self, **kwargs):
        self.column_name_list = []
        self.column_len_list = []
        self.data_file_list = []
        self.header = None
        self.file_type = None
        self.config_json_path = None
        for key, value in kwargs.items():
            setattr(self, key, value)

        data_files = [f for f in os.listdir(self.data_files_location) if # pylint: disable=no-member
                      os.path.isfile(os.path.join(self.data_files_location, f)) # pylint: disable=no-member
                      and str(f).endswith('.txt')]

        for data_file in data_files:
            setattr(self, data_file.replace('.txt', ''),
                    read_file_return_content_and_content_list_length(data_file,
                                                                     data_files_location=
                                                                     self.data_files_location)) # pylint: disable=no-member
        # set logging levels for main function console output
        logging.basicConfig(level=self.logging_level) # pylint: disable=no-member
        self.logger = logging.getLogger(__name__)


    @staticmethod
    def csv_row_header(columns, csv_value_separator):
        """
        csv row header
        :param columns:
        :param csv_value_separator:
        :return: csv row header
        """
        columns = add_quotes_to_list_items(columns)
        header_row = []

        for column in columns:
            column = column.strip("'")
            header_row.append(column)
        header_row = csv_value_separator.join(header_row) + csv_value_separator
        return header_row


    def flat_row_header(self, columns, column_lengths):
        """
        flat row header
        :param columns:
        :param column_lengths:
        :return: flat row header
        """
        header_row = []

        for i, j in zip(columns, column_lengths):
            if len(i) > j:
                self.logger.error('Header value %s is longer then expected column length '
                                  'set in config.json file!', i)
            else:
                header_row.append(str(i) + whitespace_generator(j - len(i)))
        header_row = "".join(header_row)
        return header_row


    def csv_row_output(self, columns, csv_value_separator):
        """
        function for generating csv output data row
        :param columns:
        :param csv_value_separator:
        :return: output csv data row
        """
        columns = add_quotes_to_list_items(columns)
        row = []

        for column in columns:
            column = column.strip("'")
            _val, _len = DummyFileGenerator.__getattribute__(self, column)
            value = _val[randint(0, _len)]
            row.append(value)
        row = csv_value_separator.join(row)
        return row


    def flat_row_output(self, columns, column_lengths):
        """
        function for generating flat output data row
        :param columns:
        :param column_lengths:
        :return: output flat data row
        """
        columns = add_quotes_to_list_items(columns)
        column_lengths = add_quotes_to_list_items(column_lengths)
        row = []

        for index, column in enumerate(columns):
            column = column.strip("'")
            whitespace = int(column_lengths[index])
            _val, _len = DummyFileGenerator.__getattribute__(self, column)
            value = _val[randint(0, _len)]
            if whitespace - len(value) < 0:
                self.logger.error('Column value %s is longer then expected '
                                  'column length set in config.json file!', value)
            value = value + whitespace_generator(whitespace - len(value))
            row.append(value)
        row = ''.join(row)
        return row


    def read_config(self):
        """
        read config json file function
        :return:
        """
        project_name = self.project_name  # pylint: disable=no-member

        if not self.config_json_path:
            self.config_json_path = os.sep.join([os.path.join(os.path.dirname(__file__)),
                                                 'configurables', 'config.json'])

        with open(self.config_json_path) as file:
            data = json.load(file)

        for project in data['project']:
            if project['project_name'] == project_name:
                self.header = project['header']
                self.file_type = project['file_type']
                for column in project['columns']:
                    self.column_name_list.append(column['column_name'])
                    self.data_file_list.append(str(column['datafile']).replace('.txt', ''))
                    if self.file_type == "flat":
                        self.column_len_list.append(column['column_len'])
                break
        else:
            _message = ('No such project as %s found in config.json', project_name)
            self.logger.error(_message)
            raise ValueError(_message)


    def write_output(self):
        """
        write output function
        :return:
        """
        if not os.path.exists(os.path.dirname(self.absolute_path)):  # pylint: disable=no-member
            os.makedirs(os.path.dirname(self.absolute_path))  # pylint: disable=no-member
            self.logger.info('Target folder not exists, created %s',
                             os.path.dirname(self.absolute_path)) # pylint: disable=no-member

        column_name_list = self.column_name_list
        column_len_list = self.column_len_list
        data_file_list = self.data_file_list
        output_file_name = self.absolute_path  # pylint: disable=no-member

        try:
            output_file_size = self.file_size * 1024  # pylint: disable=no-member
        except AttributeError:
            output_file_size = 0
        try:
            row_count = self.row_count  # pylint: disable=no-member
        except AttributeError:
            row_count = 0
        if row_count == 0 and output_file_size == 0:
            # use default row_count from settings.py in case no row counts
            # and no file size args provided:
            row_count = DEFAULT_ROW_COUNT

        with io.open(output_file_name, 'w', encoding=FILE_ENCODING) as output_file:
            execution_start_time = datetime.now()
            self.logger.info('File %s processing started at %s', output_file_name,
                             execution_start_time)

            if bool(self.header):
                if self.file_type == "csv":
                    output_file.write(self.csv_row_header(column_name_list, CSV_VALUE_SEPARATOR)
                                      + FILE_LINE_ENDING)
                elif self.file_type == "flat":
                    output_file.write(self.flat_row_header(column_name_list, column_len_list)
                                      + FILE_LINE_ENDING)

            iterator = 1
            while output_file.tell() < output_file_size or iterator < row_count:
                if self.file_type == "csv":
                    row = self.csv_row_output(data_file_list, CSV_VALUE_SEPARATOR)
                elif self.file_type == "flat":
                    row = self.flat_row_output(data_file_list, column_len_list)
                else:
                    self.logger.error('Unknown file_type %s, supported options are csv and flat',
                                      self.file_type)
                    sys.exit(1)

                output_file.write(row + FILE_LINE_ENDING)
                iterator += 1

                if divmod(iterator, 10000)[1] == 1:
                    self.logger.info('%s rows written', iterator - 1)

            # to get the file_size even when only row_count arg used
            output_file_size = output_file.tell()
            output_file.close()

            execution_end_time = datetime.now()
            duration = (execution_end_time - execution_start_time).seconds
            duration = str(duration / 60) + ' min.' if duration > 1000 else str(duration) + ' sec.'

            self.logger.info('File %s processing finished at %s', output_file_name,
                             execution_end_time)
            self.logger.info('%s kB file with %s rows written in %s', output_file_size / 1024,
                             iterator, duration)


    def executor(self):
        """
        main function
        :return:
        """
        DummyFileGenerator.read_config(self)
        DummyFileGenerator.write_output(self)


def args():
    """
    argparse based argument parsing function
    :return: kwargs
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--projectname', type=str, required=True)
    parser.add_argument('-ap', '--absolutepath', type=str, required=True)
    parser.add_argument('-fs', '--filesize', type=int, required=False, default=0)
    parser.add_argument('-rc', '--rowcount', type=int, required=False, default=0)
    parser.add_argument('-ll', '--logging_level', type=str, required=False, default="INFO")

    parser.add_argument('-cjp', '--config_json_path', type=str, required=False, default=None)
    parser.add_argument('-dfl', '--data_files_location', type=str, required=False,
                        default=os.sep.join((os.getcwd(), 'data_files')))
    parser.add_argument('-drc', '--default_rowcount', type=int, required=False, default=100)
    parser.add_argument('-fen', '--file_encoding', type=str, required=False, default="utf8")
    parser.add_argument('-fle', '--file_line_ending', type=str, required=False, default="\n")
    parser.add_argument('-cvs', '--csv_value_separator', type=str, required=False, default="|")

    parsed = parser.parse_args()

    project_name = parsed.projectname
    absolute_path = parsed.absolutepath
    file_size = parsed.filesize
    row_count = parsed.rowcount
    logging_level = parsed.logging_level
    config_json_path = parsed.config_json_path
    data_files_location = parsed.data_files_location
    default_rowcount = parsed.default_rowcount
    file_encoding = parsed.file_encoding
    file_line_ending = parsed.file_line_ending
    csv_value_separator = parsed.csv_value_separator

    kwargs = {"project_name": project_name, "absolute_path": absolute_path,
              "file_size": file_size, "row_count": row_count,
              "logging_level": logging_level,
              "data_files_location": data_files_location,
              "config_json_path": config_json_path,
              "default_rowcount": default_rowcount,
              "file_encoding": file_encoding,
              "file_line_ending": file_line_ending,
              "csv_value_separator": csv_value_separator
              }

    return kwargs


if __name__ == "__main__":
    KWARGS = args()
    OBJ = DummyFileGenerator(**KWARGS)
    DummyFileGenerator.executor(OBJ)
