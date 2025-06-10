import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."
    
    path = None
    try: 
        path = os.path.abspath(f"{working_directory}/{directory}")
    except:
        return f'Error: cannot find absolute path for "{working_directory}/{directory}"'

    work_path = os.path.abspath(working_directory)
    if not path.startswith(work_path):
        return f'Error: "{path}" not in working directory "{work_path}"'
    dir = []
    try: 
        dir = os.listdir(path)
    except Exception as e:
        return f'Error: unable to list directory "{path}"'

    out = ""
    for file in dir:
        try:
            file_size = os.path.getsize(os.path.join(path, file))
            is_dir = os.path.isdir(os.path.join(path, file))
            out += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
        except:
            return f'Error: unable to get file info for "{file}"'
    
    return out

