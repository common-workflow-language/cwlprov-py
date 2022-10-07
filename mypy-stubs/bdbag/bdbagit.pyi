from bagit import *
from bdbag import (
    BAGIT_VERSION as BAGIT_VERSION,
    PROJECT_URL as PROJECT_URL,
    VERSION as VERSION,
)
from collections.abc import Generator
from typing import Any

algorithms_guaranteed: Any
SUPPORTED_BAGIT_SPECS: Any

class BaggingInterruptedError(RuntimeError): ...
class BagManifestConflict(BagError): ...
class UnexpectedRemoteFile(ManifestErrorDetail): ...

class BDBag(Bag):
    remote_entries: Any
    def __init__(self, path: Any | None = ...) -> None: ...
    def save(self, processes: int = ..., manifests: bool = ...) -> None: ...
    def validate(
        self,
        processes: int = ...,
        fast: bool = ...,
        completeness_only: bool = ...,
        callback: Any | None = ...,
    ) -> bool: ...
