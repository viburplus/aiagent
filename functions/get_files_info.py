import os
import sys
from google.genai import types

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

def get_files_info(working_directory, directory="."):

    full_path = os.path.abspath(os.path.join(working_directory, directory))
    abs_working = os.path.abspath(working_directory)

    contents = ""
    size = 0

    if not (full_path == abs_working or full_path.startswith(abs_working + os.sep)):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n')
    elif not os.path.isdir(full_path):
        print(f'Error: "{directory}" is not a directory\n')
    else:
        if directory == ".":
            contents = "Result for current directory:\n"
        else:
            contents = f"Result for '{directory}' directory:\n"

        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            try:
                size = os.path.getsize(entry_path)
            except Exception as e:
                print(f'Error: {e}')

            contents += f"- {entry}: file_size={size}, is_dir={is_dir}\n"

    return contents

