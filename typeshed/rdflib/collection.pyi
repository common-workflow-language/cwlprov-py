from typing import Any

class Collection:
    __doc__: str
    graph: Any
    uri: Any
    def __init__(self, graph, uri, seq=...) -> None: ...
    def n3(self): ...
    def __len__(self): ...
    def index(self, item): ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value) -> None: ...
    def __delitem__(self, key) -> None: ...
    def __iter__(self): ...
    def append(self, item): ...
    def __iadd__(self, other): ...
    def clear(self): ...
