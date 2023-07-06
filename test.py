import os

def create_folders_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directories: {directory}")
    else:
        print(f"Directories already exist: {directory}")

# Example usage
file_path = "/home/anzen/Music/new_file/newer_file/newest_file/"
create_folders_if_not_exists(file_path)

