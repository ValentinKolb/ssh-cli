import validators
from inquirer.errors import ValidationError
from sshconf import read_ssh_config

from .config import CONFIG_FILE_PATH


def is_number(_, x):
    """
    This function checks if a given input is a number.
    :param x: what to check
    :return: True if x is a number, raises a ValidationError otherwise
    """
    if not x.isdigit():
        raise ValidationError(x, reason='Must be a number')
    else:
        return True


def is_not_empty(_, x):
    """
    This function checks if a given input is not empty.
    :param x: what to check
    :return: True if x is not empty, raises a ValidationError otherwise
    """
    if not x:
        raise ValidationError(x, reason='Cannot be empty')
    else:
        return True


def is_valid_hostname(_, x):
    """
    This function checks if a given input is a valid hostname.
    :param x: what to check
    :return: True if x is a valid hostname, raises a ValidationError otherwise
    """
    if not (validators.domain(x) or validators.ipv4(x) or validators.ipv6(x)):
        raise ValidationError(x, reason='Not a valid hostname, must be a domain or an IP address.')
    else:
        return True


def host_exists(_, x):
    """
    This function checks if a given host already exists in the ssh config file.
    :param x: what to check
    :return: True if x is not empty, raises a ValidationError otherwise
    """
    c = read_ssh_config(CONFIG_FILE_PATH)
    if x in c.hosts():
        raise ValidationError(x, reason='Host already exists, delete it first.')
    else:
        return True
