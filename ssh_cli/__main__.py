from argparse import ArgumentParser
from importlib.metadata import version

import inquirer
from termcolor import cprint

from .cmds import CreateCmd, ConnectCmd, DeleteCmd, EditorCmd, ListCmd, ShowHostCmd, CleanupCmd
from .cmds.interface import Command
from .config import CONFIG_FILE_PATH, KEY_DIR_PATH, KEY_TYPE, DEFAULT_USER, SSH_DEFAULT_PORT, EDITOR

COMMANDS = [ListCmd(), ShowHostCmd(), ConnectCmd(), CreateCmd(), DeleteCmd(), EditorCmd(), CleanupCmd()]


def _show_title():
    """
    This function prints the welcome title.
    """
    print()
    cprint("Welcome to the SSH CLI Tool", "green")
    print()
    cprint("This tool helps you manage your ssh config and keys", "green")
    cprint("(c) Valentin Kolb 2024", "green")
    print()


class ShowCLIConfig(Command):

    @property
    def help(self):
        return "Show the configuration of the CLI"

    @property
    def cmd(self):
        return "config"

    def run(self, *args, **kwargs) -> int:
        """
        This function prints the configuration of this tool.
        """
        cprint("Configuration", "green")
        cprint(f"Config file path: {CONFIG_FILE_PATH}")
        cprint(f"Key directory path: {KEY_DIR_PATH}")
        cprint(f"Key type: {KEY_TYPE}")
        cprint(f"Default user: {DEFAULT_USER}")
        cprint(f"Default port: {SSH_DEFAULT_PORT}")
        cprint(f"Editor: {EDITOR}")
        return 0


class ShellCmd(Command):

    @property
    def help(self):
        return "Start the interactive shell"

    @property
    def cmd(self):
        return "shell"

    def run(self, *args, **kwargs) -> int:

        questions = [
            inquirer.List(
                "cmd",
                message="What do you want to do?",
                choices=[cmd.help for cmd in COMMANDS],
            ),
        ]

        while True:
            answers = inquirer.prompt(questions)

            if answers is None and inquirer.confirm("Do you want to exit?", default=True):
                break
            elif answers is None:
                continue

            for cmd in COMMANDS:
                if cmd.help == answers["cmd"]:
                    cmd.run()
                    break
            else:
                cprint("Invalid option", "red")

            print()

        cprint("Exiting - run `ssh-cli` to start again.", "yellow")
        return 0


class VersionCmd(Command):

    @property
    def help(self):
        return "Show the version of this tool"

    @property
    def cmd(self):
        return "version"

    def run(self, *args, **kwargs) -> int:
        cprint(f"ssh-cli v{version(__package__ or __name__)}", "green")
        return 0


def main():
    """
    This function parses the command line arguments and runs the appropriate function.
    """

    # create a parser object
    parser = ArgumentParser(
        description="A simple CLI tool to manage your ssh config",
    )

    commands = [ShellCmd(), *COMMANDS, ShowCLIConfig(), VersionCmd()]

    # add the arguments
    for cmd in commands:
        parser.add_argument(f"--{cmd.cmd}", action="store_true", help=cmd.help)

    args = parser.parse_args()

    # show the title
    _show_title()

    # run the appropriate function
    for cmd in commands:
        if getattr(args, cmd.cmd):
            code = cmd.run()
            exit(code)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
