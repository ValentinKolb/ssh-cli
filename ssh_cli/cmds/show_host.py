from sshconf import read_ssh_config

from .interface import Command
from ..config import CONFIG_FILE_PATH
from ..lib import show_host_config, select_host


class ShowHost(Command):
    """
    This class implements the "show" command that shows the details of a host.
    """
    @property
    def help(self):
        return "Show the details of a host"

    @property
    def cmd(self):
        return "show"

    def run(self, *args, **kwargs) -> int:
        if not (host := select_host()):
            return 1

        c = read_ssh_config(CONFIG_FILE_PATH)

        show_host_config(host, c)

        return 0
