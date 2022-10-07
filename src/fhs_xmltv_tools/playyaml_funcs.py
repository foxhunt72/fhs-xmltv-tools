"""Extra functions for command playyaml."""

import subprocess  # noqa:S404


def execute_command(command, shell=False, capture_output=True, text=True):
    """Execute a command..

    Args:
        command: command to execute as array (shell=False) or as string (shell=True)
        shell: boolean using shell (like pipe commands in bash)
        capture_output: capture output from command
        text: output is Text

    Returns:
        output of subprocess  .stdout / .stderr / .returncode
    """
    return subprocess.run(  # noqa:DUO116
        command, shell=shell, capture_output=capture_output, text=text  # noqa:S602
    )


def base64_2_str(base64_message):
    """Convert base64 message to text.

    Args:
        base64_message: base64 message you want to decode

    Returns:
        message: as type str
    """
    import base64

    base64_bytes = base64_message.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("ascii")
    return message


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
