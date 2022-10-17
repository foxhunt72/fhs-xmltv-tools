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


def search_program_create_program_return(program_data):
    """Return search_program item.

    Args:
        program_data: item of xmltv_data.programma

    Returns:
        dicts with channel, title, discription, start, stop
    """
    ad = {
        "channel": program_data.channel,
        "title": program_data.title,
        "description": program_data.desc,
        "start": program_data.start,
        "stop": program_data.stop,
    }
    return ad


def search_programs_sql(sqltype, sqlconnect, search_str, force_case=False):
    """Search all the programs and return list of results.

    Args:
        sqltype: type of connection for example sqlite
        sqlconnect: connect for sql, for example for sqlite, this is the db file inclusief path
        search_str: string object or regex search.
        force_case: case sensitive search or not

    Returns:
        list of search_Program_create_program_return items
    """
    result = []
    from .sql import init_sql, create_engine_url

    sqlalchemy_url = create_engine_url(sqltype, sqlconnect)

    if init_sql(sqlalchemy_url) is None:
        print(f"ERROR: can't open sql url: {sqlalchemy_url}")
        exit(1)

    session = config.SQL["session"]
    Program = config.SQL["program"]

    if force_case:
        print("ERROR: force case not implmented.")
        exit(2)

    for p in session.query(Program).filter(
        (Program.title.like(f"%{search_str}%")) | (Program.desc.like(f"%{search_str}%"))
    ):
        result.append(search_program_create_program_return(p))
    return result


def delete_sql(sqltype, sqlconnect, days):
    """Delete sql entries older than days.

    Args:
        sqltype: type of connection for example sqlite
        sqlconnect: connect for sql, for example for sqlite, this is the db file inclusief path
        days: integer days to keep

    Returns:
        Result
    """
    from .sql import init_sql, create_engine_url
    from datetime import datetime, timedelta

    sqlalchemy_url = create_engine_url(sqltype, sqlconnect)

    if init_sql(sqlalchemy_url) is None:
        print(f"ERROR: can't open sql url: {sqlalchemy_url}")
        exit(1)

    session = config.SQL["session"]
    Program = config.SQL["program"]

    past_date = datetime.now() + timedelta(days=-days)
    past_date_str = past_date.strftime("%Y%m%d")

    print(f"cleaning (deleting) all entries before {past_date:%Y-%m-%d}")

    my_query = session.query(Program).filter(Program.start < past_date_str)
    my_query.delete()
    session.commit()
    return True
