from rdflib import BNode as BNode, Literal as Literal, URIRef as URIRef, Variable as Variable
from rdflib.compat import etree as etree
from rdflib.query import Result as Result, ResultException as ResultException, ResultParser as ResultParser, ResultSerializer as ResultSerializer
from typing import Any, IO, Optional

SPARQL_XML_NAMESPACE: str
RESULTS_NS_ET: Any
log: Any

class XMLResultParser(ResultParser):
    def parse(self, source, content_type: Optional[str] = ...): ...

class XMLResult(Result):
    bindings: Any
    vars: Any
    askAnswer: Any
    def __init__(self, source, content_type: Optional[str] = ...) -> None: ...

def parseTerm(element): ...

class XMLResultSerializer(ResultSerializer):
    def __init__(self, result) -> None: ...
    def serialize(self, stream: IO, encoding: str = ..., **kwargs): ...

class SPARQLXMLWriter:
    writer: Any
    def __init__(self, output, encoding: str = ...) -> None: ...
    def write_header(self, allvarsL) -> None: ...
    def write_ask(self, val) -> None: ...
    def write_results_header(self) -> None: ...
    def write_start_result(self) -> None: ...
    def write_end_result(self) -> None: ...
    def write_binding(self, name, val) -> None: ...
    def close(self) -> None: ...
