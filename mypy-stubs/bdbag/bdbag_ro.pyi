from bdbag import (
    BAGIT_VERSION as BAGIT_VERSION,
    VERSION as VERSION,
    add_mime_types as add_mime_types,
    escape_uri as escape_uri,
    guess_mime_type as guess_mime_type,
)
from bdbag.bdbagit import force_unicode as force_unicode
from typing import Any

logger: Any
BAG_CREATOR_NAME: Any
BAG_CREATOR_URI: str
BAG_CONFORMS_TO: Any
ORCID_BASE_URL: str
DEFAULT_RO_MANIFEST: Any

def check_input(obj) -> None: ...
def read_bag_ro_metadata(bag_path, metadata_path: str = ...): ...
def write_bag_ro_metadata(obj, bag_path, metadata_path: str = ...) -> None: ...
def serialize_bag_ro_metadata(obj, bag_path) -> None: ...
def init_ro_manifest(
    creator_name: Any | None = ...,
    creator_uri: Any | None = ...,
    creator_orcid: Any | None = ...,
    author_name: Any | None = ...,
    author_uri: Any | None = ...,
    author_orcid: Any | None = ...,
): ...
def add_file_metadata(
    manifest,
    source_url: Any | None = ...,
    local_path: Any | None = ...,
    media_type: Any | None = ...,
    retrieved_on: Any | None = ...,
    retrieved_by: Any | None = ...,
    created_on: Any | None = ...,
    created_by: Any | None = ...,
    authored_on: Any | None = ...,
    authored_by: Any | None = ...,
    conforms_to: Any | None = ...,
    bundled_as: Any | None = ...,
    update_existing: bool = ...,
) -> None: ...
def add_provenance(
    obj,
    created_on: Any | None = ...,
    created_by: Any | None = ...,
    authored_on: Any | None = ...,
    authored_by: Any | None = ...,
    retrieved_from: Any | None = ...,
    retrieved_on: Any | None = ...,
    retrieved_by: Any | None = ...,
): ...
def add_aggregate(
    obj,
    uri,
    mediatype: Any | None = ...,
    conforms_to: Any | None = ...,
    bundled_as: Any | None = ...,
    update_existing: bool = ...,
): ...
def add_annotation(
    obj,
    about,
    uri: Any | None = ...,
    content: Any | None = ...,
    motivatedBy: Any | None = ...,
    update_existing: bool = ...,
): ...
def make_bundled_as(
    uri: Any | None = ..., folder: Any | None = ..., filename: Any | None = ...
): ...
def make_created_by(name, uri: Any | None = ..., orcid: Any | None = ...): ...
def make_created_on(date: Any | None = ...): ...
def make_authored_by(name, uri: Any | None = ..., orcid: Any | None = ...): ...
def make_authored_on(date: Any | None = ...): ...
def make_retrieved_by(name, uri: Any | None = ..., orcid: Any | None = ...): ...
def make_retrieved_on(date: Any | None = ...): ...
def ensure_payload_path_prefix(input_path): ...

FILETYPE_ONTOLOGY_MAP: Any
MIMETYPE_EXTENSION_MAP: Any
