from bagit_profile import *
from bdbag import guess_mime_type as guess_mime_type
from typing import Any

class BDBProfile(Profile):
    def __init__(self, url, profile: Any | None = ..., ignore_baginfo_tag_case: bool = ...) -> None: ...
    def validate_serialization(self, path_to_bag): ...
