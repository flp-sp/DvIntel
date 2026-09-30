from datetime import datetime
import json
from memory import Memory

class Tools:
    def get_date():
        return datetime.now()

    def read_file(path: str):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(path: str, content: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Arquivo '{path}' salvo com sucesso ({len(content)} caracteres)."

    AVAILABLE_FUNTIONS = {
        "get_date":get_date,
        "read_file":read_file,
        "write_file":write_file
    }

    TOOLS = [
        {
        "type":"function",
        "function":{
            "name":"get_date",
            "description":"Get current date and time",
            "parameters":{
                "type":"object",
                "properties":{
                    "date":{
                        "type":"string",
                        "description":"Date and time, e.g. 2026-09-30 09:18:50.102243"
                    }
                },
                "required":[]
            }
        }
        },
        {
            "type":"function",
            "function":{
                "name":"read_file",
                "description":"Read a file by the given path file",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "path":{
                            "type":"string",
                            "description":"File path to be read"
                        }
                    },
                    "required":["path"]
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"write_file",
                "description":"Write a file on the given path file",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "path":{
                            "type":"string",
                            "description":"File path to be write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Full content to be writen on the file."
                        }
                    },
                    "required":["path", "content"]
                }
            }
        }

    ]

    def __init__(self):
        pass

    def tool_calls_request(self, tool_calls):
        memory_controller = Memory()
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.AVAILABLE_FUNTIONS[function_name]

            if tool_call.function.arguments:
                args = tool_call.function.arguments
                args = json.loads(args)
            else:
                {}

            function_output = function_to_call(**args)
            memory_controller.salvar("tool", str(function_output), tool_call.id, function_name)


    def get_tools(self):
        return self.TOOLS