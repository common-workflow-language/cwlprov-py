from collections.abc import Generator
from prov import Error as Error
from prov.constants import PROV as PROV, PROV_ACTIVITY as PROV_ACTIVITY, PROV_ALTERNATE as PROV_ALTERNATE, PROV_ASSOCIATION as PROV_ASSOCIATION, PROV_ATTR_ENDER as PROV_ATTR_ENDER, PROV_ATTR_ENDTIME as PROV_ATTR_ENDTIME, PROV_ATTR_INFORMANT as PROV_ATTR_INFORMANT, PROV_ATTR_RESPONSIBLE as PROV_ATTR_RESPONSIBLE, PROV_ATTR_STARTER as PROV_ATTR_STARTER, PROV_ATTR_STARTTIME as PROV_ATTR_STARTTIME, PROV_ATTR_TIME as PROV_ATTR_TIME, PROV_ATTR_TRIGGER as PROV_ATTR_TRIGGER, PROV_ATTR_USED_ENTITY as PROV_ATTR_USED_ENTITY, PROV_BASE_CLS as PROV_BASE_CLS, PROV_COMMUNICATION as PROV_COMMUNICATION, PROV_DELEGATION as PROV_DELEGATION, PROV_DERIVATION as PROV_DERIVATION, PROV_END as PROV_END, PROV_GENERATION as PROV_GENERATION, PROV_ID_ATTRIBUTES_MAP as PROV_ID_ATTRIBUTES_MAP, PROV_INVALIDATION as PROV_INVALIDATION, PROV_LOCATION as PROV_LOCATION, PROV_MENTION as PROV_MENTION, PROV_N_MAP as PROV_N_MAP, PROV_ROLE as PROV_ROLE, PROV_START as PROV_START, PROV_USAGE as PROV_USAGE, XSD_QNAME as XSD_QNAME
from prov.serializers import Serializer as Serializer
from typing import Any

class ProvRDFException(Error): ...

class AnonymousIDGenerator:
    def __init__(self) -> None: ...
    def get_anon_id(self, obj, local_prefix: str = ...): ...

LITERAL_XSDTYPE_MAP: Any
relation_mapper: Any
predicate_mapper: Any

def attr2rdf(attr): ...
def valid_qualified_name(bundle, value, xsd_qname: bool = ...): ...

class ProvRDFSerializer(Serializer):
    def serialize(self, stream: Any | None = ..., rdf_format: str = ..., PROV_N_MAP=..., **kwargs) -> None: ...
    document: Any
    def deserialize(self, stream, rdf_format: str = ..., relation_mapper=..., predicate_mapper=..., **kwargs): ...
    def valid_identifier(self, value): ...
    def encode_rdf_representation(self, value): ...
    def decode_rdf_representation(self, literal, graph): ...
    def encode_document(self, document, PROV_N_MAP=...): ...
    def encode_container(self, bundle, PROV_N_MAP=..., container: Any | None = ..., identifier: Any | None = ...): ...
    def decode_document(self, content, document, relation_mapper=..., predicate_mapper=...) -> None: ...
    def decode_container(self, graph, bundle, relation_mapper=..., predicate_mapper=...) -> None: ...

def walk(children, level: int = ..., path: Any | None = ..., usename: bool = ...) -> Generator[Any, None, None]: ...
def literal_rdf_representation(literal): ...