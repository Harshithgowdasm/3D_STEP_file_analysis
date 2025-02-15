"""
STEP File Renaming Script

This script renames STEP files in a specified folder by:
1. Removing unnecessary parts of filenames, keeping only the base name.
2. Ensuring all files have a standardized `.step` extension.
3. Optionally, it includes a commented-out section to rename files with sequential numbering.

Usage:
- Modify the `folder_path` variable to point to the target directory.
- Ensure the folder contains `.step` files before running.

"""

import os

# Specify the folder containing STEP files
folder_path = r"S:\03_HiWiS\Harshith\ILSC-APP\abc_0000_step_v00\step_00"

# Iterate through all files in the directory
for filename in os.listdir(folder_path):
    # Check if the file has a .step extension
    if filename.endswith(".step"):
        # Extract the base name (before the first underscore) to rename the file
        base_name = filename.split('_')[0]
        
        # Construct full old and new file paths
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, f"{base_name}.step")
        
        # Rename the file
        os.rename(old_path, new_path)

print("Files have been renamed.")

# ---- Alternative Sequential Renaming (Commented Out) ----
# Uncomment this section if you want to rename files sequentially (e.g., abc_00000001.step)
"""
start_number = 1  # Define the starting number for renaming

# Get all files in the directory and sort them
files = sorted(os.listdir(folder_path))

# Rename each file with sequential numbering
for index, filename in enumerate(files, start=start_number):
    new_name = f"abc_{index:08}.step"  # Generate new name with 8-digit numbering
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)
    
    os.rename(old_path, new_path)  # Rename the file

print("Files have been renamed with sequential numbering.")
"""
