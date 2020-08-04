import csv

from dummy_file_generator.utils import QUOTING_MAP


class Writer(object):
    """Abstract class"""

    def setup_writer(self, file_handler, **kwargs):
        raise NotImplementedError("Derived classes should implement this.")

    def write_row(self, row):
        raise NotImplementedError("Derived classes should implement this.")


class CsvWriter(Writer):
    def setup_writer(self, file_handler, **kwargs):
        self.writer = csv.writer(file_handler,
                                 delimiter=kwargs.get('csv_value_separator'),
                                 quoting=QUOTING_MAP.get(kwargs.get('csv_quoting')),
                                 quotechar=kwargs.get('csv_quote_char'))


    def write_row(self, row):
        self.writer.writerow(row)


class FlatWriter(Writer):
    def setup_writer(self, file_handler, **kwargs):
        self.writer = file_handler

    def write_row(self, row):
        self.writer.write(row)


class Consumer(Writer):

    def __init__(self, arg):
        self.writer = arg()

    def setup_writer(self, file_handler, **kwargs):
        return self.writer.setup_writer(file_handler, **kwargs)

    def write_row(self, row):
        return self.writer.write_row(row)
