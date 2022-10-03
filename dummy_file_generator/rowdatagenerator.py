"""row data generator factory module"""
import logging
from random import randint

from dummy_file_generator.exceptions import DummyFileGeneratorException

logger = logging.getLogger(__name__)


class CsvRowDataGenerator:
    """
    csv row data generator implementation
    """

    def __init__(self, data_files_contents, columns):
        self.data_files_contents = data_files_contents
        self.columns = columns
        self.column_names = [x.get("column_name") for x in self.columns]

    def generate_header_row(self):
        """
        generate header row method
        :return:
        """
        return self.column_names

    def generate_body_row(self):
        """
        generate body row method
        :return:
        """
        row = []

        for column in self.columns:
            try:
                (
                    _column_values_list,
                    _column_values_list_item_count,
                ) = self.data_files_contents[column["datafile"]]
            except KeyError as key_err:
                raise DummyFileGeneratorException(
                    f"Cannot find corresponding data_file for "
                    f'column {column.get("column_name")}, '
                    f"Key Error: {key_err}"
                )

            value = _column_values_list[randint(0, _column_values_list_item_count - 1)]
            row.append(value)

        return row


class FlatRowDataGenerator:
    """
    flat row data generator implementation
    """

    @staticmethod
    def _whitespace_value_filler(whitespace_count):
        """
        whitespace value filler method
        :param whitespace_count:
        :return:
        """
        whitespace_char = " "
        return whitespace_count * whitespace_char

    def __init__(self, data_files_contents, columns):
        self.data_files_contents = data_files_contents
        self.columns = columns
        self.column_names = [x.get("column_name") for x in self.columns]
        self.column_lengths = [x.get("column_len") for x in self.columns]

    def generate_header_row(self):
        """
        generate header row method
        :return:
        """
        header_row = []

        for column in self.columns:
            whitespace_count = column["column_len"] - len(column["column_name"])
            header_row.append(
                column["column_name"]
                + FlatRowDataGenerator._whitespace_value_filler(whitespace_count)
            )

        return "".join(header_row)

    def generate_body_row(self):
        """
        generate body row method
        :return:
        """
        row = []

        for column in self.columns:
            try:
                (
                    _column_values_list,
                    _column_values_list_item_count,
                ) = self.data_files_contents[column["datafile"]]
            except KeyError as key_err:
                raise DummyFileGeneratorException(
                    f"Cannot find corresponding data_file for "
                    f'column {column.get("column_name")}, '
                    f"Key Error: {key_err}"
                )
            value = _column_values_list[randint(0, _column_values_list_item_count - 1)]
            whitespace_count = column["column_len"] - len(value)
            row.append(
                value + FlatRowDataGenerator._whitespace_value_filler(whitespace_count)
            )

        return "".join(row)


class DictRowDataGenerator:
    """
    dict row data generator implementation
    """

    def __init__(self, data_files_contents, columns):
        self.data_files_contents = data_files_contents
        self.columns = columns
        self.column_names = [x.get("column_name") for x in self.columns]
        self.column_lengths = [x.get("column_len") for x in self.columns]

    def generate_header_row(self):
        """
        generate header row method
        :return:
        """
        logger.info("DictRowDataGenerator cannot generate header row, skipping")
        pass

    def generate_body_row(self):
        """
        generate body row method
        :return:
        """
        row = dict()

        for column in self.columns:
            try:
                (
                    _column_values_list,
                    _column_values_list_item_count,
                ) = self.data_files_contents[column["datafile"]]
            except KeyError as key_err:
                raise DummyFileGeneratorException(
                    f"Cannot find corresponding data_file for "
                    f'column {column.get("column_name")}, '
                    f"Key Error: {key_err}"
                )
            value = _column_values_list[randint(0, _column_values_list_item_count - 1)]
            row[column['column_name']] = value

        return row


class RowDataGenerator:
    """
    row data generator factory
    """

    def __init__(self, file_type, data_files_contents, columns):
        _mapped_generator_class = {
            "csv": CsvRowDataGenerator,
            "flat": FlatRowDataGenerator,
            "json": DictRowDataGenerator,
        }[file_type]

        self.generator = _mapped_generator_class(data_files_contents, columns)

    def generate_header_row(self):
        """
        generate header row factory method
        :return:
        """
        return self.generator.generate_header_row()

    def generate_body_row(self):
        """
        generate body row factory method
        :return:
        """
        return self.generator.generate_body_row()
