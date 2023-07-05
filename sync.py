# Make a function to treverse mouted directory and stores the files with their name and add
# Make a function to check if the directory is mounted
# Make a function to check for changes in a file


import os
import time
import threading
from functions import read_file
import hashlib
import json


file_path = 'test.txt'
threads = []



def check_dir_status():

    paths = read_file(file_path)
    while True:
        for path in paths:
            if os.path.exists(path):
                sync_thread = threading.Thread(target=sync, name=f"Thread {path}", args=(path,))
                sync_thread.start()
                threads.append(sync_thread)
        for i in threads:
            i.join()
            print("Thread joined back to main thread")
        threads.clear()
    
                
        time.sleep(6)
        print()



def sync(directory_path):

    print(f"{directory_path} tread is started.....")
    directory_name = os.path.basename(directory_path)
    

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
    

    def update_changes(directory_name,directory_path):

        previous_scan_path = f"metadata/scan_{directory_name}.json"
        changes_path = f'metadata/changes_{directory_name}.json' 
        changed_files = {}

        if os.path.isfile(previous_scan_path):
            with open(previous_scan_path, 'r') as file:
                previous_scan_data = json.load(file)
        else:
            previous_scan_data = {}
        
        current_scan_data = scan_directory(directory_path)    
        for file_path, current_file_data in current_scan_data.items():
            previous_file_data = previous_scan_data.get(file_path)
            if previous_file_data is None or current_file_data != previous_file_data:
                changed_files[file_path] = current_file_data

        
        with open (previous_scan_path, 'w') as file:
            json.dump(current_scan_data, file, indent = 4)
        
        append_files(changed_files) #now replace or paste files

    update_changes(directory_name,directory_path)    
    print(f"{directory_path} is stopped--------")


check_dir_status()

