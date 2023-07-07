import shutil

def copy_file(source_path, destination_path):
    shutil.copy2(source_path, destination_path)
    print(f"File copied from {source_path} to {destination_path}")

# Example usage
source_path = "/home/anzen/Pictures/wallpaper/pc/Guts.jpg"
destination_path = "/home/anzen/Documents/test/duck/pc/Guts.jpg"
copy_file(source_path, destination_path)
