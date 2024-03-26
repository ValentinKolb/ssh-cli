from pathlib import Path

import inquirer
from sshconf import read_ssh_config, SshConfig
from termcolor import colored

from .config import CONFIG_FILE_PATH, CANCEL


def get_public_key(host, c) -> str | None:
    """
    This function reads the public key file for a host and returns its content.
    :param host: The host name
    :param c: The ssh config object
    :return: The content of the public key file or None if the file doesn't exist
    """
    if c.host(host) is None:
        return

    if not (key_file := c.host(host).get("identityfile")):
        return

    path = f'{key_file}.pub'

    if not Path(path).exists():
        return f"public key file not found"

    with open(path) as file:
        return file.read().strip()


def select_host() -> str | None:
    """
    This function prompts the user to select a host from the ssh config file.
    :return: The selected host (hostname) or None if the user cancels
    """
    c = read_ssh_config(CONFIG_FILE_PATH)
    questions = [
        inquirer.List(
            "host",
            message="Select the Host?",
            choices=[CANCEL, *sorted(c.hosts())]
        ),
    ]
    answers = inquirer.prompt(questions)

    if answers["host"] == CANCEL or answers is None:
        return

    return answers["host"]


def confirm_action(message=None) -> bool:
    """
    This function prompts the user to confirm an action.
    :param message: The message to display (default: "Are you sure?")
    :return: True if the user confirms, False otherwise
    """
    return inquirer.confirm(message or "Are you sure?", default=False)


def show_host_config(host: str, c: SshConfig):
    """
    This function prints the configuration of a host.
    :param host: The host name
    :param c: The ssh config object
    """
    print(f"Host: {colored(host, attrs=['bold'])}")
    for key in c.host(host).keys():
        print(f"\t{key}: {colored(c.host(host).get(key), attrs=['underline'])}")
    if public_key := get_public_key(host, c):
        print(f"Public key: {colored(public_key, attrs=['reverse'])}")
