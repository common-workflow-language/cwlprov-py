from bdbag.fetch.transports.base_transport import (
    BaseFetchTransport as BaseFetchTransport,
)
from typing import Any

logger: Any

class TAGFetchTransport(BaseFetchTransport):
    def __init__(self, config, keychain, **kwargs) -> None: ...
    @staticmethod
    def fetch(url, output_path, **kwargs): ...
    def cleanup(self) -> None: ...
