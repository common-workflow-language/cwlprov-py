from prov.constants import *
import datetime
import io
import typing
from _typeshed import Incomplete
from prov import Error as Error, serializers as serializers
from prov.identifier import (
    Identifier as Identifier,
    Namespace as Namespace,
    QualifiedName as QualifiedName,
)
from typing import Any, Callable, Iterable, Optional, Union
from typing_extensions import TypeAlias
import os

QualifiedNameCandidate: TypeAlias = Union[QualifiedName, str, Identifier]
OptionalID: TypeAlias = Optional[QualifiedNameCandidate]
EntityRef: TypeAlias = Union["ProvEntity", QualifiedNameCandidate]
ActivityRef: TypeAlias = Union["ProvActivity", QualifiedNameCandidate]
AgentRef: TypeAlias = Union[
    "ProvAgent", "ProvEntity", "ProvActivity", QualifiedNameCandidate
]
GenrationRef: TypeAlias = Union["ProvGeneration", QualifiedNameCandidate]
UsageRef: TypeAlias = Union["ProvUsage", QualifiedNameCandidate]
RecordAttributesArg: TypeAlias = Union[
    dict[QualifiedNameCandidate, Any], Iterable[tuple[QualifiedNameCandidate, Any]]
]
NameValuePair: TypeAlias = tuple[QualifiedName, Any]
DatetimeOrStr: TypeAlias = Union[datetime.datetime, str]
NSCollection: TypeAlias = dict[str, str] | Iterable[Namespace]
PathLike: TypeAlias = Union[str, bytes, os.PathLike[Any]]

def parse_xsd_datetime(value: str) -> datetime.datetime | None: ...
def parse_boolean(value: str) -> bool | None: ...

DATATYPE_PARSERS = {
    datetime.datetime: parse_xsd_datetime,
}
# Mappings for XSD datatypes to Python standard types
SupportedXSDParsedTypes: TypeAlias = (
    str | datetime.datetime | float | int | bool | Identifier | None
)
XSD_DATATYPE_PARSERS: dict[QualifiedName, Callable[[str], SupportedXSDParsedTypes]]

def parse_xsd_types(value: str, datatype: QualifiedName) -> SupportedXSDParsedTypes: ...
def first(a_set: set[Any]) -> Any | None: ...
def encoding_provn_value(
    value: str | datetime.datetime | float | bool | QualifiedName,
) -> str: ...

class Literal:
    def __init__(
        self,
        value: Any,
        datatype: QualifiedName | None = None,
        langtag: str | None = None,
    ) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    @property
    def value(self) -> str: ...
    @property
    def datatype(self) -> QualifiedName | None: ...
    @property
    def langtag(self) -> str | None: ...
    def has_no_langtag(self) -> bool: ...
    def provn_representation(self) -> str: ...

class ProvException(Error): ...
class ProvWarning(Warning): ...

class ProvExceptionInvalidQualifiedName(ProvException):
    qname: Incomplete
    def __init__(self, qname: Any) -> None: ...

class ProvElementIdentifierRequired(ProvException): ...

class ProvRecord:
    FORMAL_ATTRIBUTES: tuple[QualifiedName, ...]
    def __init__(
        self,
        bundle: ProvBundle,
        identifier: QualifiedName | None,
        attributes: RecordAttributesArg | None = None,
    ) -> None: ...
    def __hash__(self) -> int: ...
    def copy(self) -> ProvRecord: ...
    def get_type(self) -> QualifiedName: ...
    def get_asserted_types(self) -> set[QualifiedName]: ...
    def add_asserted_type(self, type_identifier: QualifiedName) -> None: ...
    def get_attribute(
        self, attr_name: QualifiedNameCandidate
    ) -> set[QualifiedName]: ...
    @property
    def identifier(self) -> QualifiedName | None: ...
    @property
    def attributes(self) -> list[tuple[QualifiedName, Any]]: ...
    @property
    def args(self) -> tuple[QualifiedName, ...]: ...
    @property
    def formal_attributes(self) -> tuple[tuple[QualifiedName, Any], ...]: ...
    @property
    def extra_attributes(self) -> tuple[tuple[QualifiedName, Any], ...]: ...
    @property
    def bundle(self) -> ProvBundle: ...
    @property
    def label(self) -> str: ...
    @property
    def value(self) -> Any: ...
    def add_attributes(self, attributes: RecordAttributesArg) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def get_provn(self) -> str: ...
    def is_element(self) -> bool: ...
    def is_relation(self) -> bool: ...

