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


"""cwlprov Research Object."""
__author__ = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__ = "© 2018 Software Freedom Conservancy (SFC)"
__license__ = (
    "Apache License, version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"
)

import atexit
import importlib.resources
import logging
import pathlib
import urllib.parse
from collections.abc import Iterable
from contextlib import ExitStack
from functools import partial
from typing import TYPE_CHECKING, Optional, Set, Union

import arcp
from bdbag.bdbagit import BDBag
from rdflib import BNode, Graph, Namespace, URIRef
from rdflib.namespace import DC, DCTERMS, FOAF, OWL
from rdflib.term import Identifier, Node

_logger = logging.getLogger(__name__)

MANIFEST_PATH = pathlib.PurePosixPath("metadata/manifest.json")


def _resource_as_path(path: str) -> pathlib.Path:
    file_manager = ExitStack()
    atexit.register(file_manager.close)
    ref = importlib.resources.files(__package__) / path
    p = file_manager.enter_context(importlib.resources.as_file(ref))
    if not p.exists():
        raise OSError(f"{p} is missing.")
    return p


# RDF namespaces we might query for later
ORE = Namespace("http://www.openarchives.org/ore/terms/")
BUNDLE = Namespace("http://purl.org/wf4ever/bundle#")
PROV = Namespace("http://www.w3.org/ns/prov#")
RO = Namespace("http://purl.org/wf4ever/ro#")
ROTERMS = Namespace("http://purl.org/wf4ever/roterms#")
PAV = Namespace("http://purl.org/pav/")
WFDESC = Namespace("http://purl.org/wf4ever/wfdesc#")
WFPROV = Namespace("http://purl.org/wf4ever/wfprov#")
SCHEMA = Namespace("http://schema.org/")
CWLPROV = Namespace("https://w3id.org/cwl/prov#")
OA = Namespace("http://www.w3.org/ns/oa#")


class ResearchObject:
    manifest: Graph

    def __init__(self, bag: "BDBag") -> None:
        """Create a ResearchObject from a BDBag."""
        if not bag.normalized_filesystem_names:
            # Not populated? Validate
            bag.validate()
        self.bag = bag
        self.root_path = pathlib.Path(bag.path).absolute()
        self.root_uri = self._find_arcp()
        self._load_manifest()

    def _find_arcp(self) -> str:
        ext_id = self.bag.info.get("External-Identifier")
        if ext_id and arcp.is_arcp_uri(ext_id):
            _logger.debug("External-Identifier defines bagit root: %s", ext_id)
            return ext_id
        else:
            u = arcp.arcp_random()
            if ext_id:
                _logger.warning("External-Identifier not an arcp URI", ext_id)
            else:
                _logger.warning("External-Identifier not found in bag-info.txt")

            _logger.info("Temporary bagit root: %s", u)
            return u

    @property
    def id(self) -> Optional["Identifier"]:
        """Determine the Identifier for this RO."""
        i = self.id_uriref
        if isinstance(i, BNode):
            return next(self.manifest.objects(i, OWL.sameAs))
        return None

    @property
    def id_uriref(self) -> Node:
        """Find the URI reference for this RO."""
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
            _logger.error("Warning: More than 1 Research Object in manifest")
            # We can't just return the first one as order is not guaranteed

        _logger.info("Using root as fallback RO identifier: %s", self.root_uri)
        return URIRef(self.root_uri)

    def resolve_uri(self, relative_uri: Union[str, pathlib.PurePosixPath]) -> str:
        return urllib.parse.urljoin(self.root_uri, str(relative_uri))

    def resolve_path(self, uri_path: Union[str, pathlib.PurePosixPath]) -> pathlib.Path:
        if arcp.is_arcp_uri(str(uri_path)):
            uri = arcp.parse_arcp(uri_path)
            # Ensure same base URI meaning this bagit
            if urllib.parse.urljoin(str(uri_path), "/") != self.root_uri:
                raise Exception(
                    f"{uri_path} does not have the expected base URI: {self.root_uri}."
                )
            # Strip initial / so path is relative
            path = pathlib.PurePosixPath(uri.path[1:])
        else:
            path = pathlib.PurePosixPath(uri_path)
        if path.is_absolute():
            raise Exception(f"The resolved {path} from {uri_path} is absolute.")

        if not str(path) in self.bag.entries:
            raise OSError("Not found in bag manifest/tagmanifest: %s", uri_path)
        # resolve as OS-specific path
        absolute = pathlib.Path(self.root_path, path)
        # ensure it did not climb out (will throw ValueError if not)
        if not absolute.relative_to(self.root_path):
            raise Exception(
                f"Resolved, absolute path {absolute} is outside the "
                f"acceptable root: {self.root_path}."
            )
        return absolute

    def _load_manifest(self) -> Graph:
        manifest_file = self.resolve_path(MANIFEST_PATH)
        base_arcp = self.resolve_uri(MANIFEST_PATH)

        # Avoid resolving JSON-LD context https://w3id.org/bundle/context
        # so this test works offline
        context = _resource_as_path("context/bundle.jsonld").as_uri()
        g = Graph()
        with open(manifest_file, encoding="UTF-8") as f:
            jsonld = f.read()
            # replace with file:/// URI
            jsonld = jsonld.replace("https://w3id.org/bundle/context", context)
        _logger.info("Parsing RO manifest %s", manifest_file)
        g.parse(data=jsonld, format="json-ld", publicID=base_arcp)
        self.manifest = g
        return g

    def _uriref(
        self,
        path: Optional[Union[str, pathlib.PurePosixPath]] = None,
        uri: Optional[Union[str, Node]] = None,
    ) -> Node:
        if uri:
            return URIRef(str(uri))
        elif path:
            return URIRef(self.resolve_uri(path))
        else:
            return self.id_uriref

    @property
    def conformsTo(self) -> set[str]:
        """Find which things this RO conforms to."""
        resource = self._uriref()
        return set(map(str, self.manifest.objects(resource, DCTERMS.conformsTo)))

    @property
    def createdBy(self) -> set["Agent"]:
        """Find the set of Agents who created this RO."""
        resource = self._uriref()
        new_agent = partial(Agent, self.manifest)
        return set(map(new_agent, self.manifest.objects(resource, PAV.createdBy)))

    @property
    def authoredBy(self) -> set["Agent"]:
        """Find the set of Agents who authored this RO."""
        resource = self._uriref()
        new_agent = partial(Agent, self.manifest)
        return set(map(new_agent, self.manifest.objects(resource, PAV.authoredBy)))

    def annotations_about(
        self,
        path: Optional[Union[str, pathlib.PurePosixPath]] = None,
        uri: Optional[str] = None,
    ) -> set["Annotation"]:
        resource = self._uriref(path=path, uri=uri)
        new_annotation = partial(Annotation, self.manifest)
        return set(map(new_annotation, self.manifest.subjects(OA.hasTarget, resource)))

    def annotations_with_content(
        self,
        path: Optional[Union[str, pathlib.PurePosixPath]] = None,
        uri: Optional[Union[str, Identifier]] = None,
    ) -> set["Annotation"]:
        resource = self._uriref(path=path, uri=uri)
        new_annotation = partial(Annotation, self.manifest)
        return set(map(new_annotation, self.manifest.subjects(OA.hasBody, resource)))

    def describes(
        self,
        path: Optional[Union[str, pathlib.PurePosixPath]] = None,
        uri: Optional[Union[str, Identifier]] = None,
    ) -> Optional[Identifier]:
        return next(
            (
                a.hasTarget
                for a in self.annotations_with_content(path, uri)
                if a.motivatedBy == OA.describing
            ),
            None,
        )

    def provenance(
        self,
        path: Optional[Union[str, pathlib.PurePosixPath]] = None,
        uri: Optional[str] = None,
    ) -> Optional[set[Node]]:
        for a in self.annotations_about(path, uri):
            if a.motivatedBy == PROV.has_provenance:
                return a.hasBodies
        return None

    def resources_with_provenance(self) -> Iterable[Node]:
        """Find the resources of this Workflow that have provenance."""
        new_annotation = partial(Annotation, self.manifest)
        anns = map(
            new_annotation, self.manifest.subjects(OA.motivatedBy, PROV.has_provenance)
        )
        for a in anns:
            yield from a.hasTargets

    def mediatype(
        self,
        path: Optional[Union[str, pathlib.PurePosixPath]] = None,
        uri: Optional[str] = None,
    ) -> Optional[str]:
        resource = self._uriref(path=path, uri=uri)
        return next(map(str, self.manifest.objects(resource, DC["format"])), None)

    def bundledAs(
        self,
        path: Optional[Union[str, pathlib.PurePosixPath]] = None,
        uri: Optional[str] = None,
    ) -> Optional[str]:
        resource = self._uriref(path=path, uri=uri)
        return next(
            map(str, self.manifest.objects(resource, BUNDLE["bundledAs"])), None
        )

    @property
    def workflow_id(self) -> Optional[Identifier]:
        """The identifier of the primary Workflow Run."""
        wf_id = self.describes(uri=self.id)
        _logger.debug("Primary Workflow run: %s", wf_id)
        return wf_id


