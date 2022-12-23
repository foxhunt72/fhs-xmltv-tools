"""Console script for fhs_xmltv_tools."""
import pathlib

from xmltv import xmltv_helpers
from xmltv.models.xmltv import Tv
from .__version__ import __project_name__


def xmltv_load(xmltv_file):
    """List channels xml.

    Args:
        xmltv_file: file name to load xmltv data from

    Returns:
        xmltv data array

    """
    xmltv_in_file = pathlib.Path(xmltv_file)
    data = xmltv_helpers.serialize_xml_from_file(xmltv_in_file, Tv)
    return data


def xmltv_save(xmltv_file, xmltv_data):
    """Write channels xml.

    Args:
        xmltv_file: file name to write xmltv data to
        xmltv_data: data object with xmltv data.
    """
    xmltv_out = pathlib.Path(xmltv_file)
    xmltv_helpers.write_file_from_xml(xmltv_out, xmltv_data)


def xmltv_empty(source_data_url="", source_info_name="", source_info_url=""):
    """Create empty xmltv forum.

    Args:
        source_data_url: url of source
        source_info_name: source name
        source_info_url: url of your source

    Returns:
        xmltv source
    """
    empty_xmltv = Tv()
    empty_xmltv.source_data_url = source_data_url
    empty_xmltv.source_info_name = source_info_name
    empty_xmltv.source_info_url = source_info_url
    empty_xmltv.generator_info_url = "https://github.com/foxhunt72/fhs-xmltv-tools"
    empty_xmltv.generator_info_name = __project_name__
    return empty_xmltv
