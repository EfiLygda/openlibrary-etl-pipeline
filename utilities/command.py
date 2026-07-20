"""
Module for running commands via the command line
"""

import subprocess

def run_command(
        cmd: list[str],
        ignore_errors: bool = False,
        debug: bool = False,
) -> subprocess.CompletedProcess[str]:
    """
    Function for running a command via the command line

    :param cmd: list[str], the command as a list
    :param ignore_errors: bool, whether to ignore errors or not
    :param debug: bool, whether to display stdout and stderr

    """

    # Run the command by capturing its output as text
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    # Print the standard output of the command
    if debug and result.stdout:
        print(result.stdout)

    # Print the standard error of the command
    if debug and result.stderr:
        print(result.stderr)

    # If an error occurred raise a CalledProcessError
    if result.returncode != 0 and not ignore_errors:
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=cmd,
            output=result.stdout,
            stderr=result.stderr
        )

    return result