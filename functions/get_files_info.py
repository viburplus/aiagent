import os
import sys

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

