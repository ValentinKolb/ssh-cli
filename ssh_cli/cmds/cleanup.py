import os

from sshconf import read_ssh_config
from termcolor import cprint

from .interface import Command
from ..config import CONFIG_FILE_PATH, KEY_DIR_PATH
from ..lib import confirm_action


def _cleanup_key_files(c):
    """
    This function removes all key files that are not in the ssh config file.
    :param c: the ssh config object
    """

    # step 1, get all key files from ssh config
    used_key_files = [c.host(host).get("identityfile") for host in c.hosts()]

    # step 2, get all key files from key directory
    found_key_files = set(
        os.path.join(KEY_DIR_PATH, f).removesuffix(".pub")
        for f in os.listdir(KEY_DIR_PATH)
        if os.path.isfile(os.path.join(KEY_DIR_PATH, f))
    )

    # step 3, get all key files that are not in the ssh config
    unused_key_files = [key_file for key_file in found_key_files if key_file not in used_key_files]

    # step 4, remove all key files that are not in the ssh config
    for key_file in unused_key_files:

        if not confirm_action(f"Remove key files `{key_file}` and `{key_file}.pub`?"):
            cprint(f"Skipping ...", "green")
            continue

        try:
            os.remove(key_file)
            cprint(f'Removed key files `{key_file}`', "green")
        except FileNotFoundError:
            cprint(f'Key files `{key_file}` could not be removed', "yellow")

        try:
            os.remove(f'{key_file}.pub')
            cprint(f'Removed public key files `{key_file}.pub`', "green")
        except FileNotFoundError:
            cprint(f'Public key files `{key_file}.pub` could not be removed', "yellow")


class CleanupKeys(Command):
    """
    This class implements the "cleanup" command that removes all key files that are not in the ssh config.
    """

    @property
    def cmd(self):
        return "cleanup"

    @property
    def help(self):
        return "Cleanup all key files that are not in the ssh config"

    def run(self):
        c = read_ssh_config(CONFIG_FILE_PATH)

        cprint("This will remove all key files that are not in uns in the ssh config", "yellow")

        # remove all key files that are not in the ssh config
        _cleanup_key_files(c)

        cprint("Cleanup complete", "green")
        return 0
