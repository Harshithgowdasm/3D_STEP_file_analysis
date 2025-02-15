#This script organizes files in a specified directory by distributing them into subfolders, each containing up to 1,000 files. 
# It sequentially creates folders (e.g., "step_00", "step_01") and moves files into them, stopping after creating 10 folders.

import os
import shutil

# Define the source directory (files will remain in this directory, but be organized into subfolders)
source_dir = r"S:\03_HiWiS\Harshith\ILSC-APP\abc_0000_step_v00"

# Number of files per folder
files_per_folder = 1000

# Get a sorted list of all files in the source directory
all_files = sorted(os.listdir(source_dir))

# Initialize folder index and file counter
folder_index = 0
file_count = 0

# Loop through the files and distribute them into folders
for filename in all_files:
    # Ignore non-files or directories (if any exist)
    if not os.path.isfile(os.path.join(source_dir, filename)):
        continue

    # Create a new folder if necessary
    if file_count == 0:
        folder_name = f"step_{folder_index:02}"  # Example: step_00, step_01, etc.
        new_folder_path = os.path.join(source_dir, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

    # Move the file into the current folder
    src_path = os.path.join(source_dir, filename)
    dest_path = os.path.join(new_folder_path, filename)
    shutil.move(src_path, dest_path)

    # Update the file count
    file_count += 1

    # If the current folder reaches its limit, move to the next folder
    if file_count == files_per_folder:
        folder_index += 1
        file_count = 0

    # Stop if all 10 folders are filled
    if folder_index >= 10:
        break

print("Files have been successfully organized into folders!")
