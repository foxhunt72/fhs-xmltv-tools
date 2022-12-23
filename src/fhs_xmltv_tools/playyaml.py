"""Playyaml file."""

import os
import sys
from pprint import pprint

import yaml

from . import config
from .playyaml_lib import func_dict_parse, play as play_lib


def check_console():
    """Check if CONFIG.console is not none."""
    if config.CONSOLE is None:
        from rich.console import Console

        config.CONSOLE = Console()


def load_yaml(filename):
    """Load yaml file from disk.

    Args:
        filename: file to load

    Returns:
        struct from yaml file
    """
    try:
        with open(os.path.expanduser(filename), "r") as file:
            data = yaml.safe_load(file)
    except Exception as e:  # noqa:B902
        sys.stderr.write(f"can't open config file: {filename}  {e}")
        exit(1)
    return data


def play_command_loadxml(task):
    """Play command loadxml.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_load_save import xmltv_load

    check_console()
    store = task.get("store", "default")
    if "file" not in task:
        sys.stderr.write(f"missing file entry in task {str(task)}")
        exit(3)
    file = task.get("file")
    with config.CONSOLE.status(f"Loading...{file} to store {store}", spinner="dots"):
        config.STORE[store] = xmltv_load(file)
    print(f"Loaded {file} to store {store}")
    return True


def play_command_empty_xml(task):
    """Play command emptyxml.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_load_save import xmltv_empty

    check_console()
    store = task.get("store", "default")
    source_info_url = task.get("source_info_url")
    source_info_name = task.get("source_info_name")
    source_data_url = task.get("source_data_url")
    config.STORE[store] = xmltv_empty(
        source_info_url=source_info_url,
        source_info_name=source_info_name,
        source_data_url=source_data_url
    )
    print(f"Create empty xmltv store {store}")
    return True


def play_command_savexml(task):
    """Play command savexml.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_load_save import xmltv_save

    check_console()
    store = task.get("store", "default")
    if "file" not in task:
        sys.stderr.write(f"missing file entry in task {str(task)}")
        exit(3)
    file = task.get("file")
    with config.CONSOLE.status(f"Loading...{file} to store {store}", spinner="dots"):
        xmltv_save(file, config.STORE[store])
    print(f"Saved {file} to store {store}")
    return True


def play_command_rename_channel(task):
    """Play command rename_channel.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_channels import rename_channel

    check_console()
    store = task.get("store", "default")
    options_dict = {"new_id": task["new_id"]}
    if task["only_one"] != "":
        options_dict["only_one"] = True
    if task["new_display_name"] != "":
        options_dict["displayname"] = task["new_display_name"]

    channel_dict = {task["channel_id"]: options_dict}
    with config.CONSOLE.status(f"Rename channel from store {store}", spinner="dots"):
        config.STORE[store] = rename_channel(
            config.STORE[store], channel_dict
        )
    return True


def play_command_only_channels(task):
    """Play command only_channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_channels import channels_remove_all_channels_not_in_list
    from .xmltv_programs import programme_remove_all_channels_not_in_list

    check_console()
    store = task.get("store", "default")
    if "channels" not in task:
        sys.stderr.write(f"missing channels entry in task {str(task)}")
        exit(3)
    channels = task.get("channels")
    split_char = task.get("split_char","")
    if type(channels) == str and split_char != "":
        channels = channels.split(split_char)
    with config.CONSOLE.status(f"Removing channels from store {store}", spinner="dots"):
        config.STORE[store] = channels_remove_all_channels_not_in_list(
            config.STORE[store], channels
        )
    with config.CONSOLE.status(
        f"Removing programme from store {store}", spinner="dots"
    ):
        config.STORE[store] = programme_remove_all_channels_not_in_list(
            config.STORE[store], channels
        )
    print(f"Removed channels and programs from store {store}")
    return True


def play_command_add(task):
    """Play command add 2 xmltv stores.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_channels import join_channels
    from .xmltv_programs import join_programs

    check_console()
    store = task.get("store", "default")
    if "add_store" not in task:
        sys.stderr.write(f"missing add_store entry in task {str(task)}")
        exit(3)
    add_store = task.get("add_store")

    with config.CONSOLE.status("Join channels...", spinner="dots"):
        config.STORE[store] = join_channels(
            config.STORE[store], config.STORE[add_store]
        )

    with config.CONSOLE.status("Join programs...", spinner="dots"):
        config.STORE[store] = join_programs(
            config.STORE[store], config.STORE[add_store]
        )

    print(f"Add channels and programs from store {add_store} to store {store}")
    return True


