#!/usr/bin/env python
  
## © 2018 Software Freedom Conservancy (SFC)
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

"""
cwlprov Provenance

"""
__author__      = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__   = "© 2018 Software Freedom Conservancy (SFC)"
__license__     = "Apache License, version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"

import logging
from prov.identifier import Identifier
from prov.model import *

from .utils import *

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
    if isinstance(uri_or_identifier, Identifier):
        return uri_or_identifier
    else:
        return Identifier(str(uri_or_identifier))

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

    def activity(self, uri=None):
        if not uri:
            uri = self.run_id
        activity_id = _as_identifier(uri)
        activity = first(self.prov_doc.get_record(activity_id))
        if not activity:
            _logger.warning("Provenance %s does not describe step %s", self, uri)
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


class Activity:
    def __init__(self, provenance, activity):
        self.provenance = provenance
        self.prov_activity = activity
    
    @property
    def id(self):
        return self.prov_activity.identifier

    @property
    def uri(self):
        return self.id.uri
