from bdbag.fetch import *
from bdbag import stob as stob
from bdbag.fetch.transports.fetch_boto3 import BOTO3FetchTransport as BOTO3FetchTransport
from bdbag.fetch.transports.fetch_ftp import FTPFetchTransport as FTPFetchTransport
from bdbag.fetch.transports.fetch_globus import GlobusTransferFetchTransport as GlobusTransferFetchTransport
from bdbag.fetch.transports.fetch_http import HTTPFetchTransport as HTTPFetchTransport
from bdbag.fetch.transports.fetch_tag import TAGFetchTransport as TAGFetchTransport
from typing import Any

logger: Any
DEFAULT_FETCH_TRANSPORTS: Any
DEFAULT_SUPPORTED_SCHEMES: Any

def find_fetcher(scheme, fetch_config, keychain, **kwargs): ...
