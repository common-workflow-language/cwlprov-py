import typing_extensions as te
from rdflib import BNode as BNode
from rdflib.query import Result as Result
from typing import Any, Optional, Tuple
from urllib.error import URLError as URLError

log: Any

class SPARQLConnectorException(Exception): ...

class SPARQLConnector:
    returnFormat: Any
    query_endpoint: Any
    update_endpoint: Any
    kwargs: Any
    def __init__(self, query_endpoint: Optional[str] = ..., update_endpoint: Optional[str] = ..., returnFormat: str = ..., method: te.Literal['GET', 'POST', 'POST_FORM'] = ..., auth: Optional[Tuple[str, str]] = ..., **kwargs) -> None: ...
    @property
    def method(self): ...
    @method.setter
    def method(self, method) -> None: ...
    def query(self, query, default_graph: str = ..., named_graph: str = ...): ...
    def update(self, query, default_graph: Optional[str] = ..., named_graph: Optional[str] = ...): ...
