from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    """
    This class is an abstract class that defines the interface for a command.
    """

    @property
    @abstractmethod
    def help(self):
        ...

    @property
    @abstractmethod
    def cmd(self):
        ...

    @abstractmethod
    def run(self, *args, **kwargs) -> int:
        ...
