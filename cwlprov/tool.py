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
cwlprov Command Line Tool
"""
__author__      = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__   = "© 2018 Software Freedom Conservancy (SFC)"
__license__     = "Apache License, version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"

import arcp
import argparse
import bagit
import bdbag
import dateutil.parser
import errno
import json
import logging
import os.path
import pathlib
import posixpath
import shutil
import sys
import urllib.parse

from bdbag.bdbagit import BDBag, BagError
from enum import IntEnum
from functools import partial
from pathlib import Path
from prov.identifier import Identifier
from prov.model import *
from uuid import UUID

from .ro import ResearchObject
from .prov import Provenance
from .utils import *

_logger = logging.getLogger(__name__)


BAGIT_RO_PROFILES = (
    "https://w3id.org/ro/bagit/profile", 
    "http://raw.githubusercontent.com/fair-research/bdbag/master/profiles/bdbag-ro-profile.json"
)
CWLPROV_SUPPORTED = (
    # Decreasing order as first item is output as example
    "https://w3id.org/cwl/prov/0.5.0",
    "https://w3id.org/cwl/prov/0.4.0",
    "https://w3id.org/cwl/prov/0.3.0",
)

MANIFEST_JSON = posixpath.join("metadata", "manifest.json")

TIME_PADDING = " " * 26  # len("2018-08-08 22:44:06.573330")

# PROV namespaces
CWLPROV = Namespace("cwlprov", "https://w3id.org/cwl/prov#")

class Status(IntEnum):
    """Exit codes from main()"""
    OK = 0
    UNHANDLED_ERROR = errno.EPERM
    UNKNOWN_COMMAND = errno.EINVAL
    UNKNOWN_FORMAT = errno.EINVAL
    IO_ERROR = errno.EIO
    BAG_NOT_FOUND = errno.ENOENT
    NOT_A_DIRECTORY = errno.ENOTDIR
    UNKNOWN_RUN = errno.ENODATA
    PERMISSION_ERROR = errno.EACCES
    # User-specified exit codes
    # http://www.tldp.org/LDP/abs/html/exitcodes.html
    MISSING_PROFILE = 166
    INVALID_BAG = 167
    UNSUPPORTED_CWLPROV_VERSION = 168



def parse_args(args=None):
    parser = argparse.ArgumentParser(description='cwlprov explores Research Objects containing provenance of Common Workflow Language executions. <https://w3id.org/cwl/prov/>')
    parser.add_argument("--directory", "-d", 
        help="Path to CWLProv Research Object (default: .)",
        default=None
        )

    parser.add_argument("--relative", default=None, action='store_true',
        help="Output paths relative to current directory (default if -d is missing or relative)")
    parser.add_argument("--absolute", default=None, action='store_false',
        dest="relative", help="Output absolute paths (default if -d is absolute)")

    parser.add_argument("--verbose", "-v", default=0, action='count',
        help="Verbose logging (repeat for more verbose)")
    parser.add_argument("--quiet", "-q", default=False, action='store_true',
        help="No logging or hints")

    parser.add_argument("--hints", default=True, action='store_true',
        help="Show hints on cwlprov usage")
    parser.add_argument("--no-hints", default=True, action='store_false',
        dest="hints", help="Do not show hints")
    subparsers = parser.add_subparsers(title='commands', dest="cmd")

    parser_validate = subparsers.add_parser('validate', help='validate the CWLProv Research Object')
    parser_info = subparsers.add_parser('info', help='show research object metadata')
    parser_who = subparsers.add_parser('who', help='show who ran the workflow')    
    parser_prov = subparsers.add_parser('prov', help='export workflow execution provenance in PROV format')
    parser_prov.add_argument("id", default=None, nargs="?", help="workflow run UUID")
    parser_prov.add_argument("--format", "-f", default="files", 
        choices=["files"] + list(MEDIA_TYPES.keys()),
        help="Output in PROV format (default: files)")
    parser_prov.add_argument("--formats", "-F", default=False, 
        action='store_true', help="List available PROV formats")

    parser_input = subparsers.add_parser('inputs', help='list workflow/step input files/values')
    parser_input.add_argument("--run", default=None, help="workflow run UUID")
    parser_input.add_argument("id", default=None, nargs="?", help="step/workflow run UUID to show")
    parser_input.add_argument("--parameters",  default=True, action='store_true',
        help="Show parameter names")
    parser_input.add_argument("--no-parameters", default=True, action='store_false',
        dest="parameters", help="Do not show parameter names")
    parser_input.add_argument("--format", default="files", 
        choices=["files", "json", "values"],
        help="Output format, (default: files)")

    parser_output = subparsers.add_parser('outputs', help='list workflow/step output files/values')
    parser_output.add_argument("--run", default=None, help="workflow run UUID")
    parser_output.add_argument("id", default=None, nargs="?", help="step/workflow run UUID to show")
    parser_output.add_argument("--parameters",  default=True, action='store_true',
        help="Show parameter names")
    parser_output.add_argument("--no-parameters", default=True, action='store_false',
        dest="parameters", help="Do not show parameter names")


    parser_run = subparsers.add_parser('run', help='show workflow execution log')
    parser_run.add_argument("id", default=None, nargs="?", help="workflow run UUID")
    parser_run.add_argument("--step", "-s", default=None, 
        help="Show only step with given UUID")
    parser_run.add_argument("--steps",  default=True, action='store_true',
        help="List steps of workflow")
    parser_run.add_argument("--no-steps", default=True, action='store_false',
        dest="steps", help="Do not list steps")

    parser_run.add_argument("--start",  default=True, action='store_true',
        help="Show start timestamps (default)")
    parser_run.add_argument("--no-start", "-S", default=True, action='store_false',
        dest="start", help="Do not show start timestamps")

    parser_run.add_argument("--end", "-e", default=False, action='store_true',
        help="Show end timestamps")
    parser_run.add_argument("--no-end", default=False, action='store_false',
        dest="end", help="Do not show end timestamps")


    parser_run.add_argument("--duration",  default=True, action='store_true',
        help="Show step duration (default)")
    parser_run.add_argument("--no-duration", "-D", default=True, action='store_false',
        dest="duration", help="Do not show step duration")

    parser_run.add_argument("--labels",  default=True, action='store_true',
        help="Show activity labels")
    parser_run.add_argument("--no-labels", "-L", default=True, action='store_false',
        dest="labels", help="Do not show activity labels")


    parser_run.add_argument("--inputs", "-i", default=False, 
        action='store_true', help="Show inputs")
    parser_run.add_argument("--outputs", "-o", default=False, 
        action='store_true', help="Show outputs")

    parser_runs = subparsers.add_parser('runs', help='list all workflow executions in RO')

    return parser.parse_args(args)

def _determine_bagit_folder(folder=None):
    # Absolute so we won't climb to ../../../../../ forever
    # and have resolved any symlinks
    folder = pathlib.Path(folder or "").absolute()
    while True:
        _logger.debug("Determining bagit folder: %s", folder)
        bagit_file = folder / "bagit.txt"
        if bagit_file.is_file():
            _logger.info("Detected %s", bagit_file)
            return folder
        _logger.debug("%s not found", bagit_file)
        if folder == folder.parent:
            _logger.info("No bagit.txt detected")
            return None
        folder = folder.parent

def _info_set(bag, key):
    v = bag.info.get(key, [])
    if isinstance(v, list):
        return set(v)
    else:
        return set([v])

def validate_bag(bag, full_validation=False):
    valid_bag = bag.validate(fast=not full_validation)
    if not valid_bag:
        _logger.error("Invalid BagIt folder: %s", bag.path)
        # Specific errors already output from bagit library
        return Status.INVALID_BAG
    # Check we follow right profile
    profiles = _info_set(bag, "BagIt-Profile-Identifier")
    supported_ro = set(BAGIT_RO_PROFILES).intersection(profiles)
    if not supported_ro:
        _logger.warning("Missing BdBag profile: %s", bag.path)
        if args.hints and not args.quiet:
            print("Try adding to %s/bag-info.txt:" % bag.path)
            print("BagIt-Profile-Identifier: %s" % BAGIT_RO_PROFILES[0])
        if full_validation:
            return Status.MISSING_PROFILE
    # Check we have a manifest
    has_manifest = MANIFEST_JSON in bag.tagfile_entries()
    if not has_manifest:
        _logger.warning("Missing from tagmanifest: %s", MANIFEST_JSON)
        return Status.MISSING_MANIFEST
    return Status.OK

def validate_ro(ro, full_validation=False, args=None):
    # If it has this prefix, it's probably OK
    cwlprov = set(p for p in ro.conformsTo if p.startswith("https://w3id.org/cwl/prov/"))
    if not cwlprov:
        if full_validation or not args.quiet: 
            _logger.warning("Missing CWLProv profile: %s", ro.bag.path)
        if full_validation and args.hints and not args.quiet:
            print("Try adding to %s/metadata/manifest.json:" % ro.bag.path)
            print('{\n  "id": "/",\n  "conformsTo", "%s",\n  ...\n}' %
                CWLPROV_SUPPORTED[0])
            return Status.MISSING_PROFILE
    supported_cwlprov = set(CWLPROV_SUPPORTED).intersection(cwlprov)
    if cwlprov and not supported_cwlprov:
        # Probably a newer one this code don't support yet; it will 
        # probably be fine
        _logger.warning("Unsupported CWLProv version: %s", cwlprov)
        if args.hints:
            print("Supported profiles:\n %s" %
                    "\n ".join(CWLPROV_SUPPORTED)
                 )
        if full_validation:
            return Status.UNSUPPORTED_CWLPROV_VERSION
    return Status.OK


def _as_uuid(w, args):
    try:
        uuid = UUID(w.replace("urn:uuid:", ""))
        return (uuid.urn, uuid, str(uuid))
    except ValueError:
        if not args.quiet:
            logger.warn("Invalid UUID %s", w)
        # return -as-is
        return w, None, str(w)

def _wf_id(ro, args, run=None):
    w = run or args.id or ro.workflow_id
    # ensure consistent UUID URIs
    return _as_uuid(w, args)

def _prov_with_attr(prov_doc, prov_type, attrib_value, with_attrib=PROV_ATTR_ACTIVITY):
    for elem in prov_doc.get_records(prov_type):
        if (with_attrib, attrib_value) in elem.attributes:
            yield elem

def _prov_attr(attr, elem):
    return first(elem.get_attribute(attr))

def _usage(activity_id, prov_doc, args):
    if not args.inputs:
        return
    usage = _prov_with_attr(prov_doc, ProvUsage, activity_id, PROV_ATTR_ACTIVITY)
    for u in usage:
        entity = _prov_attr(PROV_ATTR_ENTITY, u)
        entity_id = entity and entity.uri.replace("urn:uuid:", "").replace("urn:hash::sha1:", "")
        role = _prov_attr(PROV_ROLE, u)
        time = _prov_attr(PROV_ATTR_TIME, u)
        if args.start and args.end:
            # 2 col timestamps
            time_part = "%s %s " % (time or "(unknown usage time)     ", TIME_PADDING)
        elif args.start or args.end:
            # 1 col timestamp
            time_part = "%s " % (time or "(unknown usage time)     ")
        else:
            time_part = ""        
        print("%sIn   %s < %s" % (time_part, entity_id, role or ""))

def _generation(activity_id, prov_doc, args):
    if not args.outputs:
        return
    gen = _prov_with_attr(prov_doc, ProvGeneration, activity_id, PROV_ATTR_ACTIVITY)
    for g in gen:
        entity = _prov_attr(PROV_ATTR_ENTITY, g)
        entity_id = entity.uri.replace("urn:uuid:", "").replace("urn:hash::sha1:", "")
        role = _prov_attr(PROV_ROLE, g)
        time = _prov_attr(PROV_ATTR_TIME, g)
        if args.start and args.end:
            # 2 col timestamps
            time_part = "%s %s " % (TIME_PADDING, time or "(unknown generation time)")
        elif args.start or args.end:
            # 1 col timestamp
            time_part = "%s " % (time or "(unknown generation time)")
        else:
            time_part = ""        
        print("%sOut  %s > %s" % (time_part, entity_id, role or ""))



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

def _prov_format(ro, uri, media_type):
    for prov in (ro.provenance(uri) or ()):
        if media_type == ro.mediatype(prov):
            return ro.resolve_path(prov)

def _prov_document(ro, uri, args):
    # Preferred order
    candidates = ("xml", "json", "nt", "ttl", "rdf")
    # Note: Not all of these parse consistently with rdflib in py3
    rdf_candidates = ("ttl", "nt", "rdf", "jsonld")
    for c in candidates:
        prov = _prov_format(ro, uri, MEDIA_TYPES.get(c))
        if prov:
            _logger.info("Loading %s", prov)
            if c in rdf_candidates:
                doc = ProvDocument.deserialize(source=prov, format="rdf", rdf_format=c)
            else:
                doc = ProvDocument.deserialize(source=prov, format=c)
            return doc.unified()
    _logger.warning("No PROV compatible format found for %s", uri)
    return None



def _set_log_level(quiet=None, verbose=0):
    if quiet: # -q
        log_level = logging.ERROR
    if not verbose: # default
        log_level = logging.WARNING
    elif verbose == 1: # -v
        log_level = logging.INFO
    else: # -v -v
        log_level = logging.DEBUG            
    logging.basicConfig(level=log_level)

class Tool:
    def __init__(self, args=None):
        self.args = parse_args(args)

    def main(self):
        # type: (...) -> None
        """cwlprov command line tool"""
        args = self.args
                
        if args.relative is not None:
            self.relative_paths = args.relative
        else:
            if args.directory and Path(args.directory).is_absolute():
                # absolute if -d is absolute
                self.relative_paths = False
            else:
                # default: relative if -d is relative
                self.relative_paths = True
                # FIXME: What if -d ../../ ? 
        
        if args.quiet and args.verbose:
            _logger.error("Incompatible parameters: --quiet --verbose")
            return Status.UNKNOWN_COMMAND
        _set_log_level(args.quiet, args.verbose)

        folder = args.directory or _determine_bagit_folder()
        if not folder:        
            _logger.error("Could not find bagit.txt, try cwlprov -d mybag/")
            return Status.BAG_NOT_FOUND
        folder = pathlib.Path(folder)
        if not folder.exists():
            _logger.error("No such file or directory: %s",  folder)
            return Status.BAG_NOT_FOUND
        if not folder.is_dir():
            _logger.error("Not a directory: %s", folder)
            return Status.NOT_A_DIRECTORY
        bagit_file = folder / "bagit.txt"
        if not bagit_file.is_file():
            _logger.error("File not found: %s", bagit_file)
            return Status.BAG_NOT_FOUND


        full_validation = args.cmd == "validate"
        _logger.info("Opening BagIt %s", folder)
        ## BagIt check
        try:
            bag = BDBag(str(folder))
        except BagError as e:
            _logger.fatal(e)
            return Status.INVALID_BAG
        except PermissionError as e:
            _logger.fatal(e)
            return Status.PERMISSION_ERROR
        except OSError as e:
            _logger.fatal(e)
            return Status.IO_ERROR
        # Unhandled errors will show Python stacktrace

        invalid = validate_bag(bag, full_validation)
        if invalid:
            return invalid
        
        self.ro = ResearchObject(bag)
        invalid = validate_ro(self.ro, full_validation, args)
        if invalid:
            return invalid

        if full_validation:
            if not args.quiet:
                print("Valid CWLProv RO: %s" % folder)
            return Status.OK

        # Else, find the other commands
        COMMANDS = {
            "info": self.info,
            "who": self.who,
            "prov": self.prov,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "run": self.run,
            "runs": self.runs,
        }
        
        cmd = COMMANDS.get(args.cmd)
        if not cmd:
            # Light-weight validation
            if not args.quiet:
                print("Detected CWLProv research Object: %s" % folder)
            return Status.OK
        
        return cmd()

    def _path(self, path):
        p = self.ro.resolve_path(str(path))
        if self.relative_paths:
            return os.path.relpath(Path(p), Path())        
        else:
            return Path(p).absolute()        

    def info(self):
        ro = self.ro
        args = self.args

        # About RO?
        if not args.quiet:
            print(ro.bag.info.get("External-Description", "Research Object"))
        print("ID: %s" % ro.id)
        cwlprov = set(p for p in ro.conformsTo if p.startswith("https://w3id.org/cwl/prov/"))
        if cwlprov:
            print("Profile: %s" % many(cwlprov))
        w = ro.workflow_id
        if w:
            print("Workflow ID: %s" % w)
        when = ro.bag.info.get("Bagging-Date")
        if when:
            print("Packaged: %s" % when)
        return Status.OK

    def who(self): 
        ro = self.ro
        args = self.args

        # about RO?
        createdBy = many(ro.createdBy)
        authoredBy = many(ro.authoredBy)
        if createdBy or not args.quiet:
            print("Packaged By: %s" % createdBy or "(unknown)")
        if authoredBy or not args.quiet:
            print("Executed By: %s" % authoredBy or "(unknown)")
        return Status.OK

    def prov(self):
        ro = self.ro
        args = self.args

        uri,uuid,name = _wf_id(ro, args)

        if args.format == "files":
            for prov in ro.provenance(uri) or ():
                if args.formats:
                    format = ro.mediatype(prov) or ""
                    format = EXTENSIONS.get(format, format)
                    print("%s %s" % (format, (self._path(prov))))
                else:
                    print("%s" % self._path(prov))
        else:
            media_type = MEDIA_TYPES.get(args.format, args.format)
            prov = _prov_format(ro, uri, media_type)
            if not prov:
                _logger.error("Unrecognized format: %s", args.format)
                return Status.UNKNOWN_FORMAT
            with prov.open(encoding="UTF-8") as f:
                shutil.copyfileobj(f, sys.stdout)
                print() # workaround for missing trailing newline
        return Status.OK

    def inputs(self):
        ro = self.ro
        args = self.args
        wf_uri,wf_uuid,wf_name = _wf_id(ro, args, args.run)
        a_uri,a_uuid,a_name = _wf_id(ro, args)
        if not ro.provenance(wf_uri):
            _logger.error("No provenance found for: %s", wf_name)
            if args.run:
                # We'll need to give up
                return Status.UNKNOWN_RUN
            else:
                _logger.info("Assuming primary provenance --run %s", ro.workflow_id)
                wf_uri,wf_uuid,wf_name = _as_uuid(ro.workflow_id, args)
                if not ro.provenance(wf_uri):
                    _logger.error("No provenance found for: %s", wf_name)
                    return Status.UNKNOWN_RUN

        try:
            provenance = Provenance(ro, wf_uri)
        except OSError:
            # assume Error already printed by _prov_document
            return Status.UNKNOWN_RUN
        
        activity = provenance.activity(a_uri)
        if not activity:
            _logger.error("Provenance does not describe step %s: %s", wf_name, a_uri)
            if not args.run and args.hints:
                print("If the step is in nested provenance, try '--run UUID' as found in 'cwlprov run'")
            return Status.UNKNOWN_RUN
        activity_id = activity.id

        if wf_uri != a_uri:
            _logger.info("Inputs for step %s in workflow %s", a_name, wf_name)
        else:
            _logger.info("Inputs for workflow %s", wf_name)

        job = {}
        
        usage = activity.usage()
        for u in usage:

            entity_id = u.entity_id
            role = u.role

            # Naively assume CWL identifier structure of URI
            if not role:
                _logger.warning("Unknown role for usage %s, skipping input", u)
                role_name = None
                continue
            
            # poor mans CWL parameter URI deconstruction
            role_name = str(role)
            role_name = role_name.split("/")[-1]
            role_name = urllib.parse.unquote(role_name)
            
            if args.parameters and not args.quiet:            
                print("Input %s:" % role_name) 
            time = u.time
            entity = u.entity()
            if not entity:
                _logger.warning("No provenance for used entity %s", entity_id)
                continue

            if args.verbose:
                print(entity)
            file_candidates = [entity]
            file_candidates.extend(entity.specializationOf())
            
            for file_candidate in file_candidates:
                bundled = ro.bundledAs(uri=file_candidate.uri)
                if not bundled:
                    continue
                if args.verbose:
                    print(bundled)
                bundled_path = self._path(bundled)
                job[role_name] = {}
                job[role_name]["class"] = "File"
                job[role_name]["path"] = str(bundled_path)
                print(bundled_path)
                break

            # Perhaps it has prov:value ? 
            value = entity.value
            if value is not None: # but might be False
                job[role_name] = value
                print(value)
        print(json.dumps(job))

    def outputs(self):
        ro = self.ro
        args = self.args
        wf_uri,wf_uuid,wf_name = _wf_id(ro, args, args.run)
        a_uri,a_uuid,a_name = _wf_id(ro, args)
        if not ro.provenance(wf_uri):
            if args.run:
                _logger.error("No provenance found for: %s in", wf_name)
                # We'll need to give up
                return Status.UNKNOWN_RUN
            else:
                _logger.debug("No provenance found for: %s in", wf_name)
                _logger.info("Assuming primary run --run %s", ro.workflow_id)
                wf_uri,wf_uuid,wf_name = _as_uuid(ro.workflow_id, args)
                if not ro.provenance(wf_uri):
                    _logger.error("No provenance found for: %s", wf_name)
                    return Status.UNKNOWN_RUN

        prov_doc = _prov_document(ro, wf_uri, args)
        if not prov_doc:
            # Error already printed by _prov_document
            return Status.UNKNOWN_RUN

        activity_id = Identifier(a_uri)
        activity = first(prov_doc.get_record(activity_id))
        if not activity:
            _logger.error("Provenance %s does not describe step %s", wf_name, a_uri)
            if not args.run and args.hints:
                print("If the step is in nested provenance, try '--run UUID' as found in 'cwlprov run'")
            return Status.UNKNOWN_RUN
        if args.verbose:
            if wf_uri != a_uri:
                _logger.info("Outputs for step %s in workflow %s", (a_name, wf_name))
            else:
                _logger.info("Outputs for workflow %s", (wf_name))

        gen = _prov_with_attr(prov_doc, ProvGeneration, activity_id, PROV_ATTR_ACTIVITY)
        for g in gen:
            if args.verbose:
                print(g)
            entity_id = _prov_attr(PROV_ATTR_ENTITY, g)
            role = _prov_attr(PROV_ROLE, g)
            if args.parameters and not args.quiet:
                if isinstance(role, QualifiedName):
                    role_name = role.localpart
                else:
                    role_name = str(role)
                print("Output %s:" % role_name) 
            time = _prov_attr(PROV_ATTR_TIME, g)
            entity = first(prov_doc.get_record(entity_id))
            if not entity:
                _logger.warning("No provenance for generated entity %s", entity_id)
                continue

            file_candidates = [entity]
            general_id = None
            specializations = set(_prov_with_attr(prov_doc, ProvSpecialization, entity_id, PROV_ATTR_SPECIFIC_ENTITY))
            if specializations:
                specialization = first(specializations)
                if args.verbose:
                    print(specialization)
                general_id = _prov_attr(PROV_ATTR_GENERAL_ENTITY, specialization)
                generalEntity = general_id and first(prov_doc.get_record(general_id))
                if args.verbose and generalEntity:
                    print(generalEntity)
                file_candidates.append(generalEntity)
            
            for file_candidate in file_candidates:
                bundled = ro.bundledAs(uri=file_candidate.identifier.uri)
                if not bundled:
                    continue
                if args.verbose:
                    print(bundled)
                bundled_path = self._path(bundled)
                print(bundled_path)
                break

            # Perhaps it has prov:value ? 
            value = _prov_attr(PROV_VALUE, entity)
            if not value is None: # might be False
                print(value)        

    def runs(self):
        ro = self.ro
        args = self.args        
        for run in ro.resources_with_provenance():
            name = run.replace("urn:uuid:", "")
            
            if args.verbose or not args.quiet:
                # Also load up the provenance to find its name
                prov_doc = _prov_document(ro, run, args)
                if not prov_doc:
                    print(name)
                    _logger.warning("No provenance found for: %s", name)
                    continue
                
                activity_id = Identifier(run)
                activity = first(prov_doc.get_record(activity_id))
                if not activity:
                    _logger.error("Provenance does not describe activity %s", run)
                    return Status.UNKNOWN_RUN
                label = first(activity.get_attribute("prov:label")) or ""
                is_master = run == ro.workflow_id
                print("%s %s %s" % (name, is_master and "*" or " ", label))
            else:
                print(name)
        if args.hints and not args.quiet:
            print("Legend:")
            print(" * master workflow")


    def run(self):
        ro = self.ro
        args = self.args
        uri,uuid,name = _wf_id(ro, args)
        if not ro.provenance(uri):
            _logger.error("No provenance found for: %s", name)
            #if args.hints:
            #    print("Try --search to examine all provenance files")
            return Status.UNKNOWN_RUN

        prov_doc = _prov_document(ro, uri, args)
        if not prov_doc:
            # Error already printed by _prov_document
            return Status.UNKNOWN_RUN

        if args.verbose:
            print("Workflow run:",  name)
        activity_id = Identifier(uri)
        activity = first(prov_doc.get_record(activity_id))
        if not activity:
            _logger.error("Provenance does not describe activity %s", uri)
            return Status.UNKNOWN_RUN
        if args.verbose:
            print(activity)
        label = ""
        if args.labels:
            label = " %s " % (first(activity.get_attribute("prov:label")) or "")
        
        start = first(_prov_with_attr(prov_doc, ProvStart, activity_id))
        start_time = start and _prov_attr(PROV_ATTR_TIME, start)
        end = first(_prov_with_attr(prov_doc, ProvEnd, activity_id))
        end_time = end and _prov_attr(PROV_ATTR_TIME, end)
        
        

        if args.verbose and start:
            print(start)
        padded_start_time = ""
        if args.end and args.start:
            # 2 columns
            padded_start_time = "%s %s " % (start_time, TIME_PADDING)        
        elif args.end or args.start:
            # 1 column, we don't care which
            padded_start_time = "%s " % (start_time)
        print("%sFlow %s [%s" % (padded_start_time, name, label))

        # inputs
        _usage(activity_id, prov_doc, args)
            
        # steps
        have_nested = False
        if args.steps:
            started = _prov_with_attr(prov_doc, ProvStart, activity_id, PROV_ATTR_STARTER)
            steps = map(partial(_prov_attr, PROV_ATTR_ACTIVITY), started)
            for child in steps:
                c_activity = first(prov_doc.get_record(child))
                if args.verbose:
                    print(c_activity)

                c_label = ""
                if args.labels:
                    c_label = " %s " % (first(c_activity.get_attribute("prov:label")) or "")
                c_start = first(_prov_with_attr(prov_doc, ProvStart, child))
                c_start_time = c_start and _prov_attr(PROV_ATTR_TIME, c_start)
                c_end = first(_prov_with_attr(prov_doc, ProvEnd, child))
                c_end_time = c_end and _prov_attr(PROV_ATTR_TIME, c_end)

                c_duration = ""
                if args.duration:
                    if c_start_time and c_end_time:
                        c_duration = " (%s)" % (c_end_time - c_start_time)
                    else:
                        c_duration = " (unknown duration)"

                c_provenance = ro.provenance(child.uri)
                have_nested = have_nested or c_provenance
                c_id = str(child.uri).replace("urn:uuid:", "")
                c_start_time = args.start and ("%s " % c_start_time or "(unknown start time)     ")
                c_end_time = args.end and "%s " % (c_end_time or TIME_PADDING)
                print("%s%sStep %s %s%s%s" % (c_start_time or "", c_end_time or "", c_id, c_provenance and "*" or " ", c_label, c_duration))
                _usage(child, prov_doc, args)
                _generation(child, prov_doc, args)



        # generated
        _generation(activity_id, prov_doc, args)

        if args.verbose and end:
            print(end)

        # end
        padded_end_time = ""
        if args.end and args.start:
            padded_end_time = "%s %s " % (TIME_PADDING, end_time)        
        elif args.end or args.start:
            padded_end_time = "%s " % (end_time)

        w_duration = ""
        if args.duration:
            if start_time and end_time:
                w_duration = " (%s)" % (end_time - start_time)
            else:
                w_duration = " (unknown duration)"

        print("%sFlow %s ]%s%s" % (padded_end_time, name, label, w_duration))

        if args.hints and not args.quiet:
            print("Legend:")
            print("  [ Workflow start")
            if args.inputs:
                print("  < Used as input")
            if args.outputs:
                print("  > Generated as output")
            if have_nested:
                print("  * Nested provenance, use UUID to explore: cwlprov run %s" % c_id)
            print("  ] Workflow end")

        return Status.OK        

def main(args=None):
    tool = Tool(args)
    return tool.main()
