import os
from prov.model import ProvDocument

__all__ = ["Error", "model", "read"]

class Error(Exception): ...

def read(
    source: str | bytes | os.PathLike[str], format: str | None = None
) -> ProvDocument | None: ...

# Names in __all__ with no definition:
#   model
