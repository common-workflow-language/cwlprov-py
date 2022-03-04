from rdflib.graph import Graph
from rdflib.serializer import Serializer
from typing import IO, Optional

class NTSerializer(Serializer):
    def __init__(self, store: Graph) -> None: ...
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., **args): ...

class NT11Serializer(NTSerializer):
    def __init__(self, store: Graph) -> None: ...
