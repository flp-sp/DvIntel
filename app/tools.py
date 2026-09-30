from datetime import datetime
from memory import Memory

class Tools:
    def get_date():
        return datetime.now()

    AVAILABLE_FUNTIONS = {
        "get_date":get_date()
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
        }    
    ]

    def __init__(self):
        pass

    def tool_calls_request(self, tool_calls):
        memory_controller = Memory()
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_output = self.AVAILABLE_FUNTIONS[function_name]
            memory_controller.salvar("tool", str(function_output), tool_call.id, function_name)


    def get_tools(self):
        return self.TOOLS