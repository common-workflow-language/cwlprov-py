from rdflib.graph import Graph
from rdflib.serializer import Serializer
from typing import Any, IO, Optional

class JsonLDSerializer(Serializer):
    def __init__(self, store: Graph) -> None: ...
    def serialize(self, stream: IO[bytes], base: Optional[str] = ..., encoding: Optional[str] = ..., **kwargs): ...

def from_rdf(graph, context_data: Any | None = ..., base: Any | None = ..., use_native_types: bool = ..., use_rdf_type: bool = ..., auto_compact: bool = ..., startnode: Any | None = ..., index: bool = ...): ...

class Converter:
    context: Any
    use_native_types: Any
    use_rdf_type: Any
    def __init__(self, context, use_native_types, use_rdf_type) -> None: ...
    def convert(self, graph): ...
    def from_graph(self, graph): ...
    def process_subject(self, graph, s, nodemap): ...
    def add_to_node(self, graph, s, p, o, s_node, nodemap) -> None: ...
    def type_coerce(self, o, coerce_type): ...
    def to_raw_value(self, graph, s, o, nodemap): ...
    def to_collection(self, graph, l_): ...
