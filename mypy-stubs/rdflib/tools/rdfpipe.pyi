from rdflib import plugin as plugin
from rdflib.graph import ConjunctiveGraph as ConjunctiveGraph
from rdflib.parser import Parser as Parser
from rdflib.serializer import Serializer as Serializer
from rdflib.store import Store as Store
from rdflib.util import guess_format as guess_format
from typing import Any

DEFAULT_INPUT_FORMAT: str
DEFAULT_OUTPUT_FORMAT: str

def parse_and_serialize(input_files, input_format, guess, outfile, output_format, ns_bindings, store_conn: str = ..., store_type: Any | None = ...) -> None: ...
def make_option_parser(): ...
def main() -> None: ...
