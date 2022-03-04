from bdbag import get_typed_exception as get_typed_exception, urlsplit as urlsplit
from bdbag.fetch.resolvers.base_resolver import BaseResolverHandler as BaseResolverHandler
from collections import OrderedDict as OrderedDict
from typing import Any

logger: Any

class DataGUIDResolverHandler(BaseResolverHandler):
    def __init__(self, identifier_resolvers, args) -> None: ...
    def resolve(self, identifier, headers: Any | None = ...): ...
    def handle_response(self, response): ...
