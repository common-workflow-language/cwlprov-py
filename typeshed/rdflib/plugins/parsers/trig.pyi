from .notation3 import RDFSink as RDFSink, SinkParser as SinkParser
from rdflib import ConjunctiveGraph as ConjunctiveGraph
from rdflib.parser import Parser as Parser

def becauseSubGraph(*args, **kwargs) -> None: ...

class TrigSinkParser(SinkParser):
    def directiveOrStatement(self, argstr, h): ...
    def labelOrSubject(self, argstr, i, res): ...
    def graph(self, argstr, i): ...

class TrigParser(Parser):
    def __init__(self) -> None: ...
    def parse(self, source, graph, encoding: str = ...) -> None: ...
