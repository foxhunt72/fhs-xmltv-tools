"""Console script for fhs_xmltv_tools."""
import sys

from pprint import pprint
import typer
main = typer.Typer(pretty_exceptions_show_locals=False)


import fhs_xmltv_tools.config as config

@main.command()
def list_channels(
    xmltv_file: str = typer.Option(..., help="read xmltv file", envvar="fhs_xmltv_file"),
    ignore_empty_id: bool = typer.Option(False, "--ignore-empty-id"),
    force_color: bool = typer.Option(None, "--force-color/--no-color", help="force color in pipelines"),
):
    """List channels xml."""
    from rich.console import Console
    from rich.table import Table
    from .xmltv_load_save import xmltv_load

    console = Console(force_terminal=force_color)
    with console.status("Loading...", spinner='dots'):
        data=xmltv_load(xmltv_file)

    table = Table(title="Channels")
    table.add_column("Index", justify="right", style="cyan")
    table.add_column("Id", style="green")
    table.add_column("Channel", style="cyan")
    for index, channel in enumerate(data.channel):
        if channel.id == "" and ignore_empty_id == True:
            continue
        table.add_row(str(index+1), channel.id, (channel.display_name[0]).content[0])
    console.print(table)


@main.command()
def channel_details(
    index: int,
    xmltv_file: str = typer.Option(..., help="read xmltv file", envvar="fhs_xmltv_file"),
):
    """List channels xml."""
    from .xmltv_load_save import xmltv_load
    from .xmltv_programs import xmltv_programs_test

    data=xmltv_load(xmltv_file)
    channel = data.channel[index-1]
    pprint(channel)
    print("")
    print("")
    programs=xmltv_programs_test(data, channel.id)
    pprint(list(programs))

@main.command()
def analyze_programs(
    xmltv_file: str = typer.Option(..., help="read xmltv file", envvar="fhs_xmltv_file"),
    force_color: bool = typer.Option(None, "--force-color/--no-color", help="force color in pipelines"),
):
    """Analyze channels xml."""
    from rich.console import Console
    from rich.table import Table
    from .xmltv_load_save import xmltv_load
    from .xmltv_programs import analyze_programs

    console = Console(force_terminal=force_color)
    with console.status("Loading...", spinner='dots'):
        data=xmltv_load(xmltv_file)

    with console.status("Analysing...", spinner='dots'):
         result = analyze_programs(data)

    table = Table(title="Channels")
    table.add_column("Id", style="cyan")
    table.add_column("start time", style="green")
    table.add_column("end time", style="cyan")
    table.add_column("programs", justify="right", style="green")
    for p in result:
        table.add_row(p, result[p]['first_start'], result[p]['last_stop'], str(result[p]['programs']))
    console.print(table)


@main.command()
def search_program(
    search:  str = typer.Option(..., help="regex search"),
    xmltv_file: str = typer.Option(..., help="read xmltv file", envvar="fhs_xmltv_file"),
    force_color: bool = typer.Option(None, "--force-color/--no-color", help="force color in pipelines"),
    force_case: bool = typer.Option(False, "--force-case-sensitive"),
):
    """Search program in xml."""
    from rich.console import Console
    from rich.table import Table
    from .xmltv_load_save import xmltv_load
    from .xmltv_programs import search_programs

    console = Console(force_terminal=force_color)
    with console.status("Loading...", spinner='dots'):
        data=xmltv_load(xmltv_file)

    with console.status("Searching...", spinner='dots'):
         result = search_programs(data, search, force_case=force_case)

    table = Table(title="Programs")
    table.add_column("Channel", style="cyan")
    table.add_column("start time", style="green")
    table.add_column("end time", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Description", style="cyan")
    for p in result:
        table.add_row(p['channel'], p['start'], p['stop'], p['title'], p['description'])
    console.print(table)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
