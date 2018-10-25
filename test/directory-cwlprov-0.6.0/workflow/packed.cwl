{
    "class": "Workflow",
    "doc": "Inspect provided directory and return filenames. Generate a new directory and return it (including content).\n",
    "hints": [
        {
            "class": "DockerRequirement",
            "dockerPull": "debian:8"
        }
    ],
    "inputs": [
        {
            "type": "Directory",
            "id": "#main/dir"
        }
    ],
    "steps": [
        {
            "in": [],
            "out": [
                "#main/generate/dir1"
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
                        "valueFrom": "pwd; mkdir -p dir1/a/b; echo -n a > dir1/a.txt; echo -n b > dir1/a/b.txt; echo -n c > dir1/a/b/c.txt;\n"
                    }
                ],
                "inputs": [],
                "outputs": [
                    {
                        "type": "Directory",
                        "outputBinding": {
                            "glob": "dir1"
                        },
                        "id": "#main/generate/0b68f68e-488a-4766-be96-41b807df9666/dir1"
                    }
                ],
                "id": "#main/generate/0b68f68e-488a-4766-be96-41b807df9666"
            },
            "id": "#main/generate"
        },
        {
            "in": [
                {
                    "source": "#main/dir",
                    "id": "#main/ls/dir"
                }
            ],
            "out": [
                "#main/ls/listing"
            ],
            "run": {
                "class": "CommandLineTool",
                "baseCommand": "ls",
                "inputs": [
                    {
                        "type": "Directory",
                        "inputBinding": {
                            "position": 1
                        },
                        "id": "#main/ls/6e0c2dd0-9bcc-42f5-b5ed-4b76d54a0b37/dir"
                    }
                ],
                "outputs": [
                    {
                        "type": "File",
                        "id": "#main/ls/6e0c2dd0-9bcc-42f5-b5ed-4b76d54a0b37/listing",
                        "outputBinding": {
                            "glob": "97c2d154cd3eb14c5554f6051e9c236c7fdb128a"
                        }
                    }
                ],
                "id": "#main/ls/6e0c2dd0-9bcc-42f5-b5ed-4b76d54a0b37",
                "stdout": "97c2d154cd3eb14c5554f6051e9c236c7fdb128a"
            },
            "id": "#main/ls"
        }
    ],
    "outputs": [
        {
            "type": "Directory",
            "outputSource": "#main/generate/dir1",
            "id": "#main/dir1"
        },
        {
            "type": "File",
            "outputSource": "#main/ls/listing",
            "id": "#main/listing"
        }
    ],
    "id": "#main",
    "cwlVersion": "v1.0"
}