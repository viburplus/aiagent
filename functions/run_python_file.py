import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional arguments to the executed file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):

    target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)

    if not target.startswith(abs_work):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    elif not os.path.exists(target):
        return f'Error: File "{file_path}" not found.'

    elif not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    else:

        output = []

        try:
            complProc = subprocess.run(["python", target]+args, text=True, capture_output=True, cwd=abs_work, timeout=30)

        except Exception as e:
            return f"Error: executing Python file: {e}"
        
        print("DEBUG:", repr(complProc.stdout), repr(complProc.stderr))

        if complProc.stdout:
            output.append(f"STDOUT:{complProc.stdout}")
        if complProc.stderr:
            output.append(f"STDERR:{complProc.stderr}")
        if complProc.returncode != 0:
            output.append(f" Process exited with code {complProc.returncode}")

        return " ".join(output) if output else "No output produced"