import os
import hashlib
import json



def scan_directory(directory_path):
    file_data = {}
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as file:
                file_content = file.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            file_size = os.path.getsize(file_path)
            file_data[file_path] = {
                'hash': file_hash,
                'size': file_size
            }
    return file_data



previous_scan_path = 'metadata/previous_scan.json'


if os.path.isfile(previous_scan_path):
    with open(previous_scan_path, 'r') as file:
        previous_scan_data = json.load(file)
else:
    previous_scan_data = {}



directory_path = '/home/anzen/Pictures/wallpaper'
current_scan_data = scan_directory(directory_path)


changed_files = {}
for file_path, current_file_data in current_scan_data.items():
    previous_file_data = previous_scan_data.get(file_path)
    if previous_file_data is None or current_file_data != previous_file_data:
        changed_files[file_path] = current_file_data


#write to complete file data
with open(previous_scan_path, 'w') as file:
    json.dump(current_scan_data, file, indent=4)

#write to changes file data
changes_path = 'metadata/changes.json'
with open(changes_path, 'w') as file:
    json.dump(changed_files, file, indent=4)
