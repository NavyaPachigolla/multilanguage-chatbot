from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


# ================= BASE CLASS =================

class BaseLLM:

    def generate(self, messages):
        raise NotImplementedError


# ================= GROQ IMPLEMENTATION =================

class GroqLLM(BaseLLM):

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, messages):

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=messages,

            temperature=0
        )

        return response.choices[0].message.content