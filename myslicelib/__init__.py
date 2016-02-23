import sys

try:
    assert sys.version_info >= (3,5)
except AssertionError:
    exit("MySlice Lib requires Python 3.5")

from typing import Set
from myslicelib.util import Credential, Endpoint

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Setup(metaclass=Singleton):

    def __init__(self):
        self._setup = True
        self._credential = None
        self._endpoints = None

    @property
    def credential(self) -> Credential:
        return self._credential

    @credential.setter
    def credential(self, credential: Credential) -> None:
        self._credential = credential

    @credential.deleter
    def credential(self) -> None:
        del self._credential

    @property
    def endpoints(self) -> Set[Endpoint]:
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints: Set[Endpoint]) -> None:
        self._endpoints = endpoints

    @endpoints.deleter
    def endpoints(self) -> None:
        del self._endpoints

setup = Setup()