import abc
from typing import Any


class FilenameRegex:
    def __init__(self, filename_regex: str):
        self.filename_regex = filename_regex


class State(metaclass=abc.ABCMeta):
    # @abc.abstractmethod
    # def serialize(self) -> Any:
    #     pass
    pass


class Investigator(State, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def investigate(self) -> Any:
        pass
