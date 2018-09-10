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
cwlprov Research Object

"""
__author__      = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__   = "© 2018 Software Freedom Conservancy (SFC)"
__license__     = "Apache License, version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"

import pkg_resources
import urllib.parse
import pathlib
import json
import arcp
from rdflib import Namespace, URIRef, Graph, Literal
from rdflib.namespace import RDF,RDFS,SKOS,DCTERMS,FOAF,XSD,DC

MANIFEST_PATH=pathlib.PurePosixPath("metadata/manifest.json")

def _resource_as_path(path):
    filename = pkg_resources.resource_filename(__package__, path)
    p = pathlib.Path(filename)
    assert p.exists
    return p




# RDF namespaces we might query for later
ORE = Namespace("http://www.openarchives.org/ore/terms/")
PROV = Namespace("http://www.w3.org/ns/prov#")
RO = Namespace("http://purl.org/wf4ever/ro#")
WFDESC = Namespace("http://purl.org/wf4ever/wfdesc#")
WFPROV = Namespace("http://purl.org/wf4ever/wfprov#")
SCHEMA = Namespace("http://schema.org/")
CWLPROV = Namespace("https://w3id.org/cwl/prov#")
OA = Namespace("http://www.w3.org/ns/oa#")

class ResearchObject:
    def __init__(self, bag):
        if not bag.normalized_filesystem_names:
            # Not populated? Validate
            bag.validate()
        self.bag = bag
        self.root_path = pathlib.Path(bag.path).absolute()        
        self.root_uri = self._find_arcp()
        self._load_manifest()
        
    def _find_arcp(self):
        ext_id = self.bag.info.get("External-Identifier")
        if ext_id and arcp.is_arcp_uri(ext_id):
            return ext_id
        else:
            return arcp.arcp_random()
    
    @property
    def id(self):
        manifest = URIRef(self.resolve_uri("metadata/manifest.json"))
        ros = set(self.manifest.subjects(ORE.isDescribedBy, manifest))
        if not ros:
            ros = set(self.manifest.subjects(ORE.aggregates))
        if not ros:
            # _:bnode owl:sameAs arcp://.../
            ros = set(self.manifest.subjects(OWL.sameAs, URIRef(self.root_uri)))
        if len(ros) == 1:
            return ros.pop()
        elif ros:
            print("Warning: More than 1 Research Object in manifest", file=sys.stderr)
            # We can't just return the first one as order is not guaranteed

        # Use arcp://.../ root as fallback
        return URIRef(self.root_uri)
    
    def resolve_uri(self, relative_uri):
        return urllib.parse.urljoin(self.root_uri, str(relative_uri))

    def resolve_path(self, uri_path):
        if arcp.is_arcp_uri(str(uri_path)):
            uri = arcp.parse_arcp(uri_path)
            # Ensure same base URI meaning this bagit
            assert urllib.parse.urljoin(uri, "/") == self.root_uri
            # Strip initial / so path is relative
            path = pathlib.PurePosixPath(uri.path[1:])
        else:            
            path = pathlib.PurePosixPath(uri_path)
        assert not path.is_absolute()

        if not str(path) in self.bag.entries:
            raise IOError("Not found in bag manifest/tagmanifest: %s" % uri_path)
        # resolve as OS-specific path
        absolute = pathlib.Path(self.root_path, path)
        # ensure it did not climb out (will throw ValueError if not)
        assert absolute.relative_to(self.root_path)
        return absolute

    def _load_manifest(self):
        manifest_file = self.resolve_path(MANIFEST_PATH)
        base_arcp = self.resolve_uri(MANIFEST_PATH)

        # Avoid resolving JSON-LD context https://w3id.org/bundle/context
        # so this test works offline
        context = _resource_as_path("context/bundle.jsonld").as_uri()
        g = Graph()
        with open(manifest_file, "r", encoding="UTF-8") as f:
            jsonld = f.read()
            # replace with file:/// URI
            jsonld = jsonld.replace("https://w3id.org/bundle/context", context)
        g.parse(data=jsonld, format="json-ld", publicID=base_arcp)
        self.manifest = g
        return g


    def _uriref(self, path=None, uri=None):
        if uri:
            return URIRef(uri)
        elif path:
            return URIRef(self.resolve_uri(path))
        else:
            return self.id

    @property
    def conformsTo(self, path=None, uri=None):
        resource = self._uriref(path=path, uri=uri)
        return set(map(str, self.manifest.objects(resource, DCTERMS.conformsTo)))

