from rdflib.graph import ConjunctiveGraph, Graph
from rdflib.serializer import Serializer
from typing import Any, IO, Optional, Union

class HextuplesSerializer(Serializer):
    default_context: Any
    contexts: Any
    def __init__(self, store: Union[Graph, ConjunctiveGraph]) -> None: ...
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., **kwargs): ...
