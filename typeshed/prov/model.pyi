from prov.constants import *
from prov import Error as Error, serializers as serializers
from prov.identifier import Identifier as Identifier, Namespace as Namespace, QualifiedName as QualifiedName
from typing import Any, List, Set

logger: Any

def parse_xsd_datetime(value): ...
def parse_boolean(value): ...

DATATYPE_PARSERS: Any
XSD_DATATYPE_PARSERS: Any

def parse_xsd_types(value, datatype): ...
def first(a_set): ...
def encoding_provn_value(value): ...

class Literal:
    def __init__(self, value, datatype: Any | None = ..., langtag: Any | None = ...) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self): ...
    @property
    def value(self): ...
    @property
    def datatype(self): ...
    @property
    def langtag(self): ...
    def has_no_langtag(self): ...
    def provn_representation(self): ...

class ProvException(Error): ...
class ProvWarning(Warning): ...

class ProvExceptionInvalidQualifiedName(ProvException):
    qname: Any
    def __init__(self, qname) -> None: ...

class ProvElementIdentifierRequired(ProvException): ...

class ProvRecord:
    FORMAL_ATTRIBUTES: Any
    def __init__(self, bundle, identifier, attributes: Any | None = ...) -> None: ...
    def __hash__(self): ...
    def copy(self): ...
    def get_type(self): ...
    def get_asserted_types(self): ...
    def add_asserted_type(self, type_identifier) -> None: ...
    def get_attribute(self, attr_name) -> Set[str]: ...
    @property
    def identifier(self) -> QualifiedName: ...
    @property
    def attributes(self): ...
    @property
    def args(self): ...
    @property
    def formal_attributes(self): ...
    @property
    def extra_attributes(self): ...
    @property
    def bundle(self): ...
    @property
    def label(self): ...
    @property
    def value(self): ...
    def add_attributes(self, attributes) -> None: ...
    def __eq__(self, other): ...
    def get_provn(self) -> str: ...
    def is_element(self): ...
    def is_relation(self): ...

class ProvElement(ProvRecord):
    def __init__(self, bundle, identifier, attributes: Any | None = ...) -> None: ...
    def is_element(self): ...

class ProvRelation(ProvRecord):
    def is_relation(self): ...

class ProvEntity(ProvElement):
    def wasGeneratedBy(self, activity, time: Any | None = ..., attributes: Any | None = ...): ...
    def wasInvalidatedBy(self, activity, time: Any | None = ..., attributes: Any | None = ...): ...
    def wasDerivedFrom(self, usedEntity, activity: Any | None = ..., generation: Any | None = ..., usage: Any | None = ..., attributes: Any | None = ...): ...
    def wasAttributedTo(self, agent, attributes: Any | None = ...): ...
    def alternateOf(self, alternate2): ...
    def specializationOf(self, generalEntity): ...
    def hadMember(self, entity): ...

class ProvActivity(ProvElement):
    FORMAL_ATTRIBUTES: Any
    def set_time(self, startTime: Any | None = ..., endTime: Any | None = ...) -> None: ...
    def get_startTime(self): ...
    def get_endTime(self): ...
    def used(self, entity, time: Any | None = ..., attributes: Any | None = ...): ...
    def wasInformedBy(self, informant, attributes: Any | None = ...): ...
    def wasStartedBy(self, trigger, starter: Any | None = ..., time: Any | None = ..., attributes: Any | None = ...): ...
    def wasEndedBy(self, trigger, ender: Any | None = ..., time: Any | None = ..., attributes: Any | None = ...): ...
    def wasAssociatedWith(self, agent, plan: Any | None = ..., attributes: Any | None = ...): ...

