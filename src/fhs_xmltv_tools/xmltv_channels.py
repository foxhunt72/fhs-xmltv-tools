"testtest""xmltv_channels script for fhs_xmltv_tools."""

from . import config  # noqa: F401
from .xmltv_programs import search_and_replace_channel_id
from xmltv.models.xmltv import DisplayName


def get_channel_by_channel_id(xmltv_data, channel_id):
    """Get channel from channel list with channel_id.

    Args:
        xmltv_data: data object with xmltv data.
        channel_id: channel id we want to search.

    Returns:
        channel
    """
    for my_channel in xmltv_data.channel:
        if my_channel.id == channel_id:
            return my_channel
    return None


def get_channel_index_by_channel_id(xmltv_data, channel_id):
    """Get channel index from channel list with channel_id.

    Args:
        xmltv_data: data object with xmltv data.
        channel_id: channel id we want to search.

    Returns:
        channel_index
    """
    for (i, my_channel) in enumerate(xmltv_data.channel):
        if my_channel.id == channel_id:
            return i
    return -1


def channels_remove_all_channels_not_in_list(xmltv_data, channel_set):
    """Remove all channels that are not in the list.

    Args:
        xmltv_data: data object with xmltv data.
        channel_set: set of channel id you want to keep

    Returns:
        xmltv_data
    """
    for p in range(len(xmltv_data.channel), 0, -1):
        if (xmltv_data.channel[p - 1]).id not in channel_set:
            del xmltv_data.channel[p - 1]
    return xmltv_data


def join_channels(xmltv_data, xmltv_data_add, only_channels=None):
    """Add the channels from xmltv_data_add to the channels from xmtv_data.

    Args:
        xmltv_data: data object with xmltv data.
        xmltv_data_add: data object with xmltv data jou want to add.

    Returns:
        xmltv_data
    """
    for p in xmltv_data_add.channel:
        if only_channels is not None:
            if p.id not in only_channels:
                continue
        xmltv_data.channel.append(p)
    return xmltv_data


def return_list(var_input):
    """Return a list a var as var is not a list.

    Args:
        var_input: variable input

    Returns:
        list
    """
    if type(var_input) != list():
        return [var_input]
    else:
        return var_input


def return_channel_displayname(p):
    """Return display info.

    Args:
        p: input from yaml

    Returns:
        displayname
    """
    if type(p) == str():
        return DisplayName(content=p, lang=None)
    if type(p) == dict():
        for q in p:
            return DisplayName(content=p[q], lang=q)
    return DisplayName(content=f"unknown {str(p)}")


def rename_channel(xmltv_data, channel):
    """Rename channel base on channel struct.

    Args:
        xmltv_data: data object with xmltv data.
        channel: channel struct

    Returns:
        xmltv_data
    """
    if type(channel) != dict:
        print('channel needs to by of type dict not {str(channel)}.')
        return xmltv_data

    for q in channel:
        nothing_found = True
        while (channel_index := get_channel_index_by_channel_id(xmltv_data, q)) != -1:
            nothing_found = False
            print(f"{q=}  {channel_index=}")
            if 'new_id' in channel[q]:
                search_and_replace_channel_id(xmltv_data, q, channel[q]['new_id'])
                xmltv_data.channel[channel_index].id = channel[q]['new_id']
            # check displayname
            if 'displayname' in channel[q]:
                displayname = return_list(channel[q]['displayname'])
                xmltv_data.channel[channel_index].display_name = []
                for p in displayname:
                    xmltv_data.channel[channel_index].display_name.append(return_channel_displayname(p))
            if channel[q].get('only_one', False) is True:
                break
        if nothing_found is True:
            print(f'channel with id {q}, not found, skipping')
        # check icon
        # check url
    return xmltv_data


def rename_channels(xmltv_data, channels):
    """Rename channels base on channels struct.

    Args:
        xmltv_data: data object with xmltv data.
        channels: channels struct

    Returns:
        xmltv_data
    """
    for channel in channels:
        xmltv_data = rename_channel(xmltv_data, channel)

    return xmltv_data
