"""Functions to get info out of a xmltv."""

from pprint import pprint

from . import config  # noqa: F401


def get_info(input_var):
    """Return info from input.

    Args:
        input_var: program.title or program.desc

    Returns:
        info
    """
    if input_var == []:
        return ""
    try:
        if input_var[0].content == []:
            return ""
        return input_var[0].content[0]
    except KeyError:
        pprint(input_var)
    except IndexError:
        pprint(input_var)
    return "Error"


def get_program_title(program):
    """Return title from program.

    For now only the first but TODO: check lang

    Args:
        program: details of program

    Returns:
        program title
    """
    return get_info(program.title)


def get_program_desc(program):
    """Return desc from program.

    For now only the first but TODO: check lang

    Args:
        program: details of program

    Returns:
        program description
    """
    return get_info(program.desc)
