import logging
import sys


def whitespace_generator(i):
    if int(i):
        return i * ' '
    else:
        logging.error(f'whitespace_generator error - variable i is not integer')
        sys.exit(1)


def list_to_stmt(statement, add_plus_sign, add_comma):
    if bool(add_plus_sign) and bool(add_comma):
        return str(statement).replace("'", "").replace("),", ")+','+").strip('[]')
    if bool(add_plus_sign) and not bool(add_comma):
        return str(statement).replace("'", "").replace("),", ")+").strip('[]')
    else:
        return str(statement).replace("'", "").strip('[]')


class Headers:
    @staticmethod
    def return_csv_header(column_list):
        return list_to_stmt(statement=column_list, add_plus_sign=False, add_comma=False).replace(' ', '') + '\n'

    @staticmethod
    def return_flat_header(column_name_list, column_len_list):
        header_row = []

        for i, j in zip(column_name_list, column_len_list):
            if len(i) > j:
                logging.error(f'Header value for {i} is longer ({len(i)}) then '
                              f'expected column length set in config.json file ({j})!')
            else:
                header_row.append(i + whitespace_generator(j - len(i)))

        return list_to_stmt(header_row, add_plus_sign=False, add_comma=False).replace(', ', '') + '\n'
