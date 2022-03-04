from rdflib.namespace import DefinedNamespace as DefinedNamespace, Namespace as Namespace
from rdflib.term import URIRef as URIRef

class DCAM(DefinedNamespace):
    domainIncludes: URIRef
    memberOf: URIRef
    rangeIncludes: URIRef
    VocabularyEncodingScheme: URIRef
