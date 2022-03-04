from rdflib import Graph as Graph, Namespace as Namespace, RDF as RDF, Variable as Variable
from rdflib.query import Result as Result, ResultParser as ResultParser
from typing import Any

RS: Any

class RDFResultParser(ResultParser):
    def parse(self, source, **kwargs): ...

class RDFResult(Result):
    vars: Any
    bindings: Any
    askAnswer: Any
    graph: Any
    def __init__(self, source, **kwargs) -> None: ...
