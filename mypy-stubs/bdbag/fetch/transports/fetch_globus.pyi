from bdbag.fetch import *
from bdbag import get_typed_exception as get_typed_exception, urlsplit as urlsplit
from bdbag.fetch.transports.base_transport import (
    BaseFetchTransport as BaseFetchTransport,
)
from typing import Any

logger: Any
globus_sdk: Any
globus_sdk_name: str

class GlobusTransferFetchTransport(BaseFetchTransport):
    def __init__(self, config, keychain, **kwargs) -> None: ...
    @staticmethod
    def validate_auth_config(auth): ...
    def get_credentials(self, url): ...
    def fetch(self, url, output_path, **kwargs): ...
    def cleanup(self) -> None: ...
