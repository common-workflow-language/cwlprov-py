import io
from _typeshed import Incomplete
from prov import serializers as serializers
from prov.model import ProvDocument as ProvDocument

logger: Incomplete
__version__: float
__date__: str
__updated__: str
DEBUG: int
TESTRUN: int
PROFILE: int
GRAPHVIZ_SUPPORTED_FORMATS: Incomplete

class CLIError(Exception):
    msg: Incomplete
    def __init__(self, msg: str) -> None: ...

def convert_file(infile: io.FileIO, outfile: io.FileIO, output_format: str) -> None: ...
def main(argv: list | None = None) -> int: ...
