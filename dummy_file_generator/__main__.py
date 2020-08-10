""" dummy file generator main runner """
import io
import os
import json
import csv
import argparse
import logging

from random import randint
from datetime import datetime

from dummy_file_generator.utils import add_quotes_to_list_items, \
    whitespace_generator, get_data_file_content_list_with_item_count
from dummy_file_generator.settings import DEFAULT_ROW_COUNT, FILE_ENCODING, \
    FILE_LINE_ENDING, LOGGING_LEVEL

logging.basicConfig()
LOGGER = logging.getLogger(__name__)

QUOTING_MAP = {"NONE": csv.QUOTE_NONE,
               "MINIMAL": csv.QUOTE_MINIMAL,
               "NONNUMERIC": csv.QUOTE_NONNUMERIC,
               "ALL": csv.QUOTE_ALL}


class CsvWriter:
    def __init__(self, file_handler, **kwargs):
        self.writer = csv.writer(file_handler,
                                 delimiter=kwargs.get('csv_value_separator'),
                                 quoting=QUOTING_MAP.get(kwargs.get('csv_quoting')),
                                 quotechar=kwargs.get('csv_quote_char'))

    def write_row(self, row):
        self.writer.writerow(row)


class FlatWriter:
    def __init__(self, file_handler, **kwargs):
        self.writer = file_handler

    def write_row(self, row):
        self.writer.write(row)


class Writer:
    def __init__(self, file_handler, file_type, **kwargs):
        _mapped_writer = {
            "csv": CsvWriter,
            "flat": FlatWriter,
        }[file_type]

        self.writer = _mapped_writer(file_handler, **kwargs)

    def write_row(self, row):
        self.writer.write_row(row)


class CsvRowGenerator:
    def __init__(self):
        pass


class FlatRowGenerator:
    def __init__(self):
        pass


class RowGenerator:
    def __init__(self):
        pass


class DummyFileGeneratorException(Exception):
    """
    dummy file generator custom exception type
    """


