from enum import Enum
from typing import IO, Union, Iterable, Dict

class FormatWarning(object):
    def __init__(self, file : str, line : int, column : int, message : str):
        self.__file = file
        self.__line = line
        self.__column = column
        self.__message = message

    @property
    def file(self) -> str:
        return self.__file
    @property
    def line(self) -> int:
        return self.__line
    @property
    def column(self) -> int:
        return self.__column
    @property
    def message(self) -> str:
        return self.__message


class Languages(Enum):
    C = "C"
    Cpp = "Cpp"


def language(l):
    def _wrapper(fn):
        return fn
    return _wrapper

class Token(object):
    """ Type representing a token. """

    def __init__(self, file : str, line : int, column : int,
            ttype : Enum, value : Enum = None):
        self.__file = file
        self.__line = line
        self.__column = column
        self.__value = value
        self.__ttype = ttype

    @property
    def file(self) -> str:
        return self.__file
    @property
    def line(self) -> int:
        return self.__line
    @property
    def column(self) -> int:
        return self.__column
    @property
    def value(self) -> Union[str, Enum]:
        return self.__value
    @property
    def ttype(self) -> Enum:
        return self.__ttype
