"""Entry point for PyFyre CLI installed via pip or setuptools.

Example:
    >>> pyfyre create hello-world
"""

import os
import sys
import pathlib
from typing import List, Optional

_HELP_MESSAGE = (
    "Commands:\n"
    "    pyfyre help\n"
    "        Show this message.\n"
    "    pyfyre version\n"
    "        Show the current version of PyFyre.\n"
    "    pyfyre create [path]\n"
    "        Create a new PyFyre project in the specified path.\n"
    "        If no path is supplied, the default is 'pyfyre-app'.\n"
    "        The directory name of the path will be your project's name.\n"
    "    pyfyre run\n"
    "        Run the PyFyre project in the current directory in development mode.\n"
    "    pyfyre build\n"
    "        Build the PyFyre project in the current directory for production.\n"
)


def execute(args: Optional[List[str]] = None) -> None:
    args = args or sys.argv
    args_list: List[Optional[str]] = [None, None, None]

    for index, arg in enumerate(args):
        try:
            args_list[index] = arg
        except IndexError:
            break

    command = args_list[1] or "help"

    if command == "help":
        print(_HELP_MESSAGE)
    elif command == "version":
        print("PyFyre 0.6.4-alpha")
    elif command == "create":
        from pyfyre_cli.create_app import create_app

        app_name = args_list[2] or "pyfyre-app"
        app_path = pathlib.Path(os.path.abspath(app_name))
        app_path_parts = app_path.parts[:-1]

        if not app_path_parts:
            print("You can't create a project in that directory.")
        else:
            create_app(app_path.parts[-1], os.path.join(*app_path_parts))
    elif command == "run":
        from pyfyre_cli.run_app import run_app

        run_app()
    elif command == "build":
        from pyfyre_cli.build_app import build_app

        build_app(production=True)
    else:
        print("Command not found.")
        print(_HELP_MESSAGE)
