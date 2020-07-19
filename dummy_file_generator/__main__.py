""" dummy file generator main runner """
import io
import os
import json
import argparse
import logging

from random import randint
from datetime import datetime

from dummy_file_generator.utils import add_quotes_to_list_items, \
    whitespace_generator, get_data_file_content_list_with_item_count
from dummy_file_generator.settings import DEFAULT_ROW_COUNT, FILE_ENCODING, \
    FILE_LINE_ENDING, CSV_VALUE_SEPARATOR, LOGGING_LEVEL


class DummyFileGeneratorException(Exception):
    """
    dummy file generator custom exception type
    """


class DummyFileGenerator:
    """
    main project class
    """

    @staticmethod
    def _get_default_config_json_file_path():
        """
        returns default config.json file path
        :return:
        """
        return os.sep.join([os.path.join(os.path.dirname(__file__)), 'configs', 'config.json'])

    def __init__(self, logging_level=None, **kwargs):
        data_files_location = kwargs.get('data_files_location')
        config_json_path = kwargs.get('config_json_path') or \
                           DummyFileGenerator._get_default_config_json_file_path()
        project_name = kwargs.get('project_name')
        self.file_type = kwargs.get('file_type')
        self.column_name_list = []
        self.column_len_list = []
        self.data_file_list = []
        self.header = None
        self.logger = None

        self._setup_logging(logging_level=logging_level)
        self._set_vars_from_data_files_content(data_files_location=data_files_location)
        self._read_config_file(config_json_path=config_json_path, project_name=project_name)
        self._validate_config_file()

    def _setup_logging(self, logging_level=None):
        # set logging levels for main function console output
        logging.basicConfig(level=logging_level or LOGGING_LEVEL)
        self.logger = logging.getLogger(__name__)

    def _set_vars_from_data_files_content(self, data_files_location):
        data_files = [f for f in os.listdir(data_files_location) if
                      os.path.isfile(os.path.join(data_files_location, f))
                      and str(f).endswith('.txt')]

        for data_file in data_files:
            setattr(self, 'data_file_' + data_file.replace('.txt', ''),
                    get_data_file_content_list_with_item_count(data_file,
                                                               data_files_location=
                                                               data_files_location))

    def _read_config_file(self, config_json_path, project_name):
        """
        read config json file function
        :return:
        """
        with open(config_json_path) as file:
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
            raise DummyFileGeneratorException(f'Project {project_name} not found in config.json')

    def _validate_config_file(self):
        if self.file_type not in ('csv', 'flat'):
            raise DummyFileGeneratorException(f'Unknown file_type {self.file_type}, '
                                              'supported options are csv or flat')

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
            _val, _len = DummyFileGenerator.__getattribute__(self, 'data_file_' + column)
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
            _val, _len = DummyFileGenerator.__getattribute__(self, 'data_file_' + column)
            value = _val[randint(0, _len)]
            if whitespace < len(value):
                self.logger.error('Column value %s is longer then expected '
                                  'column length set in config.json file!', value)
            value = value + whitespace_generator(whitespace - len(value))
            row.append(value)
        row = ''.join(row)
        return row

    def _create_target_folder(self, absolute_path):
        if not os.path.exists(os.path.dirname(absolute_path)):
            try:
                os.makedirs(os.path.dirname(absolute_path))
                self.logger.info('Target folder not existing, created %s',
                                 os.path.dirname(absolute_path))
            except OSError as os_err:
                raise DummyFileGeneratorException(f'Cannot create target folder {os_err}')

    def write_output_file(self, **file_scope_kwargs):
        """
        write output function
        :return:
        """
        absolute_path = file_scope_kwargs['absolute_path']
        row_count = file_scope_kwargs.get('row_count') or 0
        file_size = file_scope_kwargs.get('file_size') * 1024 or 0
        file_encoding = file_scope_kwargs.get('file_encoding') or FILE_ENCODING
        file_line_ending = file_scope_kwargs.get('file_line_ending') or FILE_LINE_ENDING
        csv_value_separator = file_scope_kwargs.get('csv_value_separator') or CSV_VALUE_SEPARATOR

        if row_count == 0 and file_size == 0:
            # use default row_count from settings.py in case no row counts
            # and no file size args provided:
            row_count = DEFAULT_ROW_COUNT

        self._create_target_folder(absolute_path)

        with io.open(absolute_path, 'w', encoding=file_encoding) as output_file:
            execution_start_time = datetime.now()
            self.logger.info('File %s processing started at %s', absolute_path,
                             execution_start_time)

            if bool(self.header):
                if self.file_type == "csv":
                    output_file.write(self.csv_row_header(self.column_name_list,
                                                          csv_value_separator)
                                      + file_line_ending)

                elif self.file_type == "flat":
                    output_file.write(self.flat_row_header(self.column_name_list,
                                                           self.column_len_list)
                                      + file_line_ending)

            _rows_written = 0
            while output_file.tell() < file_size or _rows_written < row_count:
                row = None
                if self.file_type == "csv":
                    row = self.csv_row_output(self.data_file_list, csv_value_separator)
                elif self.file_type == "flat":
                    row = self.flat_row_output(self.data_file_list, self.column_len_list)

                output_file.write(row + file_line_ending)

                _rows_written += 1

                if divmod(_rows_written, 10000)[1] == 1 and _rows_written > 1:
                    self.logger.info('%s rows written', _rows_written)

            # to get the file_size even when only row_count arg used
            _output_file_size = output_file.tell()

            execution_end_time = datetime.now()
            duration = (execution_end_time - execution_start_time).seconds
            duration = str(duration / 60) + ' min.' if duration > 1000 else str(duration) + ' sec.'

            self.logger.info('File %s processing finished at %s', absolute_path,
                             execution_end_time)
            self.logger.info('%s kB file with %s rows written in %s', _output_file_size / 1024,
                             _rows_written, duration)


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
        "data_files_location": data_files_location,
        "config_json_path": config_json_path,
        "default_rowcount": default_rowcount,
    }
    file_scope_kwargs = {
        "absolute_path": absolute_path,
        "file_size": file_size,
        "row_count": row_count,
        "file_encoding": file_encoding,
        "file_line_ending": file_line_ending,
        "csv_value_separator": csv_value_separator,
    }
    return logging_level, project_scope_kwargs, file_scope_kwargs


if __name__ == "__main__":
    PARSED_ARGS = parse_args()
    DFG = DummyFileGenerator(PARSED_ARGS[0], **PARSED_ARGS[1])
    DFG.write_output_file(**PARSED_ARGS[2])
