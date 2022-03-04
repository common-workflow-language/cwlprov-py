from rdflib import Graph as Graph
from rdflib.query import Result as Result, ResultParser as ResultParser

class GraphResultParser(ResultParser):
    def parse(self, source, content_type): ...
