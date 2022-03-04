from rdflib.namespace import DefinedNamespace as DefinedNamespace, Namespace as Namespace
from rdflib.term import URIRef as URIRef

class DCMITYPE(DefinedNamespace):
    Collection: URIRef
    Dataset: URIRef
    Event: URIRef
    Image: URIRef
    InteractiveResource: URIRef
    MovingImage: URIRef
    PhysicalObject: URIRef
    Service: URIRef
    Software: URIRef
    Sound: URIRef
    StillImage: URIRef
    Text: URIRef
