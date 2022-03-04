from bdbag import get_typed_exception as get_typed_exception, urlsplit as urlsplit
from bdbag.bdbag_config import DEFAULT_ID_RESOLVERS as DEFAULT_ID_RESOLVERS, DEFAULT_RESOLVER_CONFIG as DEFAULT_RESOLVER_CONFIG, ID_RESOLVER_TAG as ID_RESOLVER_TAG
from typing import Any

logger: Any

def find_resolver(identifier, resolver_config): ...
def resolve(identifier, resolver_config=...): ...
