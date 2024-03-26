from prettytable import PrettyTable
from sshconf import read_ssh_config
from termcolor import cprint

from .interface import Command
from ..config import CONFIG_FILE_PATH


class ListHosts(Command):
    """
    This class implements the "list" command that lists all the hosts in the ssh config file.
    """

    @property
    def help(self):
        return "List all the hosts in the ssh config file"

    @property
    def cmd(self):
        return "list"

    def run(self, *args, **kwargs) -> int:
        """
        This function lists all the hosts in the ssh config file and prints them in a table.
        """
        c = read_ssh_config(CONFIG_FILE_PATH)

        table = PrettyTable()

        table.field_names = ["Name", "Host"]
        table.add_rows(
            [
                [
                    host,
                    c.host(host).get("hostname"),
                ]
                for host in sorted(c.hosts())
            ]
        )

        cprint(table)

        return 0
