import os
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="THe directory to read the file from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(working_directory)
    print(f"Working directory: {full_path}")
    target_file = os.path.abspath(os.path.join(full_path, file_path))
    print(f"Target file: {target_file}")
    if not target_file.startswith(full_path):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        max_chars = 10000
        with open(target_file, "r") as file:
            file_content_string = file.read(max_chars)
            if len(file.read()) > max_chars:
                file_content_string += (f'[...File "{file_path}" truncated at 10000 characters]')
    
        return file_content_string
    except Exception as e:
        return f'Error: reading file: {e}'