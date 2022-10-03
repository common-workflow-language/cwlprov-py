from rdflib.namespace import DefinedNamespace as DefinedNamespace, Namespace as Namespace
from rdflib.term import URIRef as URIRef

class VANN(DefinedNamespace):
    changes: URIRef
    example: URIRef
    preferredNamespacePrefix: URIRef
    preferredNamespaceUri: URIRef
    termGroup: URIRef
    usageNote: URIRef
