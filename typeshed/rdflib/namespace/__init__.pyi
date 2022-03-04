from collections.abc import Generator
from typing import Any

from rdflib.namespace._BRICK import BRICK
from rdflib.namespace._CSVW import CSVW
from rdflib.namespace._DC import DC
from rdflib.namespace._DCAT import DCAT
from rdflib.namespace._DCMITYPE import DCMITYPE
from rdflib.namespace._DCTERMS import DCTERMS
from rdflib.namespace._DCAM import DCAM
from rdflib.namespace._DOAP import DOAP
from rdflib.namespace._FOAF import FOAF
from rdflib.namespace._ODRL2 import ODRL2
from rdflib.namespace._ORG import ORG
from rdflib.namespace._OWL import OWL
from rdflib.namespace._PROF import PROF
from rdflib.namespace._PROV import PROV
from rdflib.namespace._QB import QB
from rdflib.namespace._RDF import RDF
from rdflib.namespace._RDFS import RDFS
from rdflib.namespace._SDO import SDO
from rdflib.namespace._SH import SH
from rdflib.namespace._SKOS import SKOS
from rdflib.namespace._SOSA import SOSA
from rdflib.namespace._SSN import SSN
from rdflib.namespace._TIME import TIME
from rdflib.namespace._VANN import VANN
from rdflib.namespace._VOID import VOID
from rdflib.namespace._XSD import XSD

__all__ = [
    "is_ncname",
    "split_uri",
    "Namespace",
    "ClosedNamespace",
    "NamespaceManager",
    "BRICK",
    "RDF",
    "RDFS",
    "CSVW",
    "DC",
    "DCAT",
    "DCMITYPE",
    "DCTERMS",
    "DOAP",
    "FOAF",
    "ODRL2",
    "ORG",
    "OWL",
    "PROF",
    "PROV",
    "QB",
    "SDO",
    "SH",
    "SKOS",
    "SOSA",
    "SSN",
    "TIME",
    "VANN",
    "VOID",
    "XSD",
    "OWL",
]

class Namespace(str):
    def __new__(cls, value: Any): ...
    @property
    def title(self): ...
    def term(self, name: Any): ...
    def __getitem__(self, key: Any): ...
    def __getattr__(self, name: Any): ...
    def __contains__(self, ref): ...

class URIPattern(str):
    def __new__(cls, value: Any): ...
    def __mod__(self, *args: Any, **kwargs: Any): ...
    def format(self, *args: Any, **kwargs: Any): ...

class DefinedNamespaceMeta(type):
    def __getitem__(cls, name, default: Any | None = ...): ...
    def __getattr__(cls, name): ...
    def __add__(cls, other): ...
    def __contains__(cls, item): ...

class DefinedNamespace(metaclass=DefinedNamespaceMeta):
    def __init__(self) -> None: ...

class ClosedNamespace(Namespace):
    def __new__(cls, uri: Any, terms: Any): ...
    @property
    def uri(self): ...
    def term(self, name: Any): ...
    def __getitem__(self, key: Any): ...
    def __getattr__(self, name: Any): ...
    def __dir__(self): ...
    def __contains__(self, ref): ...

class NamespaceManager:
    graph: Any
    def __init__(self, graph) -> None: ...
    def __contains__(self, ref): ...
    def reset(self) -> None: ...
    @property
    def store(self): ...
    def qname(self, uri): ...
    def qname_strict(self, uri): ...
    def normalizeUri(self, rdfTerm) -> str: ...
    def compute_qname(self, uri, generate: bool = ...): ...
    def compute_qname_strict(self, uri, generate: bool = ...): ...
    def bind(self, prefix, namespace, override: bool = ..., replace: bool = ...) -> None: ...
    def namespaces(self) -> Generator[Any, None, None]: ...
    def absolutize(self, uri, defrag: int = ...): ...

def is_ncname(name): ...

XMLNS = "http://www.w3.org/XML/1998/namespace"

def split_uri(uri: Any, split_start: Any = ...): ...

from rdflib.namespace._CSVW import CSVW
from rdflib.namespace._DC import DC
from rdflib.namespace._DCAT import DCAT
from rdflib.namespace._DCTERMS import DCTERMS
from rdflib.namespace._DOAP import DOAP
from rdflib.namespace._FOAF import FOAF
from rdflib.namespace._ODRL2 import ODRL2
from rdflib.namespace._ORG import ORG
from rdflib.namespace._OWL import OWL
from rdflib.namespace._PROF import PROF
from rdflib.namespace._PROV import PROV
from rdflib.namespace._QB import QB
from rdflib.namespace._RDF import RDF
from rdflib.namespace._RDFS import RDFS
from rdflib.namespace._SDO import SDO
from rdflib.namespace._SH import SH
from rdflib.namespace._SKOS import SKOS
from rdflib.namespace._SOSA import SOSA
from rdflib.namespace._SSN import SSN
from rdflib.namespace._TIME import TIME
from rdflib.namespace._VOID import VOID
from rdflib.namespace._XSD import XSD
