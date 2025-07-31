import os

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(abs_working_directory, directory))
    
    if not target_dir.startswith(abs_working_directory):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(target_dir):
        return (f'Error: "{directory}" is not a directory')
    try:
        contents = os.listdir(target_dir)
        list_of_files = []
        for item in contents:
            filepath = os.path.join(target_dir, item)
            list_of_files.append(item + ": file_size=" + str(os.path.getsize(filepath)) + "bytes, is_dir=" + str(os.path.isdir(filepath)))
        return "\n".join(list_of_files)
    except Exception as e:
        return (f'Error listing files {e}')