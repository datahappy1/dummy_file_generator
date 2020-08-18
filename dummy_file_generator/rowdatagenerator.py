from random import randint

from dummy_file_generator.exceptions import DummyFileGeneratorException
from dummy_file_generator.utils import whitespace_generator


class CsvRowDataGenerator:
    def __init__(self, data_files_contents, columns, **kwargs):
        self.data_files_contents = data_files_contents
        self.columns = columns
        self.column_names = [x.get('column_name') for x in self.columns]

    def generate_header_row(self):
        return self.column_names

    def generate_body_row(self):
        row = []

        for column in self.columns:
            try:
                _column_values_list, _column_values_list_item_count = self.data_files_contents[column['datafile']]
            except AttributeError as attr_err:
                raise DummyFileGeneratorException(f'Cannot find corresponding data_file for '
                                                  f'column {column.get("column_name")}, '
                                                  f'Attribute Error: {attr_err}')

            value = _column_values_list[randint(0, _column_values_list_item_count - 1)]
            row.append(value)

        return row


class FlatRowDataGenerator:
    def __init__(self, data_files_contents, columns, **kwargs):
        self.data_files_contents = data_files_contents
        self.columns = columns
        self.column_names = [x.get('column_name') for x in self.columns]
        self.column_lengths = [x.get('column_len') for x in self.columns]
        self.file_line_ending = kwargs.get('file_line_ending')

    def generate_header_row(self):
        _header_row = []

        for _column_values_list, _column_length in zip(self.column_names,
                                                       self.column_lengths):
            _header_row.append(str(_column_values_list) +
                               whitespace_generator(_column_length - len(_column_values_list)))

        header_row = "".join(_header_row)

        return header_row

    def generate_body_row(self):
        row = []

        for column in self.columns:
            try:
                _column_values_list, _column_values_list_item_count = self.data_files_contents[column['datafile']]
                _whitespace_count = column.get('column_len')
            except AttributeError as attr_err:
                raise DummyFileGeneratorException(f'Cannot find corresponding data_file for '
                                                  f'column {column.get("column_name")}, '
                                                  f'Attribute Error: {attr_err}')
            value = _column_values_list[randint(0, _column_values_list_item_count - 1)]
            row.append(str(value) + whitespace_generator(_whitespace_count - len(value)))

        row = "".join(row)

        return row


class RowDataGenerator:
    def __init__(self, file_type, data_files_contents, columns, **kwargs):
        _mapped_generator_class = {
            "csv": CsvRowDataGenerator,
            "flat": FlatRowDataGenerator,
        }[file_type]

        self.generator = _mapped_generator_class(data_files_contents, columns, **kwargs)

    def generate_header_row(self):
        return self.generator.generate_header_row()

    def generate_body_row(self):
        return self.generator.generate_body_row()
