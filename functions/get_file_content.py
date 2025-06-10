import os

def get_file_content(working_directory, file_path):
    path = ""
    work_path= ""

    try:
        work_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
    except Exception as e:
        return f"Error: {e}"
    
    if not path.startswith(work_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    out = ""
    try:
        f = open(path)
        out = f.read(10_000)
    except Exception as e:
        return f"Error: {e}"
    
    if len(out) >= 10_000:
        out += f'[...File "{file_path}" truncated at 10000 characters]'
    return out