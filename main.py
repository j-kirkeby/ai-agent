import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

if len(sys.argv) not in [2, 3]:
    print("Usage: python3 main.py <prompt> [--verbose]")
    exit(1)
verbose = False
if len(sys.argv) == 3:
    if sys.argv[2] == "--verbose":
        verbose = True
    else:
        print("Usage: python3 main.py <prompt> [--verbose]")

prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]

prompt = sys.argv[1]
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
reply = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
print(reply.text)

if verbose:
    print(f"User prompt: {sys.argv[1]}")
    print(f"Prompt tokens: {reply.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {reply.usage_metadata.candidates_token_count}")