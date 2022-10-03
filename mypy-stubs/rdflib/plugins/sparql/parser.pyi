from .parserutils import Comp as Comp, Param as Param, ParamList as ParamList
from rdflib.compat import decodeUnicodeEscape as decodeUnicodeEscape
from typing import Any

DEBUG: bool

def neg(literal): ...
def setLanguage(terms): ...
def setDataType(terms): ...
def expandTriples(terms): ...
def expandBNodeTriples(terms): ...
def expandCollection(terms): ...

IRIREF: Any
PN_CHARS_BASE_re: str
PN_CHARS_U_re: Any
PN_CHARS_re: Any
PN_PREFIX: Any
PNAME_NS: Any
PN_LOCAL_ESC_re: str
PERCENT_re: str
PLX_re: Any
PN_LOCAL: Any
PNAME_LN: Any
BLANK_NODE_LABEL: Any
VARNAME: Any
VAR1: Any
VAR2: Any
LANGTAG: Any
INTEGER: Any
EXPONENT_re: str
DECIMAL: Any
DOUBLE: Any
INTEGER_POSITIVE: Any
DECIMAL_POSITIVE: Any
DOUBLE_POSITIVE: Any
INTEGER_NEGATIVE: Any
DECIMAL_NEGATIVE: Any
DOUBLE_NEGATIVE: Any
STRING_LITERAL_LONG1: Any
STRING_LITERAL_LONG2: Any
STRING_LITERAL1: Any
STRING_LITERAL2: Any
NIL: Any
ANON: Any
A: Any
BaseDecl: Any
PrefixDecl: Any
Prologue: Any
Var: Any
PrefixedName: Any
iri: Any
String: Any
RDFLiteral: Any
NumericLiteralPositive: Any
NumericLiteralNegative: Any
NumericLiteralUnsigned: Any
NumericLiteral: Any
BooleanLiteral: Any
BlankNode: Any
GraphTerm: Any
VarOrTerm: Any
VarOrIri: Any
GraphRef: Any
GraphRefAll: Any
GraphOrDefault: Any
DataBlockValue: Any
Verb: Any
VerbSimple = Var
Integer = INTEGER
TriplesNode: Any
TriplesNodePath: Any
GraphNode: Any
GraphNodePath: Any
PathMod: Any
PathOneInPropertySet: Any
Path: Any
PathNegatedPropertySet: Any
PathPrimary: Any
PathElt: Any
PathEltOrInverse: Any
PathSequence: Any
PathAlternative: Any
VerbPath = Path
ObjectPath = GraphNodePath
ObjectListPath: Any
GroupGraphPattern: Any
Collection: Any
CollectionPath: Any
Object = GraphNode
ObjectList: Any
PropertyListPathNotEmpty: Any
PropertyListPath: Any
PropertyListNotEmpty: Any
PropertyList: Any
BlankNodePropertyList: Any
BlankNodePropertyListPath: Any
TriplesSameSubject: Any
TriplesTemplate: Any
QuadsNotTriples: Any
Quads: Any
QuadPattern: Any
QuadData: Any
TriplesSameSubjectPath: Any
TriplesBlock: Any
MinusGraphPattern: Any
GroupOrUnionGraphPattern: Any
Expression: Any
ExpressionList: Any
RegexExpression: Any
SubstringExpression: Any
StrReplaceExpression: Any
ExistsFunc: Any
NotExistsFunc: Any
Aggregate: Any
BuiltInCall: Any
ArgList: Any
iriOrFunction: Any
FunctionCall: Any
BrackettedExpression: Any
PrimaryExpression: Any
UnaryExpression: Any
MultiplicativeExpression: Any
AdditiveExpression: Any
NumericExpression = AdditiveExpression
RelationalExpression: Any
ValueLogical = RelationalExpression
ConditionalAndExpression: Any
ConditionalOrExpression: Any
Constraint: Any
Filter: Any
SourceSelector = iri
DefaultGraphClause = SourceSelector
NamedGraphClause: Any
DatasetClause: Any
GroupCondition: Any
GroupClause: Any
Load: Any
Clear: Any
Drop: Any
Create: Any
Add: Any
Move: Any
Copy: Any
InsertData: Any
DeleteData: Any
DeleteWhere: Any
DeleteClause: Any
InsertClause: Any
UsingClause: Any
Modify: Any
Update1: Any
InlineDataOneVar: Any
InlineDataFull: Any
DataBlock: Any
ValuesClause: Any
ConstructTriples: Any
ConstructTemplate: Any
OptionalGraphPattern: Any
GraphGraphPattern: Any
ServiceGraphPattern: Any
Bind: Any
InlineData: Any
GraphPatternNotTriples: Any
GroupGraphPatternSub: Any
HavingCondition = Constraint
HavingClause: Any
OrderCondition: Any
OrderClause: Any
LimitClause: Any
OffsetClause: Any
LimitOffsetClauses: Any
SolutionModifier: Any
SelectClause: Any
WhereClause: Any
SubSelect: Any
SelectQuery: Any
ConstructQuery: Any
AskQuery: Any
DescribeQuery: Any
Update: Any
Query: Any
UpdateUnit: Any
QueryUnit = Query
expandUnicodeEscapes_re: Any

def expandUnicodeEscapes(q): ...
def parseQuery(q): ...
def parseUpdate(q): ...
