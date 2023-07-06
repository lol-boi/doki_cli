import csv
import os
from tabulate import tabulate
from functions import read_file,write_file

#Add a system to check if a path to sync is already in another parent path and resolve it




file_add = 'test.csv'
def view_dir(): 
    nested_list = read_file(file_add)
    print(tabulate(nested_list,['S.No','Sync_path','Paste_path'], showindex="always",tablefmt="rounded_grid"))


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


cli_interface()
