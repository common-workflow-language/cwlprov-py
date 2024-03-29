from typing import Any

class XMLWriter:
    stream: Any
    element_stack: Any
    nm: Any
    extra_ns: Any
    closed: bool
    def __init__(self, stream, namespace_manager, encoding: Any | None = ..., decl: int = ..., extra_ns: Any | None = ...) -> None: ...
    indent: Any
    parent: bool
    def push(self, uri) -> None: ...
    def pop(self, uri: Any | None = ...) -> None: ...
    def element(self, uri, content, attributes=...) -> None: ...
    def namespaces(self, namespaces: Any | None = ...) -> None: ...
    def attribute(self, uri, value) -> None: ...
    def text(self, text) -> None: ...
    def qname(self, uri): ...
