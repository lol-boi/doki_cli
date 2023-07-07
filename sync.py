#use source and destination

import os
import time
import threading
import shutil
from functions import read_file
import hashlib
import json


file_path = 'test.csv'
threads = []

def create_folders_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directories: {directory}")


def check_dir_status():

    paths = read_file(file_path)
    for i in range(1):
        for path in paths:
            create_folders_if_not_exists(path[1])
            if os.path.exists(path[0]):
                sync_thread = threading.Thread(target=sync, name=f"Thread {path[0]}", args=(path[0],path[1]))
                sync_thread.start()
                threads.append(sync_thread)
            else:
                print(path," does not exist")
        for i in threads:
            i.join()
        threads.clear()
    
                
        time.sleep(6)
        print()



def sync(directory_path,Paste_path):

    print(f"{directory_path} tread is started.....")
    directory_name = os.path.basename(directory_path)
    

    def update_dir(changes,target_path,des_path):
        new_changes =[]
        for i in changes: 
            new_path = os.path.relpath(i,target_path)
            new_path = os.path.join(Paste_path,new_path)
            create_folders_if_not_exists(new_path)
            new_changes.append(new_path)
        count = 0 
        for i in changes:
            shutil.copy2(i,new_changes[count])
            count += 1

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

        update_dir(changed_files,directory_path,Paste_path)
    


    update_changes(directory_name,directory_path)   
    print(f"{directory_path} is stopped--------")
        
check_dir_status()

