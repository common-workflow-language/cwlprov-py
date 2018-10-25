{
    "class": "Workflow",
    "inputs": [],
    "outputs": [
        {
            "type": "File",
            "outputSource": "#main/step1/file1",
            "id": "#main/file1"
        }
    ],
    "steps": [
        {
            "in": [],
            "out": [
                "#main/step1/file1",
                "#main/step1/file1csv"
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
                        "valueFrom": "echo \"abc\" > f.txt; echo \"3\" > f.txt.size; echo \"a\" > f.txt.firstletter; echo \"a,b,c\" > f.csv; echo \"1,2,3\" > f.csv.columns; echo \"ignored\" > f.txt.ignoreme;\n"
                    }
                ],
                "inputs": [],
                "outputs": [
                    {
                        "type": "File",
                        "outputBinding": {
                            "glob": "f.txt"
                        },
                        "secondaryFiles": [
                            ".size",
                            ".firstletter",
                            "^.csv"
                        ],
                        "id": "#main/step1/7da948a5-da6f-461e-a093-ac36a8fc002e/file1"
                    },
                    {
                        "type": "File",
                        "outputBinding": {
                            "glob": "f.csv"
                        },
                        "secondaryFiles": [
                            ".columns"
                        ],
                        "id": "#main/step1/7da948a5-da6f-461e-a093-ac36a8fc002e/file1csv"
                    }
                ],
                "id": "#main/step1/7da948a5-da6f-461e-a093-ac36a8fc002e"
            },
            "id": "#main/step1"
        }
    ],
    "id": "#main",
    "cwlVersion": "v1.0"
}