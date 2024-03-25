import inquirer
from termcolor import cprint

from .cli import cmd_cleanup, cmd_connect, cmd_create, cmd_delete, cmd_editor, cmd_list


def main():
    """
    This is the main function that starts the tool and prompts the user to select an action.
    """
    print()
    cprint("Welcome to the SSH Tool", "green")
    print()
    cprint("This tool helps you manage your ssh config and keys", "green")
    cprint("(c) Valentin Kolb 2024", "green")

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

    cprint("Exiting - run `ssh-cli` to start again.", "yellow")


if __name__ == "__main__":
    main()
