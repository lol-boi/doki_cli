import os
import threading
import shutil
from functions import read_file
import hashlib
import json
import sys
import re
import datetime
from functions import *
from functions import file_add as file_path

threads = []

def create_folders_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directories: {directory}")


def sync_target_dir(arg):

    paths = read_file(file_path)
    if (arg == 'r'):
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
            print()
    elif(arg == 'n'):
        while True:
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
            print()
    else:
        print("Exit form sync_target_dir.")




def sync(directory_path,Destination_path):

    print(f"{directory_path} tread is started.....")
    directory_name = os.path.basename(directory_path)
    

    def update_dir(changes,target_path,des_path):
        new_changes =[]
        for i in changes: 
            new_path = os.path.relpath(i,target_path)
            new_path = os.path.join(Destination_path,new_path)
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

        update_dir(changed_files,directory_path,Destination_path)
    
    update_changes(directory_name,directory_path)   
    print(f"{directory_path} is stopped--------")
        



def main():
    length = len(sys.argv)
    if length == 1:
        print("Arguments Error! use 'python doki.py -h' for help.") 
    
    elif length == 2 and sys.argv[1] == '-h':
        print(''' Usage: python scan.py    [OPTION...]    [ARGUMENT....] 
    Help Options:
        -h        Show help options
        -t        Set the sync time  (Synchronizes everyday at the time)
        -r        Sync only once   (Synchronizes the directories only once) 
        -e        Edit the sync targets or use 'python read.py'
        -n        Run doki in normal mode 
              
    Help Argumens:
        -t        Time format  [HH:MM] 
              
    By default doki Synchronizes continously''')
    elif length == 3 and sys.argv[1] == '-t':
        if not re.match(r'^\d{2}:\d{2}$', sys.argv[2]):
            print("Invalid format: (HH:MM) ")
            return
        hour, minute = map(int, sys.argv[2].split(':'))

        while True:
            current_time = datetime.datetime.now().time()
            desired_time = datetime.time(hour, minute)
            
            if current_time >= desired_time:
                sync_target_dir('r')
                break 
    elif length == 2 and sys.argv[1] == '-r':
        print("Synchronizing") 
        sync_target_dir('r')
    elif length == 2 and sys.argv[1] == '-e':
        cli_interface()
    elif length == 2 and sys.argv[1] == '-n':
        sync_target_dir('n')
    else:
       print("Arguments Error! use 'python doki.py -h' for help.")  


main()