class Annotation:
    """Annotation."""

    def __init__(self, graph: Graph, uri: str) -> None:
        """Create an Annotation."""
        self._graph = graph
        self._id = uri

    @property
    def hasBody(self) -> Optional[Node]:
        """Find the first body Node of this Annotation, if any."""
        return next(self._graph.objects(self._id, OA.hasBody), None)

    @property
    def hasBodies(self) -> set[Node]:
        """Find the set of body Nodes of this Annotation."""
        return set(self._graph.objects(self._id, OA.hasBody))

    @property
    def hasTarget(self) -> Optional[Identifier]:
        """Find the first target of this Annotation, if any."""
        return next(self._graph.objects(self._id, OA.hasTarget), None)

    @property
    def hasTargets(self) -> set[Node]:
        """Find which Noes this Annotation targets."""
        return set(self._graph.objects(self._id, OA.hasTarget))

    @property
    def motivatedBy(self) -> Optional[Node]:
        """Find the Node that motivated this Annotation."""
        return next(self._graph.objects(self._id, OA.motivatedBy), None)

    def __repr__(self) -> str:
        """Identifiy this Annotation."""
        return "<Annotation %s>" % self._id


class Agent:
    """Agent."""

    def __init__(self, graph: Graph, uri: str) -> None:
        """Create an Agent."""
        self._graph = graph
        self._id = uri

    @property
    def uri(self) -> Optional[str]:
        if isinstance(self._id, URIRef):
            return self._id
        return None

    @property
    def name(self) -> Optional[Node]:
        """Find the next node in the graph, if any."""
        return next(self._graph.objects(self._id, FOAF.name), None)

    @property
    def orcid(self) -> Optional[Node]:
        """Find the ORCID associated with this Agent, if any."""
        return next(self._graph.objects(self._id, ROTERMS.orcid), None)

    def __repr__(self) -> str:
        """Identify this Agent."""
        return "<Agent %s>" % self._id

    def __str__(self) -> str:
        """Print the name, identifier, and uri of this Agent."""
        s = str(self.name) or "(unknown)"
        if o := self.orcid:
            s += " <%s>" % o
        if u := self.uri:
            s += " <%s>" % u
        return s
