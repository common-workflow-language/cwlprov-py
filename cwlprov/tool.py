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
cwlprov Command Line Tool
"""
__author__      = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__   = "© 2018 Software Freedom Conservancy (SFC)"
__license__     = "Apache License, version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"

from cwlprov import __version__

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
import shlex
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
    "https://w3id.org/cwl/prov/0.6.0",
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
    PROV_NOT_FOUND = errno.ENOENT
    NOT_A_DIRECTORY = errno.ENOTDIR
    UNKNOWN_RUN = errno.ENODATA
    UNKNOWN_ACTIVITY = errno.ENODATA
    UNKNOWN_TOOL = errno.ENODATA
    PERMISSION_ERROR = errno.EACCES
    NOT_IMPLEMENTED = errno.ENOSYS
    # User-specified exit codes
    # http://www.tldp.org/LDP/abs/html/exitcodes.html
    MISSING_PROFILE = 166
    INVALID_BAG = 167
    UNSUPPORTED_CWLPROV_VERSION = 168
    CANT_LOAD_CWL = 169
    MISSING_PLAN = 170



def parse_args(args=None):
    parser = argparse.ArgumentParser(description='cwlprov explores Research Objects containing provenance of Common Workflow Language executions. <https://w3id.org/cwl/prov/>')
    
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    # Common options
    parser.add_argument("--directory", "-d", 
        help="Path to CWLProv Research Object (default: .)",
        default=None
        )
    parser.add_argument("--relative", default=None, action='store_true',
        help="Output paths relative to current directory (default if -d is missing or relative)")
    parser.add_argument("--absolute", default=None, action='store_false',
        dest="relative", help="Output absolute paths (default if -d is absolute)")

    parser.add_argument("--output", "-o", default="-",
        help="File to write output to (default: stdout)")

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

    # Common options for parser_input and parser_output
    run_option = argparse.ArgumentParser(add_help=False)
    run_option.add_argument("--run", default=None, help="workflow run UUID that contains step")
    run_option.add_argument("id", default=None, nargs="?", help="step/workflow run UUID")

    io_outputs = argparse.ArgumentParser(add_help=False)
    io_outputs.add_argument("--parameters",  default=True, action='store_true',
        help="Show parameter names")
    io_outputs.add_argument("--no-parameters", default=True, action='store_false',
        dest="parameters", help="Do not show parameter names")
    io_outputs.add_argument("--format", default="any",
        choices=["any", "files", "values", "uris", "json"],
        help="Output format, (default: any)")
        # Tip: These formats are NOT the same as in parser_prov

    parser_input = subparsers.add_parser('inputs', 
        help='list workflow/step input files/values', 
        parents=[run_option, io_outputs])

    parser_output = subparsers.add_parser('outputs', 
        help='list workflow/step output files/values', 
        parents=[run_option, io_outputs])

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

    parser_runs = subparsers.add_parser('runs', help='List all workflow executions in RO')

    parser_rerun = subparsers.add_parser('rerun', 
        help='Rerun a workflow or step', 
        parents=[run_option])
    parser_rerun.add_argument("--cwlrunner", default="cwl-runner", help="Executable for running cwl (default: cwl-runner)")
    parser_rerun.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments to cwl runner")

    parser_derived = subparsers.add_parser('derived', 
        help='List what was derived from a data item, based on activity usage/generation')
    parser_derived.add_argument("--run", default=None, help="workflow run UUID which provenance to examine")
    parser_derived.add_argument("data", 
        help="Data file, hash or UUID")

    parser_derived.add_argument("--recurse",  default=True, action='store_true',
        help="Recurse transitive derivations (default)")
    parser_derived.add_argument("--no-recurse", default=True, action='store_false',
        dest="recurse", help="Do not recurse transitive derivations")

    parser_derived.add_argument("--maxdepth", default=None, type=int,    
        help="Maximum depth of transitive derivations (default: infinity)")
    
    parser_stats = subparsers.add_parser('runtimes', 
        help='Calculate average step execution runtimes',
        parents=[run_option])
    
    return parser.parse_args(args)



def _find_bagit_folder(folder=None):
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


def _simpler_uuid(uri):
    return str(uri).replace("urn:uuid:", "")

def _as_uuid(w):
    try:
        uuid = UUID(w.replace("urn:uuid:", ""))
        return (uuid.urn, uuid, str(uuid))
    except ValueError:
        logger.warn("Invalid UUID %s", w)
        # return -as-is
        return w, None, str(w)

def _prov_with_attr(prov_doc, prov_type, attrib_value, with_attrib=PROV_ATTR_ACTIVITY):
    for elem in prov_doc.get_records(prov_type):
        if (with_attrib, attrib_value) in elem.attributes:
            yield elem

def _prov_attr(attr, elem):
    return first(elem.get_attribute(attr))


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
        if self.args.output != "-":
            self.output = open(self.args.output, mode="w", encoding="UTF-8")
        else:
            self.output = None # sys.stdout
    
    def close(self):
        if self.output:
            # Close --output file
            self.output.close()
            self.output = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _determine_relative(self):
        args = self.args        

        if args.relative is False:
            _logger.debug("Output paths absolute")
            self.relative_paths = None
            return

        _logger.debug("Determining output paths")

        if not self.output: # stdout
            _logger.debug("Output paths relative to current directory?")
            relative_to = Path()
        else:
            _logger.debug("Output paths relative to (resolved parent) path of %s?", args.output)
            relative_to = Path(args.output).resolve().parent

        if args.relative:
            # We'll respect the parameter
            # Either calculate --relative ; or None for --absolute
            _logger.debug("Output paths relative to %s", relative_to)
            self.relative_paths = args.relative and relative_to or None
            return
        
        assert(args.relative is None) # only remaining option
        _logger.debug("Neither --relative nor --absolute given")

        if self.output:
            _logger.debug("Considering if paths should be relative to --output %s", args.output)

            # Only relative if we can avoid ../ (use --relative to force)
            # assuming _determine_folder has already parsed args.directory
            try:
                # Check if bag folder is reachable from output folder                    
                f = self.folder.resolve() # Compare as resolved - following symlinks etc
                rel = f.relative_to(relative_to)
                self.relative_paths = relative_to
                _logger.debug("Relative as bag %s is within output folder %s", f, relative_to)
            except ValueError:
                # Would need ../ - bail out to absolute paths
                self.relative_paths = None
                _logger.debug("Absolute as bag %s not within output folder %s", self.folder, relative_to)

        elif args.directory and Path(args.directory).is_absolute():
            _logger.debug("Output paths absolute as --directory %s is absolute", args.directory)
            self.relative_paths = None
        else:
            _logger.debug("Output paths relative to %s as --directory %s is relative", relative_to, args.directory)
            self.relative_paths = relative_to

    def _determine_logging(self):
        if self.args.quiet and self.args.verbose:
            _logger.error("Incompatible parameters: --quiet --verbose")
            return Status.UNKNOWN_COMMAND
        _set_log_level(self.args.quiet, self.args.verbose)

    def _determine_folder(self):        
        folder = self.args.directory or _find_bagit_folder()
        if not folder:        
            _logger.error("Could not find bagit.txt, try cwlprov -d mybag/")
            return Status.BAG_NOT_FOUND
        self.folder = pathlib.Path(folder)
        if not self.folder.exists():
            _logger.error("No such file or directory: %s",  self.folder)
            return Status.BAG_NOT_FOUND
        if not self.folder.is_dir():
            _logger.error("Not a directory: %s", folder)
            return Status.NOT_A_DIRECTORY
        bagit_file = self.folder / "bagit.txt"
        if not bagit_file.is_file():
            _logger.error("File not found: %s", bagit_file)
            return Status.BAG_NOT_FOUND

    def _determine_hints(self):
        # Don't output hints for --quiet or --output
        self.hints = self.args.hints and not self.args.quiet and not self.output

    def main(self):
        # type: (...) -> None
        """cwlprov command line tool"""
        args = self.args
        
        status = self._determine_logging()
        if status:
            return status
        # Now that logging is determined we can report on args.output
        if self.output:
            _logger.debug("Output to %s", args.output)
        
        status = self._determine_hints()
        if status:
            return status
    
        status = self._determine_folder()
        if status:
            return status

        status = self._determine_relative()
        if status:
            return status

        full_validation = args.cmd == "validate"
        _logger.info("Opening BagIt %s", self.folder)
        ## BagIt check
        try:
            bag = BDBag(str(self.folder))
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

        invalid = self.validate_bag(bag, full_validation)
        if invalid:
            return invalid
        
        self.ro = ResearchObject(bag)
        invalid = self.validate_ro(full_validation)
        if invalid:
            return invalid

        if full_validation:
            if not args.quiet:
                self.print("Valid CWLProv RO: %s" % self._absolute_or_relative_path(self.folder))
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
            "rerun": self.rerun,
            "derived": self.derived,
            "runtimes": self.runtimes,
        }
        
        cmd = COMMANDS.get(args.cmd)
        if not cmd:
            # Light-weight validation
            if not args.quiet:
                self.print("Detected CWLProv Research Object: %s" % self.folder)
            else:
                self.print(self.folder)
            return Status.OK
        
        return cmd()

    def _resource_path(self, path, absolute=False):
        p = self.ro.resolve_path(str(path))
        return self._absolute_or_relative_path(p, absolute)

    def _absolute_or_relative_path(self, path, absolute=False):
        p = Path(path)
        if not absolute and self.relative_paths:
            cwd = Path(self.relative_paths)
            return os.path.relpath(p, cwd)
        else:
            return Path(p).absolute()

    def _wf_id(self, run=None):
        w = run or self.args.id or self.ro.workflow_id
        # ensure consistent UUID URIs
        return _as_uuid(w)

    def validate_bag(self, bag, full_validation=False):
        try:
            valid_bag = bag.validate(fast=not full_validation)
        except BagError as e:
            _logger.error("BagIt validation failed for: %s: %s", bag.path, e)
            return Status.INVALID_BAG
        if not valid_bag:
            _logger.error("Invalid BagIt folder: %s", bag.path)
            # Specific errors already output from bagit library
            return Status.INVALID_BAG
        # Check we follow right profile
        profiles = _info_set(bag, "BagIt-Profile-Identifier")
        supported_ro = set(BAGIT_RO_PROFILES).intersection(profiles)
        if not supported_ro:
            _logger.warning("Missing BdBag profile: %s", bag.path)
            if self.hints:
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

    def validate_ro(self, full_validation=False):
        ro = self.ro
        args = self.args
        # If it has this prefix, it's probably OK
        cwlprov = set(p for p in ro.conformsTo if p.startswith("https://w3id.org/cwl/prov/"))
        if not cwlprov:
            if full_validation or not args.quiet: 
                _logger.warning("Missing CWLProv profile: %s", ro.bag.path)
            if full_validation and self.hints:
                print("Try adding to %s/metadata/manifest.json:" % ro.bag.path)
                print('{\n  "id": "/",\n  "conformsTo", "%s",\n  ...\n}' %
                    CWLPROV_SUPPORTED[0])
                return Status.MISSING_PROFILE
        supported_cwlprov = set(CWLPROV_SUPPORTED).intersection(cwlprov)
        if cwlprov and not supported_cwlprov:
            # Probably a newer one this code don't support yet; it will 
            # probably be fine
            _logger.warning("Unsupported CWLProv version: %s", cwlprov)
            if self.hints:
                print("Supported profiles:\n %s" %
                        "\n ".join(CWLPROV_SUPPORTED)
                    )
            if full_validation:
                return Status.UNSUPPORTED_CWLPROV_VERSION
        return Status.OK

    def info(self):
        ro = self.ro
        args = self.args

        # About RO?
        if not args.quiet:
            self.print(ro.bag.info.get("External-Description", "Research Object"))
        self.print("Research Object ID: %s" % ro.id)
        cwlprov = set(p for p in ro.conformsTo if p.startswith("https://w3id.org/cwl/prov/"))
        if cwlprov:
            self.print("Profile: %s" % many(cwlprov))
        w = ro.workflow_id
        if w:
            self.print("Workflow run ID: %s" % w)
        when = ro.bag.info.get("Bagging-Date")
        if when:
            self.print("Packaged: %s" % when)
        return Status.OK

    def who(self): 
        ro = self.ro
        args = self.args

        # about RO?
        createdBy = many(ro.createdBy)
        authoredBy = many(ro.authoredBy)
        if createdBy or not args.quiet: # skip (unknown) on -q)
            self.print("Packaged By: %s" % createdBy or "(unknown)")
        if authoredBy or not args.quiet:
            self.print("Executed By: %s" % authoredBy or "(unknown)")
        return Status.OK

    def _derived_from(self, uuid):
        pass

    def _entity_from_data_argument(self):
        # Is it a UUID?
        data_uuid = None
        data_file = None
        try:
            data_uuid = UUID(args.data)
        except ValueError:
            pass
        
        if data_uuid:
            _logger.debug("Assuming UUID %s", data_uuid)
            pass
        else:
            # Is it a filename within the RO?
            try:
                data_file = self.research_object.resolve_path(args.data)
            except OSError:
                pass

            # A file from our current directory?
            if os.path.exists(args.data):
                data_file = pathlib.Path(args.data)


    def derived(self):
        ro = self.ro
        args = self.args
        
        _data_entity = _entity_from_data_argument(args.data)

        return Status.OK

    def runtimes(self):
        ro = self.ro
        args = self.args
        
        error,activity = self._load_activity_from_provenance()
        if error:
            return error

        plans = {}

        for step in activity.steps():
            plan = step.plan()
            if not plan:
                plan = step.identifier
            durations = plans.setdefault(plan, [])            
            dur = step.duration()
            if dur:
                durations.append(dur)
        
        # TODO: Support CSV output?

        # Assume no more than 99 hours for well-aligned columns
        format="%015s %015s %015s %04s %s"
        if not args.quiet:
            self.print(format, *("min avg max n step".split()))
        # TODO: Sort from max-to-lowest average?
        for plan in plans:
            durations = plans[plan]
            self.print(format,
                min(durations), average(durations), max(durations), len(durations),
                plan.localpart or plan)

        return Status.OK



    def prov(self):
        ro = self.ro
        args = self.args

        uri,uuid,name = self._wf_id()

        if args.format == "files":
            for prov in ro.provenance(uri) or ():
                if args.formats:
                    format = ro.mediatype(prov) or ""
                    format = EXTENSIONS.get(format, format)
                    self.print("%s %s" % (format, (self._resource_path(prov))))
                else:
                    self.print("%s" % self._resource_path(prov))
        else:
            media_type = MEDIA_TYPES.get(args.format, args.format)
            prov = _prov_format(ro, uri, media_type)
            if not prov:
                _logger.error("Unrecognized format: %s", args.format)
                return Status.UNKNOWN_FORMAT
            with prov.open(encoding="UTF-8") as f:
                shutil.copyfileobj(f, self.output or sys.stdout)
                self.print() # workaround for missing trailing newline
        return Status.OK

    def inputs(self):
        return self._inputs_or_outputs(is_inputs=True)
    
    def outputs(self):
        return self._inputs_or_outputs(is_inputs=False)

    def _load_provenance(self, wf_uri):
        if not self.ro.provenance(wf_uri):
            if self.args.run:
                _logger.error("No provenance found for specified run: %s", wf_uri)
                # We'll need to give up
                return Status.UNKNOWN_RUN
            else:
                _logger.debug("No provenance found for activity: %s", wf_uri)
                _logger.info("Assuming primary provenance --run %s", self.ro.workflow_id)
                wf_uri,_,_ = _as_uuid(self.ro.workflow_id)
                if not self.ro.provenance(wf_uri):
                    _logger.error("No provenance found for: %s", wf_uri)
                    return Status.UNKNOWN_RUN

        try:
            provenance = Provenance(self.ro, wf_uri)
        except OSError:
            # assume Error already printed by _prov_document
            return Status.PROV_NOT_FOUND
        self.provenance = provenance
        return Status.OK

    def _load_activity_from_provenance(self):
        wf_uri,wf_uuid,wf_name = self._wf_id(self.args.run)
        a_uri,a_uuid,a_name = self._wf_id()
        error = self._load_provenance(wf_uri)
        if error != Status.OK:
            return (error, None)
        
        activity = self.provenance.activity(a_uri)
        if activity:
            return (Status.OK, activity)
        else:
            _logger.error("Provenance does not describe step %s: %s", wf_name, a_uri)
            if not self.args.run and self.hints:
                print("If the step is in nested provenance, try '--run UUID' as found in 'cwlprov run'")
            return (Status.UNKNOWN_ACTIVITY, None)

    def _inputs_or_outputs(self, is_inputs):
        if is_inputs:
            put_s = "Input"
        else:
            put_s = "Output"

        ro = self.ro
        args = self.args
        wf_uri,wf_uuid,wf_name = self._wf_id(self.args.run)
        a_uri,a_uuid,a_name = self._wf_id()
        if not self.ro.provenance(wf_uri):            
            if args.run:
                _logger.error("No provenance found for: %s", wf_name)
                # We'll need to give up
                return Status.UNKNOWN_RUN
            else:
                _logger.debug("No provenance found for: %s", wf_name)
                _logger.info("Assuming primary provenance --run %s", ro.workflow_id)
                wf_uri,wf_uuid,wf_name = _as_uuid(ro.workflow_id)
                if not ro.provenance(wf_uri):
                    _logger.error("No provenance found for: %s", wf_name)
                    return Status.UNKNOWN_RUN

        try:
            provenance = Provenance(self.ro, wf_uri)
        except OSError:
            # assume Error already printed by _prov_document
            return Status.UNKNOWN_RUN
        
        activity = provenance.activity(a_uri)
        if not activity:
            _logger.error("Provenance does not describe step %s: %s", wf_name, a_uri)
            if not self.args.run and self.hints:
                print("If the step is in nested provenance, try '--run UUID' as found in 'cwlprov run'")
            return Status.UNKNOWN_RUN
        activity_id = activity.id



        if wf_uri != a_uri:
            _logger.info("%ss for step %s in workflow %s", put_s, a_name, wf_name)
        else:
            _logger.info("%ss for workflow %s", put_s, wf_name)

        job = {}
        
        if is_inputs:
            records = activity.usage()
        else:
            records = activity.generation()

        for u in records:
            entity_id = u.entity_id
            role = u.role

            # Naively assume CWL identifier structure of URI
            if not role:
                _logger.warning("Unknown role for %s, skipping", u)
                role_name = None
                continue
            
            # poor mans CWL parameter URI deconstruction
            role_name = str(role)
            role_name = role_name.split("/")[-1]
            role_name = urllib.parse.unquote(role_name)
            
            if args.parameters and not args.quiet and args.format != "json":
                self.print("%s %s:", put_s, role_name)
            time = u.time
            entity = u.entity()
            if not entity:
                _logger.warning("No provenance for used entity %s", entity_id)
                continue

            file_candidates = [entity]
            file_candidates.extend(entity.specializationOf())
            if self.args.format in ("uris", "any"):
                self.print(file_candidates[-1].uri)
                continue

            printed_file = False
            for file_candidate in file_candidates:
                bundled = self.ro.bundledAs(uri=file_candidate.uri)
                if not bundled:
                    continue
                _logger.debug("entity %s bundledAs %s", file_candidate.uri, bundled)
                bundled_path = self._resource_path(bundled)
                job[role_name] = {}
                job[role_name]["class"] = "File"
                job[role_name]["path"] = str(bundled_path)
                if self.args.format in ("files", "any"):
                    self.print(bundled_path)
                    printed_file = True
                if self.args.format=="values":
                    # Warning: This will print all of the file straight to stdout
                    with open(self._resource_path(bundled, absolute=False)) as f:
                        shutil.copyfileobj(f, self.output or sys.stdout)
                    printed_file = True
                break
            if printed_file:
                continue # next usage

            # Still here? Perhaps it has prov:value ?
            value = entity.value
            if value is not None: # but might be False
                job[role_name] = value
                if self.args.format in ("values", "any"):
                    self.print(value)
                elif self.args.format == "files":
                    # We'll have to make a new file!
                    with tempfile.NamedTemporaryFile(delete=False) as f:
                        b = str(value).encode("utf-8")
                        f.write(b)                        
                        self.print(f.name)

        if self.args.format == "json":
            self.print(json.dumps(job))

    def _entity_as_json(self, entity, absolute=True):
        _logger.debug("json from %s", entity)
        file_candidates = [entity]
        file_candidates.extend(entity.specializationOf())
        for file_candidate in file_candidates:
            bundled = self.ro.bundledAs(uri=file_candidate.uri)            
            if not bundled:
                continue
            _logger.debug("entity %s bundledAs %s", file_candidate.uri, bundled)
            bundled_path = self._resource_path(bundled, absolute=absolute)
            json = {
                "class": "File",
                "path": str(bundled_path),
            }
            if entity.basename:
                json["basename"] = entity.basename
            if entity.nameroot:
                json["nameroot"] = entity.nameroot
            if entity.nameext:
                json["nameext"] = entity.nameext
            f = partial(self._entity_as_json, absolute=absolute)
            secondaries = list(map(f, entity.secondary_files()))
            if secondaries:
                json["secondaries"] = secondaries
            _logger.debug("file as json: %s", json)
            return json

        # Perhaps it has prov:value ?
        value = entity.value
        if value is not None: # ..but might be False
            _logger.debug("value as json: %s", value)
            return value
        
        # TODO: Handle Directory
        # TODO: Handle collection


        # Still here? No idea, fallback is just return the URI :(
        json = {
            "class": "File", # ??
            "location": entity.uri,
        }
        _logger.debug("uri as json: %s", json)
        return json

    def _inputs_or_outputs_job(self, activity, is_inputs, absolute):
        activity_id = activity.id

        job = {}

        if is_inputs:
            records = activity.usage()
        else:
            records = activity.generation()
        for u in records:
            entity_id = u.entity_id
            role = u.role

            # Naively assume CWL identifier structure of URI
            if not role:
                _logger.warning("Unknown role for %s, skipping", u)
                role_name = None
                continue
            
            # poor mans CWL parameter URI deconstruction
            role_name = str(role)
            role_name = role_name.split("/")[-1]
            role_name = urllib.parse.unquote(role_name)

            entity = u.entity()
            if not entity:
                _logger.warning("No provenance for entity %s", entity_id)
                continue
            job[role_name] = self._entity_as_json(entity, absolute=absolute)

        return job

    def runs(self):
        ro = self.ro
        args = self.args        
        for run in ro.resources_with_provenance():
            name = _simpler_uuid(run)
            
            if args.verbose or not args.quiet:
                # Also load up the provenance to find its name
                prov_doc = _prov_document(ro, run, args)
                if not prov_doc:
                    self.print(name)
                    _logger.warning("No provenance found for: %s", name)
                    continue
                
                activity_id = Identifier(run)
                activity = first(prov_doc.get_record(activity_id))
                if not activity:
                    _logger.error("Provenance does not describe activity %s", run)
                    return Status.UNKNOWN_RUN
                label = first(activity.get_attribute("prov:label")) or ""
                is_master = run == ro.workflow_id
                self.print("%s %s %s" % (name, is_master and "*" or " ", label))
            else:
                self.print(name)
        if self.hints:
            self.print("Legend:")
            self.print(" * master workflow")

    
    def rerun(self):
        if not self.args.id or self.args.id == "-":
            # Might be used to rerun default workflow
            self.args.id = None
        if not self.args.id and not self.args.run:
            wf_file = self._find_workflow()
            _logger.debug("Master workflow, re-using level 0 primary job")
            wf_arg = wf_file
            job_file = self._find_primary_job()
        else:
            _logger.debug("Recreating job from level 1 provenance")
            (error,a) = self._load_activity_from_provenance()
            if error:
                return error
            _logger.info("Rerunning step <%s> %s", a.id.uri, a.label)
            # Create job JSON from original input values
            job = self._recreate_job(a, absolute=True)
            job_file = self._temporary_job(job)

            # Now find which tool was rerun
            p = a.plan()
            if not p:
                _logger.warning("Could not find Association with Plan for %s" % a)
                return Status.MISSING_PLAN
            _logger.info("Step was executed with plan %s", p.uri)

            wf_file = self.ro.resolve_path(p.uri)
            if not "#" in p.uri:
                # Top-level cwl file
                wf_arg = wf_file
            else:
                # part of cwl file (e.g. a command line tool)

                # Workaround as Association links to the identified workflow step, 
                # but cwltool needs the (sometimes not identified) reference behind
                # the step's "run" property
                cwl = self._load_cwl(wf_file)
                if not cwl:
                    return Status.CANT_LOAD_CWL
                step_id = "#%s" % p.localpart
                run = self._find_step_run(cwl, step_id)
                if not isinstance(run, str):
                    _logger.error("Not implemented: rerun of inline 'run' of step %s", step_id)
                    return Status.NOT_IMPLEMENTED
                if run.startswith("#"):
                    wf_arg = "%s%s" % (wf_file, run)
                    _logger.info("Tool %s", wf_arg)
                else:
                    _logger.warning("Non-local 'run' %s might be missing from RO", step_id)                    
                    wf_arg = run
                    # TODO: Check if it's in snapshot/ or an absolute URI?

        return self._exec_cwlrunner(wf_arg, job_file)

    def _load_cwl(self, wf_file):
        _logger.debug("Loading CWL as JSON: %s", wf_file)
        with open(wf_file) as f:
            # FIXME: Load as yaml in case it is not JSON?
            cwl = json.load(f)
        ver = cwl["cwlVersion"]
        _logger.debug("Loaded CWL version: %s", ver)
        if not ver.startswith("v1."):
            _logger.fatal("Unsupported cwlVersion %s in %s", ver, wf_file)
            return None
        return cwl

    def _find_step_run(self, cwl, step_id):
        step = find_dict_with_item(cwl, step_id)
        if not step:
            _logger.error("Could not find step for ")
        _logger.debug("Found CWL step: %s", step)
        if step.get("class") in ("Workflow", "CommandLineTool", "ExpressionTool"):
            # We can execute directly
            return step_id
        return step.get("run")

    def _exec_cwlrunner(self, wf_arg, job_file):
        # Switch to a new temporary directory
        tmpdir = tempfile.mkdtemp(prefix="cwlprov.", suffix=".tmp")
        _logger.debug("cd %s", tmpdir)
        os.chdir(tmpdir)

        # Change to the new cwl runner process so Ctrl-C etc works
        if " " in self.args.cwlrunner:
            # Split out any cwl-runner arguments
            cwlargs = shlex.split(self.args.cwlrunner)
        else:
            cwlargs = [self.args.cwlrunner]
        cwlargs.append(str(wf_arg))
        cwlargs.append(str(job_file))
        cwlargs.extend(self.args.args)
    
        _logger.info("%s", " ".join(cwlargs))
        os.execlp(cwlargs[0], *cwlargs)
    
        # Still here? Above should have taken over this python process!
        _logger.fatal("Could not execute cwl-runner")
        return Status.UNHANDLED_ERROR
        
    def _find_workflow(self):
        #TODO find path in manifest
        path = "workflow/packed.cwl"
        p = self.ro.resolve_path(str(path))
        return p

    def _find_primary_job(self):
        #TODO find path in manifest
        path = "workflow/primary-job.json"
        p = self.ro.resolve_path(str(path))
        return p

    def _recreate_job(self, activity, absolute):
        # TODO: Actually do it
        job = self._inputs_or_outputs_job(activity, is_inputs=True, absolute=absolute)
        _logger.debug("Recreated job: %s", job)
        return job

    def _temporary_job(self, job):
        with tempfile.NamedTemporaryFile(mode="w", prefix="rerun-", suffix=".json", delete=False, encoding="UTF-8") as f:
            json.dump(job, f, indent=2)
            _logger.info("Temporary job: %s", f.name)
            return f.name
 
    def _usage(self, activity_id, prov_doc):
        args = self.args
        if not args.inputs:
            return
        usage = _prov_with_attr(prov_doc, ProvUsage, activity_id, PROV_ATTR_ACTIVITY)
        for u in usage:
            entity = _prov_attr(PROV_ATTR_ENTITY, u)
            entity_id = entity and _simpler_uuid(entity.uri).replace("urn:hash::sha1:", "")
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
            self.print("%sIn   %s < %s" % (time_part, entity_id, role or ""))

    def _generation(self, activity_id, prov_doc):
        args = self.args
        if not args.outputs:
            return
        gen = _prov_with_attr(prov_doc, ProvGeneration, activity_id, PROV_ATTR_ACTIVITY)
        for g in gen:
            entity = _prov_attr(PROV_ATTR_ENTITY, g)
            entity_id = entity and _simpler_uuid(entity.uri).replace("urn:hash::sha1:", "")
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
            self.print("%sOut  %s > %s" % (time_part, entity_id, role or ""))

    def print(self, msg="", *args):
        if args and isinstance(msg, str) and "%" in msg:
            msg = msg % args
            print(msg, file=self.output or sys.stdout)
        else:
            print(msg, *args, file=self.output or sys.stdout)

    def run(self):
        ro = self.ro
        args = self.args
        uri,uuid,name = self._wf_id()
        if not ro.provenance(uri):
            _logger.error("No provenance found for: %s", name)
            #if self.hints:
            #    print("Try --search to examine all provenance files")
            return Status.UNKNOWN_RUN

        prov_doc = _prov_document(ro, uri, args)
        if not prov_doc:
            # Error already printed by _prov_document
            return Status.UNKNOWN_RUN

        if args.verbose:
            self.print("Workflow run:",  name)
        activity_id = Identifier(uri)
        activity = first(prov_doc.get_record(activity_id))
        if not activity:
            _logger.error("Provenance does not describe activity %s", uri)
            return Status.UNKNOWN_RUN
        if args.verbose:
            self.print(activity)
        label = ""
        if args.labels:
            label = " %s " % (first(activity.get_attribute("prov:label")) or "")
        
        start = first(_prov_with_attr(prov_doc, ProvStart, activity_id))
        start_time = start and _prov_attr(PROV_ATTR_TIME, start)
        end = first(_prov_with_attr(prov_doc, ProvEnd, activity_id))
        end_time = end and _prov_attr(PROV_ATTR_TIME, end)
        
        

        if args.verbose and start:
            self.print(start)
        padded_start_time = ""
        if args.end and args.start:
            # 2 columns
            padded_start_time = "%s %s " % (start_time, TIME_PADDING)        
        elif args.end or args.start:
            # 1 column, we don't care which
            padded_start_time = "%s " % (start_time)
        self.print("%sFlow %s [%s" % (padded_start_time, name, label))

        # inputs
        self._usage(activity_id, prov_doc)
            
        # steps
        have_nested = False
        if args.steps:
            started = _prov_with_attr(prov_doc, ProvStart, activity_id, PROV_ATTR_STARTER)
            steps = map(partial(_prov_attr, PROV_ATTR_ACTIVITY), started)
            for child in steps:
                c_activity = first(prov_doc.get_record(child))
                if args.verbose:
                    self.print(c_activity)

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
                c_id = _simpler_uuid(child.uri)
                c_start_time = args.start and ("%s " % c_start_time or "(unknown start time)     ")
                c_end_time = args.end and "%s " % (c_end_time or TIME_PADDING)
                self.print("%s%sStep %s %s%s%s" % (c_start_time or "", c_end_time or "", c_id, c_provenance and "*" or " ", c_label, c_duration))
                self._usage(child, prov_doc)
                self._generation(child, prov_doc)



        # generated
        self._generation(activity_id, prov_doc)

        if args.verbose and end:
            self.print(end)

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

        self.print("%sFlow %s ]%s%s" % (padded_end_time, name, label, w_duration))

        if self.hints:
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
    with Tool(args) as tool:
        try:
            return tool.main()
        except OSError as e:
            _logger.fatal(e)
            return Status.IO_ERROR

