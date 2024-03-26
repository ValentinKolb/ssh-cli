import subprocess

from termcolor import cprint

from .interface import Command
from ..config import EDITOR, CONFIG_FILE_PATH


class Editor(Command):
    """
    This class implements the "editor" command that opens the ssh config file in the default editor.
    """

    @property
    def help(self):
        return "Edit the ssh config file"

    @property
    def cmd(self):
        return "editor"

    def run(self, *args, **kwargs) -> int:
        """
        This function opens the ssh config file in the default editor.
        """
        res = subprocess.run([EDITOR, CONFIG_FILE_PATH])
        if res.returncode != 0:
            cprint(f"Error opening config file: {res.stderr}", "red")
            return 1

        cprint("Config file saved, consider calling cleanup ...", "green")
        return 0
