import csv
import os
from tabulate import tabulate
from functions import read_file

#Add a system to check if a path to sync is already in another parent path and resolve it




file_add = 'test.txt'
def view_dir(): 
    array = read_file(file_add)
    nested_list = [[element] for element in array]
    print(tabulate(nested_list,['S.No','Directories'], showindex="always",tablefmt="rounded_grid"))


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
            input_array = input("Enter the directories, seprated by spaces: ")
            input_array = input_array.split()
            print(input_array)
            with open(file_add, 'a') as file:
                for i in input_array:
                    file.write(i + '\n')

        elif choice == 1: 
            view_dir()
            
            with open(file_add, 'r') as file:
                lines = file.readlines()    
            del_line_index = int(input("Enter the line to be deleted: "))
            if del_line_index <= len(lines):
                del lines[del_line_index]
                with open(file_add, 'w') as file:
                    file.writelines(lines)
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


cli_interface()
