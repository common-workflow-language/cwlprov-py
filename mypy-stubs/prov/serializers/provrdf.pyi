import io
import prov.model as pm
from _typeshed import Incomplete
from prov import Error as Error
from prov.constants import (
    PROV as PROV,
    PROV_ACTIVITY as PROV_ACTIVITY,
    PROV_ALTERNATE as PROV_ALTERNATE,
    PROV_ASSOCIATION as PROV_ASSOCIATION,
    PROV_ATTR_ENDER as PROV_ATTR_ENDER,
    PROV_ATTR_ENDTIME as PROV_ATTR_ENDTIME,
    PROV_ATTR_INFORMANT as PROV_ATTR_INFORMANT,
    PROV_ATTR_RESPONSIBLE as PROV_ATTR_RESPONSIBLE,
    PROV_ATTR_STARTER as PROV_ATTR_STARTER,
    PROV_ATTR_STARTTIME as PROV_ATTR_STARTTIME,
    PROV_ATTR_TIME as PROV_ATTR_TIME,
    PROV_ATTR_TRIGGER as PROV_ATTR_TRIGGER,
    PROV_ATTR_USED_ENTITY as PROV_ATTR_USED_ENTITY,
    PROV_BASE_CLS as PROV_BASE_CLS,
    PROV_COMMUNICATION as PROV_COMMUNICATION,
    PROV_DELEGATION as PROV_DELEGATION,
    PROV_DERIVATION as PROV_DERIVATION,
    PROV_END as PROV_END,
    PROV_GENERATION as PROV_GENERATION,
    PROV_ID_ATTRIBUTES_MAP as PROV_ID_ATTRIBUTES_MAP,
    PROV_INVALIDATION as PROV_INVALIDATION,
    PROV_LOCATION as PROV_LOCATION,
    PROV_MENTION as PROV_MENTION,
    PROV_N_MAP as PROV_N_MAP,
    PROV_ROLE as PROV_ROLE,
    PROV_START as PROV_START,
    PROV_USAGE as PROV_USAGE,
    XSD_QNAME as XSD_QNAME,
)
from prov.identifier import QualifiedName as QualifiedName
from prov.serializers import Serializer as Serializer
from rdflib.graph import ConjunctiveGraph
from rdflib.term import Literal as RDFLiteral, URIRef
from typing import Any, Generator

class ProvRDFException(Error): ...

class AnonymousIDGenerator:
    def __init__(self) -> None: ...
    def get_anon_id(self, obj: pm.ProvRecord, local_prefix: str = "id") -> str: ...

LITERAL_XSDTYPE_MAP: Incomplete
RELATION_MAP: Incomplete
PREDICATE_MAP: Incomplete

def attr2rdf(attr: QualifiedName) -> URIRef: ...

class ProvRDFSerializer(Serializer):
    def serialize(
        self,
        stream: io.IOBase,
        rdf_format: str = "trig",
        PROV_N_MAP: dict[pm.QualifiedName, str] = ...,
        **kwargs: Any,
    ) -> None: ...
    document: Incomplete
    def deserialize(
        self,
        stream: io.IOBase,
        rdf_format: str = "trig",
        relation_mapper: dict[URIRef, str] = ...,
        predicate_mapper: dict[URIRef, pm.QualifiedName] = ...,
        **kwargs: Any,
    ) -> pm.ProvDocument: ...
    def valid_identifier(
        self, value: pm.QualifiedNameCandidate
    ) -> pm.QualifiedName | None: ...
    def encode_rdf_representation(self, value: Any) -> RDFLiteral | URIRef: ...
    def decode_rdf_representation(
        self, literal: Any, graph: ConjunctiveGraph
    ) -> Any: ...
    def encode_document(
        self, document: pm.ProvDocument, PROV_N_MAP: dict[pm.QualifiedName, str] = ...
    ) -> ConjunctiveGraph: ...
    def encode_container(
        self,
        bundle: pm.ProvBundle,
        PROV_N_MAP: dict[pm.QualifiedName, str] = ...,
        container: ConjunctiveGraph | None = None,
        identifier: str | None = None,
    ) -> ConjunctiveGraph: ...
    def decode_document(
        self,
        content: ConjunctiveGraph,
        document: pm.ProvDocument,
        relation_mapper: dict[URIRef, str] = ...,
        predicate_mapper: dict[URIRef, pm.QualifiedName] = ...,
    ) -> None: ...
    def decode_container(
        self,
        graph: ConjunctiveGraph,
        bundle: pm.ProvBundle,
        relation_mapper: dict[URIRef, str] = ...,
        predicate_mapper: dict[URIRef, pm.QualifiedName] = ...,
    ) -> None: ...

def walk(
    children: list, level: int = 0, path: dict = None, usename: bool = True
) -> Generator[dict]: ...
def literal_rdf_representation(literal: pm.Literal) -> RDFLiteral: ...
