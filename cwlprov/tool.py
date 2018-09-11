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

import sys
import argparse
from functools import partial

import dateutil.parser

from cwlprov.ro import ResearchObject

# TODO: Move any use these to cwlprov.*
import arcp
import bagit
from uuid import UUID
import bdbag
from bdbag.bdbagit import BDBag
import posixpath
import pathlib
from pathlib import Path
import shutil
from prov.identifier import Identifier
from prov.model import *
from enum import IntEnum

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

class Status(IntEnum):
    """Exit codes from main()"""
    OK = 0
    UNKNOWN_COMMAND = 1
    BAG_NOT_FOUND = 2
    INVALID_BAG = 3
    MISSING_PROFILE = 4
    UNSUPPORTED_CWLPROV_VERSION = 5
    UNKNOWN_RUN = 6
    UNKNOWN_FORMAT = 7

def parse_args(args=None):
    parser = argparse.ArgumentParser(description='cwlprov')
    parser.add_argument("--directory", "-d", 
        help="Path to CWLProv Research Object folder (default: .)",
        default=None
        )
    parser.add_argument("--verbose", default=False, action='store_true',
        help="More verbose logging")
    parser.add_argument("--quiet", "-q", default=True, action='store_true',
        help="No logging or hints")

    parser.add_argument("--hints", default=True, action='store_true',
        help="Show hints on cwlprov usage")
    parser.add_argument("--no-hints", default=True, action='store_false',
        dest="hints", help="Do not show hints")
    subparsers = parser.add_subparsers(title='commands', dest="cmd")
    parser_validate = subparsers.add_parser('validate', help='validate the CWLProv RO')
    parser_info = subparsers.add_parser('info', help='CWLProv RO')
    parser_prov = subparsers.add_parser('prov', help='show provenance')
    parser_prov.add_argument("id", default=None, nargs="?", help="workflow run UUID")
    parser_prov.add_argument("--format", "-f", default="files", help="Output in PROV format (default: files)")
    parser_prov.add_argument("--formats", "-F", default=False, 
        action='store_true', help="List available PROV formats")

    parser_run = subparsers.add_parser('run', help='show workflow execution')
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

    parser_who = subparsers.add_parser('who', help='who ran the workflow')

    return parser.parse_args(args)

def _determine_bagit_folder(folder=None):
    # Absolute so we won't climb to ../../../../../ forever
    # and have resolved any symlinks
    folder = pathlib.Path().absolute()
    while True:
        bagit_file = folder / "bagit.txt"
        if bagit_file.is_file():
            return folder
        if folder == folder.parent:
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
        print("Invalid BagIt folder: %s" % bag.path,
            file=sys.stderr)
        # Specific errors already output from bagit library
        return Status.INVALID_BAG
    # Check we follow right profile
    profiles = _info_set(bag, "BagIt-Profile-Identifier")
    supported_ro = set(BAGIT_RO_PROFILES).intersection(profiles)
    if not supported_ro:
        if full_validation or not args.quiet:
            print("Missing BdBag profile: %s" % bag.path,
                file=sys.stderr)
        if full_validation and args.hints and not args.quiet:
            print("Try adding to %s/bag-info.txt:" % bag.path)
            print("BagIt-Profile-Identifier: %s" % BAGIT_RO_PROFILES[0])
            return Status.MISSING_PROFILE
    # Check we have a manifest
    has_manifest = MANIFEST_JSON in bag.tagfile_entries()
    if not has_manifest:
        print("Missing from tagmanifest: " + MANIFEST_JSON, file=sys.stderr)
        return Status.MISSING_MANIFEST
    return Status.OK

def validate_ro(ro, full_validation=False, args=None):
    # If it has this prefix, it's probably OK
    cwlprov = set(p for p in ro.conformsTo if p.startswith("https://w3id.org/cwl/prov/"))
    if not cwlprov:
        if full_validation or not args.quiet: 
            print("Missing CWLProv profile: %s" % ro.bag.path,
                file=sys.stderr)
        if full_validation and args.hints and not args.quiet:
            print("Try adding to %s/metadata/manifest.json:" % ro.bag.path)
            print('{\n  "id": "/",\n  "conformsTo", "%s",\n  ...\n}' %
                CWLPROV_SUPPORTED[0])
            return Status.MISSING_PROFILE
    supported_cwlprov = set(CWLPROV_SUPPORTED).intersection(cwlprov)
    if cwlprov and not supported_cwlprov:
        # Probably a newer one this code don't support yet; it will 
        # probably be fine
        if full_validation or not args.quiet: 
            print("Unsupported CWLProv version: %s" % cwlprov, file=sys.stderr)
        if full_validation and args.hints and not args.quiet:
            print("Supported profiles:\n %s" %
                    "\n ".join(CWLPROV_SUPPORTED)
                 )
            return Status.UNSUPPORTED_CWLPROV_VERSION
    return Status.OK

