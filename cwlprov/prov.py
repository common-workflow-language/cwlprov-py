# © 2018 Software Freedom Conservancy (SFC)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


"""
cwlprov Provenance

"""
__author__      = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__   = "© 2018 Software Freedom Conservancy (SFC)"
__license__     = "Apache License, version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"

import logging
from prov.identifier import Identifier, Namespace
from prov.model import *
from .utils import *

CWLPROV = Namespace("cwlprov", "https://w3id.org/cwl/prov#")

_logger = logging.getLogger(__name__)

MEDIA_TYPES = {
    "ttl": 'text/turtle; charset="UTF-8"',
    "rdf": 'application/rdf+xml',
    "json": 'application/json',
    "jsonld": 'application/ld+json',
    "xml": 'application/xml',
    "provn": 'text/provenance-notation; charset="UTF-8"',
    "nt": 'application/n-triples',
}
EXTENSIONS = dict((v,k) for (k,v) in MEDIA_TYPES.items())

def _as_identifier(uri_or_identifier):
    if not uri_or_identifier:
        return None
    if isinstance(uri_or_identifier, Identifier):
        return uri_or_identifier
    else:
        return Identifier(str(uri_or_identifier))

def _prov_attr(attr, elem):
    return first(elem.get_attribute(attr))

class Provenance:
    def __init__(self, ro, run=None):
        self.ro = ro
        self.run_id = Identifier(run or ro.workflow_id)
        self._path = None
        self.prov_doc, self._path = self._load_prov_document()
        if not self.prov_doc:
            raise OSError("No provenance found for %s" % self.run_id)

    def __repr__(self):
        return "Provenance<%s from %s>" % (self.uri, self._path)


    @property
    def uri(self):
        return self.run_id.uri

    def entity(self, uri):
        entity = first(self.prov_doc.get_record(_as_identifier(uri)))
        if not entity:
            _logger.warning("Entity %s not found in %s", uri, self)
            return None
        return Entity(self, entity)

    def activity(self, uri=None):
        if not uri:
            uri = self.run_id
        activity_id = _as_identifier(uri)
        activity = first(self.prov_doc.get_record(activity_id))
        if not activity:
            _logger.warning("Activity %s not found in %s", uri, self)
            return None
        return Activity(self, activity)

    def _prov_format(self, media_type):
        for prov in (self.ro.provenance(self.uri) or ()):
            if media_type == self.ro.mediatype(prov):
                return self.ro.resolve_path(prov)

    def _load_prov_document(self):
        # Preferred order
        candidates = ("xml", "json", "nt", "ttl", "rdf")
        # Note: Not all of these parse consistently with rdflib in py3
        rdf_candidates = ("ttl", "nt", "rdf", "jsonld")
        for c in candidates:
            prov = self._prov_format(MEDIA_TYPES.get(c))
            if prov:
                _logger.info("Loading %s", prov)
                if c in rdf_candidates:
                    doc = ProvDocument.deserialize(source=prov, format="rdf", rdf_format=c)
                else:
                    doc = ProvDocument.deserialize(source=prov, format=c)
                return doc.unified(), prov
        _logger.warn("No PROV compatible format found for %s", self.uri)
        return None, None

    def record_with_attr(self, prov_type, attrib_value, with_attrib=PROV_ATTR_ACTIVITY):
        for elem in self.prov_doc.get_records(prov_type):
            if (with_attrib, attrib_value) in elem.attributes:
                yield elem
    

class _Prov:
    def __init__(self, provenance, record):
        self.provenance = provenance
        self.record = record
        _logger.debug(record)

    def _records(self, ProvClass, CreateClass, attr):
        records = self.provenance.record_with_attr(ProvClass, self.id, attr)
        return (CreateClass(self.provenance, r) for r in records)

    @property
    def id(self):
        return self.record.identifier

    @property
    def label(self):
        return self._prov_attr("prov:label")

    @property
    def type(self):
        return self._prov_attr("prov:type")

    def types(self):
        return set(self._prov_attrs("prov:type"))

    @property
    def uri(self):
        i = self.id
        return i and i.uri
    
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.uri)
    
    def __str__(self):
        return self.record.get_provn()

    def _prov_attr(self, attr):
        return first(self._prov_attrs(attr))

    def _prov_attrs(self, attr):
        return self.record.get_attribute(attr)


