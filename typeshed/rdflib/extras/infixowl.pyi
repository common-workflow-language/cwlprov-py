from collections.abc import Generator
from rdflib import Namespace
from typing import Any

class Infix:
    function: Any
    def __init__(self, function) -> None: ...
    def __ror__(self, other): ...
    def __or__(self, other): ...
    def __rlshift__(self, other): ...
    def __rshift__(self, other): ...
    def __call__(self, value1, value2): ...

nsBinds: Any

def generateQName(graph, uri): ...
def classOrTerm(thing): ...
def classOrIdentifier(thing): ...
def propertyOrIdentifier(thing): ...
def manchesterSyntax(thing, store, boolean: Any | None = ..., transientList: bool = ...): ...
def GetIdentifiedClasses(graph) -> Generator[Any, None, None]: ...
def termDeletionDecorator(prop): ...

class TermDeletionHelper:
    prop: Any
    def __init__(self, prop) -> None: ...
    def __call__(self, f): ...

class Individual:
    factoryGraph: Any
    def serialize(self, graph) -> None: ...
    graph: Any
    qname: Any
    def __init__(self, identifier: Any | None = ..., graph: Any | None = ...) -> None: ...
    def clearInDegree(self) -> None: ...
    def clearOutDegree(self) -> None: ...
    def delete(self) -> None: ...
    def replace(self, other) -> None: ...
    type: Any
    identifier: Any
    sameAs: Any

ACE_NS: Any

class AnnotatableTerms(Individual):
    label: Any
    def __init__(self, identifier, graph: Any | None = ..., nameAnnotation: Any | None = ..., nameIsLabel: bool = ...) -> None: ...
    def handleAnnotation(self, val): ...
    PN_sgProp: Any
    CN_sgProp: Any
    CN_plProp: Any
    TV_sgProp: Any
    TV_plProp: Any
    TV_vbgProp: Any
    def setupACEAnnotations(self) -> None: ...
    comment: Any
    seeAlso: Any

class Ontology(AnnotatableTerms):
    imports: Any
    comment: Any
    def __init__(self, identifier: Any | None = ..., imports: Any | None = ..., comment: Any | None = ..., graph: Any | None = ...) -> None: ...
    def setVersion(self, version) -> None: ...

def AllClasses(graph) -> Generator[Any, None, None]: ...
def AllProperties(graph) -> Generator[Any, None, None]: ...

class ClassNamespaceFactory(Namespace):
    def term(self, name): ...
    def __getitem__(self, key, default: Any | None = ...): ...
    def __getattr__(self, name): ...

CLASS_RELATIONS: Any

def ComponentTerms(cls) -> Generator[Any, None, None]: ...
def DeepClassClear(classToPrune) -> None: ...

class MalformedClass(Exception):
    msg: Any
    def __init__(self, msg) -> None: ...

def CastClass(c, graph: Any | None = ...): ...

class Class(AnnotatableTerms):
    def serialize(self, graph) -> None: ...
    def setupNounAnnotations(self, nounAnnotations) -> None: ...
    subClassOf: Any
    equivalentClass: Any
    disjointWith: Any
    complementOf: Any
    comment: Any
    def __init__(self, identifier: Any | None = ..., subClassOf: Any | None = ..., equivalentClass: Any | None = ..., disjointWith: Any | None = ..., complementOf: Any | None = ..., graph: Any | None = ..., skipOWLClassMembership: bool = ..., comment: Any | None = ..., nounAnnotations: Any | None = ..., nameAnnotation: Any | None = ..., nameIsLabel: bool = ...) -> None: ...
    extent: Any
    annotation: Any
    extentQuery: Any
    def __hash__(self): ...
    def __eq__(self, other): ...
    def __iadd__(self, other): ...
    def __isub__(self, other): ...
    def __invert__(self): ...
    def __or__(self, other): ...
    def __and__(self, other): ...
    parents: Any
    def isPrimitive(self): ...
    def subSumpteeIds(self) -> Generator[Any, None, None]: ...

class OWLRDFListProxy:
    graph: Any
    def __init__(self, rdfList, members: Any | None = ..., graph: Any | None = ...) -> None: ...
    def __eq__(self, other): ...
    def __len__(self): ...
    def index(self, item): ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value) -> None: ...
    def __delitem__(self, key) -> None: ...
    def clear(self) -> None: ...
    def __iter__(self): ...
    def __contains__(self, item): ...
    def append(self, item) -> None: ...
    def __iadd__(self, other): ...

class EnumeratedClass(OWLRDFListProxy, Class):
    def isPrimitive(self): ...
    def __init__(self, identifier: Any | None = ..., members: Any | None = ..., graph: Any | None = ...) -> None: ...
    def serialize(self, graph) -> None: ...

class BooleanClassExtentHelper:
    operator: Any
    def __init__(self, operator) -> None: ...
    def __call__(self, f) -> Generator[None, None, Any]: ...

class Callable:
    __call__: Any
    def __init__(self, anycallable) -> None: ...

class BooleanClass(OWLRDFListProxy, Class):
    def getIntersections() -> None: ...
    getIntersections: Any
    def getUnions() -> None: ...
    getUnions: Any
    def __init__(self, identifier: Any | None = ..., operator=..., members: Any | None = ..., graph: Any | None = ...) -> None: ...
    def copy(self): ...
    def serialize(self, graph) -> None: ...
    def isPrimitive(self): ...
    def changeOperator(self, newOperator) -> None: ...
    def __or__(self, other): ...

def AllDifferent(members) -> None: ...

class Restriction(Class):
    restrictionKinds: Any
    onProperty: Any
    restrictionType: Any
    restrictionRange: Any
    def __init__(self, onProperty, graph=..., allValuesFrom: Any | None = ..., someValuesFrom: Any | None = ..., value: Any | None = ..., cardinality: Any | None = ..., maxCardinality: Any | None = ..., minCardinality: Any | None = ..., identifier: Any | None = ...) -> None: ...
    def serialize(self, graph) -> None: ...
    def isPrimitive(self): ...
    def __hash__(self): ...
    def __eq__(self, other): ...
    allValuesFrom: Any
    someValuesFrom: Any
    hasValue: Any
    cardinality: Any
    maxCardinality: Any
    minCardinality: Any
    def restrictionKind(self): ...

some: Any
only: Any
max: Any
min: Any
exactly: Any
value: Any
PropertyAbstractSyntax: str

class Property(AnnotatableTerms):
    def setupVerbAnnotations(self, verbAnnotations) -> None: ...
    subPropertyOf: Any
    inverseOf: Any
    domain: Any
    range: Any
    comment: Any
    def __init__(self, identifier: Any | None = ..., graph: Any | None = ..., baseType=..., subPropertyOf: Any | None = ..., domain: Any | None = ..., range: Any | None = ..., inverseOf: Any | None = ..., otherType: Any | None = ..., equivalentProperty: Any | None = ..., comment: Any | None = ..., verbAnnotations: Any | None = ..., nameAnnotation: Any | None = ..., nameIsLabel: bool = ...) -> None: ...
    def serialize(self, graph) -> None: ...
    extent: Any
    def replace(self, other) -> None: ...

def CommonNSBindings(graph, additionalNS=...) -> None: ...