{
    "$graph": [
        {
            "class": "CommandLineTool",
            "inputs": [
                {
                    "type": "File",
                    "secondaryFiles": [
                        ".idx"
                    ],
                    "id": "#sec-tool.cwl/file1"
                }
            ],
            "outputs": [],
            "baseCommand": "true",
            "id": "#sec-tool.cwl"
        },
        {
            "class": "Workflow",
            "inputs": [
                {
                    "type": "File",
                    "secondaryFiles": [
                        ".idx"
                    ],
                    "id": "#main/file1"
                }
            ],
            "outputs": [],
            "steps": [
                {
                    "in": [
                        {
                            "source": "#main/file1",
                            "id": "#main/step1/file1"
                        }
                    ],
                    "out": [],
                    "run": "#sec-tool.cwl",
                    "id": "#main/step1"
                }
            ],
            "id": "#main"
        }
    ],
    "cwlVersion": "v1.0"
}