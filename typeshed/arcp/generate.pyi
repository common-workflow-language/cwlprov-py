from base64 import urlsafe_b64decode as urlsafe_b64decode
from typing import Any

SCHEME: str

def arcp_uuid(uuid, path: str = ..., query: Any | None = ..., fragment: Any | None = ...) -> str: ...
def arcp_random(path: str = ..., query: Any | None = ..., fragment: Any | None = ..., uuid: Any | None = ...) -> str: ...
def arcp_location(location, path: str = ..., query: Any | None = ..., fragment: Any | None = ..., namespace=...): ...
def arcp_name(name, path: str = ..., query: Any | None = ..., fragment: Any | None = ...): ...
def arcp_hash(bytes: bytes = ..., path: str = ..., query: Any | None = ..., fragment: Any | None = ..., hash: Any | None = ...): ...
