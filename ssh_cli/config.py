import os
import sys
from pathlib import Path

from termcolor import cprint

CONFIG_FILE_PATH = os.getenv("SSH_CLI_CONFIG_PATH") or str(Path.home()) + "/.ssh/config"
KEY_DIR_PATH = os.getenv("SSH_CLI_KEY_DIR") or str(Path.home()) + "/.ssh/keys"
KEY_TYPE = os.getenv("SSH_CLI_KEY_TYPE") or "ed25519"
DEFAULT_USER = os.getenv("SSH_CLI_DEFAULT_USER") or os.getenv("USER")
SSH_DEFAULT_PORT = os.getenv("SSH_CLI_DEFAULT_PORT") or 22
EDITOR = os.getenv("SSH_CLI_EDITOR") or os.getenv("EDITOR") or "nano"
CANCEL = "❌  Cancel"

if 'pytest' not in sys.modules.keys():
    # check if the config file exists
    if not Path(CONFIG_FILE_PATH).exists():
        # create the config file if it doesn't exist
        Path(CONFIG_FILE_PATH).touch()
        cprint(f"Config file created at {CONFIG_FILE_PATH}", "yellow")

    # check if the key directory exists
    if not Path(KEY_DIR_PATH).exists():
        # create the key directory if it doesn't exist
        Path(KEY_DIR_PATH).mkdir(parents=True)
        cprint(f"Key directory created at {KEY_DIR_PATH}", "yellow")

    # check if all the required environment variables are set
    if not DEFAULT_USER:
        raise ValueError("Environment variable USER not set, please set it to your username")
