"""
project_properties module
"""
import json
from typing import Optional

from dummy_file_generator.exceptions import DummyFileGeneratorException


class ProjectProperties:
    """
    ProjectProperties class
    """
    def __init__(self, **kwargs):
        self.project_name: str = kwargs["project_name"]
        self.header: bool = kwargs["header"]
        self.file_type: str = kwargs["file_type"]
        self.columns: list = kwargs["columns"]
        self.csv_value_separator: Optional[str] = kwargs["csv_value_separator"]
        self.csv_quoting: Optional[str] = kwargs["csv_quoting"]
        self.csv_quote_char: Optional[str] = kwargs["csv_quote_char"]
        self.csv_escape_char: Optional[str] = kwargs["csv_escape_char"]

        self._validate_project_properties()

    def _validate_project_properties(self) -> None:
        """
        simple config file validation method
        :return:
        """
        _column_name_list = [x.get("column_name") for x in self.columns]
        _data_file_list = [x.get("datafile") for x in self.columns]
        _column_len_list = [x.get("column_len") for x in self.columns]

        if self.file_type not in ("csv", "flat", "json"):
            raise DummyFileGeneratorException(
                f"Unknown file_type {self.file_type}, "
                f"supported options are csv or flat"
            )

        if not _column_name_list:
            raise DummyFileGeneratorException("No columns set in config")

        if any(x is None for x in _column_name_list):
            raise DummyFileGeneratorException("Not all columns set in config")

        if not _data_file_list:
            raise DummyFileGeneratorException("No datafile value set in config")

        if any(x is None for x in _data_file_list):
            raise DummyFileGeneratorException("Not all datafile values set in config")

        if not self.header and self.file_type in ("csv", "flat"):
            raise DummyFileGeneratorException(
                "No `header` value set in config for `csv` or `flat` file, supported options are `true` or `false`"
            )

        if self.header and self.file_type == "json":
            raise DummyFileGeneratorException(
                "The `header` value cannot be set in config for `json` file type"
            )

        if self.file_type == "csv" and not self.csv_value_separator:
            raise DummyFileGeneratorException(
                "No `csv_value_separator` value set in config for `csv` file type"
            )

        if self.file_type == "csv" and not self.csv_quoting:
            raise DummyFileGeneratorException(
                "Missing `csv_quoting` value for `csv` file type"
            )

        if (
            self.file_type == "csv"
            and self.csv_quoting != "NONE"
            and not self.csv_quote_char
        ):
            raise DummyFileGeneratorException(
                "If `csv_quoting` is not `NONE`, `csv_quote_char` must be set for `csv` file type"
            )

        if self.file_type == "flat" and not _column_len_list:
            raise DummyFileGeneratorException(
                "No `column_len` value set in config for `flat` file type"
            )

        if self.file_type == "flat" and any(x is None for x in _column_len_list):
            raise DummyFileGeneratorException(
                "Not all `column_len` values set in config for `flat` file type"
            )

    def __str__(self):
        return str(self)


def get_validated_project_properties_from_config_file(
    config_json_path: str, project_name: str
) -> ProjectProperties:
    """
    get validated project properties from config file function
    :param config_json_path:
    :param project_name:
    :return:
    """
    try:
        with open(config_json_path) as file:
            json_data = json.load(file)
    except FileNotFoundError as file_not_found_err:
        raise DummyFileGeneratorException(
            f"Cannot open {config_json_path}, "
            f"File Not Found error: {file_not_found_err}"
        )
    except json.JSONDecodeError as json_decode_err:
        raise DummyFileGeneratorException(
            f"Cannot load {config_json_path}, " f"JSON decode error: {json_decode_err}"
        )

    for project in json_data["project"]:
        if project["project_name"] == project_name:
            return ProjectProperties(
                **dict(
                    project_name=project_name,
                    header=project.get("header"),
                    file_type=project.get("file_type"),
                    columns=project.get("columns"),
                    csv_value_separator=project.get("csv_value_separator"),
                    csv_quoting=project.get("csv_quoting"),
                    csv_quote_char=project.get("csv_quote_char"),
                    csv_escape_char=project.get("csv_escape_char"),
                )
            )
        break
    else:
        raise DummyFileGeneratorException(
            f"Project {project_name} not found in {config_json_path}"
        )
