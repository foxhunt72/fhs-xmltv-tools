"""Functions to get info out of a xmltv."""

from fhs_xmltv_tools import config  # noqa: F401


def get_program_title(program):
    """Return title from program.

    For now only the first but TODO: check lang

    Args:
        program: details of program

    Returns:
        program title
    """
    return (program.title[0]).content[0]


def get_program_desc(program):
    """Return desc from program.

    For now only the first but TODO: check lang

    Args:
        program: details of program

    Returns:
        program description
    """
    return (program.desc[0]).content[0]
