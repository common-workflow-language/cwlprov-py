from requests.utils import requote_uri as requote_uri
from typing import Any
from urllib.parse import urlparse as urlparse, urlunsplit as urlunsplit
from urllib.request import (
    urlcleanup as urlcleanup,
    urlopen as urlopen,
    urlretrieve as urlretrieve,
)

__bagit_version__: str
__bagit_profile_version__: str
version: Any
VERSION: Any
PROJECT_URL: str
BAGIT_VERSION: Any
BAGIT_PROFILE_VERSION: Any
BAG_PROFILE_TAG: str
BDBAG_PROFILE_ID: str
BDBAG_RO_PROFILE_ID: str
CONTENT_DISP_REGEX: Any
FILTER_REGEX: Any
FILTER_DOCSTRING: str
DEFAULT_LOG_FORMAT: str
DEFAULT_CONFIG_PATH: Any
