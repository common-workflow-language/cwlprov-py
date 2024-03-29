from collections.abc import Generator
from rdflib import ConjunctiveGraph as ConjunctiveGraph, Graph as Graph
from rdflib.store import Store as Store
from typing import Any

destructiveOpLocks: Any

class AuditableStore(Store):
    store: Any
    context_aware: Any
    formula_aware: bool
    transaction_aware: bool
    reverseOps: Any
    rollbackLock: Any
    def __init__(self, store) -> None: ...
    def open(self, configuration, create: bool = ...): ...
    def close(self, commit_pending_transaction: bool = ...) -> None: ...
    def destroy(self, configuration) -> None: ...
    def query(self, *args, **kw): ...
    def add(self, triple, context, quoted: bool = ...) -> None: ...
    def remove(self, spo, context: Any | None = ...) -> None: ...
    def triples(self, triple, context: Any | None = ...) -> Generator[Any, None, None]: ...
    def __len__(self, context: Any | None = ...): ...
    def contexts(self, triple: Any | None = ...) -> Generator[Any, None, None]: ...
    def bind(self, prefix, namespace) -> None: ...
    def prefix(self, namespace): ...
    def namespace(self, prefix): ...
    def namespaces(self): ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
