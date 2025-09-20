from prov.constants import *
import io
import prov
from _typeshed import Incomplete
from lxml import etree
from prov.model import (
    DEFAULT_NAMESPACES as DEFAULT_NAMESPACES,
    sorted_attributes as sorted_attributes,
)
from prov.serializers import Serializer as Serializer
from typing import Any

logger: Incomplete
FULL_NAMES_MAP: Incomplete
FULL_PROV_RECORD_IDS_MAP: Incomplete
XML_XSD_URI: str

class ProvXMLException(prov.Error): ...

class ProvXMLSerializer(Serializer):
    def serialize(
        self, stream: io.IOBase, force_types: bool = False, **kwargs: Any
    ) -> None: ...
    def serialize_bundle(
        self,
        bundle: prov.model.ProvBundle,
        element: etree._Element | None = None,
        force_types: bool = False,
    ) -> etree._Element: ...
    def deserialize(
        self, stream: io.IOBase, **kwargs: Any
    ) -> prov.model.ProvDocument: ...
    def deserialize_subtree(
        self,
        xml_doc: etree._Element,
        bundle: prov.model.ProvDocument | prov.model.ProvBundle,
    ) -> prov.model.ProvDocument | prov.model.ProvBundle: ...

def xml_qname_to_QualifiedName(
    element: etree._Element, qname_str: str
) -> prov.model.QualifiedName: ...