def play_command_change_timezone(task):
    """Change timezone in program data.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_programs import search_and_replace_in_start_and_stop

    check_console()
    store = task.get("store", "default")
    if "search" not in task:
        sys.stderr.write(f"missing search entry (search string) in task {str(task)}")
        exit(3)
    if "replace" not in task:
        sys.stderr.write(f"missing replace entry (replace string) in task {str(task)}")
        exit(3)
    search = task.get("search")
    replace = task.get("replace")

    with config.CONSOLE.status(
        "Search and replace in start/stop program time...", spinner="dots"
    ):
        config.STORE[store] = search_and_replace_in_start_and_stop(
            config.STORE[store], search, replace
        )

    print(
        f"Search and replace in start/stop time programs: store {store} search:{search} / replace:{replace}"
    )
    return True


def play_command_analyse_programs(task):
    """Analyse programs for a store.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv_programs import display_table_analyse_programs

    check_console()
    store = task.get("store", "default")
    title = task.get("title", None)
    display_table_analyse_programs(
        config.CONSOLE, config.STORE[store], add_source_column=True, source_name=title
    )
    return True


def play_command_xmltv2sql(task):
    """Save xmltv data to sql.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv2sql import save_xmltv_to_sql

    check_console()
    store = task.get("store", "default")
    sqltype = task.get("sqltype", "sqlite")
    if "sqlconnect" not in task:
        sys.stderr.write(f"missing sqlconnect entry in task {str(task)}")
        exit(3)
    sqlconnect = task.get("sqlconnect")
    with config.CONSOLE.status("Save xmltv data to sql...", spinner="dots"):
        save_xmltv_to_sql(config.STORE[store], sqltype, sqlconnect)
    return True


def play_command_clean_sql(task):
    """Save xmltv data to sql.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .xmltv2sql import delete_sql

    check_console()
    days = task.get("days", 90)
    sqltype = task.get("sqltype", "sqlite")
    if "sqlconnect" not in task:
        sys.stderr.write(f"missing sqlconnect entry in task {str(task)}")
        exit(3)
    sqlconnect = task.get("sqlconnect")
    with config.CONSOLE.status("Save xmltv data to sql...", spinner="dots"):
        delete_sql(sqltype, sqlconnect, days)
    return True


