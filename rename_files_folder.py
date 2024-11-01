import os

# Specify the folder path
folder_path = 'abc_0000'
start_number = 1

# Get all files in the directory
files = sorted(os.listdir(folder_path))

# Rename each file with sequential numbering
for index, filename in enumerate(files, start=start_number):
    # Generate the new filename with 8 digits
    new_name = f"abc_{index:08}.step"
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)
    
    # Rename the file
    os.rename(old_path, new_path)

print("Files have been renamed.")
