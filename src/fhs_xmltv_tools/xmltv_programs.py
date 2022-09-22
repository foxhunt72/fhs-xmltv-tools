"""xmltv_programs script for fhs_xmltv_tools."""


def xmltv_programs(xmltv_data, channel_id):
    """List programs for channel id."""
    list_programs = []
    for p in xmltv_data.programme:
        if p.channel == channel_id:
            list_programs.append(p)
    return p

def xmltv_programs_output(program):
    return f"{(program.title[0]).content[0]} {program.start} - {program.stop}"

def xmltv_programs_test(xmltv_data, channel_id):
    for p in xmltv_programs(xmltv_data, channel_id):
        yield xmltv_programs_output(p)


def analyze_programs(xmltv_data, filter=None, filter_argument=None):
    data={}

    if filter is not None:
        programme=filter(xmltv_data, filter_arguement)
    else:
        programme=xmltv_data.programme

    for p in programme:
        if p.channel not in data:
            data[p.channel]={}
            data[p.channel]['programs']=0
            data[p.channel]['first_start']=p.start
            data[p.channel]['last_stop']=p.stop
        data[p.channel]['programs'] += 1
        if p.start < data[p.channel]['first_start']:
            data[p.channel]['first_start']=p.start
        if p.stop > data[p.channel]['last_stop']:
            data[p.channel]['last_stop']=p.stop
    return data
