"""Console script for fhs_xmltv_tools."""
import sys
from pprint import pprint

from fhs_xmltv_tools import config  # noqa: F401

import typer

main = typer.Typer(pretty_exceptions_show_locals=False)


@main.command()
def list_channels(
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
    ignore_empty_id: bool = typer.Option(False, "--ignore-empty-id"),  # noqa: B008
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
):
    """List channels xml.

    Args:
        xmltv_file: xmltv file to use
        force_color: force color in a pipe
        ignore_empty_id: hide channels without a channel id

    """
    from rich.console import Console
    from rich.table import Table
    from .xmltv_load_save import xmltv_load

    console = Console(force_terminal=force_color)
    with console.status("Loading...", spinner="dots"):
        data = xmltv_load(xmltv_file)

    table = Table(title="Channels")
    table.add_column("Index", justify="right", style="cyan")
    table.add_column("Id", style="green")
    table.add_column("Channel", style="cyan")
    for index, channel in enumerate(data.channel):
        if channel.id == "" and ignore_empty_id:
            continue
        table.add_row(str(index + 1), channel.id, (channel.display_name[0]).content[0])
    console.print(table)


@main.command()
def channel_details(
    index: int = 0,
    channelid: str = "",
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
):
    """List channels xml.

    Args:
        index: channel index in list, number van 1 to len(list)
        channelid: channelid to search
        xmltv_file: xmltv file to use

    """
    from .xmltv_load_save import xmltv_load
    from .xmltv_programs import xmltv_programs_test
    from .xmltv_channels import get_channel_by_channel_id

    if index == 0 and channelid == "":
        print("needs index or channelid option")
        exit(1)

    if index != 0 and channelid != "":
        print("needs only index or channelid option, not both.")
        exit(2)

    data = xmltv_load(xmltv_file)
    if index != 0:
        channel = data.channel[index - 1]
    else:
        channel = get_channel_by_channel_id(data, channelid)
    pprint(channel)
    print("")
    print("")
    programs = xmltv_programs_test(data, channel.id)
    pprint(list(programs))


@main.command()
def analyse_programs(
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
):
    """Analyse channels xml.

    Args:
        force_color: force color in pipeline for example
        xmltv_file: xmltv file to use

    """
    from rich.console import Console
    from rich.table import Table
    from .xmltv_load_save import xmltv_load
    from .xmltv_programs import analyse_programs

    console = Console(force_terminal=force_color)
    with console.status("Loading...", spinner="dots"):
        data = xmltv_load(xmltv_file)

    with console.status("Analysing...", spinner="dots"):
        result = analyse_programs(data)

    table = Table(title="Channels")
    table.add_column("Id", style="cyan")
    table.add_column("start time", style="green")
    table.add_column("end time", style="cyan")
    table.add_column("programs", justify="right", style="green")
    for p in result:
        table.add_row(
            p,
            result[p]["first_start"],
            result[p]["last_stop"],
            str(result[p]["programs"]),
        )
    console.print(table)


@main.command()
def search_program(
    search: str = typer.Option(..., help="regex search"),  # noqa: B008
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
    force_case: bool = typer.Option(False, "--force-case-sensitive"),  # noqa: B008
):
    """Search program in xml.

    Args:
        search: string or regex to search
        force_color: force color in pipeline for example
        force_case: normal search is case insensitive but with this option force case sensitive
        xmltv_file: xmltv file to use

    """
    from rich.console import Console
    from rich.table import Table
    from .xmltv_load_save import xmltv_load
    from .xmltv_programs import search_programs

    console = Console(force_terminal=force_color)
    with console.status("Loading...", spinner="dots"):
        data = xmltv_load(xmltv_file)

    with console.status("Searching...", spinner="dots"):
        result = search_programs(data, search, force_case=force_case)

    table = Table(title="Programs")
    table.add_column("Channel", style="cyan")
    table.add_column("start time", style="green")
    table.add_column("end time", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Description", style="cyan")
    for p in result:
        table.add_row(p["channel"], p["start"], p["stop"], p["title"], p["description"])
    console.print(table)


@main.command()
def write_xmlfile_channels(
    channel_file: str,
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
    xmltv_out: str = typer.Option(  # noqa: B008
        ..., help="write xmltv file", envvar="fhs_xmltv_out"
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
):
    """Write xmlfile with only used channels to xml.

    Args:
        channel_file: file with channels one per line
        xmltv_file: xmltv file to use
        xmltv_out: write xmltv file
        force_color: force color in pipeline for example
    """
    from rich.console import Console
    from .xmltv_load_save import xmltv_load, xmltv_save
    from .xmltv_channels import channels_remove_all_channels_not_in_list
    from .xmltv_programs import programme_remove_all_channels_not_in_list

    with open(channel_file, "r") as f:
        channels = set(f.read().splitlines())

    console = Console(force_terminal=force_color)
    # load xmltv file
    with console.status("Loading...", spinner="dots"):
        data = xmltv_load(xmltv_file)

    with console.status("Removing channels...", spinner="dots"):
        data = channels_remove_all_channels_not_in_list(data, channels)

    with console.status("Removing programs...", spinner="dots"):
        data = programme_remove_all_channels_not_in_list(data, channels)

    with console.status("Saving...", spinner="dots"):
        xmltv_save(xmltv_out, data)


@main.command()
def join_xml_files(
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
    xmltv_file_add: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
    xmltv_out: str = typer.Option(  # noqa: B008
        ..., help="write xmltv file", envvar="fhs_xmltv_out"
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
):
    """Join 2 xml files and write them out as 1 xml.

    Args:
        xmltv_file: xmltv file to use
        xmltv_file_add: xmltv file to use
        xmltv_out: write xmltv file
        force_color: force color in pipeline for example
    """
    from rich.console import Console
    from .xmltv_load_save import xmltv_load, xmltv_save
    from .xmltv_channels import join_channels
    from .xmltv_programs import join_programs

    console = Console(force_terminal=force_color)
    # load xmltv file
    with console.status("Loading file 1...", spinner="dots"):
        data = xmltv_load(xmltv_file)

    with console.status("Loading file 2...", spinner="dots"):
        data02 = xmltv_load(xmltv_file_add)

    with console.status("Join channels...", spinner="dots"):
        data = join_channels(data, data02)

    with console.status("Join programs...", spinner="dots"):
        data = join_programs(data, data02)

    with console.status("Saving...", spinner="dots"):
        xmltv_save(xmltv_out, data)


@main.command()
def run_tasks(
    yaml_command: str = typer.Option(  # noqa: B008
        ..., help="read yaml file", envvar="fhs_xmltv_yaml"
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
):
    """Run tasks in yaml file.

    Args:
        yaml_command: xmltv file to use
        force_color: force color in pipeline for example
    """
    from rich.console import Console
    from .playyaml import play

    config.CONSOLE = Console(force_terminal=force_color)
    play(yaml_command)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
