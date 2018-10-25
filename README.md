# CWLProv Python tool

The `cwlprov` Python tool is a command line interface to validate and inspect 
[CWLProv](https://w3id.org/cwl/prov) Research Objects that capture workflow runs,
typically executed in a [Common Workflow Language](https://www.commonwl.org/)
implementation.

## Installation

You'll need [Python 3](https://www.python.org/downloads/).

To install from [pip](https://pypi.org/project/cwlprov/) try:

    pip3 install cwlprov

If you would rather install from the checkout of this source code:

    pip3 install .

## Usage

Use `cwlprov --help`  to see all options. For instance `cwlprov validate` will validate the folder is valid according to CWLProv.

The [test/](test/) folder contains some examples of workflow runs for different CWLProv profiles.


## License

This repository is distributed under [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0) 

See the file [LICENSE.txt](LICENSE.txt) for details, and [NOTICE](NOTICE) for required notices.

SPDX-License-Identifier: Apache-2.0

## Contributing

cwlprov.py is maintained at https://github.com/common-workflow-language/cwlprov-py/ by the [Common Workflow Language](https://www.commonwl.org/) project.

Feel free to raise an
[issue](https://github.com/common-workflow-language/cwlprov-py/issues) or a
[pull request](https://github.com/common-workflow-language/cwlprov-py/pulls) to
contribute to CWLProv. Contributions are assumed to be covered by 
[section 5 of the Apache License](https://www.apache.org/licenses/LICENSE-2.0#contributions).

For an informal CWLProv discussion with other developers, join the (relatively
quiet) Gitter room
[common-workflow-language/cwlprov](https://gitter.im/common-workflow-language/cwlprov),
or the (more busy)
[common-workflow-language/common-workflow-language](https://gitter.im/common-workflow-language/common-workflow-language).


### Code of Conduct

The CWL Project is dedicated to providing a harassment-free experience for
everyone, regardless of gender, gender identity and expression, sexual
orientation, disability, physical appearance, body size, age, race, or
religion. We do not tolerate harassment of participants in any form. This code
of conduct applies to all CWL Project spaces, including the Google Group, the
Gitter chat room, the Google Hangouts chats, both online and off. Anyone who
violates this code of conduct may be sanctioned or expelled from these spaces
at the discretion of the leadership team.

For more details, see our 
[Code of Conduct](https://github.com/common-workflow-language/common-workflow-language/blob/master/CODE_OF_CONDUCT.md).

