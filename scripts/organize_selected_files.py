import shutil
import os
# Manuallly selected (text file), It reads the file names and their classifications from the text file, 
# constructs the full source and destination paths, and moves the files to the appropriate folders.

# Define paths
source_dir = r"S:\03_HiWiS\Harshith\ILSC-APP\abc_0000_step_v00\automated_filter_no"
simple_dest = r"S:\03_HiWiS\Harshith\ILSC-APP\3D_STEP_file_analysis\Selected_Manually\new_partitions\Simple"
complex_dest = r"S:\03_HiWiS\Harshith\ILSC-APP\3D_STEP_file_analysis\Selected_Manually\new_partitions\Complex"

# Path to the text file containing file names and classification
text_file = r"S:\03_HiWiS\Harshith\ILSC-APP\3D_STEP_file_analysis\selected.txt"

# Read file and process each line
with open(text_file, "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        
        parts = line.split("-")
        if len(parts) != 2:
            print(f"Skipping invalid line: {line}")
            continue
        
        file_name, category = parts
        full_file_name = f"0000{file_name}.step"  # Append leading zeros
        
        source_path = os.path.join(source_dir, full_file_name)
        
        # Determine destination
        if category.lower() == "sim":
            destination_path = os.path.join(simple_dest, full_file_name)
        elif category.lower() == "co":
            destination_path = os.path.join(complex_dest, full_file_name)
        else:
            print(f"Skipping unknown category in line: {line}")
            continue
        
        # Copy file if it exists
        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied {source_path} to {destination_path}")
        else:
            print(f"File not found: {source_path}")
