import os

# Specify the folder path
folder_path = 'Selected'
start_number = 1

# Get all files in the directory
#files = sorted(os.listdir(folder_path))

# Rename each file with sequential numbering
#for index, filename in enumerate(files, start=start_number):
#    # Generate the new filename with 8 digits
#    new_name = f"abc_{index:08}.step"
#    old_path = os.path.join(folder_path, filename)
#    new_path = os.path.join(folder_path, new_name)
    
    # Rename the file
#    os.rename(old_path, new_path)

for filename in os.listdir(folder_path):
    # Check if the file has a .step extension
    if filename.endswith(".step"):
        # Split at the first underscore and keep the first part
        base_name = filename.split('_')[0]
        
        # Set full old and new paths
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, f"{base_name}.step")
        
        # Rename the file
        os.rename(old_path, new_path)

print("Files have been renamed.")

