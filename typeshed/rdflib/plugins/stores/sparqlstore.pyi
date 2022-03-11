from .sparqlconnector import SPARQLConnector as SPARQLConnector
from collections.abc import Generator
from rdflib import BNode as BNode, Variable as Variable
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as DATASET_DEFAULT_GRAPH_ID
from rdflib.plugins.stores.regexmatching import NATIVE_REGEX as NATIVE_REGEX
from rdflib.store import Store as Store
from rdflib.term import Node as Node
from typing import Any, Callable, Optional, Tuple, Union

LIMIT: str
OFFSET: str
ORDERBY: str
BNODE_IDENT_PATTERN: Any
NodeToSparql = Callable[..., str]

class SPARQLStore(SPARQLConnector, Store):
    formula_aware: bool
    transaction_aware: bool
    graph_aware: bool
    regex_matching: Any
    node_to_sparql: Any
    nsBindings: Any
    sparql11: Any
    context_aware: Any
    def __init__(self, query_endpoint: str = ..., sparql11: bool = ..., context_aware: bool = ..., node_to_sparql: NodeToSparql = ..., returnFormat: str = ..., auth: Optional[Tuple[str, str]] = ..., **sparqlconnector_kwargs) -> None: ...
    query_endpoint: Any
    def open(self, configuration: str, create: bool = ...): ...
    def create(self, configuration) -> None: ...
    def destroy(self, configuration) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def add(self, _, context: Any | None = ..., quoted: bool = ...) -> None: ...
    def addN(self, quads) -> None: ...
    def remove(self, _, context) -> None: ...
    debug: Any
    def query(self, query, initNs: Any | None = ..., initBindings: Any | None = ..., queryGraph: Any | None = ..., DEBUG: bool = ...): ...
    def triples(self, spo, context: Any | None = ...) -> Generator[Any, None, None]: ...
    def triples_choices(self, _, context: Any | None = ...) -> None: ...
    def __len__(self, context: Any | None = ...): ...
    def contexts(self, triple: Any | None = ...): ...
    def bind(self, prefix, namespace) -> None: ...
    def prefix(self, namespace): ...
    def namespace(self, prefix): ...
    def namespaces(self) -> Generator[Any, None, None]: ...
    def add_graph(self, graph) -> None: ...
    def remove_graph(self, graph) -> None: ...
    def subjects(self, predicate: Any | None = ..., object: Any | None = ...) -> Generator[Any, None, None]: ...
    def predicates(self, subject: Any | None = ..., object: Any | None = ...) -> Generator[Any, None, None]: ...
    def objects(self, subject: Any | None = ..., predicate: Any | None = ...) -> Generator[Any, None, None]: ...
    def subject_predicates(self, object: Any | None = ...) -> Generator[Any, None, None]: ...
    def subject_objects(self, predicate: Any | None = ...) -> Generator[Any, None, None]: ...
    def predicate_objects(self, subject: Any | None = ...) -> Generator[Any, None, None]: ...

class SPARQLUpdateStore(SPARQLStore):
    where_pattern: Any
    STRING_LITERAL1: str
    STRING_LITERAL2: str
    STRING_LITERAL_LONG1: str
    STRING_LITERAL_LONG2: str
    String: Any
    IRIREF: str
    COMMENT: str
    BLOCK_START: str
    BLOCK_END: str
    ESCAPED: str
    BlockContent: Any
    BlockFinding: Any
    BLOCK_FINDING_PATTERN: Any
    postAsEncoded: Any
    autocommit: Any
    dirty_reads: Any
    def __init__(self, query_endpoint: Optional[str] = ..., update_endpoint: Optional[str] = ..., sparql11: bool = ..., context_aware: bool = ..., postAsEncoded: bool = ..., autocommit: bool = ..., dirty_reads: bool = ..., **kwds) -> None: ...
    query_endpoint: Any
    update_endpoint: Any
    def open(self, configuration: Union[str, Tuple[str, str]], create: bool = ...): ...
    def query(self, *args, **kwargs): ...
    def triples(self, *args, **kwargs): ...
    def contexts(self, *args, **kwargs): ...
    def __len__(self, *args, **kwargs): ...
    def open(self, configuration, create: bool = ...) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def add(self, spo, context: Any | None = ..., quoted: bool = ...) -> None: ...
    def addN(self, quads) -> None: ...
    def remove(self, spo, context) -> None: ...
    def setTimeout(self, timeout) -> None: ...
    debug: Any
    def update(self, query, initNs=..., initBindings=..., queryGraph: Any | None = ..., DEBUG: bool = ...) -> None: ...
    def add_graph(self, graph) -> None: ...
    def remove_graph(self, graph) -> None: ...
    def subjects(self, predicate: Any | None = ..., object: Any | None = ...) -> Generator[Any, None, None]: ...
    def predicates(self, subject: Any | None = ..., object: Any | None = ...) -> Generator[Any, None, None]: ...
    def objects(self, subject: Any | None = ..., predicate: Any | None = ...) -> Generator[Any, None, None]: ...
    def subject_predicates(self, object: Any | None = ...) -> Generator[Any, None, None]: ...
    def subject_objects(self, predicate: Any | None = ...) -> Generator[Any, None, None]: ...
    def predicate_objects(self, subject: Any | None = ...) -> Generator[Any, None, None]: ...