import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

    file_contents = ""

    target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)

    if not (target == abs_work or target.startswith(abs_work + os.sep)):
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n')
    elif not os.path.isfile(target):
        print(f'Error: File not found or is not a regular file: "{file_path}"')
    else:
        with open(target, "r") as f:
            file_contents = f.read(MAX_CHARS)

        if os.path.getsize(target) > MAX_CHARS:
            file_contents += f'[...File "{file_path}" truncated at 10000 characters]'

    return file_contents