def _many(s):
    return ", ".join(map(str, s))

def info(ro, args):
    # About RO?
    if not args.quiet:
        print(ro.bag.info.get("External-Description", "Research Object"))
    print("ID: %s" % ro.id)
    cwlprov = set(p for p in ro.conformsTo if p.startswith("https://w3id.org/cwl/prov/"))
    if cwlprov:
        print("Profile: %s" % _many(cwlprov))
    w = ro.workflow_id
    if w:
        print("Workflow ID: %s" % w)
    when = ro.bag.info.get("Bagging-Date")
    if when:
        print("Packaged: %s" % when)
    return Status.OK

def who(ro, args): 
    # about RO?
    createdBy = _many(ro.createdBy)
    authoredBy = _many(ro.authoredBy)
    if createdBy or not quiet:
        print("Packaged By: %s" % createdBy or "(unknown)")
    if authoredBy or not quiet:
        print("Executed By: %s" % authoredBy or "(unknown)")
    return Status.OK

def path(p, ro):
    p = ro.resolve_path(str(p))
    return Path(p).relative_to(Path().absolute())

def _wf_id(ro, args):
    w = args.id or ro.workflow_id
    uuid = None
    # ensure consistent UUID URIs
    try:
        uuid = UUID(w.replace("urn:uuid:", ""))
        return (uuid.urn, uuid)
    except ValueError:
        if not args.quiet:
            print("Warning: Invalid UUID %s" % w, file=sys.stderr)
        return w, None

def _first(iterable):
    return next(iter(iterable), None)

def _prov_with_attr(prov_doc, prov_type, attrib_value, with_attrib=PROV_ATTR_ACTIVITY):
    for elem in prov_doc.get_records(prov_type):
        if (with_attrib, attrib_value) in elem.attributes:
            yield elem

def _prov_attr(attr, elem):
    return _first(elem.get_attribute(attr))

def run(ro, args):
    uri,uuid = _wf_id(ro, args)
    name = str(uuid or uri)
    if not ro.provenance(uri):
        print("No provenance found: %s" % name, file=sys.stderr)
        return Status.UNKNOWN_RUN

    prov_doc = _prov_document(ro, uri, args)
    if not prov_doc:
        # Error already printed by _prov_document
        return Status.UNKNOWN_RUN

    if not args.quiet:
        print("Workflow run:",  name)
    activity_id = Identifier(uri)
    activity = _first(prov_doc.get_record(activity_id))
    if not activity:
        print("Provenance does not describe activity %s" % uri, file=sys.stderr)
        return Status.UNKNOWN_RUN
    label = ""
    if args.labels:
        label = " %s " % (_first(activity.get_attribute("prov:label")) or "")
    
    start = _first(_prov_with_attr(prov_doc, ProvStart, activity_id))
    start_time = start and _prov_attr(PROV_ATTR_TIME, start)
    end = _first(_prov_with_attr(prov_doc, ProvEnd, activity_id))
    end_time = end and _prov_attr(PROV_ATTR_TIME, end)
    
    PADDING = " " * 26  # len("2018-08-08 22:44:06.573330")
    
    w_duration = ""
    if args.duration:
        if start_time and end_time:
            w_duration = " (%s)" % (end_time - start_time)
        else:
            w_duration = " (unknown duration)"

    padded_start_time = ""
    if args.end and args.start:
        # 2 columns
        padded_start_time = "%s %s " % (start_time, PADDING)        
    elif args.end or args.start:
        # 1 column, we don't care which
        padded_start_time = "%s " % (start_time)
    print("%sFlow %s >%s%s" % (padded_start_time, name, label, w_duration))

    # inputs
    usage = _prov_with_attr(prov_doc, ProvUsage, activity_id, PROV_ATTR_ACTIVITY)
    for u in usage:
        print(u)

    # steps
    have_nested = False
    if args.steps:
        started = _prov_with_attr(prov_doc, ProvStart, activity_id, PROV_ATTR_STARTER)
        steps = map(partial(_prov_attr, PROV_ATTR_ACTIVITY), started)
        for child in steps:
            c_activity = _first(prov_doc.get_record(child))
            c_label = ""
            if args.labels:
                c_label = " %s " % (_first(c_activity.get_attribute("prov:label")) or "")
            c_start = _first(_prov_with_attr(prov_doc, ProvStart, child))
            c_start_time = c_start and _prov_attr(PROV_ATTR_TIME, c_start)
            c_end = _first(_prov_with_attr(prov_doc, ProvEnd, child))
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
            c_end_time = args.end and "%s " % (c_end_time or PADDING)
            print("%s%sStep %s %s%s%s" % (c_start_time or "", c_end_time or "", c_id, c_provenance and "*" or " ", c_label, c_duration))

    # end
    padded_end_time = ""
    if args.end and args.start:
        padded_end_time = "%s %s " % (PADDING, end_time)        
    elif args.end or args.start:
        padded_end_time = "%s " % (end_time)
    print("%sFlow %s <%s%s" % (padded_end_time, name, label, w_duration))

    if args.hints and not args.quiet:
        print("Legend:")
        print("  > Workflow start")
        if have_nested:
            print("  * Nested provenance, use UUID to explore: cwlprov run %s" % c_id)
        print("  < Workflow start")

    return Status.OK


