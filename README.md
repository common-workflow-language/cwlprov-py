# CWLProv Python tool

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1471375.svg)](https://doi.org/10.5281/zenodo.1471375)

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

If you would like to use the `cwltool rerun` feature you may also need:

    pip3 install cwlref-runner 


## Development

To develop cwlprov-py it is recommended to set up a new [virtualenv](https://docs.python.org/3/library/venv.html):

    virtualenv -p python3 venv

To activate the environment and install your development version of cwlprov:

    . venv3/bin/activate
    pip3 install .


## Usage

Use `cwlprov --help`  to see all options. For instance `cwlprov validate` will validate the folder is valid according to CWLProv.

    $ cwlprov --help
    usage: cwlprov [-h] [--version] [--directory DIRECTORY] [--relative]
                [--absolute] [--output OUTPUT] [--verbose] [--quiet] [--hints]
                [--no-hints]
                {validate,info,who,prov,inputs,outputs,run,runs,rerun,derived,runtimes}
                ...

    cwlprov explores Research Objects containing provenance of Common Workflow
    Language executions. <https://w3id.org/cwl/prov/>

    optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    --directory DIRECTORY, -d DIRECTORY
                            Path to CWLProv Research Object (default: .)
    --relative            Output paths relative to current directory (default if
                            -d is missing or relative)
    --absolute            Output absolute paths (default if -d is absolute)
    --output OUTPUT, -o OUTPUT
                            File to write output to (default: stdout)
    --verbose, -v         Verbose logging (repeat for more verbose)
    --quiet, -q           No logging or hints
    --hints               Show hints on cwlprov usage
    --no-hints            Do not show hints

    commands:
    {validate,info,who,prov,inputs,outputs,run,runs,rerun,derived,runtimes}
        validate            validate the CWLProv Research Object
        info                show research object metadata
        who                 show who ran the workflow
        prov                export workflow execution provenance in PROV format
        inputs              list workflow/step input files/values
        outputs             list workflow/step output files/values
        run                 show workflow execution log
        runs                List all workflow executions in RO
        rerun               Rerun a workflow or step
        derived             List what was derived from a data item, based on
                            activity usage/generation
        runtimes            Calculate average step execution runtimes

The [test/](test/) folder contains some examples of workflow runs for different CWLProv profiles.

All commands for `cwlprov` will attempt to detect the CWLProv research object from the current directory, alternatively take the `--directory` option to specify the root folder.

The `--quiet` option may be used in scripts for less verbose outputs. The `--verbose` option has the opposite affect to enable logging. For debug logging, use `-vv` or `--verbose --verbose`.

Note that the general arguments listed above must be provided *before* the _command_, e.g. 

    cwlprov --quiet --directory /tmp/1 validate

Many of the commands accept additional arguments, which can be accessed by `cwlprov COMMAND --help`, e.g.:

    $ cwlprov run --help
    usage: cwlprov run [-h] [--step STEP] [--steps] [--no-steps] [--start]
                    [--no-start] [--end] [--no-end] [--duration]
                    [--no-duration] [--labels] [--no-labels] [--inputs]
                    [--outputs]
                    [id]

    positional arguments:
    id                    workflow run UUID

    optional arguments:
    -h, --help            show this help message and exit
    --step STEP, -s STEP  Show only step with given UUID
    --steps               List steps of workflow
    --no-steps            Do not list steps
    --start               Show start timestamps (default)
    --no-start, -S        Do not show start timestamps
    --end, -e             Show end timestamps
    --no-end              Do not show end timestamps
    --duration            Show step duration (default)
    --no-duration, -D     Do not show step duration
    --labels              Show activity labels
    --no-labels, -L       Do not show activity labels
    --inputs, -i          Show inputs
    --outputs, -o         Show outputs

### Validation

Running `cwlprov` with no commands will return with status 0 if a CWLProv folder structure is detected:

    $ cd test/revsort-cwlprov-0.4.0
    test/revsort-cwlprov-0.4.0$ cwlprov 
    Detected CWLProv Research Object: /home/stain/src/cwlprov-py/test/revsort-cwlprov-0.4.0

    $ cd /tmp
    /tmp$ cwlprov
    ERROR:cwlprov.tool:Could not find bagit.txt, try cwlprov -d mybag/

If a cwlprov is not detected or invalid, an error code is raised.

    cwlprov && echo Do cwlprov-stuff
    ERROR:cwlprov.tool:Could not find bagit.txt, try cwlprov -d mybag/

Combined with the `--quiet` option `cwlprov` can be useful to find the root of a CWLProv folder:

    test/revsort-cwlprov-0.4.0/metadata/provenance$ cwlprov -q
    /home/stain/src/cwlprov-py/test/revsort-cwlprov-0.4.0

All commands of `cwlprov` will by default perform a _quick validation_, which conforms all files are present in the correct file size. For instance, if we remove a file:
    
    test/revsort-cwlprov-0.4.0$ rm data/32/327fc7aedf4f6b69a42a7c8b808dc5a7aff61376 

    test/revsort-cwlprov-0.4.0$ cwlprov 
    ERROR:cwlprov.tool:BagIt validation failed for: /home/stain/src/cwlprov-py/test/revsort-cwlprov-0.4.0: Payload-Oxum validation failed. Expected 3 files and 3333 bytes but found 2 files and 2222 bytes

To perform full validation, use `cwlprov validate`:

    test/revsort-cwlprov-0.4.0$ cwlprov validate 
    WARNING:bdbag.bdbagit:data/32/327fc7aedf4f6b69a42a7c8b808dc5a7aff61376 exists in manifest but was not found on filesystem
    ERROR:cwlprov.tool:BagIt validation failed for: /home/stain/src/cwlprov-py/test/revsort-cwlprov-0.4.0: Bag validation failed: data/32/327fc7aedf4f6b69a42a7c8b808dc5a7aff61376 exists in manifest but was not found on filesystem

    test/revsort-cwlprov-0.4.0$ git checkout . 

    test/revsort-cwlprov-0.4.0$ cwlprov validate
    Valid CWLProv RO: .

Unlike the quick validation, `cwlprov validate` will confirm checksums on all files, and thus detect byte-level changes. For instance, let's pretend `I` has been replaced with lower case `i` in a data file:

    test/revsort-cwlprov-0.4.0$ sed -i 's/I/i/g' data/32/327fc7aedf4f6b69a42a7c8b808dc5a7aff61376
    test/revsort-cwlprov-0.4.0$ cwlprov 
    Detected CWLProv Research Object: /home/stain/src/cwlprov-py/test/revsort-cwlprov-0.4.0

    test/revsort-cwlprov-0.4.0$ cwlprov validate
    WARNING:bdbag.bdbagit:data/32/327fc7aedf4f6b69a42a7c8b808dc5a7aff61376 sha1 validation failed: expected="327fc7aedf4f6b69a42a7c8b808dc5a7aff61376" found="60c41d3758bc8b03e78db07bc0f17d1804d2662d"
    ERROR:cwlprov.tool:BagIt validation failed for: /home/stain/src/cwlprov-py/test/revsort-cwlprov-0.4.0: Bag validation failed: data/32/327fc7aedf4f6b69a42a7c8b808dc5a7aff61376 sha1 validation failed: expected="327fc7aedf4f6b69a42a7c8b808dc5a7aff61376" found="60c41d3758bc8b03e78db07bc0f17d1804d2662d"

### Research Object information

The `cwlprov info` command gives high-level information about the research object and its identifiers.

    test/revsort-cwlprov-0.4.0$ cwlprov info
    Research Object of CWL workflow run
    Research Object ID: arcp://uuid,d47d3d43-4830-44f0-aa32-4cda74849c63/
    Profile: https://w3id.org/cwl/prov/0.4.0
    Workflow run ID: urn:uuid:d47d3d43-4830-44f0-aa32-4cda74849c63
    Packaged: 2018-08-21

The `Profile` indicates the version of the CWLProv the research object implements, 
which determine which features of a workflow run is represented.

Note that a warning will be printed if an unknown CWLProv version is detected:

    $ cwlprov
    WARNING:cwlprov.tool:Unsupported CWLProv version: {'https://w3id.org/cwl/prov/0.8.0'}
    Supported profiles:
    https://w3id.org/cwl/prov/0.6.0
    https://w3id.org/cwl/prov/0.5.0
    https://w3id.org/cwl/prov/0.4.0
    https://w3id.org/cwl/prov/0.3.0

This typically means that cwlprov-py is outdated, although that is normally harmless. Try `pip install --upgrade cwlprov` 

The `cwlprov who` command will try to determine the user that ran the workflow.

    $ cwlprov who
    Packaged By: cwltool 1.0.20180925133620 <urn:uuid:d9c16ea5-c3fd-4c56-b125-f3a5207e6c38>
    Executed By: Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>

_Note that for privacy concerns, CWL executors like [cwltool](https://github.com/common-workflow-language/cwltool)
would not log such user information unless this has been enabled with options like `--orcid` `--full-name` or `--enable-user-provenance`._

### Workflow run

To list the step executions of a workflow use `cwlprov run`:

    test/revsort-cwlprov-0.4.0$ cwlprov run
    2018-08-21 17:26:24.467844 Flow d47d3d43-4830-44f0-aa32-4cda74849c63 [ Run of workflow/packed.cwl#main 
    2018-08-21 17:26:24.530884 Step 6f501717-0c97-492e-b18a-10bc096f1797   Run of workflow/packed.cwl#main/rev  (0:00:01.122498)
    2018-08-21 17:26:25.656084 Step e7c8b2c0-dee6-4c61-b674-f0807cb47344   Run of workflow/packed.cwl#main/sorted  (0:00:01.087999)
    2018-08-21 17:26:26.752493 Flow d47d3d43-4830-44f0-aa32-4cda74849c63 ] Run of workflow/packed.cwl#main  (0:00:02.284649)
    Legend:
    [ Workflow start
    ] Workflow end

The listing can be customized, see `cwlprov run --help` for details. For example:

    test/revsort-cwlprov-0.4.0$ cwlprov --no-hints run --no-labels --start --end --no-duration 
    2018-08-21 17:26:24.467844                            Flow d47d3d43-4830-44f0-aa32-4cda74849c63 [
    2018-08-21 17:26:24.530884 2018-08-21 17:26:25.653382 Step 6f501717-0c97-492e-b18a-10bc096f1797  
    2018-08-21 17:26:25.656084 2018-08-21 17:26:26.744083 Step e7c8b2c0-dee6-4c61-b674-f0807cb47344  
                               2018-08-21 17:26:26.752493 Flow d47d3d43-4830-44f0-aa32-4cda74849c63 ]

### Nested workflows

Nested workflows, steps that themselves are workflows, are indicated in `cwlprov run` with a `*`:

    (venv3) stain@biggie:~/src/cwlprov-py/test/nested-cwlprov-0.3.0$ cwlprov run
    2018-08-08 22:44:06.573330 Flow 39408a40-c1c8-4852-9747-87249425be1e [ Run of workflow/packed.cwl#main 
    2018-08-08 22:44:06.691722 Step 4f082fb6-3e4d-4a21-82e3-c685ce3deb58   Run of workflow/packed.cwl#main/create-tar  (0:00:00.010133)
    2018-08-08 22:44:06.702976 Step 0cceeaf6-4109-4f08-940b-f06ac959944a * Run of workflow/packed.cwl#main/compile  (unknown duration)
    2018-08-08 22:44:12.680097 Flow 39408a40-c1c8-4852-9747-87249425be1e ] Run of workflow/packed.cwl#main  (0:00:06.106767)
    Legend:
    [ Workflow start
    * Nested provenance, use UUID to explore: cwlprov run 0cceeaf6-4109-4f08-940b-f06ac959944a
    ] Workflow end

    (venv3) stain@biggie:~/src/cwlprov-py/test/nested-cwlprov-0.3.0$ cwlprov run 0cceeaf6-4109-4f08-940b-f06ac959944a
    2018-08-08 22:44:06.607210 Flow 0cceeaf6-4109-4f08-940b-f06ac959944a [ Run of workflow/packed.cwl#main 
    2018-08-08 22:44:06.707070 Step 83752ab4-8227-4d4a-8baa-78376df34aed   Run of workflow/packed.cwl#main/untar  (0:00:00.008149)
    2018-08-08 22:44:06.718554 Step f56d8478-a190-4251-84d9-7f69fe0f6f8b   Run of workflow/packed.cwl#main/argument  (0:00:00.532052)
    2018-08-08 22:44:07.251588 Flow 0cceeaf6-4109-4f08-940b-f06ac959944a ] Run of workflow/packed.cwl#main  (0:00:00.644378)
    Legend:
    [ Workflow start
    ] Workflow end

_Note that there is a bug in CWLProv 0.3.0 logging shown above; steps of nested workflows are misleadingly labeled under `#main`_

You can list all workflow runs (including nested workflow runs) with `cwlprov runs`:

    test/nested-cwlprov-0.3.0$ cwlprov runs
    39408a40-c1c8-4852-9747-87249425be1e * Run of workflow/packed.cwl#main
    0cceeaf6-4109-4f08-940b-f06ac959944a   Run of workflow/packed.cwl#main
    Legend:
    * master workflow

To explore the nested workflow run with other commands you may have to provide the run UUID with `--run` argument, e.g. 

    test/nested-cwlprov-0.3.0$ cwlprov outputs --format=files --run 0cceeaf6-4109-4f08-940b-f06ac959944a 83752ab4-8227-4d4a-8baa-78376df34aed
    Output example_out:
    data/93/93035905e94e150874f5a881d39f3c5c6378dd38



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

