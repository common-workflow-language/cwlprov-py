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

from cwlprov.ro import ResearchObject

# TODO: Move any use these to cwlprov.*
import arcp
import bagit

import bdbag
from bdbag.bdbagit import BDBag
import posixpath
import pathlib

from enum import IntEnum

BAGIT_RO_PROFILES = set((
    "https://w3id.org/ro/bagit/profile", 
    "http://raw.githubusercontent.com/fair-research/bdbag/master/profiles/bdbag-ro-profile.json"
))
CWLPROV_SUPPORTED = set((
    # Decreasing order as first item is output as example
    "https://w3id.org/cwl/prov/0.4.0",
    "https://w3id.org/cwl/prov/0.3.0",
))

MANIFEST_JSON = posixpath.join("metadata", "manifest.json")

class Status(IntEnum):
    """Exit codes from main()"""
    OK = 0
    BAG_NOT_FOUND = 1
    INVALID_BAG = 2
    MISSING_PROFILE = 3
    UNSUPPORTED_CWLPROV_VERSION = 4

def parse_args(args=None):
    parser = argparse.ArgumentParser(description='cwlprov')
    parser.add_argument("--directory", "-d", 
        help="Path to CWLProv Research Object folder (default: .)",
        default=None
        )
    subparsers = parser.add_subparsers(title='commands', dest="cmd")
    parser_info = subparsers.add_parser('info', help='display brief info about the CWLProv RO')
    parser_validate = subparsers.add_parser('validate', help='validate the CWLProv RO')
    parser_inputs = subparsers.add_parser('inputs', help='show inputs')

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

def main(args=None):
    # type: (...) -> None
    """cwlprov command line tool"""
    args = parse_args(args)

    folder = args.directory or _determine_bagit_folder()
    if not folder:        
        print("Could not find bagit.txt, try cwlprov -d mybag/", file=sys.stderr)
        return Status.BAG_NOT_FOUND

    ## BagIt check
    bag = BDBag(folder)
    # Always do a minimal validation, but
    # will also test checksum on --validate
    validate = args.cmd == "validate"
    valid_bag = bag.validate(fast=validate)

    ## RO check
    profiles = set(bag.info.get("BagIt-Profile-Identifier", ()))
    supported_ro = BAGIT_RO_PROFILES.intersection(profiles)
    
    has_manifest = MANIFEST_JSON in bag.tagfile_entries()
    if not has_manifest:
        print("Missing " + MANIFEST_JSON)
        return Status.MISSING_MANIFEST

    ro = ResearchObject(bag)
    cwlprov = set()
    for p in ro.conformsTo:
        if "https://w3id.org/cwl/prov/" in p:
            cwlprov.add(p)
    supported_cwlprov = CWLPROV_SUPPORTED.intersection(cwlprov)
    if cwlprov and not supported_cwlprov:
        print("Unsupported CWLProv version: %s" % cwlprov, file=sys.stderr)


    ##PROV check
    # TODO: Prov check

    if validate:
        # TODO: More checks, e.g. every PROV file valid?
        if not valid_bag:
            print("Invalid BagIt folder: %s" % folder,
                file=sys.stderr)
            return Status.INVALID_BAG
        if not supported_ro:
            print("Missing BdBag profile (e.g. %s): %s" %
                (next(iter(BAGIT_RO_PROFILES)), folder),
                file=sys.stderr)
            return Status.MISSING_PROFILE
        if not cwlprov:
            print("Missing CWLProv profile (e.g. %s): %s" %
                (next(iter(CWLPROV_SUPPORTED)), folder),
                file=sys.stderr)
            return Status.MISSING_PROFILE
        if not supported_cwlprov:
            # Warning already printed above
            print("Supported CWLProv profiles: %s" %
                " ".join(CWLPROV_SUPPORTED),
                file=sys.stderr)
            return Status.MISSING_PROFILE


            return Status.UNSUPPORTED_CWLPROV_VERSION

    # Probably went fine if we made it to here
    return Status.OK

if __name__ == "__main__":
    sys.exit(main())

