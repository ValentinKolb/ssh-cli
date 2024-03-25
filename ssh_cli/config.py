import os
from pathlib import Path

CONFIG_FILE_PATH = os.getenv("SSH_CONFIG_PATH") or str(Path.home()) + "/.ssh/config"
KEY_DIR_PATH = os.getenv("SSH_KEY_DIR") or str(Path.home()) + "/.ssh/keys"
DEFAULT_USER = os.getenv("USER")
SSH_DEFAULT_PORT = os.getenv("SSH_DEFAULT_PORT") or 22
EDITOR = os.getenv("EDITOR") or "nano"
CANCEL = "❌  Cancel"

# check if the config file exists
if not Path(CONFIG_FILE_PATH).exists():
    raise FileNotFoundError(f"Config file not found at {CONFIG_FILE_PATH}")

# check if the key directory exists
if not Path(KEY_DIR_PATH).exists():
    raise FileNotFoundError(f"Key directory not found at {KEY_DIR_PATH}")

# check if all the required environment variables are set
if not DEFAULT_USER:
    raise ValueError("Environment variable USER not set, please set it to your username")
