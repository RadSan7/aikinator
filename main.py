import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    function_args = function_call_part.args or {}
    function_args["working_directory"] = "./calculator"
    working_directory = function_args["working_directory"]
    directory = function_args.get("directory")

    function_name = function_call_part.name

    print(function_call_part)
    match function_name:
    
        case "get_files_info":
            result = get_files_info(working_directory,directory)
        case "get_file_content":
            result = get_file_content(working_directory, directory)
        case "run_python_file":
            result = run_python_file(working_directory, directory)
        case "write_file":
            result = write_file(working_directory, directory, function_args.get("content", ""))
        case _:
            print("test error")
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": result},
        )
    ],
)



def main():
        # Allow passing prompt from terminal (e.g., ai "your question")
    args = sys.argv[1:]
    verbose = False

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    prompt = " ".join(args)
    system_prompt = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file content
- Execute Python files with optional arguments
- Write or overwrite files
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    function_call_part = None
    for part in response.candidates[0].content.parts:
        if part.function_call is not None:
            function_call_part = part.function_call
            break
    
    function_result = call_function(function_call_part, verbose)
    if function_result.parts[0].function_response:
        if verbose:
            print(f"-> {function_result.parts[0].function_response.response}")    
    else:
        raise ValueError("Function call did not return a valid response.")
    
main()