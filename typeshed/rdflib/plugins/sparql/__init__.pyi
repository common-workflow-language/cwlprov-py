from . import operators as operators, parser as parser, parserutils as parserutils
from .processor import prepareQuery as prepareQuery, processUpdate as processUpdate
from typing import Any

SPARQL_LOAD_GRAPHS: bool
SPARQL_DEFAULT_GRAPH_UNION: bool
CUSTOM_EVALS: Any
PLUGIN_ENTRY_POINT: str
all_entry_points: Any
