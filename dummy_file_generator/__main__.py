""" dummy file generator main runner """
import io
import json
import argparse
import logging

from datetime import datetime

from dummy_file_generator.exceptions import DummyFileGeneratorException
from dummy_file_generator.utils import get_path_from_project_sub_folder, \
    load_data_files_content, create_target_folder_if_not_exists
from dummy_file_generator.rowdatagenerator import RowDataGenerator
from dummy_file_generator.settings import DEFAULT_ROW_COUNT, FILE_ENCODING, \
    FILE_LINE_ENDING, LOGGING_LEVEL
from dummy_file_generator.writer import Writer

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


class DummyFileGenerator:
    """
    main project class
    """

    @staticmethod
    def _setup_logging(logging_level=None):
        """
        set logging levels for main function console output
        :param logging_level:
        :return:
        """
        LOGGER.setLevel(logging_level or LOGGING_LEVEL)

    def __init__(self, logging_level=None, **kwargs):
        data_files_location = kwargs.get('data_files_location') or \
                              get_path_from_project_sub_folder('data_files')
        config_json_path = kwargs.get('config_json_path') or \
                           get_path_from_project_sub_folder('configs',
                                                            'config.json')
        project_name = kwargs.get('project_name')
        if not project_name:
            raise DummyFileGeneratorException(f'Missing mandatory argument project_name')

        self.default_rowcount = kwargs.get('default_rowcount') or DEFAULT_ROW_COUNT
        self.data_files_contents = load_data_files_content(data_files_location=data_files_location)

        self.file_type = None
        self.header = None
        self.columns = dict()
        self.csv_file_props = {"csv_value_separator": None,
                               "csv_quoting": None,
                               "csv_quote_char": None,
                               "csv_escape_char": None}

        self._setup_logging(logging_level=logging_level)
        self._set_vars_from_config_file(config_json_path=config_json_path,
                                        project_name=project_name)
        self._validate_config_file_data()

    def __repr__(self):
        return str(id(self))

    def _set_vars_from_config_file(self, config_json_path, project_name):
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
                self.csv_file_props['csv_value_separator'] = project.get('csv_value_separator')
                self.csv_file_props['csv_quoting'] = project.get('csv_quoting')
                self.csv_file_props['csv_quote_char'] = project.get('csv_quote_char')
                self.csv_file_props['csv_escape_char'] = project.get('csv_escape_char')
                self.columns = project.get('columns')
                break
        else:
            raise DummyFileGeneratorException(f'Project {project_name} not found '
                                              f'in {config_json_path}')

    def _validate_config_file_data(self):
        """
        simple config file validation method
        :return:
        """
        _column_name_list = [x.get('column_name') for x in self.columns]
        _data_file_list = [x.get('datafile') for x in self.columns]
        _column_len_list = [x.get('column_len') for x in self.columns]

        if self.file_type not in ('csv', 'flat'):
            raise DummyFileGeneratorException(f'Unknown file_type {self.file_type}, '
                                              f'supported options are csv or flat')

        if not _column_name_list:
            raise DummyFileGeneratorException('No columns set in config')

        if any(x is None for x in _column_name_list):
            raise DummyFileGeneratorException('Not all columns set in config')

        if not _data_file_list:
            raise DummyFileGeneratorException('No datafile value set in config')

        if any(x is None for x in _data_file_list):
            raise DummyFileGeneratorException('Not all datafile values set in config')

        if not self.header:
            raise DummyFileGeneratorException('No header value set in config, '
                                              'supported options are true or false')

        if self.file_type == 'csv' and not self.csv_file_props.get('csv_value_separator'):
            raise DummyFileGeneratorException('No csv_value_separator value set in config')

        if self.file_type == 'csv' and not self.csv_file_props.get('csv_quoting'):
            raise DummyFileGeneratorException('Missing csv_quoting value')

        if self.file_type == 'csv' and self.csv_file_props.get('csv_quoting') != "NONE" and \
                not self.csv_file_props.get('csv_quote_char'):
            raise DummyFileGeneratorException('If csv_quoting is not "NONE", '
                                              'csv_quote_char must be set')

        if self.file_type == 'flat' and not _column_len_list:
            raise DummyFileGeneratorException('No column_len value set in config')

        if self.file_type == 'flat' and any(x is None for x in _column_len_list):
            raise DummyFileGeneratorException('Not all column_len values set in config')

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

        create_target_folder_if_not_exists(generated_file_path)

        with io.open(generated_file_path, 'w', encoding=file_encoding) \
                as output_file:
            execution_start_time = datetime.now()
            LOGGER.info('File %s processing started at %s', generated_file_path,
                        execution_start_time)

            writer = Writer(file_type=self.file_type,
                            file_handler=output_file,
                            **{"csv_value_separator": self.csv_file_props['csv_value_separator'],
                               "csv_quoting": self.csv_file_props['csv_quoting'],
                               "csv_quote_char": self.csv_file_props['csv_quote_char'],
                               "csv_escape_char": self.csv_file_props['csv_escape_char'],
                               "file_line_ending": file_line_ending}
                            )

            row_data_generator = RowDataGenerator(file_type=self.file_type,
                                                  data_files_contents=self.data_files_contents,
                                                  columns=self.columns)

            if bool(self.header):
                writer.write_row(row_data_generator.generate_header_row())

            rows_written = 0
            while output_file.tell() < file_size or rows_written < row_count:
                writer.write_row(row_data_generator.generate_body_row())
                rows_written += 1

                if divmod(rows_written, 10000)[1] == 1 and rows_written > 1:
                    LOGGER.info('%s rows written', rows_written)

            execution_end_time = datetime.now()
            _duration = (execution_end_time - execution_start_time).seconds
            duration = str(_duration / 60) + ' min.' if _duration > 1000 \
                else str(_duration) + ' sec.'

            LOGGER.info('File %s processing finished at %s', generated_file_path,
                        execution_end_time)
            LOGGER.info('%s kB file with %s rows written in %s', output_file.tell() / 1024,
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
