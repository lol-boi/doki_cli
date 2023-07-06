import csv

def read_file(path):
    nested_array= [] 
    with open(path,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            nested_array.append(row)
    return nested_array

def write_file(file_add):
    input_array = input("Enter the Sync_path and Paste_path , seprated by space: ")
    input_array = input_array.split()
    print(input_array)
    with open(file_add, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(input_array)