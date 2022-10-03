from rdflib.graph import Graph
from typing import Any, IO, Optional

class Serializer:
    store: Any
    encoding: str
    base: Any
    def __init__(self, store: Graph) -> None: ...
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., **args) -> None: ...
    def relativize(self, uri: str): ...
