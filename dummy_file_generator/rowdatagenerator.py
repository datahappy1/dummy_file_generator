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

    def _get_value_for_row_from_column(self, column):
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
        return _column_values_list[randint(0, _column_values_list_item_count - 1)]

    def generate_header_row(self):
        """
        generate header row method
        :return:
        """
        return [x.get("column_name") for x in self.columns]

    def generate_body_row(self, **kwargs):
        """
        generate body row method
        :return:
        """
        row = []

        for column in self.columns:
            value = self._get_value_for_row_from_column(column=column)
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
        return whitespace_count * " "

    def __init__(self, data_files_contents, columns):
        self.data_files_contents = data_files_contents
        self.columns = columns

    def _get_value_for_row_from_column(self, column):
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
        return _column_values_list[randint(0, _column_values_list_item_count - 1)]

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

    def generate_body_row(self, **kwargs):
        """
        generate body row method
        :return:
        """
        row = []

        for column in self.columns:
            value = self._get_value_for_row_from_column(column=column)
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

    def _get_value_for_row_from_column(self, column):
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
        return _column_values_list[randint(0, _column_values_list_item_count - 1)]

    def generate_header_row(self):
        """
        generate header row method
        :return:
        """
        raise DummyFileGeneratorException(
            "Cannot generate header row in DictRowDataGenerator"
        )

    def generate_body_row(self, **kwargs):
        """
        generate body row method
        :return:
        """
        row = dict()

        def _set_row_data(cols, context_col=None):
            for column in cols:
                if isinstance(column.get("__array_columns"), list):
                    row[column["column_name"]] = []
                    _set_row_data(
                        cols=column["__array_columns"],
                        context_col=column["column_name"],
                    )
                    continue
                if column.get("columns"):
                    value = dict()
                    for nested_col in column.get("columns"):
                        value[
                            nested_col["column_name"]
                        ] = self._get_value_for_row_from_column(column=nested_col)
                else:
                    value = self._get_value_for_row_from_column(column=column)

                if context_col:
                    row[context_col].append(value)
                else:
                    row[column["column_name"]] = value

        _set_row_data(cols=self.columns)

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

    def generate_body_row(self, **kwargs):
        """
        generate body row factory method
        :return:
        """
        return self.generator.generate_body_row(**kwargs)
