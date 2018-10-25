#!/usr/bin/env python

# © Copyright 2018 Software Freedom Conservancy (SFC)
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

__author__      = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__   = "© 2018 Software Freedom Conservancy (SFC)"
__license__     = "Apache License, version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>"

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

import cwlprov

setup(
  name = 'cwlprov',
  packages = find_packages(exclude=['contrib', 'docs', 'tests']), # Required
  version = cwlprov.__version__,
  description = 'cwlprov API for Python',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Stian Soiland-Reyes',
  author_email = 'stain@apache.org',
  include_package_data=True,
  # https://www.apache.org/licenses/LICENSE-2.0
  license = "Apache License, Version 2.0",
  url = 'https://github.com/common-workflow-language/cwlprov-py',
#  download_url = 'https://github.com/stain/arcp-py/archive/0.1.0.tar.gz',
  keywords = "cwl prov cwlprov provenance",
  
  install_requires=[
          'prov >= 1.5.1',
          'bdbag >= 1.4.1',
          #'bagit >= 1.6.4', # Transitive from bdbag
          'arcp >= 0.2.0',
          'rdflib-jsonld >= 0.4.0',
          'rdflib >= 4.2.2',        
  ],
  tests_require=['pytest'],
  entry_points={
      'console_scripts': ["cwlprov=cwlprov.tool:main"]
  },
  python_requires='>=3.6, <4',
  classifiers=[
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'Development Status :: 2 - Pre-Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
     # 'License :: OSI Approved :: Apache Software License',
     # https://github.com/pypa/pypi-legacy/issues/564
    #'License :: OSI Approved',
    # 'License :: OSI Approved :: Apache License, Version 2.0 (Apache-2.0)',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet',
    'Topic :: System :: Archiving :: Packaging',
],
  
)
