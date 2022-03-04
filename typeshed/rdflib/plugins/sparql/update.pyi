from rdflib import Graph as Graph, Variable as Variable
from rdflib.plugins.sparql.evaluate import evalBGP as evalBGP, evalPart as evalPart
from rdflib.plugins.sparql.sparql import QueryContext as QueryContext

def evalLoad(ctx, u) -> None: ...
def evalCreate(ctx, u) -> None: ...
def evalClear(ctx, u) -> None: ...
def evalDrop(ctx, u) -> None: ...
def evalInsertData(ctx, u) -> None: ...
def evalDeleteData(ctx, u) -> None: ...
def evalDeleteWhere(ctx, u) -> None: ...
def evalModify(ctx, u) -> None: ...
def evalAdd(ctx, u) -> None: ...
def evalMove(ctx, u) -> None: ...
def evalCopy(ctx, u) -> None: ...
def evalUpdate(graph, update, initBindings=...) -> None: ...
