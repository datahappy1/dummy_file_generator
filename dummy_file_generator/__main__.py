""" dummy file generator main runner """
import argparse
import json
import os
import io
import logging

from datetime import datetime
from dummy_file_generator.lib.flat_writer import flat_row_header, flat_row_output
from dummy_file_generator.lib.csv_writer import csv_row_header, csv_row_output
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
        for key, value in kwargs.items():
            setattr(self, key, value)

    def read_config(self):
        """
        read config json file function
        :return:
        """
        project_name = self.project_name  # pylint: disable=no-member
        config_path = os.sep.join([os.path.join(os.path.dirname(__file__)),
                                   'configurables', 'config.json'])

        with open(config_path) as file:
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
                raise ValueError("No such project found in config.json")

    def write_output(self):
        """
        write output function
        :return:
        """
        if not os.path.exists(os.path.dirname(self.absolute_path)):  # pylint: disable=no-member
            os.makedirs(os.path.dirname(self.absolute_path))  # pylint: disable=no-member

        column_name_list = self.column_name_list
        column_len_list = self.column_len_list
        data_file_list = self.data_file_list
        output_file_size = self.file_size * 1024  # pylint: disable=no-member
        row_count = self.row_count  # pylint: disable=no-member
        output_file_name = self.absolute_path  # pylint: disable=no-member
        if row_count == 0 and output_file_size == 0:
            # use default row_count from settings.py in case no row counts
            # and no file size args provided:
            row_count = DEFAULT_ROW_COUNT

        with io.open(output_file_name, 'w', encoding=FILE_ENCODING) as output_file:
            execution_start_time = datetime.now()
            logging.info('File %s processing started at %s', output_file_name, execution_start_time)

            if bool(self.header):
                if self.file_type == "csv":
                    output_file.write(csv_row_header(column_name_list, CSV_VALUE_SEPARATOR)
                                      + FILE_LINE_ENDING)
                elif self.file_type == "flat":
                    output_file.write(flat_row_header(column_name_list, column_len_list)
                                      + FILE_LINE_ENDING)

            iterator = 1
            while output_file.tell() < output_file_size or iterator < row_count:
                if self.file_type == "csv":
                    row = csv_row_output(data_file_list, CSV_VALUE_SEPARATOR)
                elif self.file_type == "flat":
                    row = flat_row_output(data_file_list, column_len_list)
                output_file.write(row + FILE_LINE_ENDING)
                iterator += 1

                if divmod(iterator, 10000)[1] == 1:
                    logging.info('%s rows written', iterator - 1)

            # to get the file_size even when only row_count arg used
            output_file_size = output_file.tell()
            output_file.close()

            execution_end_time = datetime.now()
            duration = (execution_end_time - execution_start_time).seconds
            duration = str(duration / 60) + ' min.' if duration > 1000 else str(duration) + ' sec.'

            logging.info('File %s processing finished at %s\n '
                         '%s kB file with %s rows written in %s',
                         output_file_name, execution_end_time,
                         output_file_size / 1024, iterator, duration)

    def main(self):
        """
        main function
        :return:
        """
        # set logging levels for main function console output
        logging.getLogger().setLevel(logging.INFO)

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

    parser.add_argument('-cjl', '--config_json_location', type=str, required=False, default=None)
    parser.add_argument('-drc', '--default_rowcount', type=int, required=False, default=100)
    parser.add_argument('-fen', '--file_encoding', type=str, required=False, default="utf8")
    parser.add_argument('-fle', '--file_line_ending', type=str, required=False, default="\n")
    parser.add_argument('-cvs', '--csv_value_separator', type=str, required=False, default="|")

    parsed = parser.parse_args()

    project_name = parsed.projectname
    file_size = parsed.filesize
    row_count = parsed.rowcount
    absolute_path = parsed.absolutepath

    config_json_location = parsed.config_json_location
    default_rowcount = parsed.default_rowcount
    file_encoding = parsed.file_encoding
    file_line_ending = parsed.file_line_ending
    csv_value_separator = parsed.csv_value_separator

    kwargs = {"project_name": project_name, "absolute_path": absolute_path,
              "file_size": file_size, "row_count": row_count,
              "config_json_location": config_json_location,
              "settings_override":{"default_rowcount": default_rowcount,
                                   "file_encoding": file_encoding,
                                   "file_line_ending": file_line_ending,
                                   "csv_value_separator": csv_value_separator}
              }

    return kwargs


if __name__ == "__main__":
    kwargs = args()
    obj = DummyFileGenerator(**kwargs)
    DummyFileGenerator.main(obj)
