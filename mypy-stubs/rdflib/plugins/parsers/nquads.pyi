from rdflib.plugins.parsers.ntriples import W3CNTriplesParser
from typing import Any

class NQuadsParser(W3CNTriplesParser):
    sink: Any
    file: Any
    buffer: str
    line: Any
    def parse(self, inputsource, sink, bnode_context: Any | None = ..., **kwargs): ...
    def parseline(self, bnode_context: Any | None = ...) -> None: ...
