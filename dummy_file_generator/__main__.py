""" dummy file generator main runner """
import argparse
import json
import io
import os
import logging

from random import randint
from datetime import datetime

from dummy_file_generator.lib.utils import add_quotes_to_list_items, \
    whitespace_generator, read_file_return_content_and_content_list_length
from dummy_file_generator.configurables.settings import DEFAULT_ROW_COUNT, FILE_ENCODING, \
    FILE_LINE_ENDING, CSV_VALUE_SEPARATOR, LOGGING_LEVEL


class DummyFileGeneratorException(Exception):
    """
    dummy file generator custom exception type
    """


class DummyFileGenerator:
    """
    main project class
    """

    def __init__(self, **kwargs):
        self.project_name = None
        self.data_files_location = None
        self.column_name_list = []
        self.column_len_list = []
        self.data_file_list = []
        self.header = None
        self.file_type = None
        self.config_json_path = None
        self.csv_value_separator = None
        self.file_encoding = None
        self.file_line_ending = None
        self.logging_level = LOGGING_LEVEL
        self.logger = None
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not self.csv_value_separator:
            self.csv_value_separator = CSV_VALUE_SEPARATOR

        if not self.file_encoding:
            self.file_encoding = FILE_ENCODING

        if not self.file_line_ending:
            self.file_line_ending = FILE_LINE_ENDING

        if not self.config_json_path:
            self.config_json_path = os.sep.join([os.path.join(os.path.dirname(__file__)),
                                                 'configurables', 'config.json'])

    def setup_logging(self):
        # set logging levels for main function console output
        logging.basicConfig(level=self.logging_level)
        self.logger = logging.getLogger(__name__)

    def set_vars_from_data_files_content(self):
        data_files = [f for f in os.listdir(self.data_files_location) if
                      os.path.isfile(os.path.join(self.data_files_location, f))
                      and str(f).endswith('.txt')]

        for data_file in data_files:
            setattr(self, data_file.replace('.txt', ''),
                    read_file_return_content_and_content_list_length(data_file,
                                                                     data_files_location=
                                                                     self.data_files_location))

    def read_config_file(self):
        """
        read config json file function
        :return:
        """
        with open(self.config_json_path) as file:
            data = json.load(file)

        for project in data['project']:
            if project['project_name'] == self.project_name:
                self.header = project['header']
                self.file_type = project['file_type']
                for column in project['columns']:
                    self.column_name_list.append(column['column_name'])
                    self.data_file_list.append(str(column['datafile']).replace('.txt', ''))
                    if self.file_type == "flat":
                        self.column_len_list.append(column['column_len'])
                break
        else:
            raise DummyFileGeneratorException('Project %s not found in config.json', self.project_name)

    def validate_config_file(self):
        if self.file_type not in ('csv', 'flat'):
            raise DummyFileGeneratorException('Unknown file_type %s, supported options are csv and flat',
                                              self.file_type)

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
        header_row = csv_value_separator.join(header_row)
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
            if whitespace < len(value):
                self.logger.error('Column value %s is longer then expected '
                                  'column length set in config.json file!', value)
            value = value + whitespace_generator(whitespace - len(value))
            row.append(value)
        row = ''.join(row)
        return row

    def write_output_file(self):
        """
        write output function
        :return:
        """
        if not os.path.exists(os.path.dirname(self.absolute_path)):
            try:
                os.makedirs(os.path.dirname(self.absolute_path))
                self.logger.info('Target folder not existing, created %s', os.path.dirname(self.absolute_path))
            except OSError as OS_ERR:
                raise DummyFileGeneratorException('Cannot create target folder %s', OS_ERR)

        with io.open(self.absolute_path, 'w', encoding=self.file_encoding) as output_file:
            execution_start_time = datetime.now()
            self.logger.info('File %s processing started at %s', self.absolute_path,
                             execution_start_time)

            if bool(self.header):
                if self.file_type == "csv":
                    output_file.write(self.csv_row_header(self.column_name_list, self.csv_value_separator)
                                      + self.file_line_ending)
                elif self.file_type == "flat":
                    output_file.write(self.flat_row_header(self.column_name_list, self.column_len_list)
                                      + self.file_line_ending)

            iterator = 1
            while output_file.tell() < self.file_size or iterator < self.row_count:
                row = None
                if self.file_type == "csv":
                    row = self.csv_row_output(self.data_file_list, self.csv_value_separator)
                elif self.file_type == "flat":
                    row = self.flat_row_output(self.data_file_list, self.column_len_list)

                output_file.write(row + self.file_line_ending)
                iterator += 1

                if divmod(iterator, 10000)[1] == 1:
                    self.logger.info('%s rows written', iterator - 1)

            # to get the file_size even when only row_count arg used
            output_file_size = output_file.tell()
            output_file.close()

            execution_end_time = datetime.now()
            duration = (execution_end_time - execution_start_time).seconds
            duration = str(duration / 60) + ' min.' if duration > 1000 else str(duration) + ' sec.'

            self.logger.info('File %s processing finished at %s', self.absolute_path,
                             execution_end_time)
            self.logger.info('%s kB file with %s rows written in %s', output_file_size / 1024,
                             iterator, duration)

