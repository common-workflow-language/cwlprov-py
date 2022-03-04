from rdflib.graph import ConjunctiveGraph, Graph
from rdflib.plugins.serializers.turtle import TurtleSerializer
from typing import Any, IO, Optional, Union

class TrigSerializer(TurtleSerializer):
    short_name: str
    indentString: Any
    default_context: Any
    contexts: Any
    def __init__(self, store: Union[Graph, ConjunctiveGraph]) -> None: ...
    store: Any
    def preprocess(self) -> None: ...
    def reset(self) -> None: ...
    stream: Any
    base: Any
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., spacious: Optional[bool] = ..., **args): ...
