from _typeshed import Incomplete
from prov.model import ProvDocument as ProvDocument

logger: Incomplete
__version__: float
__date__: str
__updated__: str
DEBUG: int
TESTRUN: int
PROFILE: int

class CLIError(Exception):
    msg: Incomplete
    def __init__(self, msg: str) -> None: ...

def main(argv: list | None = None) -> int: ...
