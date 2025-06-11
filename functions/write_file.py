import os

def write_file(working_directory, file_path, content):
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        work_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"

    if not path.startswith(work_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except Exception as e:
            return f"Error: {e}"
    
    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'