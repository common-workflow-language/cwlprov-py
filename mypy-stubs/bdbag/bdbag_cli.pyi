import argparse
from bdbag import (
    BAGIT_VERSION as BAGIT_VERSION,
    FILTER_DOCSTRING as FILTER_DOCSTRING,
    VERSION as VERSION,
    get_typed_exception as get_typed_exception,
    inspect_path as inspect_path,
)
from bdbag.bdbag_config import (
    DEFAULT_CONFIG_FILE as DEFAULT_CONFIG_FILE,
    DEFAULT_CONFIG_FILE_ENVAR as DEFAULT_CONFIG_FILE_ENVAR,
    bootstrap_config as bootstrap_config,
)
from bdbag.bdbagit import STANDARD_BAG_INFO_HEADERS as STANDARD_BAG_INFO_HEADERS
from bdbag.fetch import fetcher as fetcher
from bdbag.fetch.auth.keychain import DEFAULT_KEYCHAIN_FILE as DEFAULT_KEYCHAIN_FILE
from typing import Any

BAG_METADATA: Any
ASYNC_TRANSFER_VALIDATION_WARNING: str

class VersionAction(argparse.Action):
    def __init__(
        self, option_strings, dest=..., default=..., help: str = ...
    ) -> None: ...
    def __call__(
        self, parser, namespace, values, option_string: Any | None = ...
    ) -> None: ...

class AddMetadataAction(argparse.Action):
    def __init__(
        self, option_strings, dest, nargs: Any | None = ..., **kwargs
    ) -> None: ...
    def __call__(
        self, parser, namespace, values, option_string: Any | None = ...
    ) -> None: ...

def parse_cli(): ...
def main(): ...
