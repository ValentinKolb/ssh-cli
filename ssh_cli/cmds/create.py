import os
import subprocess

import inquirer
import validators
from sshconf import read_ssh_config
from termcolor import cprint

from .interface import Command
from ..config import DEFAULT_USER, SSH_DEFAULT_PORT, CONFIG_FILE_PATH, KEY_DIR_PATH, KEY_TYPE
from ..lib import show_host_config
from ..validation import is_valid_hostname, is_not_empty, host_exists, is_number


def _create_key_file(host) -> str or int or None:
    if not inquirer.confirm("Do you want to use a passkey?", default=True):
        return None
    password = inquirer.password("Enter a password for the key file (optional)") or ""
    key_file = f'{KEY_DIR_PATH}/{host}'
    res = subprocess.run(
        ["ssh-keygen",
         "-t", KEY_TYPE,
         "-C", f"'key_for_{host}'",
         "-f", key_file,
         "-N", password,
         "-q"
         ])
    if res.returncode != 0:
        cprint(f"Error creating key file: {res.stderr}", "red")
        return None
    return key_file


class CreateHostConfig(Command):
    """
    This class prompts the user to enter the details for a new host and then creates it in the ssh config file.
    """

    @property
    def help(self):
        return "Create a new host"

    @property
    def cmd(self):
        return "create"

    def run(self, *args, **kwargs) -> int:
        """
        This function prompts the user to enter the details for a new host and then creates it in the ssh config file.
        It also prompts the user to create a key file for the host.
        """
        c = read_ssh_config(CONFIG_FILE_PATH)

        host_config_questions = [
            inquirer.Text(
                "hostname",
                message="Hostname (e.g. example.com)",
                validate=is_valid_hostname
            ),
            inquirer.Text(
                "host",
                message="Enter a name for this host (e.g. example)",
                validate=lambda _, x: is_not_empty(_, x) and host_exists(_, x),
                default=lambda ans: ans["hostname"].split(".")[0] if validators.domain(ans["hostname"]) else None
            ),
            inquirer.Text(
                "user",
                message="Enter the username for this host",
                default=DEFAULT_USER
            ),
            inquirer.Text(
                "port",
                message="Enter the port for this host",
                default=SSH_DEFAULT_PORT,
                validate=is_number
            ),
        ]

        if (answers := inquirer.prompt(host_config_questions)) is None:
            return 1

        c.add(answers["host"], Hostname=answers["hostname"], User=answers["user"], Port=answers["port"])

        if key_file := _create_key_file(answers["host"]):
            c.set(answers["host"], IdentityFile=key_file)

        print("Host configured with the following configuration:")
        show_host_config(answers["host"], c)

        if not inquirer.confirm("Do you want to save this host?", default=True):
            if key_file:
                os.remove(key_file)
                os.remove(f'{key_file}.pub')
            cprint(f'Host {answers["host"]} not saved', "yellow")
            return 1

        c.write(CONFIG_FILE_PATH)
        cprint(f'Host {answers["host"]} saved', "green")

        return 0
