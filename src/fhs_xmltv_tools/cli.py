"""Console script for fhs_xmltv_tools."""
import sys

from pprint import pprint
import typer
main = typer.Typer()

@main.command()
def list_channels(
    xmltv_file: str = typer.Option(..., help="read xmltv file", envvar="fhs_xmltv_file"),
    ignore_empty_id: bool = typer.Option(False, "--ignore-empty-id"),
    force_color: bool = typer.Option(False, "--force-color", help="force color in pipelines"),
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

    data=xmltv_load(xmltv_file)
    channel = data.channel[index-1]
    pprint(channel)

@main.command()
def analyze_programs(
    xmltv_file: str = typer.Option(..., help="read xmltv file", envvar="fhs_xmltv_file"),
):
    """Analyze channels xml."""
    from .xmltv_load_save import xmltv_load
    from .xmltv_programs import analyze_programs

    data=xmltv_load(xmltv_file)
    result = analyze_programs(data)
    pprint(result)



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
