import os
import subprocess

from sshconf import read_ssh_config
from termcolor import cprint

from .interface import Command
from ..config import CONFIG_FILE_PATH
from ..lib import select_host, confirm_action


class Delete(Command):
    """
    This class implements the "delete" command that deletes a host from the ssh config file.
    """

    @property
    def help(self):
        return "Delete a host (and keys) from the ssh config"

    @property
    def cmd(self):
        return "delete"

    def run(self, *args, **kwargs) -> int:
        """
        This function prompts the user to select a host from the ssh config file and then deletes it.
        """
        c = read_ssh_config(CONFIG_FILE_PATH)

        host = select_host()

        if host is None:
            return 1

        # ask user to confirm
        if not confirm_action():
            cprint("Cancelled deleting", "yellow")
            return 1

        # remove key file if it exists
        if key_file := c.host(host).get("identityfile"):
            try:
                os.remove(key_file)
                os.remove(f'{key_file}.pub')
                cprint(f'Removed key files for host {host} ({key_file}(.pub))', "green")
            except FileNotFoundError:
                cprint(f"Key files not found: {key_file}(.pub)", "red")

        # remove from known_hosts file
        res = subprocess.run(["ssh-keygen", "-R", host])
        if res.returncode != 0:
            cprint(f"Error removing host from known_hosts file: {res.stderr}", "red")
        else:
            cprint(f'Removed host {host} from known_hosts file', "green")

        # remove host
        c.remove(host)
        c.write(CONFIG_FILE_PATH)
        cprint(f'Removed host {host}', "green")
