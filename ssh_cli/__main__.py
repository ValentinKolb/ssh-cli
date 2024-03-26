from argparse import ArgumentParser

import inquirer
from termcolor import cprint

from .cli import cmd_cleanup, cmd_connect, cmd_create, cmd_delete, cmd_editor, cmd_list
from .config import CONFIG_FILE_PATH, KEY_DIR_PATH, KEY_TYPE, DEFAULT_USER, SSH_DEFAULT_PORT, EDITOR, VERSION


def show_config():
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


def show_title():
    """
    This function prints the welcome title.
    """
    print()
    cprint("Welcome to the SSH CLI Tool", "green")
    print()
    cprint("This tool helps you manage your ssh config and keys", "green")
    cprint("(c) Valentin Kolb 2024", "green")
    print()


def run_shell():
    """
    This is the main function that starts the tool and prompts the user to select an action.
    """
    questions = [
        inquirer.List(
            "cmd",
            message="What do you want to do?",
            choices=[
                "Connect to host",
                "List hosts",
                "Create a new host",
                "Delete a host",
                "Edit config file",
                "Cleanup",
                "Exit"
            ],
        ),
    ]

    while True:
        answers = inquirer.prompt(questions)

        if answers is None and inquirer.confirm("Do you want to exit?", default=True):
            break
        elif answers is None:
            continue

        match answers["cmd"]:
            case "Connect to host":
                cmd_connect()
            case "List hosts":
                cmd_list()
            case "Create a new host":
                cmd_create()
            case "Delete a host":
                cmd_delete()
            case "Edit config file":
                cmd_editor()
            case "Cleanup":
                cmd_cleanup()
            case "Exit":
                break
            case _:
                print("Invalid option")

        print()

    cprint("Exiting - run `ssh-cli` to start again.", "yellow")


def main():
    """
    This function parses the command line arguments and runs the appropriate function.
    """

    # create a parser object
    parser = ArgumentParser(
        description="A simple CLI tool to manage your ssh config and keys",
    )

    # add arguments
    parser.add_argument("--shell", action="store_true", help="Run the interactive shell")
    parser.add_argument("--connect", action="store_true", help="Connect to a host")
    parser.add_argument("--list", action="store_true", help="List hosts")
    parser.add_argument("--create", action="store_true", help="Create a new host")
    parser.add_argument("--delete", action="store_true", help="Delete a host")
    parser.add_argument("--edit", action="store_true", help="Edit the config file")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup")
    parser.add_argument("--show-config", action="store_true", help="Show the config of this tool")
    parser.add_argument("--version", action="store_true", help="Print the version of the tool")

    args = parser.parse_args()

    # show the title
    show_title()

    # run the appropriate function
    if args.shell:
        run_shell()
    elif args.version:
        print(VERSION)
    elif args.connect:
        cmd_connect()
    elif args.list:
        cmd_list()
    elif args.create:
        cmd_create()
    elif args.delete:
        cmd_delete()
    elif args.edit:
        cmd_editor()
    elif args.cleanup:
        cmd_cleanup()
    elif args.show_config:
        show_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
