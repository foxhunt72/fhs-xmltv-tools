"""xmltv_channels script for fhs_xmltv_tools."""

from . import config  # noqa: F401


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


def join_channels(xmltv_data, xmltv_data_add):
    """Add the channels from xmltv_data_add to the channels from xmtv_data.

    Args:
        xmltv_data: data object with xmltv data.
        xmltv_data_add: data object with xmltv data jou want to add.

    Returns:
        xmltv_data
    """
    for p in xmltv_data_add.channel:
        xmltv_data.channel.append(p)
    return xmltv_data
