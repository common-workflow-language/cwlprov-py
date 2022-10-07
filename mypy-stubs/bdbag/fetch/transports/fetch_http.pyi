from bdbag.fetch import *
from bdbag import (
    VERSION as VERSION,
    get_typed_exception as get_typed_exception,
    stob as stob,
    urlsplit as urlsplit,
)
from bdbag.bdbag_config import (
    DEFAULT_CONFIG as DEFAULT_CONFIG,
    DEFAULT_FETCH_CONFIG as DEFAULT_FETCH_CONFIG,
    DEFAULT_FETCH_HTTP_REDIRECT_STATUS_CODES as DEFAULT_FETCH_HTTP_REDIRECT_STATUS_CODES,
    DEFAULT_FETCH_HTTP_SESSION_CONFIG as DEFAULT_FETCH_HTTP_SESSION_CONFIG,
    FETCH_CONFIG_TAG as FETCH_CONFIG_TAG,
    FETCH_HTTP_REDIRECT_STATUS_CODES_TAG as FETCH_HTTP_REDIRECT_STATUS_CODES_TAG,
)
from bdbag.fetch.auth.cookies import get_request_cookies as get_request_cookies
from bdbag.fetch.transports.base_transport import (
    BaseFetchTransport as BaseFetchTransport,
)
from typing import Any

logger: Any
CHUNK_SIZE: Any
HEADERS: Any

class HTTPFetchTransport(BaseFetchTransport):
    config: Any
    cookies: Any
    sessions: Any
    def __init__(self, config, keychain, **kwargs) -> None: ...
    @staticmethod
    def validate_auth_config(auth): ...
    def get_auth(self, url): ...
    def bypass_cert_verify(self, url): ...
    @staticmethod
    def init_new_session(session_config): ...
    def get_session(self, url): ...
    def fetch(self, url, output_path, **kwargs): ...
    def cleanup(self) -> None: ...
