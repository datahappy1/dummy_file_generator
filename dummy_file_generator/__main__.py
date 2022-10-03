""" dummy file generator main """
import io
import logging
from datetime import datetime

from dummy_file_generator.argument_parser import parse_args
from dummy_file_generator.exceptions import DummyFileGeneratorException
from dummy_file_generator.project_properties import (
    get_validated_project_properties_from_config_file,
)
from dummy_file_generator.rowdatagenerator import RowDataGenerator
from dummy_file_generator.settings import (
    DEFAULT_ROW_COUNT,
    FILE_ENCODING,
    FILE_LINE_ENDING,
    LOGGING_LEVEL,
)
from dummy_file_generator.file_path import (
    get_path_from_project_sub_folder,
    create_target_folder_if_not_exists,
)
from dummy_file_generator.data_files import load_data_files_content
from dummy_file_generator.writer import Writer

logging.basicConfig()
logger = logging.getLogger(__name__)


class DummyFileGenerator:
    """
    main project class
    """

    @staticmethod
    def _calculate_duration(start_time, end_time):
        _duration = (end_time - start_time).seconds
        return (
            str(_duration / 60) + " min."
            if _duration > 1000
            else str(_duration) + " sec."
        )

    def __init__(self, logging_level=None, **kwargs):
        logger.setLevel(logging_level or LOGGING_LEVEL)

        data_files_location = kwargs.get(
            "data_files_location"
        ) or get_path_from_project_sub_folder("data_files")

        config_json_path = kwargs.get(
            "config_json_path"
        ) or get_path_from_project_sub_folder("configs", "config.json")

        project_name = kwargs.get("project_name")
        if not project_name:
            raise DummyFileGeneratorException(
                f"Missing mandatory argument project_name"
            )

        self.default_rowcount = kwargs.get("default_rowcount") or DEFAULT_ROW_COUNT

        self.properties = get_validated_project_properties_from_config_file(
            config_json_path=config_json_path, project_name=project_name
        )

        self.data_files_contents = load_data_files_content(
            data_files_location=data_files_location
        )

    def __repr__(self):
        return str(id(self))

    def write_output_file(self, **file_scope_kwargs):
        """
        write output method
        :return:
        """
        generated_file_path = file_scope_kwargs.get("generated_file_path")
        row_count = file_scope_kwargs.get("row_count") or 0
        file_size = file_scope_kwargs.get("file_size") or 0
        file_encoding = file_scope_kwargs.get("file_encoding") or FILE_ENCODING
        file_line_ending = file_scope_kwargs.get("file_line_ending") or FILE_LINE_ENDING

        if not generated_file_path:
            raise DummyFileGeneratorException(
                "Missing mandatory argument generated_file_path"
            )

        if file_size > 0:
            file_size = file_size * 1024

        if row_count == 0 and file_size == 0:
            # use default row_count in case no row counts
            # and no file size args provided:
            row_count = self.default_rowcount

        create_target_folder_if_not_exists(generated_file_path)

        with io.open(generated_file_path, "w", encoding=file_encoding) as output_file:
            execution_start_time = datetime.now()

            logger.info(
                "File %s processing started at %s",
                generated_file_path,
                execution_start_time,
            )

            writer = Writer(
                file_type=self.properties.file_type,
                file_handler=output_file,
                **{
                    "csv_value_separator": self.properties.csv_value_separator,
                    "csv_quoting": self.properties.csv_quoting,
                    "csv_quote_char": self.properties.csv_quote_char,
                    "csv_escape_char": self.properties.csv_escape_char,
                    "file_line_ending": file_line_ending,
                },
            )

            row_data_generator = RowDataGenerator(
                file_type=self.properties.file_type,
                data_files_contents=self.data_files_contents,
                columns=self.properties.columns,
            )

            if self.properties.header:
                writer.write_row(row_data_generator.generate_header_row())

            rows_written = 0
            while output_file.tell() < file_size or rows_written < row_count:
                writer.write_row(row_data_generator.generate_body_row())
                rows_written += 1

                if divmod(rows_written, 10000)[1] == 1 and rows_written > 1:
                    logger.info("%s rows written", rows_written)

            execution_end_time = datetime.now()

            duration = DummyFileGenerator._calculate_duration(
                start_time=execution_start_time, end_time=execution_end_time
            )

            logger.info(
                "File %s processing finished at %s",
                generated_file_path,
                execution_end_time,
            )
            logger.info(
                "%s kB file with %s rows written in %s",
                output_file.tell() / 1024,
                rows_written,
                duration,
            )


def main():
    """
    main entrypoint function
    :return:
    """
    parsed_args = parse_args()
    dfg = DummyFileGenerator(parsed_args[0], **parsed_args[1])
    dfg.write_output_file(**parsed_args[2])


if __name__ == "__main__":
    main()
