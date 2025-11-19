import os

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
