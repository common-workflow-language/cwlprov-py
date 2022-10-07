from bdbag import (
    get_typed_exception as get_typed_exception,
    stob as stob,
    urlsplit as urlsplit,
)
from bdbag.bdbag_config import DEFAULT_ID_RESOLVERS as DEFAULT_ID_RESOLVERS
from typing import Any

logger: Any

class BaseResolverHandler:
    identifier_resolvers: Any
    args: Any
    def __init__(self, identifier_resolvers, args) -> None: ...
    @staticmethod
    def get_resolver_url(identifier, resolver): ...
    @classmethod
    def handle_response(cls, response) -> None: ...
    def resolve(self, identifier, headers: Any | None = ...): ...
