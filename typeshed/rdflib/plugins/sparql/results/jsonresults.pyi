from rdflib import BNode as BNode, Literal as Literal, URIRef as URIRef, Variable as Variable
from rdflib.query import Result as Result, ResultException as ResultException, ResultParser as ResultParser, ResultSerializer as ResultSerializer
from typing import Any, IO

class JSONResultParser(ResultParser):
    def parse(self, source, content_type: Any | None = ...): ...

class JSONResultSerializer(ResultSerializer):
    def __init__(self, result) -> None: ...
    def serialize(self, stream: IO, encoding: str = ...): ...

class JSONResult(Result):
    json: Any
    askAnswer: Any
    bindings: Any
    vars: Any
    def __init__(self, json) -> None: ...

def parseJsonTerm(d): ...
def termToJSON(self, term): ...
