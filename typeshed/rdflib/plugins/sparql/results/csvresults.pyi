from rdflib import BNode as BNode, Literal as Literal, URIRef as URIRef, Variable as Variable
from rdflib.query import Result as Result, ResultParser as ResultParser, ResultSerializer as ResultSerializer
from typing import Any, IO

class CSVResultParser(ResultParser):
    delim: str
    def __init__(self) -> None: ...
    def parse(self, source, content_type: Any | None = ...): ...
    def parseRow(self, row, v): ...
    def convertTerm(self, t): ...

class CSVResultSerializer(ResultSerializer):
    delim: str
    def __init__(self, result) -> None: ...
    def serialize(self, stream: IO, encoding: str = ..., **kwargs): ...
    def serializeTerm(self, term, encoding): ...