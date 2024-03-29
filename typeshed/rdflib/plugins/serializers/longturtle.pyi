from .turtle import RecursiveSerializer
from typing import Any

class LongTurtleSerializer(RecursiveSerializer):
    short_name: str
    indentString: str
    keywords: Any
    stream: Any
    def __init__(self, store) -> None: ...
    def addNamespace(self, prefix, namespace): ...
    def reset(self) -> None: ...
    base: Any
    def serialize(self, stream, base: Any | None = ..., encoding: Any | None = ..., spacious: Any | None = ..., **args) -> None: ...
    def preprocessTriple(self, triple) -> None: ...
    def getQName(self, uri, gen_prefix: bool = ...): ...
    def startDocument(self) -> None: ...
    def endDocument(self) -> None: ...
    def statement(self, subject): ...
    def s_default(self, subject): ...
    def s_squared(self, subject): ...
    def path(self, node, position, newline: bool = ...) -> None: ...
    def p_default(self, node, position, newline: bool = ...): ...
    def label(self, node, position): ...
    def p_squared(self, node, position, newline: bool = ...): ...
    def isValidList(self, l_): ...
    def doList(self, l_) -> None: ...
    def predicateList(self, subject, newline: bool = ...) -> None: ...
    def verb(self, node, newline: bool = ...) -> None: ...
    def objectList(self, objects) -> None: ...
