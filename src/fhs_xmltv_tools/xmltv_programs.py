"""xmltv_programs script for fhs_xmltv_tools."""

from . import config  # noqa: F401
from .func_xmltv import get_program_desc, get_program_title


def xmltv_programs(xmltv_data, channel_id):
    """List programs for channel id.

    Args:
        xmltv_data: data object with xmltv data.
        channel_id: channel id we want to search programs for.

    Returns:
        list of programs in xmltv_data.programme format
    """
    list_programs = []
    for p in xmltv_data.programme:
        if p.channel == channel_id:
            list_programs.append(p)
    return list_programs


def xmltv_programs_output(program):
    """Ouput a string with a program name string.

    Args:
        program: item of xmltv_data.programme

    Returns:
        string with title start time and stop time of program.
    """
    return f"{get_program_title(program)} {program.start} - {program.stop}"


def xmltv_programs_test(xmltv_data, channel_id):
    """Create string list of al programs on channel.

    Args:
        xmltv_data: data object with xmltv data.
        channel_id: channel id we want to search programs for.

    Returns:
        list of string: output of xmltv_programs_output
    """
    programs = []
    for p in xmltv_programs(xmltv_data, channel_id):
        programs.append(xmltv_programs_output(p))
    return programs


def analyse_program_initialize(program_data):
    """Return analyse program item.

    Args:
        program_data: item of xmltv_data.programma

    Returns:
        dicts with programs, first start and last_stop fields
    """
    ad = {
        "programs": 0,
        "first_start": program_data.start,
        "last_stop": program_data.stop,
    }
    return ad


def analyse_program_update(current_data, program_data):
    """Update a analyse program item.

    Args:
        current_data: current analayze program item
        program_data: xmltv_data.programma item

    Returns:
        changes current_data
    """
    current_data["programs"] += 1
    if program_data.start < current_data["first_start"]:
        current_data["first_start"] = program_data.start
    if program_data.stop > current_data["last_stop"]:
        current_data["last_stop"] = program_data.stop
    return current_data


def analyse_programs(xmltv_data, filter=None, filter_argument=None):
    """Analyze programs from xmltv_data.

    Gives information about per channel howmany programs and what the first
    start time is and the last stop time.

    Args:
        xmltv_data: data object with xmltv data.
        filter: filter function
        filter_argument: extra arguments for the filter function

    Returns:
        data dicts with key channel id and field value dicts from
        analyse_program_initialize
    """
    data = {}

    if filter is not None:
        programme = filter(xmltv_data, filter_argument)
    else:
        programme = xmltv_data.programme

    for p in programme:
        current_data = data.get(p.channel, None)
        if current_data is None:
            current_data = analyse_program_initialize(p)
        current_data = analyse_program_update(current_data, p)
        data[p.channel] = current_data
    return data


def search_program_create_program_return(program_data):
    """Return search_program item.

    Args:
        program_data: item of xmltv_data.programma

    Returns:
        dicts with channel, title, discription, start, stop
    """
    ad = {
        "channel": program_data.channel,
        "title": get_program_title(program_data),
        "description": get_program_desc(program_data),
        "start": program_data.start,
        "stop": program_data.stop,
    }
    return ad


def search_programs(xmltv_data, search_str, force_case=False):
    """Search all the programs and return list of results.

    Args:
        xmltv_data: data object with xmltv data.
        search_str: string object or regex search.
        force_case: case sensitive search or not

    Returns:
        list of search_Program_create_program_return items
    """
    result = []
    import re

    if force_case:
        search_re = re.compile(search_str)
    else:
        search_re = re.compile(search_str, re.IGNORECASE)

    programme = xmltv_data.programme
    for p in programme:
        if not search_re.search(get_program_title(p)):
            continue
        result.append(search_program_create_program_return(p))
    return result


def programme_remove_all_channels_not_in_list(xmltv_data, channel_set):
    """Remove all programs on channels that are not in the list.

    Args:
        xmltv_data: data object with xmltv data.
        channel_set: set of channel id you want to keep

    Returns:
        xmltv_data
    """
    for p in range(len(xmltv_data.programme), 0, -1):
        if (xmltv_data.programme[p - 1]).channel not in channel_set:
            del xmltv_data.programme[p - 1]
    return xmltv_data


def join_programs(xmltv_data, xmltv_data_add, only_channels=None):
    """Add the programs from xmltv_data_add to the channels from xmtv_data.

    Args:
        xmltv_data: data object with xmltv data.
        xmltv_data_add: data object with xmltv data jou want to add.

    Returns:
        xmltv_data
    """
    for p in xmltv_data_add.programme:
        if only_channels is not None:
            if p.channel not in only_channels:
                continue
        xmltv_data.programme.append(p)
    return xmltv_data


def search_and_replace_in_start_and_stop(xmltv_data, search, replace):
    """Replace in all programs in the start and stop fields the search with replace.

    Use this for example to change the timezone van ' +0000' to ' +0200'

    Args:
        xmltv_data: data object with xmltv data.
        search: string to search in start and stop
        replace: string to replace the 'search' string with in start and stop

    Returns:
        xmltv_data
    """
    for p in xmltv_data.programme:
        p.start = p.start.replace(search, replace)
        p.stop = p.stop.replace(search, replace)
    return xmltv_data


def search_and_replace_channel_id(xmltv_data, current_id, new_id):
    """Replace in all programs in the channeld id.

    Args:
        xmltv_data: data object with xmltv data.
        current_id: channel id to replace
        new_id: new channel id

    Returns:
        xmltv_data
    """
    for p in xmltv_data.programme:
        if p.channel == current_id:
            p.channel = new_id
    return xmltv_data


def display_table_analyse_programs(
    console, xmltv_data, add_source_column=False, source_name=None
):
    """Display table analyse programs.

    Args:
        xmltv_data: data object with xmltv data.
        console: rich.console object
        add_source_column: add a source info column
        source_name: name to use for source_info_name
    """
    from rich.console import Console
    from rich.table import Table

    if console is None:
        console = Console()

    with console.status("Analysing...", spinner="dots"):
        result = analyse_programs(xmltv_data)

    if source_name is None:
        source_name = xmltv_data.source_info_name

    table = Table(title=f"Channels: {source_name}")
    if add_source_column:
        table.add_column("Source name", style="green")
    table.add_column("Id", style="cyan")
    table.add_column("start time", style="green")
    table.add_column("end time", style="cyan")
    table.add_column("programs", justify="right", style="green")
    for p in result:
        if add_source_column:
            table.add_row(
                source_name,
                p,
                result[p]["first_start"],
                result[p]["last_stop"],
                str(result[p]["programs"]),
            )
        else:
            table.add_row(
                p,
                result[p]["first_start"],
                result[p]["last_stop"],
                str(result[p]["programs"]),
            )
    console.print(table)
