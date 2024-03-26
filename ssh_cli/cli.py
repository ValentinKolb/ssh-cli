import os
import subprocess
from pathlib import Path

import inquirer
import validators
from prettytable import PrettyTable
from sshconf import read_ssh_config
from termcolor import cprint, colored

from .config import CONFIG_FILE_PATH, KEY_DIR_PATH, DEFAULT_USER, SSH_DEFAULT_PORT, EDITOR, CANCEL, KEY_TYPE
from .validation import is_number, is_not_empty, is_valid_hostname, host_exists


def get_public_key(host) -> str | None:
    """
    This function reads the public key file for a host and returns its content.
    :param host: The host name
    :return: The content of the public key file or None if the file doesn't exist
    """
    c = read_ssh_config(CONFIG_FILE_PATH)

    if c.host(host) is None:
        return

    if not c.host(host).get("identityfile"):
        return

    path = f'{c.host(host).get("identityfile")}.pub'

    if not Path(path).exists():
        return f"public key file not found at {path}"

    with open(path) as file:
        return colored(file.read().strip(), "white", "on_black")


def cmd_list():
    """
    This function lists all the hosts in the ssh config file and prints them in a table.
    """
    c = read_ssh_config(CONFIG_FILE_PATH)

    table = PrettyTable()

    table.field_names = ["Name", "Host", "Public Key", "User", "Port"]
    table.add_rows(
        [
            [
                host,
                c.host(host).get("hostname"),
                get_public_key(host) or "--",
                c.host(host).get("user"),
                c.host(host).get("port")
            ]
            for host in sorted(c.hosts())
        ]
    )

    cprint(table)


def cmd_connect():
    """
    This function prompts the user to select a host from the ssh config file and then connects to it.
    """
    c = read_ssh_config(CONFIG_FILE_PATH)
    questions = [
        inquirer.List(
            "host",
            message="Select the Host you want to connect to?",
            choices=[CANCEL, *sorted(c.hosts())]
        ),
    ]
    answers = inquirer.prompt(questions)

    if answers["host"] == CANCEL:
        return

    print(f"Connecting to {answers['host']}")

    res = subprocess.run(["ssh", answers["host"]])
    if res.returncode != 0:
        cprint(f"Error connecting to host{f' : {res.stderr}' if res.stderr else ''}", "red")
        return

    if os.getenv("HOSTNAME"):
        print()
        cprint(f"Welcome back on {os.getenv('HOSTNAME')}!", "green")


def cmd_create():
    """
    This function prompts the user to enter the details for a new host and then creates it in the ssh config file.
    It also prompts the user to create a key file for the host.
    """
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

    answers = inquirer.prompt(host_config_questions)

    if answers is None:
        return

    c = read_ssh_config(CONFIG_FILE_PATH)

    c.add(answers["host"], Hostname=answers["hostname"], User=answers["user"], Port=answers["port"])

    key_file = None
    if inquirer.confirm("Do you want to use a passkey?", default=True):
        host = answers["host"]
        key_file = f'{KEY_DIR_PATH}/{host}'
        res = subprocess.run(["ssh-keygen", "-t", KEY_TYPE, "-C", f"'key_for_{host}'", "-f", key_file, "-q"])
        if res.returncode != 0:
            cprint(f"Error creating key file: {res.stderr}", "red")
            return
        c.set(host, IdentityFile=key_file)

    print("Host created with the following configuration:")
    for key in c.host(answers["host"]).keys():
        print(key, c.host(answers["host"]).get(key))

    if inquirer.confirm("Do you want to save this host?", default=True):
        c.write(CONFIG_FILE_PATH)
        cprint(f'Host {answers["host"]} saved', "green")

        if key_file:
            with open(f'{key_file}.pub') as file:
                public_key = file.read().strip()
            cprint(f"Public key for {answers['host']}: {colored(public_key, 'white', 'on_black')}")
            cprint(f'Key file for host {answers["host"]} saved at {key_file}', "green")
    else:
        # remove key file again if it was created
        if key_file:
            os.remove(key_file)
            os.remove(f'{key_file}.pub')
        cprint(f'Host {answers["host"]} not saved', "yellow")


def cmd_delete():
    """
    This function prompts the user to select a host from the ssh config file and then deletes it.
    It also deletes the key file if it exists.
    """
    c = read_ssh_config(CONFIG_FILE_PATH)
    questions = [
        inquirer.List(
            "host",
            message="Select the Host you want to delete?",
            choices=[CANCEL, *sorted(c.hosts())]
        ),
    ]
    answers = inquirer.prompt(questions)

    if answers["host"] == CANCEL or answers is None:
        return

    # ask user to confirm
    if not inquirer.confirm(f"Are you sure you want to delete {answers['host']}?", default=False):
        cprint("Cancelled deleting", "yellow")
        return

    # remove key file if it exists
    key_file = c.host(answers["host"]).get("identityfile")
    if key_file:
        os.remove(key_file)
        os.remove(f'{key_file}.pub')
        cprint(f'Removed key file for host {answers["host"]} ({key_file})', "green")

    # remove from known_hosts file
    res = subprocess.run(["ssh-keygen", "-R", answers["host"]])
    if res.returncode != 0:
        cprint(f"Error removing host from known_hosts file: {res.stderr}", "red")
    else:
        cprint(f'Removed host {answers["host"]} from known_hosts file', "green")

    # remove host
    c.remove(answers["host"])
    c.write(CONFIG_FILE_PATH)
    cprint(f'Removed host {answers["host"]}', "green")


def cmd_cleanup():
    """
    This function removes all key files that are not in the ssh config file.
    """
    c = read_ssh_config(CONFIG_FILE_PATH)

    cprint("This will remove all key files that are not in the ssh config", "yellow")

    # ask user to confirm
    if not inquirer.confirm("Are you sure you want to cleanup?", default=False):
        cprint("Cancelled cleanup", "yellow")
        return

    # read all key files
    try:
        key_files = [f for f in os.listdir(KEY_DIR_PATH) if os.path.isfile(os.path.join(KEY_DIR_PATH, f))]
    except FileNotFoundError:
        cprint("No key files found", "yellow")
        return

    # remove key files that are not in the ssh config
    for key_file in key_files:
        host = key_file.removesuffix(".pub")
        if host not in c.hosts():
            try:
                os.remove(f'{KEY_DIR_PATH}/{key_file}')
                cprint(f'Removed key file `{key_file}`', "green")
            except FileNotFoundError:
                cprint(f'Key file `{key_file}` could not be removed', "yellow")

    # todo clean up known_hosts file

    cprint("Cleanup complete", "green")


def cmd_editor():
    """
    This function opens the ssh config file in the default editor.
    """
    res = subprocess.run([EDITOR, CONFIG_FILE_PATH])
    if res.returncode != 0:
        cprint(f"Error opening config file: {res.stderr}", "red")
        return

    cprint("Config file saved, cleaning up ...", "green")
    cmd_cleanup()