class Activity(_Prov):

    def usage(self):
        return self._records(ProvUsage, Usage, PROV_ATTR_ACTIVITY)

    def generation(self):
        return self._records(ProvGeneration, Generation, PROV_ATTR_ACTIVITY)

    def association(self):
        return self._records(ProvAssociation, Association, PROV_ATTR_ACTIVITY)

    def plan(self):
        return first(a.plan_id for a in self.association() if a.plan_id)
    
    def steps(self):
        starts = self._records(ProvStart, Start, PROV_ATTR_STARTER)
        for s in starts:
            activity = s.activity()
            if activity:
                yield activity

    def start(self):
        return first(self._records(ProvStart, Start, PROV_ATTR_ACTIVITY))

    def end(self):
        return first(self._records(ProvEnd, End, PROV_ATTR_ACTIVITY))

    def duration(self):
        # Lots of guards in case start or end are missing
        start = self.start()
        s = start and start.time
        end = self.end()
        e = end and end.time
        return s and e and e-s

class _Time(_Prov):
    @property
    def time(self):
        return self._prov_attr(PROV_ATTR_TIME)

class _Start_or_End(_Time):
    @property
    def activity_id(self):
        return self._prov_attr(PROV_ATTR_ACTIVITY)
    def activity(self):
        a = self.activity_id
        return a and self.provenance.activity(a)

    @property
    def starter_id(self):
        return self._prov_attr(PROV_ATTR_STARTER)
    def starter_activity(self):
        a = self.starter_id
        return a and self.provenance.activity(a)
    

class Start(_Start_or_End):
    pass
class End(_Start_or_End):
    pass

class Association(_Prov):
    @property
    def agent_id(self):
        return self._prov_attr(PROV_ATTR_AGENT)

    @property
    def activity_id(self):
        return self._prov_attr(PROV_ATTR_ACTIVITY)

    def activity(self):
        a = self.activity_id
        return a and self.provenance.activity(a)

    @property
    def plan_id(self):
        return self._prov_attr(PROV_ATTR_PLAN)

class Specialization(_Prov):
    @property
    def general_entity_id(self):
        return self._prov_attr(PROV_ATTR_GENERAL_ENTITY)

    def general_entity(self):
        g = self.general_entity_id
        return g and self.provenance.entity(g)

    @property
    def specific_entity_id(self):
        return self._prov_attr(PROV_ATTR_SPECIFIC_ENTITY)

    def specific_entity(self):
        s = self.specific_entity_id
        return s and self.provenance.entity(s)

class Entity(_Prov):

    def specializationOf(self):
        specializations = self._records(ProvSpecialization, Specialization, PROV_ATTR_SPECIFIC_ENTITY)
        return (s.general_entity() for s in specializations)

    def generalizationOf(self):
        specializations = self._records(ProvSpecialization, Specialization, PROV_ATTR_GENERAL_ENTITY)
        return (s.specific_entity() for s in specializations)

    @property
    def value(self):
        return self._prov_attr(PROV_VALUE)

    @property
    def basename(self):
        return self._prov_attr(CWLPROV["basename"])
    @property
    def nameroot(self):
        return self._prov_attr(CWLPROV["nameroot"])
    @property
    def nameext(self):
        return self._prov_attr(CWLPROV["nameext"])

    def derivations(self):
        return self._records(ProvDerivation, Derivation, PROV_ATTR_USED_ENTITY)

    def secondary_files(self):
        return [d.generated_entity() for d in self.derivations() 
                if CWLPROV["SecondaryFile"] in d.types()]

class Derivation(_Prov):
    @property
    def generated_entity_id(self):
        return self._prov_attr(PROV_ATTR_GENERATED_ENTITY)

    def generated_entity(self):
        e_id = self.generated_entity_id
        return e_id and self.provenance.entity(e_id)

    @property
    def used_entity_id(self):
        return self._prov_attr(PROV_ATTR_USED_ENTITY)

    def used_entity(self):
        e_id = self.generated_entity_id
        return e_id and self.provenance.entity(e_id)

    @property
    def generation_id(self):
        return self._prov_attr(PROV_ATTR_GENERATION)
    @property
    def usage_id(self):
        return self._prov_attr(PROV_ATTR_USAGE)

class _Usage_Or_Generation(_Time):

    @property
    def entity_id(self):
        return self._prov_attr(PROV_ATTR_ENTITY)

    def entity(self):
        e_id = self.entity_id
        return e_id and self.provenance.entity(e_id)

    @property
    def role(self):
        return self._prov_attr(PROV_ROLE)
    
class Generation(_Usage_Or_Generation):
    pass

class Usage(_Usage_Or_Generation):
    pass


