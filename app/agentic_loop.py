import os
from dotenv import load_dotenv
from groq import Groq
from memory import Memory

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

memory_controller = Memory()

def submit_prompt(user_prompt):
    #messages.append({"role":"user","content":user_prompt})
    memory_controller.salvar("user",user_prompt)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=Memory.get_context()
    )

    response = completion.choices[0].message.content

    #messages.append({"role":"assistant","content":response})
    memory_controller.salvar("assistant", response)

    return response