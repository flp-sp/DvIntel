import os
from dotenv import load_dotenv
from groq import Groq
from memory import Memory
from tools import Tools

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

is_tool_called = True

memory_controller = Memory()
tools_handdler = Tools()

while is_tool_called:
    def submit_prompt(user_prompt):
        memory_controller.salvar("user",user_prompt)

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=Memory.get_context(),
            tools=tools_handdler.get_tools(),
            tool_choice="auto"
        )

        response = completion.choices[0].message

        if response.tool_calls:
            tools_handdler.tool_calls_request(response.tool_calls)
        else:
            is_tool_called = False

        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=Memory.get_context()
        )

        memory_controller.salvar("assistant", final_response.choices[0].message.content)
        return final_response.choices[0].message.content