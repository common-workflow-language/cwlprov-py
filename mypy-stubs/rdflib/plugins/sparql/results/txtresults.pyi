from rdflib import BNode as BNode, Literal as Literal, URIRef as URIRef
from rdflib.namespace import NamespaceManager as NamespaceManager
from rdflib.query import ResultSerializer as ResultSerializer
from rdflib.term import Variable as Variable
from typing import IO, Optional

class TXTResultSerializer(ResultSerializer):
    def serialize(self, stream: IO, encoding: str, namespace_manager: Optional[NamespaceManager] = ...): ...
