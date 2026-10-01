import os
import json
from pathlib import Path
from core import append_jsonl

MEMORY_DIR = Path("memory")
MEMORY_FILE = MEMORY_DIR / "memory.jsonl"

class Memory:
    def __init__(self):
        MEMORY_DIR.mkdir(exist_ok=True)
        if not MEMORY_FILE.exists():
            MEMORY_FILE.touch()
            self.salvar("system", "You're an AI agent, you'll be able to change code and using tools.")

    def salvar(self, role, content, tool_call_id=None, name=None):
        entry = {
            "role":role,
            "content":content
            }
        if role == "tool" and (tool_call_id is not None and name is not None):
            entry["tool_call_id"] = tool_call_id
            entry["name"] = name

        append_jsonl(MEMORY_FILE, entry)
             

    def compactar():
        pass

    def get_context(self):
        data = []
        with open (MEMORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
        return data