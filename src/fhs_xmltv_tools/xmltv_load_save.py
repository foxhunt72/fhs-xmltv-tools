"""Console script for fhs_xmltv_tools."""
from xmltv import xmltv_helpers
from xmltv.models.xmltv import *
import pathlib


def xmltv_load(xmltv_file):
    """List channels xml."""
    xmltv_in_file=pathlib.Path(xmltv_file)
    data = xmltv_helpers.serialize_xml_from_file(xmltv_in_file, Tv)
    return data


