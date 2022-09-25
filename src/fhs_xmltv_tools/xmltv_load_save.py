"""Console script for fhs_xmltv_tools."""
import pathlib

from xmltv import xmltv_helpers
from xmltv.models.xmltv import Tv


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
