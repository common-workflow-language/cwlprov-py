from bdbag.fetch import *
from bdbag import (
    get_typed_exception as get_typed_exception,
    urlcleanup as urlcleanup,
    urlretrieve as urlretrieve,
    urlsplit as urlsplit,
    urlunsplit as urlunsplit,
)
from bdbag.fetch.transports.base_transport import (
    BaseFetchTransport as BaseFetchTransport,
)
from typing import Any

logger: Any

class FTPFetchTransport(BaseFetchTransport):
    def __init__(self, config, keychain, **kwargs) -> None: ...
    @staticmethod
    def validate_auth_config(auth): ...
    def get_credentials(self, url): ...
    def fetch(self, url, output_path, **kwargs): ...
    def cleanup(self) -> None: ...
