from typing import Any, Tuple, Union
from urllib.parse import ParseResult
from uuid import NAMESPACE_URL, UUID
from pathlib import PurePosixPath

SCHEME: str

def is_arcp_uri(uri: str) -> bool: ...
def parse_arcp(uri: Union[str, PurePosixPath]) -> "ARCPParseResult": ...
def urlparse(uri: str) -> Union["ARCPParseResult", ParseResult]: ...

class ARCPParseResult(ParseResult):
    def __init__(self, *args: Any) -> None: ...
    @property
    def prefix(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def uuid(self) -> UUID: ...
    @property
    def ni(self) -> str | None: ...
    def ni_uri(self, authority: str = ...) -> str | None: ...
    def nih_uri(self) -> str | None: ...
    def ni_well_known(self, base: str = ...) -> str | None: ...
    @property
    def hash(self) -> Tuple[str, str] | None: ...
