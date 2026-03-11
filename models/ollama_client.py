import os
import requests
from dotenv import load_dotenv

load_dotenv()


class LLM:

    def invoke(self, prompt):

        response = requests.post(
            os.getenv("OLLAMA_BASE_URL"),
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
        )

        return response.json()["response"]


llm = LLM()


"""
This code defines a very small wrapper around an LLM API (Ollama) 
so your agents can call a language model using a simple method: llm.invoke(prompt).

Essentially it does:

Prompt → HTTP request → Ollama → Llama model → response text


1.
requests - A Python HTTP client used to send API requests.It sends an HTTP POST request to a server.

In this case the server is Ollama running locally.


2. Define the LLM Class
This class acts as a wrapper for the LLM API.

Instead of writing HTTP calls everywhere, your agents can simply do:

llm.invoke(prompt)
This is a clean abstraction.


3. The invoke Method

def invoke(self, prompt):

This function takes a prompt string.

Example:
prompt = "Explain this Python code"

4. Send Request to Ollama


5. Create LLM Instance
llm = LLM()

This creates a global LLM client.

Now anywhere in your project you can do:

from llm import llm

result = llm.invoke("Explain this code")


Agent → prompt → LLM wrapper → Ollama → Llama model → result
"""
