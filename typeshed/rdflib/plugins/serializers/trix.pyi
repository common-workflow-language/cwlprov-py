from rdflib.graph import Graph
from rdflib.serializer import Serializer
from typing import Any, IO, Optional

class TriXSerializer(Serializer):
    def __init__(self, store: Graph) -> None: ...
    writer: Any
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., **args): ...