MEDIA_TYPES = {
    "txt": 'text/plain; charset="UTF-8"',
    "ttl": 'text/turtle; charset="UTF-8"',
    "rdf": 'application/rdf+xml',
    "json": 'application/json',
    "jsonld": 'application/ld+json',
    "xml": 'application/xml',
    "cwl": 'text/x+yaml; charset="UTF-8"',
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
            if args.verbose:
                print("Loading %s" % prov)
            if c in rdf_candidates:
                doc = ProvDocument.deserialize(source=prov, format="rdf", rdf_format=c)
            else:
                doc = ProvDocument.deserialize(source=prov, format=c)
            return doc.unified()
    print("No PROV compatible format found for %s" % uri, file=sys.stderr)
    return None


def prov(ro, args):
    uri,uuid = _wf_id(ro, args)
    name = str(uuid or uri)

    if args.format == "files":
        for prov in ro.provenance(uri):
            if args.formats:
                format = ro.mediatype(prov) or ""
                format = EXTENSIONS.get(format, format)
                print("%s %s" % (format, (path(prov, ro))))
            else:
                print("%s" % path(prov, ro))
    else:
        media_type = MEDIA_TYPES.get(args.format, args.format)
        prov = _prov_format(ro, uri, media_type)
        if not prov:
            print("Unrecognized format: %s" % args.format)
            return Status.UNKNOWN_FORMAT
        with prov.open(encoding="UTF-8") as f:
            shutil.copyfileobj(f, sys.stdout)
            print() # workaround for missing trailing newline
    return Status.OK

def main(args=None):
    # type: (...) -> None
    """cwlprov command line tool"""
    args = parse_args(args)

    folder = args.directory or _determine_bagit_folder()
    if not folder:        
        print("Could not find bagit.txt, try cwlprov -d mybag/", file=sys.stderr)
        return Status.BAG_NOT_FOUND
    
    full_validation = args.cmd == "validate"

    ## BagIt check
    bag = BDBag(str(folder))
    invalid = validate_bag(bag, full_validation)
    if invalid:
        return invalid
    
    ro = ResearchObject(bag)
    invalid = validate_ro(ro, full_validation, args)
    if invalid:
        return invalid

    if full_validation:
        print("Valid: %s" % folder)
        return Status.OK

    # Else, find the other commands
    COMMANDS = {
        "info": info,
        "run": run,
        "who": who,
        "prov": prov
    }
    
    cmd = COMMANDS.get(args.cmd)
    if not cmd:
        # Light-weight validation
        print("Detected CWLProv research Object: %s" % folder)
        return Status.OK
    
    return cmd(ro, args)

if __name__ == "__main__":
    sys.exit(main())