class ProvGeneration(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvUsage(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvCommunication(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvStart(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvEnd(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvInvalidation(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvDerivation(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvAgent(ProvElement):
    def actedOnBehalfOf(self, responsible, activity: Any | None = ..., attributes: Any | None = ...): ...

class ProvAttribution(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvAssociation(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvDelegation(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvInfluence(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvSpecialization(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvAlternate(ProvRelation):
    FORMAL_ATTRIBUTES: Any

class ProvMention(ProvSpecialization):
    FORMAL_ATTRIBUTES: Any

class ProvMembership(ProvRelation):
    FORMAL_ATTRIBUTES: Any

PROV_REC_CLS: Any
DEFAULT_NAMESPACES: Any

class NamespaceManager(dict):
    parent: Any
    def __init__(self, namespaces: Any | None = ..., default: Any | None = ..., parent: Any | None = ...) -> None: ...
    def get_namespace(self, uri): ...
    def get_registered_namespaces(self): ...
    def set_default_namespace(self, uri) -> None: ...
    def get_default_namespace(self): ...
    def add_namespace(self, namespace): ...
    def add_namespaces(self, namespaces) -> None: ...
    def valid_qualified_name(self, qname): ...
    def get_anonymous_identifier(self, local_prefix: str = ...): ...

class ProvBundle:
    def __init__(self, records: Any | None = ..., identifier: Any | None = ..., namespaces: Any | None = ..., document: Any | None = ...) -> None: ...
    @property
    def namespaces(self): ...
    @property
    def default_ns_uri(self): ...
    @property
    def document(self): ...
    @property
    def identifier(self): ...
    @property
    def records(self): ...
    def set_default_namespace(self, uri) -> None: ...
    def get_default_namespace(self): ...
    def add_namespace(self, namespace_or_prefix, uri: Any | None = ...): ...
    def get_registered_namespaces(self): ...
    def valid_qualified_name(self, identifier): ...
    def get_records(self, class_or_type_or_tuple: type | tuple[type | tuple[Any, ...], ...] | None = ...): ...
    def get_record(self, identifier) -> List[ProvRecord] | None: ...
    def is_document(self): ...
    def is_bundle(self): ...
    def has_bundles(self): ...
    @property
    def bundles(self): ...
    def get_provn(self, _indent_level: int = ...) -> str: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    __hash__: Any
    def unified(self) -> ProvBundle: ...
    def update(self, other) -> None: ...
    def new_record(self, record_type, identifier, attributes: Any | None = ..., other_attributes: Any | None = ...): ...
    def add_record(self, record): ...
    def entity(self, identifier, other_attributes: Any | None = ...): ...
    def activity(self, identifier, startTime: Any | None = ..., endTime: Any | None = ..., other_attributes: Any | None = ...): ...
    def generation(self, entity, activity: Any | None = ..., time: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def usage(self, activity, entity: Any | None = ..., time: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def start(self, activity, trigger: Any | None = ..., starter: Any | None = ..., time: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def end(self, activity, trigger: Any | None = ..., ender: Any | None = ..., time: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def invalidation(self, entity, activity: Any | None = ..., time: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def communication(self, informed, informant, identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def agent(self, identifier, other_attributes: Any | None = ...): ...
    def attribution(self, entity, agent, identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def association(self, activity, agent: Any | None = ..., plan: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def delegation(self, delegate, responsible, activity: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def influence(self, influencee, influencer, identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def derivation(self, generatedEntity, usedEntity, activity: Any | None = ..., generation: Any | None = ..., usage: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def revision(self, generatedEntity, usedEntity, activity: Any | None = ..., generation: Any | None = ..., usage: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def quotation(self, generatedEntity, usedEntity, activity: Any | None = ..., generation: Any | None = ..., usage: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def primary_source(self, generatedEntity, usedEntity, activity: Any | None = ..., generation: Any | None = ..., usage: Any | None = ..., identifier: Any | None = ..., other_attributes: Any | None = ...): ...
    def specialization(self, specificEntity, generalEntity): ...
    def alternate(self, alternate1, alternate2): ...
    def mention(self, specificEntity, generalEntity, bundle): ...
    def collection(self, identifier, other_attributes: Any | None = ...): ...
    def membership(self, collection, entity): ...
    def plot(self, filename: Any | None = ..., show_nary: bool = ..., use_labels: bool = ..., show_element_attributes: bool = ..., show_relation_attributes: bool = ...) -> None: ...
    wasGeneratedBy: Any
    used: Any
    wasStartedBy: Any
    wasEndedBy: Any
    wasInvalidatedBy: Any
    wasInformedBy: Any
    wasAttributedTo: Any
    wasAssociatedWith: Any
    actedOnBehalfOf: Any
    wasInfluencedBy: Any
    wasDerivedFrom: Any
    wasRevisionOf: Any
    wasQuotedFrom: Any
    hadPrimarySource: Any
    alternateOf: Any
    specializationOf: Any
    mentionOf: Any
    hadMember: Any

class ProvDocument(ProvBundle):
    def __init__(self, records: Any | None = ..., namespaces: Any | None = ...) -> None: ...
    def __eq__(self, other): ...
    def is_document(self): ...
    def is_bundle(self): ...
    def has_bundles(self): ...
    @property
    def bundles(self): ...
    def flattened(self): ...
    def unified(self) -> ProvBundle: ...
    def update(self, other) -> None: ...
    def add_bundle(self, bundle, identifier: Any | None = ...) -> None: ...
    def bundle(self, identifier): ...
    def serialize(self, destination: Any | None = ..., format: str = ..., **args): ...
    @staticmethod
    def deserialize(source: Any | None = ..., content: Any | None = ..., format: str = ..., **args) -> ProvDocument: ...

def sorted_attributes(element, attributes): ...
