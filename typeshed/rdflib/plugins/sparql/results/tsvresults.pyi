from rdflib.plugins.sparql.parser import BLANK_NODE_LABEL as BLANK_NODE_LABEL, BooleanLiteral as BooleanLiteral, IRIREF as IRIREF, LANGTAG as LANGTAG, NumericLiteral as NumericLiteral, STRING_LITERAL1 as STRING_LITERAL1, STRING_LITERAL2 as STRING_LITERAL2, Var as Var
from rdflib.plugins.sparql.parserutils import Comp as Comp, CompValue as CompValue, Param as Param
from rdflib.query import Result as Result, ResultParser as ResultParser
from typing import Any

String: Any
RDFLITERAL: Any
NONE_VALUE: Any
EMPTY: Any
TERM: Any
ROW: Any
HEADER: Any

class TSVResultParser(ResultParser):
    def parse(self, source, content_type: Any | None = ...): ...
    def convertTerm(self, t): ...