class DummyFileGenerator:
    """
    main project class
    """

    @staticmethod
    def _get_path_from_project_subfolder_loc(sub_folder, filename=''):
        """
        returns file path or folder path based on the provided args
        from the dummy_file_generator/dummy_file_generator location
        :param sub_folder:
        :param filename:
        :return:
        """
        current_dir = os.path.dirname(__file__)
        current_dir_path = os.path.join(current_dir)
        return os.sep.join([current_dir_path, sub_folder, filename])

    def __init__(self, logging_level=None, **kwargs):
        data_files_location = kwargs.get('data_files_location') or \
                              DummyFileGenerator._get_path_from_project_subfolder_loc('data_files')
        config_json_path = kwargs.get('config_json_path') or \
                           DummyFileGenerator._get_path_from_project_subfolder_loc('configs',
                                                                                   'config.json')
        project_name = kwargs.get('project_name')

        if not project_name:
            raise DummyFileGeneratorException(f'Missing mandatory argument project_name')

        self.default_rowcount = kwargs.get('default_rowcount') or DEFAULT_ROW_COUNT

        self.file_type = None
        self.header = None

        self.csv_file_properties = {"csv_value_separator": None,
                                    "csv_quoting": None,
                                    "csv_quote_char": None}

        self.column_name_list = []
        self.column_len_list = []
        self.data_file_list = []

        self._setup_logging(logging_level=logging_level)
        self._set_vars_from_data_files_content(data_files_location=data_files_location)
        self._read_config_file(config_json_path=config_json_path, project_name=project_name)
        self._validate_config_file_data()

    def __repr__(self):
        return self

    @staticmethod
    def _setup_logging(logging_level=None):
        """
        set logging levels for main function console output
        :param logging_level:
        :return:
        """
        LOGGER.setLevel(logging_level or LOGGING_LEVEL)

    @staticmethod
    def _create_target_folder_if_not_exists(absolute_path):
        """
        method creating the target folder if it does not exist
        :param absolute_path:
        :return:
        """
        if not os.path.exists(os.path.dirname(absolute_path)):
            try:
                os.makedirs(os.path.dirname(absolute_path))
                LOGGER.info('Target folder not existing, created %s',
                            os.path.dirname(absolute_path))
            except OSError as os_err:
                raise DummyFileGeneratorException(f'Cannot create target folder, '
                                                  f'OSError: {os_err}')

    def _set_vars_from_data_files_content(self, data_files_location):
        """
        method setting variables from data_files, variable names have
        "data_file_" prefix to avoid issue in case the data_file name
        would collide with a already existing class variable
        :param data_files_location:
        :return:
        """
        try:
            data_files = [f for f in os.listdir(data_files_location) if
                          os.path.isfile(os.path.join(data_files_location, f))
                          and str(f).endswith('.txt')]
        except OSError as os_err:
            raise DummyFileGeneratorException(f'Cannot list data_files, '
                                              f'OSError: {os_err}')

        if not data_files:
            raise DummyFileGeneratorException(f'No data_files in {data_files_location}')

        for data_file in data_files:
            setattr(self, 'data_file_' + data_file.replace('.txt', ''),
                    get_data_file_content_list_with_item_count(data_file,
                                                               data_files_location=
                                                               data_files_location))

    def _read_config_file(self, config_json_path, project_name):
        """
        read config json file method
        :return:
        """
        try:
            with open(config_json_path) as file:
                json_data = json.load(file)
        except FileNotFoundError as file_not_found_err:
            raise DummyFileGeneratorException(f'Cannot open {config_json_path}, '
                                              f'File Not Found error: {file_not_found_err}')
        except json.JSONDecodeError as json_decode_err:
            raise DummyFileGeneratorException(f'Cannot load {config_json_path}, '
                                              f'JSON decode error: {json_decode_err}')

        for project in json_data['project']:
            if project['project_name'] == project_name:
                self.header = project.get('header')
                self.file_type = project.get('file_type')
                self.csv_file_properties['csv_value_separator'] = project.get('csv_value_separator')
                self.csv_file_properties['csv_quoting'] = project.get('csv_quoting')
                self.csv_file_properties['csv_quote_char'] = project.get('csv_quote_char')

                for column in project.get('columns'):
                    self.column_name_list.append(column.get('column_name'))
                    self.data_file_list.append(str(column.get('datafile')).replace('.txt', ''))
                    self.column_len_list.append(column.get('column_len'))
                break
        else:
            raise DummyFileGeneratorException(f'Project {project_name} not found '
                                              f'in {config_json_path}')

    def _validate_config_file_data(self):
        """
        simple config file validation method
        :return:
        """
        if self.file_type not in ('csv', 'flat'):
            raise DummyFileGeneratorException(f'Unknown file_type {self.file_type}, '
                                              f'supported options are csv or flat')

        if not self.column_name_list:
            raise DummyFileGeneratorException('No columns set in config')

        if any(x is None for x in self.column_name_list):
            raise DummyFileGeneratorException('Not all columns set in config')

        if not self.data_file_list:
            raise DummyFileGeneratorException('No datafile value set in config')

        if any(x is None for x in self.data_file_list):
            raise DummyFileGeneratorException('Not all datafile values set in config')

        if not self.header:
            raise DummyFileGeneratorException('No header value set in config, '
                                              'supported options are true or false')

        if self.file_type == 'csv' and not self.csv_file_properties.get('csv_value_separator'):
            raise DummyFileGeneratorException('No csv_value_separator value set in config')

        if self.file_type == 'csv' and \
                self.csv_file_properties.get('csv_quoting') not in QUOTING_MAP.keys():
            raise DummyFileGeneratorException('Invalid or missing csv_quoting value')

        if self.file_type == 'csv' and self.csv_file_properties.get('csv_quoting') != "NONE" and \
                not self.csv_file_properties.get('csv_quote_char'):
            raise DummyFileGeneratorException('If csv_quoting is not "NONE", csv_quote_char must be set')

        if self.file_type == 'flat' and not self.column_len_list:
            raise DummyFileGeneratorException('No column_len value set in config')

        if self.file_type == 'flat' and any(x is None for x in self.column_len_list):
            raise DummyFileGeneratorException('Not all column_len values set in config')

    @staticmethod
    def _generate_csv_header_row(columns):
        """
        csv row header
        :param columns:
        :return: csv row header
        """
        return columns

    @staticmethod
    def _generate_flat_header_row(columns, column_lengths, file_line_ending):
        """
        flat row header
        :param columns:
        :param column_lengths:
        :param file_line_ending:
        :return: flat row header
        """
        header_row = []

        for i, j in zip(columns, column_lengths):
            if len(i) > j:
                LOGGER.error('Header value %s is longer then expected column length '
                             'set in config.json file!', i)
            else:
                header_row.append(str(i) + whitespace_generator(j - len(i)))
        header_row = "".join(header_row)

        return header_row + file_line_ending

    def _generate_csv_body_row(self, columns):
        """
        method for generating csv output data row
        :param columns:
        :return: output csv data row
        """
        row = []

        for column in columns:
            column = column.strip("'")
            try:
                _val, _len = DummyFileGenerator.__getattribute__(self, 'data_file_' + column)
            except AttributeError as attr_err:
                raise DummyFileGeneratorException(f'Cannot find corresponding data_file for '
                                                  f'column {column}, Attribute Error: {attr_err}')

            value = _val[randint(0, _len)]
            row.append(value)

        return row

    def _generate_flat_body_row(self, columns, column_lengths, file_line_ending):
        """
        method for generating flat output data row
        :param columns:
        :param column_lengths:
        :param file_line_ending:
        :return: output flat data row
        """
        columns = add_quotes_to_list_items(columns)
        column_lengths = add_quotes_to_list_items(column_lengths)
        row = []

        for index, column in enumerate(columns):
            column = column.strip("'")
            whitespace = int(column_lengths[index])
            try:
                _val, _len = DummyFileGenerator.__getattribute__(self, 'data_file_' + column)
            except AttributeError as attr_err:
                raise DummyFileGeneratorException(f'Cannot find corresponding data_file for '
                                                  f'column {column}, Attribute Error: {attr_err}')

            value = _val[randint(0, _len)]
            if whitespace < len(value):
                LOGGER.error('Column value %s is longer then expected '
                             'column length set in config.json file!', value)
            value = value + whitespace_generator(whitespace - len(value))
            row.append(value)
        row = ''.join(row)

        return row + file_line_ending

    def write_output_file(self, **file_scope_kwargs):
        """
        write output method
        :return:
        """
        generated_file_path = file_scope_kwargs.get('generated_file_path')
        row_count = file_scope_kwargs.get('row_count') or 0
        file_size = file_scope_kwargs.get('file_size') or 0
        file_encoding = file_scope_kwargs.get('file_encoding') or FILE_ENCODING
        file_line_ending = file_scope_kwargs.get('file_line_ending') or FILE_LINE_ENDING

        if not generated_file_path:
            raise DummyFileGeneratorException('Missing mandatory argument generated_file_path')

        if file_size > 0:
            file_size = file_size * 1024

        if row_count == 0 and file_size == 0:
            # use default row_count in case no row counts
            # and no file size args provided:
            row_count = self.default_rowcount

        self._create_target_folder_if_not_exists(generated_file_path)

        with io.open(generated_file_path, 'w', encoding=file_encoding, newline=file_line_ending) \
                as output_file:
            execution_start_time = datetime.now()
            LOGGER.info('File %s processing started at %s', generated_file_path,
                        execution_start_time)

            writer = Writer(file_handler=output_file,
                            file_type=self.file_type,
                            **
                            {"csv_value_separator": self.csv_file_properties['csv_value_separator'],
                             "csv_quoting": self.csv_file_properties['csv_quoting'],
                             "csv_quote_char": self.csv_file_properties['csv_quote_char']}
                            )

            if bool(self.header):
                if self.file_type == "csv":
                    writer.write_row(self._generate_csv_header_row(self.column_name_list))

                elif self.file_type == "flat":
                    writer.write_row(self._generate_flat_header_row(self.column_name_list,
                                                                    self.column_len_list,
                                                                    file_line_ending))

            rows_written = 0
            while output_file.tell() < file_size or rows_written < row_count:
                if self.file_type == "csv":
                    writer.write_row(self._generate_csv_body_row(self.data_file_list))

                elif self.file_type == "flat":
                    writer.write_row(self._generate_flat_body_row(self.data_file_list,
                                                                  self.column_len_list,
                                                                  file_line_ending))

                rows_written += 1

                if divmod(rows_written, 10000)[1] == 1 and rows_written > 1:
                    LOGGER.info('%s rows written', rows_written)

            execution_end_time = datetime.now()
            output_file_size = output_file.tell()
            _duration = (execution_end_time - execution_start_time).seconds
            duration = str(_duration / 60) + ' min.' if _duration > 1000 \
                else str(_duration) + ' sec.'

            LOGGER.info('File %s processing finished at %s', generated_file_path,
                        execution_end_time)
            LOGGER.info('%s kB file with %s rows written in %s', output_file_size / 1024,
                        rows_written, duration)


