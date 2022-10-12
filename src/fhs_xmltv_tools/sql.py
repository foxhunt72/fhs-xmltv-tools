"""Sqlalchemy module."""

from . import config

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, String
except ModuleNotFoundError:
    print("python: sqlalchemy library not found.")
    exit(1)


def create_engine_url(sqltype, sqlconnect):
    """Create a engine url.

    Args:
        sqltype: which type, for now: sqlite or sqlalchemy
        sqlconnect: how to connect, for sqlite, file path

    Returns:
        full sqlalchemy sqlite url
    """
    if sqltype == "sqlite":
        return f"sqlite:///{sqlconnect}"
    if sqltype == "sqlalchemy" or sqltype == "raw":
        return sqlconnect
    print(f"ERROR: unknown sqltype: {sqltype}, options are 'sqlite' or 'sqlalchemy'")
    exit(1)


def sql_create_engine(engine_url, echo=False):
    """Create sqlalchemy engine.

    Args:
        engine_url: sql engine url 'sqlite:///proef.db'
        echo: extra debug, default False

    Returns:
        engine or None if issue
    """
    engine = create_engine(engine_url, echo=echo)
    return engine


def sql_create_session(engine_url, engine=None):
    """Create sqlalchemy session.

    Args:
        engine_url: sql engine url
        engine: predefined engine or None

    Returns:
        session or None if issue
    """
    if engine is None:
        engine = sql_create_engine(engine_url)
    Session = sessionmaker(bind=engine)
    return Session()


def init_sql(engine_url):
    """Init sql.

    Args:
        engine_url: sql engine url

    Returns:
        session or None if issue
    """
    engine = sql_create_engine(engine_url, echo=False)
    if engine is None:
        return None
    config.SQL["engine"] = engine
    session = sql_create_session(None, engine=engine)
    if session is None:
        return None

    Base = declarative_base()

    class Program(Base):
        """Program sqlalchemy base."""

        __tablename__ = "programme"

        channel = Column(String, primary_key=True)
        start = Column(String, primary_key=True)
        stop = Column(String)
        title = Column(String)
        desc = Column(String)
        date = Column(String)

        def __repr__(self):
            """Representation for a program.

            Returns:
                string description
            """
            return f"Program {self.title} {self.start} {self.channel}"

    config.SQL["session"] = session
    Base.metadata.create_all(engine)
    config.SQL["program"] = Program

    return session
