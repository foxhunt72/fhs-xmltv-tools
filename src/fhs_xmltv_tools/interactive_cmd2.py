import textwrap
from jinja2 import Template
import sys
import cmd2
import os
import yaml
from pathlib import Path
from pprint import pprint

from .playyaml_lib import play_task
from .__version__ import __app_name__,__version__


def clean_task(task, orig_func):
    """Clean task.

    Args:
        task: dict with all the tasks.
        orig_func: default functions.

    Returns:
        cleaned taskdict
    """
    for arg in orig_func['args']:
        if arg['name'] in task:
            if task[arg['name']] == arg.get('default', '_____unknown_____'):
                del task[arg['name']]
    return task


def clean_tasks(taskdict, funcdict):
    """Clean tasks.

    Args:
        taskdict: dict with all the tasks.
        funcdict: default functions.

    Returns:
        cleaned taskdict
    """
    for t in taskdict:
        my_orig_func = funcdict[t['command']]
        clean_task(t, my_orig_func)
    return taskdict


def save_tasks(filename, taskdict, funcdict):
    """Save tasks to file.

    Args:
        filename: save filename
        taskdict: save dict to task
        funcdict: funcdict we are going to use to remove the default args from tasks
    """
    taskdict = clean_tasks(taskdict, funcdict)

    with Path(filename).open("w") as target:
        yaml.dump({'tasks': taskdict}, target)


def add_argument_from_dict(input):
    """Create arguments text from dict input.

    Args:
        input: dicts with arg info

    Returns:
        String
    """
    if 'help' in  input:
        help_str=f", help='{input['help']}'"
    else:
        help_str=""
    if 'default' in input:
        default_str=f", default='{input['default']}'"
    else:
        default_str=", required=True"
    return f"'--{input['name']}', type=str{default_str}{help_str}"


def create_cmd2_class_str(my_dict):
    test_str = textwrap.dedent("""\
    class CmdLineApp(cmd2.Cmd):
        def __init__(self, funcdict, hist_file, prompt):
            super().__init__()
            self.__funcdict = funcdict
            self.__tasks = []
            self.prompt = prompt
            cmd2.Cmd.__init__(self, persistent_history_file=hist_file, persistent_history_length=200)
            del cmd2.Cmd.do_edit, cmd2.Cmd.do_alias
            del cmd2.Cmd.do_macro, cmd2.Cmd.do_run_pyscript
            del cmd2.Cmd.do_shortcuts, cmd2.Cmd.do_run_script
        # Setting this true makes it run a shell command if a cmd2/cmd command doesn't exist
        # default_to_shell = True
        save_tasks_parser = cmd2.Cmd2ArgumentParser()
        save_tasks_parser.add_argument('--file', type=str, help='filename to save.', required=True)

        @cmd2.with_argparser(save_tasks_parser)
        def do_save_tasks(self, args):
            \"\"\"Save tasks file to disk, to reuse.\"\"\"
            save_tasks(args.file, self.__tasks, self.__funcdict)


        {% for key, my_func in my_dict.items() %}
        {% if 'args' in my_func -%}
        {{ key }}_parser = cmd2.Cmd2ArgumentParser()
        {% for item in my_func['args'] -%}
        {{ key }}_parser.add_argument({{ add_argument_from_dict(item) }})
        {% endfor -%}
        #
        @cmd2.with_argparser({{ key }}_parser)
        def do_{{ key }}(self, args):
            \"\"\"{{ my_func['help'] }}.\"\"\"
            task = {
                'command': '{{ key }}',
                {% for item in my_func['args'] -%}
                '{{ item['name'] }}': args.{{ item['name'] }},
                {% endfor -%}
            }
            self.__tasks.append(task)
            play_task(task, funcdict=self.__funcdict)
        {% else -%}
        # no args
        {% endif -%}
        {% endfor -%}

    """)
    j2_template = Template(test_str)
    func_dict = {
        'add_argument_from_dict': add_argument_from_dict
    }

    j2_template.globals.update(func_dict)


    return j2_template.render({'my_dict': my_dict})


def run_cmd2(funcdict):
    test_str = create_cmd2_class_str(funcdict)
    #print(test_str)
    hist_file = os.path.expanduser(f"~/.{__app_name__}.history")
    exec(test_str, None, globals())
    c = CmdLineApp(funcdict, hist_file, prompt=f"({__app_name__}) ") # cmdline
    sys.exit(c.cmdloop())
