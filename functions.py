import csv
import os
from tabulate import tabulate
import hashlib
file_add = 'directories.csv'


def read_file(path):
    nested_array= [] 
    with open(path,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            nested_array.append(row)
    return nested_array

def write_file(file_add):
    input_array = input("Enter the Source_path and Destination_path , seprated by '||': ")
    input_array = input_array.split(sep=" || ")
    print(input_array)
    with open(file_add, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(input_array)


def view_dir(): 
    nested_list = read_file(file_add)
    print(tabulate(nested_list,['S.No','Source_path','Destination_path'], showindex="always",tablefmt="rounded_grid"))


def cli_interface():
    
    choice = 2
    menu = [['Add Directory'],['Remove Directory'],['View Directories'],['Terminate']]
    headers = ['S.No','Directories']
    while choice != 3:
        print("----- Enter the choice -----")
        print(tabulate(menu,headers,showindex="always",tablefmt="pretty"))
        choice = int(input("Enter the choice: "))
        print("you entered ", choice)
        os.system('clear') 
        


        if choice == 0:
            print("Make sure the distination_folder is empty!")
            write_file(file_add)


        elif choice == 1: 
            view_dir()
            
            lines = read_file(file_add)
            del_line_index = int(input("Enter the line to be deleted: "))
            if del_line_index <= len(lines):
                del lines[del_line_index]
                with open(file_add, 'w') as file:
                    writer = csv.writer(file)
                    writer.writerows(lines)
                print("Line deleted sucessfully!")
            else:
                print("Invalid line number!")
            
            os.system('clear')
            view_dir()                        

        elif choice == 2:
            view_dir()
        


        elif choice == 3:
            print("returned sucessfully")
            return
        


        else: 
            print("Enter the correct choice")


def hash_folder(folder_path):
    hash_object = hashlib.sha256()
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b''):
                    hash_object.update(chunk)
    folder_hash = hash_object.hexdigest()
    return folder_hash