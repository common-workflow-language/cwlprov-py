from bdbag import (
    BAG_PROFILE_TAG as BAG_PROFILE_TAG,
    BDBAG_PROFILE_ID as BDBAG_PROFILE_ID,
    DEFAULT_CONFIG_PATH as DEFAULT_CONFIG_PATH,
    VERSION as VERSION,
    get_typed_exception as get_typed_exception,
    parse_version as parse_version,
    safe_move as safe_move,
)
from bdbag.fetch import Megabyte as Megabyte
from bdbag.fetch.auth.keychain import (
    DEFAULT_KEYCHAIN_FILE as DEFAULT_KEYCHAIN_FILE,
    write_keychain as write_keychain,
)
from typing import Any

logger: Any
BAG_CONFIG_TAG: str
BAG_SPEC_VERSION_TAG: str
BAG_ALGORITHMS_TAG: str
BAG_PROCESSES_TAG: str
BAG_METADATA_TAG: str
CONFIG_VERSION_TAG: str
DEFAULT_BAG_SPEC_VERSION: str
DEFAULT_CONFIG_FILE_ENVAR: str
DEFAULT_CONFIG_FILE: Any
DEFAULT_BAG_ALGORITHMS: Any
COOKIE_JAR_TAG: str
COOKIE_JAR_SEARCH_TAG: str
COOKIE_JAR_FILE_TAG: str
COOKIE_JAR_PATHS_TAG: str
COOKIE_JAR_PATH_FILTER_TAG: str
DEFAULT_COOKIE_JAR_FILE_NAMES: Any
DEFAULT_COOKIE_JAR_SEARCH_PATHS: Any
DEFAULT_COOKIE_JAR_SEARCH_PATH_FILTER: str
DEFAULT_COOKIE_JAR_SEARCH_CONFIG: Any
FETCH_CONFIG_TAG: str
FETCH_HTTP_REDIRECT_STATUS_CODES_TAG: str
DEFAULT_FETCH_HTTP_REDIRECT_STATUS_CODES: Any
DEFAULT_FETCH_HTTP_SESSION_CONFIG: Any
DEFAULT_FETCH_CONFIG: Any
ID_RESOLVER_TAG: str
DEFAULT_ID_RESOLVERS: Any
RESOLVER_CONFIG_TAG: str
DEFAULT_RESOLVER_CONFIG: Any
DEFAULT_CONFIG: Any

def get_updated_config_keys(config): ...
def get_deprecated_config_keys(config): ...
def write_config(config=..., config_file=...) -> None: ...
def read_config(
    config_file: Any | None = ..., create_default: bool = ..., auto_upgrade: bool = ...
): ...
def upgrade_config(config_file) -> None: ...
def copy_config_items(old_config, new_config, key_names): ...
def bootstrap_config(
    config_file=..., keychain_file=..., base_dir: Any | None = ...
) -> None: ...
