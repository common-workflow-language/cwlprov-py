from bdbag.fetch import *
from bdbag import (
    get_typed_exception as get_typed_exception,
    stob as stob,
    urlsplit as urlsplit,
    urlunsplit as urlunsplit,
)
from bdbag.bdbag_config import (
    DEFAULT_CONFIG as DEFAULT_CONFIG,
    DEFAULT_FETCH_CONFIG as DEFAULT_FETCH_CONFIG,
    FETCH_CONFIG_TAG as FETCH_CONFIG_TAG,
)
from bdbag.fetch.transports.base_transport import (
    BaseFetchTransport as BaseFetchTransport,
)
from typing import Any

logger: Any
BOTO3: Any
BOTOCORE: Any
CHUNK_SIZE: Any

class BOTO3FetchTransport(BaseFetchTransport):
    config: Any
    def __init__(self, config, keychain, **kwargs) -> None: ...
    @staticmethod
    def import_boto3() -> None: ...
    @staticmethod
    def validate_auth_config(auth): ...
    def get_credentials(self, url): ...
    def fetch(self, url, output_path, **kwargs): ...
    def cleanup(self) -> None: ...
