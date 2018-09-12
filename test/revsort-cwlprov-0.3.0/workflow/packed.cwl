{
    "$graph": [
        {
            "class": "Workflow",
            "inputs": [
                {
                    "type": "string",
                    "id": "#1st-workflow.cwl/ex"
                },
                {
                    "type": "File",
                    "id": "#1st-workflow.cwl/inp"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#1st-workflow.cwl/argument/classfile",
                    "id": "#1st-workflow.cwl/classout"
                }
            ],
            "steps": [
                {
                    "run": "#arguments.cwl",
                    "in": [
                        {
                            "source": "#1st-workflow.cwl/untar/example_out",
                            "id": "#1st-workflow.cwl/argument/src"
                        }
                    ],
                    "out": [
                        "#1st-workflow.cwl/argument/classfile"
                    ],
                    "id": "#1st-workflow.cwl/argument"
                },
                {
                    "run": "#tar-param.cwl",
                    "in": [
                        {
                            "source": "#1st-workflow.cwl/ex",
                            "id": "#1st-workflow.cwl/untar/extractfile"
                        },
                        {
                            "source": "#1st-workflow.cwl/inp",
                            "id": "#1st-workflow.cwl/untar/tarfile"
                        }
                    ],
                    "out": [
                        "#1st-workflow.cwl/untar/example_out"
                    ],
                    "id": "#1st-workflow.cwl/untar"
                }
            ],
            "id": "#1st-workflow.cwl"
        },
        {
            "class": "CommandLineTool",
            "label": "Example trivial wrapper for Java 9 compiler",
            "hints": [
                {
                    "dockerPull": "openjdk:9.0.1-11-slim",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": "javac",
            "arguments": [
                "-d",
                "$(runtime.outdir)"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#arguments.cwl/src"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.class"
                    },
                    "id": "#arguments.cwl/classfile"
                }
            ],
            "id": "#arguments.cwl"
        },
        {
            "class": "Workflow",
            "label": "Nested workflow example",
            "inputs": [],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/compile/classout",
                    "id": "#main/classout"
                }
            ],
            "requirements": [
                {
                    "class": "SubworkflowFeatureRequirement"
                }
            ],
            "steps": [
                {
                    "run": "#1st-workflow.cwl",
                    "in": [
                        {
                            "default": "Hello.java",
                            "id": "#main/compile/ex"
                        },
                        {
                            "source": "#main/create-tar/tar",
                            "id": "#main/compile/inp"
                        }
                    ],
                    "out": [
                        "#main/compile/classout"
                    ],
                    "id": "#main/compile"
                },
                {
                    "requirements": [
                        {
                            "class": "InitialWorkDirRequirement",
                            "listing": [
                                {
                                    "entryname": "Hello.java",
                                    "entry": "public class Hello {\n  public static void main(String[] argv) {\n      System.out.println(\"Hello from Java\");\n  }\n}\n"
                                }
                            ]
                        }
                    ],
                    "in": [],
                    "out": [
                        "#main/create-tar/tar"
                    ],
                    "run": {
                        "class": "CommandLineTool",
                        "requirements": [
                            {
                                "class": "ShellCommandRequirement"
                            }
                        ],
                        "arguments": [
                            {
                                "shellQuote": false,
                                "valueFrom": "date\ntar cf hello.tar Hello.java\ndate\n"
                            }
                        ],
                        "inputs": [],
                        "outputs": [
                            {
                                "type": "File",
                                "outputBinding": {
                                    "glob": "hello.tar"
                                },
                                "id": "#main/create-tar/b3a0a50c-d4ea-4990-8d21-517e19551d72/tar"
                            }
                        ],
                        "id": "#main/create-tar/b3a0a50c-d4ea-4990-8d21-517e19551d72"
                    },
                    "id": "#main/create-tar"
                }
            ],
            "id": "#main"
        },
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "tar",
                "xf"
            ],
            "inputs": [
                {
                    "type": "string",
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#tar-param.cwl/extractfile"
                },
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#tar-param.cwl/tarfile"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "$(inputs.extractfile)"
                    },
                    "id": "#tar-param.cwl/example_out"
                }
            ],
            "id": "#tar-param.cwl"
        }
    ],
    "cwlVersion": "v1.0"
}