def play_command_execute_command(task):
    """Execute a program.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .playyaml_funcs import execute_command

    if "execute" not in task and "execute_base64" not in task:
        sys.stderr.write(f"missing execute or execute_base64 entry in task {str(task)}")
        exit(3)

    if "execute_base64" in task:
        from .playyaml_funcs import base64_2_str

        execute = base64_2_str(task.get("execute_base64"))
    else:
        execute = task.get("execute")
    shell = task.get("shell", False)
    capture_output = task.get("capture_output", True)

    result = execute_command(
        execute, shell=shell, capture_output=capture_output  # noqa:S604
    )  # noqa:S604
    if capture_output:
        print(result.stdout)
        print(result.stderr)
        print(f"error_code: {result.returncode}")
    return True


def task_check_tag(task, include_tags=None, exclude_tags=None):
    """Check if the task have a tag and if we skip or not this task.

    Args:
        task: task array
        include_tags: list of tags to run
        exclude_tags: list of tags to skip

    Returns:
        RunTask: boolean, True run task, False skip task
    """
    from fhs_xmltv_tools.playyaml_funcs import check_items_in_2_lists

    temp_tags = task.get("tags", [])
    tags = temp_tags if isinstance(temp_tags, list) else [temp_tags]

    if include_tags is not None and include_tags != []:  # noqa: SIM102
        # check is include tags in in tags of this task, if false then skip this task
        if check_items_in_2_lists(include_tags, tags) is False:
            return False

    if exclude_tags is not None and exclude_tags != []:  # noqa: SIM102
        # check is exclude tags in in tags of this task, if true then skip this task
        if check_items_in_2_lists(exclude_tags, tags) is True:
            return False

    return True


funcdict = {
    "analyse_programs": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "title", "help": "title name", "default": ""}
        ],
        "func": play_command_analyse_programs,
        "help": "analyse programs"
    },
    "loadxml": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "file", "help": "file name to load"}
        ],
        "func": play_command_loadxml,
        "help": "loadxml"
    },
    "emptyxml": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "source_info_url", "default": ""},
            {"name": "source_info_name", "default": ""},
            {"name": "source_data_url", "default": ""},
        ],
        "func": play_command_empty_xml,
        "alias": ["empty_xml"],
        "help": "loadxml"
    },
    "keep_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "split_char", "help": "split channel string by var", "default": ""},
            {"name": "channels", "help": "channels to keep"}
        ],
        "func": play_command_only_channels,
        "alias": ['only_channels'],
        "help": "keep only channels"
    },
    "savexml": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "file", "help": "file name to load"}
        ],
        "func": play_command_savexml,
        "help": "savexml"
    },
    "add": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "add_store", "help": "add store name"}
        ],
        "func": play_command_add,
        "help": "add"
    },
    "change_timezone": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "search", "help": "search entry"},
            {"name": "replace", "help": "replace entry"}
        ],
        "func": play_command_change_timezone,
        "help": "change_timezone"
    },
    "execute_command": {
        "args": [
            {"name": "execute", "help": "execute command", "default": ""},
            {"name": "execute_base64", "help": "execute command base64", "default": ""},
            {"name": "shell", "help": "use shell", "default": "false", "type": "boolean"},
            {"name": "capture_output", "help": "capture output", "default": "true", "type": "boolean"},
        ],
        "func": play_command_execute_command,
        "help": "execute command"
    },
    "xmltv2sql": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "sqltype", "help": "sqltype: sqlite", "default": "sqlite"},
            {"name": "sqlconnect", "help": "sqlconnect string"}
        ],
        "func": play_command_xmltv2sql,
        "alias": "savesql",
        "help": "xmltv2sql / savesql"
    },
    "rename_channel": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "channel_id", "help": "channel id to rename"},
            {"name": "new_id", "help": "new channel id"},
            {"name": "new_display_name", "default": ""},
            {"name": "only_one", "help": "rename only first occorunce", "default": ""}
        ],
        "func": play_command_rename_channel,
        "help": "rename channels"
    },
    "clean_sql": {
        "args": [
            {"name": "sqltype", "help": "sqltype: sqlite", "default": "sqlite"},
            {"name": "sqlconnect", "help": "sqlconnect string"}
        ],
        "func": play_command_clean_sql,
        "help": "clean sql"
    }
}


def play(commandfile, include_tags=None, exclude_tags=None):
    """Play commandfile.

    Args:
        commandfile: yaml file with instructions
        include_tags: list of tags to run
        exclude_tags: list of tags to skip

    Returns:
        None
    """
    play_lib(commandfile, include_tags=include_tags, exclude_tags=exclude_tags, funcdict=func_dict_parse(funcdict))

    return None

def interactive_run_cmd2():
    """Play interactive

    """
    from .interactive_cmd2 import run_cmd2

    run_cmd2(funcdict=func_dict_parse(funcdict, for_type="interactive"))
