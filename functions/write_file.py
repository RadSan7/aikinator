import os

def write_file(working_directory, file_path, content):
    work_dir= os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(work_dir, file_path)) 
    print(f"Working directory: {work_dir}")
    print(f"Target file: {target_file}")

    if not target_file.startswith(work_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    try:
        with open(target_file, "w") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing file: {e}'    
    