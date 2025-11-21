import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be (over)written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Data to be written to the file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):

    target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)
    target_dir = None

    if not (target == abs_work or target.startswith(abs_work + os.sep)):
        print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    else:
        target_dir = os.path.dirname(file_path)

        if not os.path.exists(target_dir) and target_dir != '':
            os.makedirs(os.path.dirname(file_path))

        try:
            with open(target, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        except Exception as e:
            print(f'Error: {e}')
