"""Console script for fhs_xmltv_tools."""
import sys
from pprint import pprint
from typing import List, Optional

from fhs_xmltv_tools import config  # noqa: F401

import typer

from .__version__ import __project_name__, __version__

print(f"{__project_name__}: {__version__}")
main = typer.Typer(pretty_exceptions_show_locals=False)


@main.command()
def list_channels(
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file", prompt=True
    ),  # noqa: B008
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
    from .xmltv_programs import display_table_analyse_programs

    console = Console(force_terminal=force_color)
    from .xmltv_load_save import xmltv_load

    with console.status("Loading...", spinner="dots"):
        data = xmltv_load(xmltv_file)

    display_table_analyse_programs(console, data)


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
        ..., help="read yaml file", envvar="fhs_xmltv_yaml", prompt=True
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
    include_tag: Optional[List[str]] = typer.Option(None),  # noqa: B008
    exclude_tag: Optional[List[str]] = typer.Option(None),  # noqa: B008
):
    """Run tasks in yaml file.

    Args:
        yaml_command: xmltv file to use
        force_color: force color in pipeline for example
        include_tag: tags from task to include
        exclude_tag: exclude tasks with this tag
    """
    from rich.console import Console
    from .playyaml import play

    config.CONSOLE = Console(force_terminal=force_color)
    play(yaml_command, include_tag, exclude_tag)


@main.command()
def xmltv_to_sql(
    xmltv_file: str = typer.Option(  # noqa: B008
        ..., help="read xmltv file", envvar="fhs_xmltv_file"
    ),
    sqltype: str = typer.Option(  # noqa: B008
        "sqlite",
        help="sqltype for now, (default) sqlite or sqlalchemy",
    ),
    sqlconnect: str = typer.Option(  # noqa: B008
        ...,
        help="sqlconnect how to connect.",
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
):
    """Xmltv to sql (using sqlalchemy).

    Args:
        force_color: force color in pipeline for example
        xmltv_file: xmltv file to use
        sqltype: sqltype type sqlite or sqlalchemy
        sqlconnect: connect string, this is the filepath is using sqltype = sqlite

    """
    from rich.console import Console
    from .xmltv2sql import save_xmltv_to_sql

    console = Console(force_terminal=force_color)
    from .xmltv_load_save import xmltv_load

    with console.status("Loading...", spinner="dots"):
        data = xmltv_load(xmltv_file)

    with console.status("Exporting to sql...", spinner="dots"):
        save_xmltv_to_sql(data, sqltype, sqlconnect)


@main.command()
def search_program_sql(
    search: str = typer.Option(..., help="regex search"),  # noqa: B008
    sqltype: str = typer.Option(  # noqa: B008
        "sqlite",
        help="sqltype for now, (default) sqlite or sqlalchemy",
    ),
    sqlconnect: str = typer.Option(  # noqa: B008
        ...,
        help="sqlconnect how to connect.",
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
    force_case: bool = typer.Option(False, "--force-case-sensitive"),  # noqa: B008
):
    """Search program in sql saved data.

    Args:
        search: string or regex to search
        force_color: force color in pipeline for example
        force_case: normal search is case insensitive but with this option force case sensitive
        sqltype: sqltype type sqlite or sqlalchemy
        sqlconnect: connect string, this is the filepath is using sqltype = sqlite

    """
    from rich.console import Console
    from rich.table import Table
    from .xmltv2sql import search_programs_sql

    console = Console(force_terminal=force_color)

    with console.status("Searching...", spinner="dots"):
        result = search_programs_sql(sqltype, sqlconnect, search, force_case=force_case)

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
def clean_sql(
    days: int = 90,
    sqltype: str = typer.Option(  # noqa: B008
        "sqlite",
        help="sqltype for now, (default) sqlite or sqlalchemy",
    ),
    sqlconnect: str = typer.Option(  # noqa: B008
        ...,
        help="sqlconnect how to connect.",
    ),
):
    """Clean program data from sql.

    Args:
        days: integer amount of days to keep (older program data is removed)
        sqltype: sqltype type sqlite or sqlalchemy
        sqlconnect: connect string, this is the filepath is using sqltype = sqlite

    """
    from .xmltv2sql import delete_sql

    delete_sql(sqltype, sqlconnect, days)

@main.command()
def interactive():
    """Run tasks interactive.
    """
    from .playyaml import interactive_run_cmd2

    interactive_run_cmd2()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
