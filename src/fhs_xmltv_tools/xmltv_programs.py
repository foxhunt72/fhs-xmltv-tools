"""xmltv_programs script for fhs_xmltv_tools."""

import fhs_xmltv_tools.config as config
from .func_xmltv_programs import get_program_title,get_program_desc

def xmltv_programs(xmltv_data, channel_id):
    """List programs for channel id."""
    list_programs = []
    for p in xmltv_data.programme:
        if p.channel == channel_id:
            list_programs.append(p)
    return list_programs

def xmltv_programs_output(program):
    return f"{get_program_title(program)} {program.start} - {program.stop}"

def xmltv_programs_test(xmltv_data, channel_id):
    programs = []
    for p in xmltv_programs(xmltv_data, channel_id):
        programs.append(xmltv_programs_output(p))
    return programs


def analyze_program_initialize(program_data):
    ad={}
    ad['programs']=0
    ad['first_start']=program_data.start
    ad['last_stop']=program_data.stop
    return ad


def analyze_program_update(current_data, program_data):
    current_data['programs'] += 1
    if program_data.start < current_data['first_start']:
        current_data['first_start']=program_data.start
    if program_data.stop > current_data['last_stop']:
        current_data['last_stop']=program_data.stop
    return current_data


def analyze_programs(xmltv_data, filter=None, filter_argument=None):
    data={}
    
    if filter is not None:
        programme=filter(xmltv_data, filter_arguement)
    else:
        programme=xmltv_data.programme

    for p in programme:
        current_data = data.get(p.channel, None)
        if current_data == None:
            current_data = analyze_program_initialize(p)
        current_data = analyze_program_update(current_data,p)
        data[p.channel]=current_data
    return data

def search_program_create_program_return(program_data):
    ad={}
    ad['channel']=program_data.channel
    ad['title']=get_program_title(program_data)
    ad['description']=get_program_desc(program_data)
    ad['start']=program_data.start
    ad['stop']=program_data.stop
    return ad


def search_programs(xmltv_data, search_str, force_case=False):
    """Search all the programs and return list of results."""

    result=[]
    import re
    if force_case:
        search_re=re.compile(search_str)
    else:
        search_re=re.compile(search_str, re.IGNORECASE)

    programme=xmltv_data.programme
    for p in programme:
        if not search_re.search(get_program_title(p)):
            continue
        result.append(search_program_create_program_return(p))
    return result
