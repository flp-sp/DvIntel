import os
from dotenv import load_dotenv
from groq import Groq
from memory import messages

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def submit_prompt(user_prompt):
    messages.append({"role":"user","content":user_prompt})

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    response = completion.choices[0].message.content

    messages.append({"role":"assistant","content":response})

    return response