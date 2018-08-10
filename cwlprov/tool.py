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

from enum import IntEnum


class Status(IntEnum):
    """Exit codes from main()"""
    OK = 0
    INVALID = 1 

def parse_args(args):
    parser = argparse.ArgumentParser(description='cwlprov')
    parser.add_argument("ro", 
        help="Path to CWLProv Research Object folder")
    parser.add_argument("--validate", 
        help="Validate CWLProv RO", action="store_true")
    return parser.parse_args(args)

def main(*args):
    # type: (...) -> None
    """cwlprov command line tool"""
    args = parse_args(args)
    
    bag = bagit.Bag(args.ro)    
    # Always do a minimal validation, but
    # will also test checksum on --validate
    valid = bag.validate(fast=args.validate)
    if args.validate:
        return valid : Status.OK ? Status.INVALID
    


    # Probably went fine if we made it to here        
    return Status.OK

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))

