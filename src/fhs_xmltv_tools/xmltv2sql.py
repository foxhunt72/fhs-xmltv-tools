"""Xmltv to sql routines."""

from . import config


def save_xmltv_to_sql(xmltv_data, sqltype, sqlconnect):
    """Save xml to sql.

    Args:
        xmltv_data: data object with xmltv data.
        sqltype: type of connection for example sqlite
        sqlconnect: connect for sql, for example for sqlite, this is the db file inclusief path

    Returns:
        boolean saved
    """
    from .sql import init_sql, create_engine_url
    from .func_xmltv import get_program_desc, get_program_title

    sqlalchemy_url = create_engine_url(sqltype, sqlconnect)

    if init_sql(sqlalchemy_url) is None:
        print(f"ERROR: can't open sql url: {sqlalchemy_url}")
        return False
    Program = config.SQL["program"]
    # save xmltv data to sql
    for p in xmltv_data.programme:
        program = Program(
            channel=p.channel,
            start=p.start,
            stop=p.stop,
            title=get_program_title(p),
            desc=get_program_desc(p),
            date=p.date,
        )
        config.SQL["session"].merge(program)
    config.SQL["session"].commit()
