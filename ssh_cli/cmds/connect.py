import os
import subprocess

from termcolor import cprint

from .interface import Command
from ..lib import select_host


class Connect(Command):
    """
    This class implements the "connect" command that connects to a host.
    """

    @property
    def help(self):
        return "Connect to a host via ssh"

    @property
    def cmd(self):
        return "connect"

    def run(self, *args, **kwargs) -> int:
        """
        This function prompts the user to select a host from the ssh config file and then connects to it.
        """
        if not (host := select_host()):
            return 1

        cprint(f"Connecting to {host}", "green")

        # run the ssh command
        code = subprocess.run(["ssh", host])

        # print a welcome message if the connection was successful
        if code == 0 and os.getenv("HOSTNAME"):
            print()
            cprint(f"Welcome back on {os.getenv('HOSTNAME')}!", "green")

        return 0
