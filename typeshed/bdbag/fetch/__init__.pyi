from bdbag import urlsplit as urlsplit, urlunquote as urlunquote
from typing import Any

Kilobyte: int
Megabyte: Any
SCHEME_HTTP: str
SCHEME_HTTPS: str
SCHEME_S3: str
SCHEME_GS: str
SCHEME_GLOBUS: str
SCHEME_FTP: str
SCHEME_SFTP: str
SCHEME_TAG: str

def get_transfer_summary(total_bytes, elapsed_time): ...
def check_transfer_size_mismatch(path, expected, total): ...
def ensure_valid_output_path(url, output_path: Any | None = ...): ...
