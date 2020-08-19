"""writer factory module"""
import csv

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
                                 quoting=QUOTING_MAP.get(kwargs.get('csv_quoting')),
                                 quotechar=kwargs.get('csv_quote_char'),
                                 lineterminator=kwargs.get('file_line_ending'))

    def __repr__(self):
        return self

    def write_row(self, row):
        """
        write row method
        :param row:
        :return:
        """
        self.writer.writerow(row)


class FlatWriter:
    """
    flat writer implementation
    """
    def __init__(self, file_handler, **kwargs):
        self.writer = file_handler
        self.file_line_ending = kwargs.get('file_line_ending')

    def __repr__(self):
        return self

    def write_row(self, row):
        """
        write row method
        :param row:
        :return:
        """
        self.writer.write(row + self.file_line_ending)


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
        return self

    def write_row(self, row):
        """
        write row factory method
        :param row:
        :return:
        """
        self.writer.write_row(row)
