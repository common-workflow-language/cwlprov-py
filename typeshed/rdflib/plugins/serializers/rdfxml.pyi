from rdflib.graph import Graph
from rdflib.serializer import Serializer
from rdflib.term import Identifier
from typing import Any, IO, Optional

class XMLSerializer(Serializer):
    def __init__(self, store: Graph) -> None: ...
    base: Any
    write: Any
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., **args): ...
    def subject(self, subject, depth: int = ...) -> None: ...
    def predicate(self, predicate, object, depth: int = ...) -> None: ...

def fix(val): ...

class PrettyXMLSerializer(Serializer):
    forceRDFAbout: Any
    def __init__(self, store: Graph, max_depth: int = ...) -> None: ...
    base: Any
    max_depth: Any
    nm: Any
    writer: Any
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., **args): ...
    def subject(self, subject: Identifier, depth: int = ...): ...
    def predicate(self, predicate, object, depth: int = ...) -> None: ...
