import abc
import io
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from prov import Error
from prov.model import ProvDocument
from typing import Any

__all__ = ["get", "Registry", "Serializer"]

class Serializer(ABC, metaclass=abc.ABCMeta):
    document: Incomplete
    def __init__(self, document: ProvDocument | None = None) -> None: ...
    @abstractmethod
    def serialize(self, stream: io.IOBase, **args: Any) -> None: ...
    @abstractmethod
    def deserialize(self, stream: io.IOBase, **args: Any) -> ProvDocument: ...

class DoNotExist(Error): ...

class Registry:
    serializers: dict[str, type[Serializer]]
    @staticmethod
    def load_serializers() -> None: ...

def get(format_name: str) -> type[Serializer]: ...