class File(DummyFileGenerator):
    def __init__(self, **project_scope_kwargs):
        super().__init__(**project_scope_kwargs)
        self.absolute_path = None
        self.row_count = 0
        self.file_size = 0

        if self.file_size > 0:
            self.file_size = self.file_size * 1024

        if self.row_count == 0 and self.file_size == 0:
            # use default row_count from settings.py in case no row counts
            # and no file size args provided:
            self.row_count = DEFAULT_ROW_COUNT


    def generate_file(self, **file_scope_kwargs):
        """
        main function
        :return:
        """
        for key, value in file_scope_kwargs.items():
            setattr(self, key, value)

        DummyFileGenerator.setup_logging(self)
        DummyFileGenerator.set_vars_from_data_files_content(self)
        DummyFileGenerator.read_config_file(self)
        DummyFileGenerator.validate_config_file(self)
        DummyFileGenerator.write_output_file(self)


def parse_args():
    """
    argparse based argument parsing function
    :return: kwargs
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--projectname', type=str, required=True)
    parser.add_argument('-ap', '--absolutepath', type=str, required=True)
    parser.add_argument('-fs', '--filesize', type=int, required=False,
                        default=0)
    parser.add_argument('-rc', '--rowcount', type=int, required=False,
                        default=0)
    parser.add_argument('-ll', '--logging_level', type=str, required=False,
                        default=LOGGING_LEVEL)

    parser.add_argument('-cjp', '--config_json_path', type=str, required=False,
                        default=None)
    parser.add_argument('-dfl', '--data_files_location', type=str, required=False,
                        default=os.sep.join((os.getcwd(), 'data_files')))
    parser.add_argument('-drc', '--default_rowcount', type=int, required=False,
                        default=DEFAULT_ROW_COUNT)
    parser.add_argument('-fen', '--file_encoding', type=str, required=False,
                        default=FILE_ENCODING)
    parser.add_argument('-fle', '--file_line_ending', type=str, required=False,
                        default=FILE_LINE_ENDING)
    parser.add_argument('-cvs', '--csv_value_separator', type=str, required=False,
                        default=CSV_VALUE_SEPARATOR)

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

    project_scope_kwargs = {
        "project_name": project_name,
        "logging_level": logging_level,
        "data_files_location": data_files_location,
        "config_json_path": config_json_path,
        "default_rowcount": default_rowcount,
        "csv_value_separator": csv_value_separator,
        "file_encoding": file_encoding,
        "file_line_ending": file_line_ending,
    }
    file_scope_kwargs = {
        "absolute_path": absolute_path,
        "file_size": file_size,
        "row_count": row_count,
    }
    return project_scope_kwargs, file_scope_kwargs


if __name__ == "__main__":
    KWARGS = parse_args()
    PROJECT_SCOPE_KWARGS = KWARGS[0]
    FILE_SCOPE_KWARGS = KWARGS[1]

    #OBJ = DummyFileGenerator()
    FOBJ = File(**PROJECT_SCOPE_KWARGS)
    FOBJ.generate_file(**FILE_SCOPE_KWARGS)