class ProvElement(ProvRecord):
    def __init__(
        self,
        bundle: ProvBundle,
        identifier: QualifiedName | None,
        attributes: RecordAttributesArg | None = None,
    ) -> None: ...
    def is_element(self) -> bool: ...

class ProvRelation(ProvRecord):
    def is_relation(self) -> bool: ...

class ProvEntity(ProvElement):
    def wasGeneratedBy(
        self,
        activity: ActivityRef | None = None,
        time: DatetimeOrStr | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvEntity: ...
    def wasInvalidatedBy(
        self,
        activity: ActivityRef | None,
        time: DatetimeOrStr | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvEntity: ...
    def wasDerivedFrom(
        self,
        usedEntity: EntityRef,
        activity: ActivityRef | None = None,
        generation: GenrationRef | None = None,
        usage: UsageRef | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvEntity: ...
    def wasAttributedTo(
        self, agent: AgentRef, attributes: RecordAttributesArg | None = None
    ) -> ProvEntity: ...
    def alternateOf(self, alternate2: EntityRef) -> ProvEntity: ...
    def specializationOf(self, generalEntity: EntityRef) -> ProvEntity: ...
    def hadMember(self, entity: EntityRef) -> ProvEntity: ...

class ProvActivity(ProvElement):
    FORMAL_ATTRIBUTES: Incomplete
    def set_time(
        self,
        startTime: datetime.datetime | None = None,
        endTime: datetime.datetime | None = None,
    ) -> None: ...
    def get_startTime(self) -> datetime.datetime | None: ...
    def get_endTime(self) -> datetime.datetime | None: ...
    def used(
        self,
        entity: EntityRef,
        time: DatetimeOrStr | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvActivity: ...
    def wasInformedBy(
        self, informant: ActivityRef, attributes: RecordAttributesArg | None = None
    ) -> ProvActivity: ...
    def wasStartedBy(
        self,
        trigger: EntityRef | None,
        starter: ActivityRef | None = None,
        time: DatetimeOrStr | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvActivity: ...
    def wasEndedBy(
        self,
        trigger: EntityRef | None,
        ender: ActivityRef | None = None,
        time: DatetimeOrStr | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvActivity: ...
    def wasAssociatedWith(
        self,
        agent: AgentRef,
        plan: EntityRef | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvActivity: ...

class ProvGeneration(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvUsage(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvCommunication(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvStart(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvEnd(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvInvalidation(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvDerivation(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvAgent(ProvElement):
    def actedOnBehalfOf(
        self,
        responsible: AgentRef,
        activity: ActivityRef | None = None,
        attributes: RecordAttributesArg | None = None,
    ) -> ProvAgent: ...

class ProvAttribution(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvAssociation(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvDelegation(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvInfluence(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvSpecialization(ProvRelation):
    FORMAL_ATTRIBUTES: tuple[QualifiedName, ...]

class ProvAlternate(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

class ProvMention(ProvSpecialization):
    FORMAL_ATTRIBUTES: Incomplete

class ProvMembership(ProvRelation):
    FORMAL_ATTRIBUTES: Incomplete

PROV_REC_CLS: Incomplete
DEFAULT_NAMESPACES: Incomplete

class NamespaceManager(dict[str, Namespace]):
    parent: NamespaceManager | None
    def __init__(
        self,
        namespaces: NSCollection | None = None,
        default: str | None = None,
        parent: NamespaceManager | None = None,
    ) -> None: ...
    def get_namespace(self, uri: str) -> Namespace | None: ...
    def get_registered_namespaces(self) -> Iterable[Namespace]: ...
    def set_default_namespace(self, uri: str) -> None: ...
    def get_default_namespace(self) -> Namespace | None: ...
    def add_namespace(self, namespace: Namespace) -> Namespace: ...
    def add_namespaces(self, namespaces: NSCollection) -> None: ...
    def valid_qualified_name(
        self, qname: QualifiedNameCandidate
    ) -> QualifiedName | None: ...
    def get_anonymous_identifier(self, local_prefix: str = "id") -> Identifier: ...

class ProvBundle:
    def __init__(
        self,
        records: Iterable[ProvRecord] | None = None,
        identifier: QualifiedName | None = None,
        namespaces: NSCollection | None = None,
        document: ProvDocument | None = None,
    ) -> None: ...
    @property
    def namespaces(self) -> set[Namespace]: ...
    @property
    def default_ns_uri(self) -> str | None: ...
    @property
    def document(self) -> ProvDocument | None: ...
    @property
    def identifier(self) -> QualifiedName | None: ...
    @property
    def records(self) -> list[ProvRecord]: ...
    def set_default_namespace(self, uri: str) -> None: ...
    def get_default_namespace(self) -> Namespace | None: ...
    def add_namespace(
        self, namespace_or_prefix: Namespace | str, uri: str | None = None
    ) -> Namespace: ...
    def get_registered_namespaces(self) -> Iterable[Namespace]: ...
    def valid_qualified_name(
        self, identifier: QualifiedNameCandidate
    ) -> QualifiedName | None: ...
    def mandatory_valid_qname(
        self, identifier: QualifiedNameCandidate
    ) -> QualifiedName: ...
    def get_records(
        self, class_or_type_or_tuple: type | tuple[type] | None = None
    ) -> Iterable[ProvRecord]: ...
    def get_record(self, identifier: QualifiedNameCandidate) -> list[ProvRecord]: ...
    def is_document(self) -> bool: ...
    def is_bundle(self) -> bool: ...
    def has_bundles(self) -> bool: ...
    @property
    def bundles(self) -> Iterable[ProvBundle]: ...
    def get_provn(self, _indent_level: int = 0) -> str: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    __hash__: Incomplete
    def unified(self) -> ProvBundle: ...
    def update(self, other: ProvBundle) -> None: ...
    def new_record(
        self,
        record_type: QualifiedName,
        identifier: OptionalID,
        attributes: RecordAttributesArg | None = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvRecord: ...
    def add_record(self, record: ProvRecord) -> ProvRecord: ...
    def entity(
        self,
        identifier: QualifiedNameCandidate,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvEntity: ...
    def activity(
        self,
        identifier: QualifiedNameCandidate,
        startTime: DatetimeOrStr | None = None,
        endTime: DatetimeOrStr | None = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvActivity: ...
    def generation(
        self,
        entity: EntityRef,
        activity: ActivityRef | None = None,
        time: DatetimeOrStr | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvRecord: ...
    def usage(
        self,
        activity: ActivityRef,
        entity: EntityRef | None = None,
        time: DatetimeOrStr | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvUsage: ...
    def start(
        self,
        activity: ActivityRef,
        trigger: EntityRef | None = None,
        starter: ActivityRef | None = None,
        time: DatetimeOrStr | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvStart: ...
    def end(
        self,
        activity: ActivityRef,
        trigger: EntityRef | None = None,
        ender: ActivityRef | None = None,
        time: DatetimeOrStr | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvEnd: ...
    def invalidation(
        self,
        entity: EntityRef,
        activity: ActivityRef | None = None,
        time: DatetimeOrStr | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvInvalidation: ...
    def communication(
        self,
        informed: ActivityRef,
        informant: ActivityRef,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvCommunication: ...
    def agent(
        self,
        identifier: QualifiedNameCandidate,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvAgent: ...
    def attribution(
        self,
        entity: EntityRef,
        agent: AgentRef,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvAttribution: ...
    def association(
        self,
        activity: ActivityRef,
        agent: AgentRef | None = None,
        plan: EntityRef | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvAssociation: ...
    def delegation(
        self,
        delegate: AgentRef,
        responsible: AgentRef,
        activity: ActivityRef | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvDelegation: ...
    def influence(
        self,
        influencee: EntityRef | ActivityRef | AgentRef,
        influencer: EntityRef | ActivityRef | AgentRef,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvInfluence: ...
    def derivation(
        self,
        generatedEntity: EntityRef,
        usedEntity: EntityRef,
        activity: ActivityRef | None = None,
        generation: GenrationRef | None = None,
        usage: UsageRef | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvDerivation: ...
    def revision(
        self,
        generatedEntity: EntityRef,
        usedEntity: EntityRef,
        activity: ActivityRef | None = None,
        generation: GenrationRef | None = None,
        usage: UsageRef | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvDerivation: ...
    def quotation(
        self,
        generatedEntity: EntityRef,
        usedEntity: EntityRef,
        activity: ActivityRef | None = None,
        generation: GenrationRef | None = None,
        usage: UsageRef | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvDerivation: ...
    def primary_source(
        self,
        generatedEntity: EntityRef,
        usedEntity: EntityRef,
        activity: ActivityRef | None = None,
        generation: GenrationRef | None = None,
        usage: UsageRef | None = None,
        identifier: OptionalID = None,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvDerivation: ...
    def specialization(
        self, specificEntity: EntityRef, generalEntity: EntityRef
    ) -> ProvSpecialization: ...
    def alternate(
        self, alternate1: EntityRef, alternate2: EntityRef
    ) -> ProvAlternate: ...
    def mention(
        self, specificEntity: EntityRef, generalEntity: EntityRef, bundle: EntityRef
    ) -> ProvMention: ...
    def collection(
        self,
        identifier: QualifiedNameCandidate,
        other_attributes: RecordAttributesArg | None = None,
    ) -> ProvEntity: ...
    def membership(
        self, collection: EntityRef, entity: EntityRef
    ) -> ProvMembership: ...
    def plot(
        self,
        filename: PathLike | None = None,
        show_nary: bool = True,
        use_labels: bool = False,
        show_element_attributes: bool = True,
        show_relation_attributes: bool = True,
    ) -> None: ...
    wasGeneratedBy = generation
    used = usage
    wasStartedBy = start
    wasEndedBy = end
    wasInvalidatedBy = invalidation
    wasInformedBy = communication
    wasAttributedTo = attribution
    wasAssociatedWith = association
    actedOnBehalfOf = delegation
    wasInfluencedBy = influence
    wasDerivedFrom = derivation
    wasRevisionOf = revision
    wasQuotedFrom = quotation
    hadPrimarySource = primary_source
    alternateOf = alternate
    specializationOf = specialization
    mentionOf = mention
    hadMember = membership

class ProvDocument(ProvBundle):
    def __init__(
        self,
        records: Iterable[ProvRecord] | None = None,
        namespaces: NSCollection | None = None,
    ) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def is_document(self) -> bool: ...
    def is_bundle(self) -> bool: ...
    def has_bundles(self) -> bool: ...
    @property
    def bundles(self) -> Iterable[ProvBundle]: ...
    def flattened(self) -> ProvDocument: ...
    def unified(self) -> ProvDocument: ...
    def update(self, other: ProvBundle) -> None: ...
    def add_bundle(
        self, bundle: ProvBundle, identifier: QualifiedName | None = None
    ) -> None: ...
    def bundle(self, identifier: QualifiedNameCandidate) -> ProvBundle: ...
    def serialize(
        self,
        destination: io.IOBase | PathLike | None = None,
        format: str = "json",
        **args: Any,
    ) -> str | None: ...
    @staticmethod
    def deserialize(
        source: io.IOBase | PathLike | None = None,
        content: str | bytes | None = None,
        format: str = "json",
        **args: Any,
    ) -> ProvDocument: ...

def sorted_attributes(
    element: QualifiedName, attributes: Iterable[NameValuePair]
) -> list[NameValuePair]: ...