def parse_args():
    """
    argparse based argument parsing function
    :return: kwargs
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-pn', '--projectname', type=str, required=True)
    parser.add_argument('-gp', '--generated_file_path', type=str, required=True)
    parser.add_argument('-fs', '--filesize', type=int, required=False)
    parser.add_argument('-rc', '--rowcount', type=int, required=False)
    parser.add_argument('-ll', '--logging_level', type=str, required=False)

    parser.add_argument('-cjp', '--config_json_path', type=str, required=False)
    parser.add_argument('-dfl', '--data_files_location', type=str, required=False)
    parser.add_argument('-drc', '--default_rowcount', type=int, required=False)
    parser.add_argument('-fen', '--file_encoding', type=str, required=False)
    parser.add_argument('-fle', '--file_line_ending', type=str, required=False)

    parsed = parser.parse_args()

    project_name = parsed.projectname
    generated_file_path = parsed.generated_file_path
    file_size = parsed.filesize
    row_count = parsed.rowcount
    logging_level = parsed.logging_level
    config_json_path = parsed.config_json_path
    data_files_location = parsed.data_files_location
    default_rowcount = parsed.default_rowcount
    file_encoding = parsed.file_encoding
    file_line_ending = parsed.file_line_ending

    project_scope_kwargs = {
        "project_name": project_name,
        "data_files_location": data_files_location,
        "config_json_path": config_json_path,
        "default_rowcount": default_rowcount,
    }
    file_scope_kwargs = {
        "generated_file_path": generated_file_path,
        "file_size": file_size,
        "row_count": row_count,
        "file_encoding": file_encoding,
        "file_line_ending": file_line_ending,
    }
    return logging_level, project_scope_kwargs, file_scope_kwargs


if __name__ == "__main__":
    PARSED_ARGS = parse_args()
    DFG = DummyFileGenerator(PARSED_ARGS[0], **PARSED_ARGS[1])
    DFG.write_output_file(**PARSED_ARGS[2])
