import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.call_function import call_function

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
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If you are asked for files in the root folder please call the function with "." as a parameter.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content", 
    description="Gets the content of a file (truncated if longer than 10000 characters), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get content from, relative to the working directory."
            ),
        }
    )
)
schema_write_file = types.FunctionDeclaration(
    name="write_file", 
    description="Writes content to a file, creates the folders along the path if they don't already exist. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get content from, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            )
        }
    )
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file", 
    description="Runs an existing python file (must end in .py). Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run, relative to the working directory."
            ),
        }
    )
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

prompt = sys.argv[1]
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Main loop
turn = 0
reply = ""
while turn < 20:

    reply = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    for cand in reply.candidates:
        messages.append(cand.content)

    if not reply.function_calls is None:
        for call in reply.function_calls:
            try:
                result = call_function(call, verbose)
                messages.append(result)
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")
            except Exception as e:
                raise Exception(f"Error: {e}")
    else:
        break
    
    """
    if verbose:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {reply.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {reply.usage_metadata.candidates_token_count}")
    """

    turn += 1

print(f"Final response:\n{reply.text}")