import subprocess
import sys
import os
from google import genai
from google.genai import types



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional arguments in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to execute the Python file with optional arguments in the specified directory, relative to the working directory.",
            ),
        },
    ),
)



def run_python_file(working_directory, file_path, args=[]):
    work_dir= os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(work_dir, file_path)) 

    if not target_file.startswith(work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
        ["python", target_file] + (args or []),
        cwd=working_directory,
        capture_output=True,
        text=True
    )
        return {"stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out after 30 seconds.'
    except Exception as e:
        return f'Error: executing Python file: {e}'