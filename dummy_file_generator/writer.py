"""writer factory module"""
import csv

from dummy_file_generator.exceptions import DummyFileGeneratorException
from dummy_file_generator.utils import get_map_value


QUOTING_MAP = {"NONE": csv.QUOTE_NONE,
               "MINIMAL": csv.QUOTE_MINIMAL,
               "NONNUMERIC": csv.QUOTE_NONNUMERIC,
               "ALL": csv.QUOTE_ALL}


class CsvWriter:
    """
    csv writer implementation
    """
    def __init__(self, file_handler, **kwargs):
        self.writer = csv.writer(file_handler,
                                 delimiter=kwargs.get('csv_value_separator'),
                                 quoting=get_map_value(QUOTING_MAP, kwargs['csv_quoting']),
                                 quotechar=kwargs.get('csv_quote_char'),
                                 escapechar=kwargs.get('csv_escape_char'),
                                 lineterminator=kwargs.get('file_line_ending'))

    def __repr__(self):
        return str(self.writer)

    def write_row(self, row):
        """
        write row method
        :param row:
        :return:
        """
        try:
            self.writer.writerow(row)
        except csv.Error as csv_err:
            raise DummyFileGeneratorException(f'csv writer error : {csv_err}')


class FlatWriter:
    """
    flat writer implementation
    """
    def __init__(self, file_handler, **kwargs):
        self.writer = file_handler
        self.file_line_ending = kwargs.get('file_line_ending')

    def __repr__(self):
        return str(self.writer)

    def write_row(self, row):
        """
        write row method
        :param row:
        :return:
        """
        try:
            self.writer.write(row + self.file_line_ending)
        except Exception as exc:
            raise DummyFileGeneratorException(f'flat writer error : {exc}')

class Writer:
    """
    writer factory
    """
    def __init__(self, file_type, file_handler, **kwargs):
        _mapped_writer_class = {
            "csv": CsvWriter,
            "flat": FlatWriter,
        }[file_type]

        self.writer = _mapped_writer_class(file_handler, **kwargs)

    def __repr__(self):
        return str(self.writer)

    def write_row(self, row):
        """
        write row factory method
        :param row:
        :return:
        """
        self.writer.write_row(row)
