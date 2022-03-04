from rdflib.plugins.sparql.algebra import translateQuery as translateQuery, translateUpdate as translateUpdate
from rdflib.plugins.sparql.evaluate import evalQuery as evalQuery
from rdflib.plugins.sparql.parser import parseQuery as parseQuery, parseUpdate as parseUpdate
from rdflib.plugins.sparql.sparql import Query as Query
from rdflib.plugins.sparql.update import evalUpdate as evalUpdate
from rdflib.query import Processor as Processor, Result as Result, UpdateProcessor as UpdateProcessor
from typing import Any

def prepareQuery(queryString, initNs=..., base: Any | None = ...): ...
def processUpdate(graph, updateString, initBindings=..., initNs=..., base: Any | None = ...) -> None: ...

class SPARQLResult(Result):
    vars: Any
    bindings: Any
    askAnswer: Any
    graph: Any
    def __init__(self, res) -> None: ...

class SPARQLUpdateProcessor(UpdateProcessor):
    graph: Any
    def __init__(self, graph) -> None: ...
    def update(self, strOrQuery, initBindings=..., initNs=...): ...

class SPARQLProcessor(Processor):
    graph: Any
    def __init__(self, graph) -> None: ...
    def query(self, strOrQuery, initBindings=..., initNs=..., base: Any | None = ..., DEBUG: bool = ...): ...
