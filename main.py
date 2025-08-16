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

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]

    iters = 0

    while True:
        iters += 1
        if iters > 20:
            print(f"Maximum iterations 20 reached.")
            sys.exit(1)

        try:
            final_response = generate_content(messages, available_functions, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
 
    



def generate_content(messages, available_functions, verbose):
    system_prompt = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file content
- Execute Python files with optional arguments
- Write or overwrite files
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses)) 




main()

