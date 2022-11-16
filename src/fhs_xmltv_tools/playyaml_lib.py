"""Playyaml file.

version: 0.5.1
"""

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


def check_items_in_2_lists(list1, list2):
    """Check items in 2 lists returns True in at least one item matches.

    Args:
        list1: list of strings
        list2: list of strings

    Returns:
        bool: minimal one item matched
    """
    for i in list1:  # noqa:SIM110
        if i in list2:
            return True
    return False


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


def check_arguments_in_task(task, command_dict):
    """Check arguments in task.

    Args:
        task: task array
        command_dict: command_dict array

    Returns:
        Boolean arguments correct
    """
    if "args" not in command_dict:
        # no arguments needed for this functions
        return True
    for arg in command_dict["args"]:
        argname = arg.get("name", "unknown_name")
        arghelp = arg.get("help", None)
        argdefault = arg.get("default", None)
        argtype = arg.get("type", "string")
        if argname in task:
            if argtype == "boolean":
                task[argname] = task[argname].lower() == "true"
            continue
        if argdefault is not None:
            task[argname] = argdefault
            if argtype == "boolean":
                task[argname] = task[argname].lower() == "true"
            continue
        # so if here we are missing a argname without a default so mandatoy
        sys.stderr.write(
            f"ERROR: missing argument {argname} for {arghelp or '<No Help>'} in {str(task)}"
        )
        return False
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


def loop_play_task(
    command_dict, task, *, include_tags=None, exclude_tags=None, funcdict
):
    """Handle a task that can loop.

    Args:
        command_dict: function info
        task: task array
        include_tags: list of tags to run
        exclude_tags: list of tags to skip
        funcdict: function dict

    Returns:
        Good: boolean
    """
    loop = command_dict.get("loop", None)
    if type(task[loop]) != list:
        print(f"loop variable {loop} in task but not a list.")
        exit(1)
    for i in task[loop]:
        new_task = task.copy()
        del new_task[loop]
        for p in i:
            new_task[p] = i[p]
        play_task(
            new_task,
            include_tags=include_tags,
            exclude_tags=exclude_tags,
            funcdict=funcdict,
        )
    return True


def play_loop(task):
    """Play command load_m3u_file.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    import copy

    with_items = task["with_items"]
    funcdict = task["funcdict"]
    for i in with_items:
        tasks = copy.deepcopy(task["tasks"])
        if type(i) == str:
            print(i)
            for loop_task in tasks:
                for key in loop_task:
                    if loop_task[key] == "__ITEM__":
                        loop_task[key] = i
                play_task(loop_task, funcdict=funcdict)
            pprint(tasks)
    return True


def play_task(task, *, include_tags=None, exclude_tags=None, funcdict):
    """Play a task.

    Args:
        task: task array
        include_tags: list of tags to run
        exclude_tags: list of tags to skip
        funcdict: function dict

    Returns:
        Good: boolean
    """
    check_console()
    task_name = task.get("name", task.get("command", "unknown"))
    if task_check_tag(task, include_tags=include_tags, exclude_tags=exclude_tags):
        print(f"running task: {task_name}")
    else:
        print(f"skipping task: {task_name}")
        return True

    if "command" not in task:
        sys.stderr.write(f"missing command entry in task {str(task)}")
        exit(3)

    if task["command"] == "loop":
        task["funcdict"] = funcdict

    command_dict = funcdict.get(task["command"], None)
    if command_dict is None:
        print("unknown task:  {task['command']}")
        pprint(task)
        return True

    loop = command_dict.get("loop", None)
    if loop is not None and loop in task:
        loop_play_task(
            command_dict,
            task,
            include_tags=include_tags,
            exclude_tags=exclude_tags,
            funcdict=funcdict,
        )
        return True

    if check_arguments_in_task(task, command_dict) is False:
        print("missing arguments in task.")
        exit(1)

    if "func" in command_dict:
        command_dict["func"](task)
    return True


def play(commandfile, *, include_tags=None, exclude_tags=None, funcdict):
    """Play commandfile.

    Args:
        commandfile: yaml file with instructions
        include_tags: list of tags to run
        exclude_tags: list of tags to skip
        funcdict: dicts with options

    Returns:
        None
    """
    check_console()
    data = load_yaml(commandfile)

    if "tasks" not in data:
        sys.stderr.write("missing tasks entrie in yaml file")
        exit(2)

    for task in data["tasks"]:
        play_task(
            task,
            include_tags=include_tags,
            exclude_tags=exclude_tags,
            funcdict=funcdict,
        )

    return None


def func_dict_parse(funcdict, for_type=None):
    """Parse func dict dict.

    Args:
        funcdict: dict with all the commands
        for_type: interactive or None at this moment.

    Returns:
        funcdict: parsed
    """
    new_funcdict = dict()
    for p in funcdict:
        cur_func = funcdict[p]
        if cur_func.get("hidden", False) is True:
            continue
        if (
            for_type == "interactive"
            and cur_func.get("interactive_hidden", False) is True
        ):
            continue
        new_funcdict[p] = cur_func
    new_funcdict["loop"] = {
        "args": [{"name": "with_items"}, {"name": "tasks"}],
        "func": play_loop,
        "help": "loop over multiple tasks",
    }
    return new_funcdict
