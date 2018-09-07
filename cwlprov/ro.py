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

import arcp

class ResearchObject:
    def __init__(self, bag):
        bag.validate()
        

        manifest_file = os.path.join(self.folder, "metadata", "manifest.json")
        self.assertTrue(os.path.isfile(manifest_file), "Can't find " + manifest_file)
        arcp_root = self.find_arcp()
        base = urllib.parse.urljoin(arcp_root, "metadata/manifest.json")
        g = Graph()

        # Avoid resolving JSON-LD context https://w3id.org/bundle/context
        # so this test works offline
        context = Path(get_data("tests/bundle-context.jsonld")).as_uri()
        with open(manifest_file, "r", encoding="UTF-8") as f:
            jsonld = f.read()
            # replace with file:/// URI
            jsonld = jsonld.replace("https://w3id.org/bundle/context", context)
        g.parse(data=jsonld, format="json-ld", publicID=base)
