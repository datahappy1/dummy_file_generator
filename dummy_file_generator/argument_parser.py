"""
argument_parser module
"""
import argparse


def parse_args():
    """
    argparse based argument parsing function
    :return: kwargs
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-pn", "--projectname", type=str, required=True)
    parser.add_argument("-gp", "--generated_file_path", type=str, required=True)
    parser.add_argument("-fs", "--filesize", type=int, required=False)
    parser.add_argument("-rc", "--rowcount", type=int, required=False)
    parser.add_argument("-ll", "--logging_level", type=str, required=False)

    parser.add_argument("-cjp", "--config_json_path", type=str, required=False)
    parser.add_argument("-dfl", "--data_files_location", type=str, required=False)
    parser.add_argument("-drc", "--default_rowcount", type=int, required=False)
    parser.add_argument("-fen", "--file_encoding", type=str, required=False)
    parser.add_argument("-fle", "--file_line_ending", type=str, required=False)

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
