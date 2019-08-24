""" general utilities library """


def whitespace_generator(i):
    """
    whitespaces generator function
    :param i:
    :return: whitespaces string
    """
    return int(i) * ' '


def list_to_str(columns):
    """
    list to str function
    :param columns: list
    :return: string
    """
    columns = str(columns).strip('[]').split(', ')
    return columns


def replace_multiple(main_string, to_be_replaced, new_string):
    """
    helper function to iterate over the strings to be replaced
    :param main_string:
    :param to_be_replaced:
    :param new_string:
    :return: string with replacements
    """
    for elem in to_be_replaced:
        if elem in main_string:
            main_string = main_string.replace(elem, new_string)
    return main_string
