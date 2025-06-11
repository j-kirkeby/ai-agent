import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        work_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"

    if not path.startswith(work_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    args = ["python3", path]
    try: 
        process = subprocess.run(args, timeout=30, capture_output=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    out = ""
    out += f"STDOUT: {process.stdout}\n"
    out += f"STDERR: {process.stderr}\n"
    if process.returncode != 0:
        out += f"Process exited with code {process.returncode}\n"
    if len(out) == 0:
        return "No output produced"
    return out
    