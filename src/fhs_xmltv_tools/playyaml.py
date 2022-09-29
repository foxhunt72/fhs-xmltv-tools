"""Playyaml file."""

import os
import sys
from pprint import pprint

import yaml

from . import config


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


def play_task(task):
    """Play a task.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    print(f"running task: {task.get('name', 'unknown')}")
    if "command" not in task:
        sys.stderr.write(f"missing command entry in task {str(task)}")
        exit(3)

    if task["command"] == "loadxml":
        return play_command_loadxml(task)

    if task["command"] == "only_channels":
        return play_command_only_channels(task)

    if task["command"] == "savexml":
        return play_command_savexml(task)

    if task["command"] == "add":
        return play_command_add(task)

    if task["command"] == "change_timezone":
        return play_command_change_timezone(task)

    pprint(task)
    return True


def play(commandfile):
    """Play commandfile.

    Args:
        commandfile: yaml file with instructions

    Returns:
        None
    """
    data = load_yaml(commandfile)

    if "tasks" not in data:
        sys.stderr.write("missing tasks entrie in yaml file")
        exit(2)

    for task in data["tasks"]:
        play_task(task)

    return None
