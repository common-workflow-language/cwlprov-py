from bdbag import (
    filter_dict as filter_dict,
    urlsplit as urlsplit,
    urlunquote as urlunquote,
)
from bdbag.bdbag_config import (
    DEFAULT_CONFIG as DEFAULT_CONFIG,
    DEFAULT_CONFIG_FILE as DEFAULT_CONFIG_FILE,
    DEFAULT_FETCH_CONFIG as DEFAULT_FETCH_CONFIG,
    DEFAULT_RESOLVER_CONFIG as DEFAULT_RESOLVER_CONFIG,
    FETCH_CONFIG_TAG as FETCH_CONFIG_TAG,
    RESOLVER_CONFIG_TAG as RESOLVER_CONFIG_TAG,
    read_config as read_config,
)
from bdbag.fetch.auth.cookies import get_request_cookies as get_request_cookies
from bdbag.fetch.auth.keychain import (
    DEFAULT_KEYCHAIN_FILE as DEFAULT_KEYCHAIN_FILE,
    read_keychain as read_keychain,
)
from bdbag.fetch.resolvers import resolve as resolve
from bdbag.fetch.transports import find_fetcher as find_fetcher
from bdbag.fetch.transports.base_transport import (
    BaseFetchTransport as BaseFetchTransport,
)
from typing import Any, NamedTuple

logger: Any
UNIMPLEMENTED: str

class FetchEntry(NamedTuple):
    url: Any
    length: Any
    filename: Any

def fetch_bag_files(
    bag,
    keychain_file=...,
    config_file: Any | None = ...,
    force: bool = ...,
    callback: Any | None = ...,
    filter_expr: Any | None = ...,
    **kwargs
): ...
def fetch_single_file(
    url,
    output_path: Any | None = ...,
    config_file: Any | None = ...,
    keychain_file=...,
    **kwargs
): ...
def fetch_file(url, output_path, config, keychain, fetchers, **kwargs): ...
def cleanup_fetchers(fetchers) -> None: ...
