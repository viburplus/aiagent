import os
import subprocess

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
        try:
            complProc = subprocess.run(["python", target]+args, text=True, capture_output=True, cwd=abs_work, timeout=30)

        except Exception as e:
            return f"Error: executing Python file: {e}"

        if not complProc.stdout:
            return "No output produced."

        retVal = f"STDOUT:{complProc.stdout} STDERR:{complProc.stderr}"

        if complProc.returncode != 0:
            retVal += f" Process exited with code {complProc.returncode}"

        return retVal

