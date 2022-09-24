#### functions to get info out of a xmltv_porgramme

import fhs_xmltv_tools.config as config

def get_program_title(program):
    """ Return title from program.

        For now only the first but TODO: check lang
    """
    return (program.title[0]).content[0]


def get_program_desc(program):
    """ Return desc from program.

        For now only the first but TODO: check lang
    """
    return (program.desc[0]).content[0]

