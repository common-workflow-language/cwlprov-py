from prov.constants import *
import prov.identifier
from prov.model import DEFAULT_NAMESPACES as DEFAULT_NAMESPACES, sorted_attributes as sorted_attributes
from prov.serializers import Serializer as Serializer
from typing import Any

logger: Any
FULL_NAMES_MAP: Any
FULL_PROV_RECORD_IDS_MAP: Any
XML_XSD_URI: str

class ProvXMLException(prov.Error): ...

class ProvXMLSerializer(Serializer):
    def serialize(self, stream, force_types: bool = ..., **kwargs) -> None: ...
    def serialize_bundle(self, bundle, element: Any | None = ..., force_types: bool = ...): ...
    def deserialize(self, stream, **kwargs): ...
    def deserialize_subtree(self, xml_doc, bundle): ...

def xml_qname_to_QualifiedName(element, qname_str): ...
