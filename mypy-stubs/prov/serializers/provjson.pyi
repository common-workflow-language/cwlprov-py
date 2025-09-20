from prov.constants import *
import io
import json
from _typeshed import Incomplete
from prov import Error as Error
from prov.model import (
    Identifier as Identifier,
    Literal as Literal,
    Namespace as Namespace,
    ProvBundle as ProvBundle,
    ProvDocument as ProvDocument,
    ProvRecord as ProvRecord,
    QualifiedName as QualifiedName,
    QualifiedNameCandidate as QualifiedNameCandidate,
    first as first,
    parse_xsd_datetime as parse_xsd_datetime,
)
from prov.serializers import Serializer as Serializer
from typing import Any

logger: Incomplete
ProvJSONDict = dict[str, dict[str, Any]]

class ProvJSONException(Error): ...

class AnonymousIDGenerator:
    def __init__(self) -> None: ...
    def get_anon_id(self, obj: ProvRecord, local_prefix: str = "id") -> Identifier: ...

LITERAL_XSDTYPE_MAP: Incomplete

class ProvJSONSerializer(Serializer):
    def serialize(self, stream: io.IOBase, **args: Any) -> None: ...
    def deserialize(self, stream: io.IOBase, **args: Any) -> ProvDocument: ...

class ProvJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any: ...

class ProvJSONDecoder(json.JSONDecoder):
    def decode(self, s: str, *args: Any, **kwargs: Any) -> Any: ...

def valid_qualified_name(
    bundle: ProvBundle, value: QualifiedNameCandidate | None
) -> QualifiedName | None: ...
def encode_json_document(document: ProvDocument) -> ProvJSONDict: ...
def encode_json_container(bundle: ProvBundle) -> ProvJSONDict: ...
def decode_json_document(content: ProvJSONDict, document: ProvDocument) -> None: ...
def decode_json_container(jc: ProvJSONDict, bundle: ProvBundle) -> None: ...
def encode_json_representation(value: Any) -> Any: ...
def decode_json_representation(literal: Any, bundle: ProvBundle) -> Any: ...
def literal_json_representation(literal: Literal) -> dict[str, str]: ...
