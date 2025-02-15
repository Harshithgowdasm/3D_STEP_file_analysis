"""
STEP File Hole Detection Script

This script analyzes STEP files to detect cylindrical holes based on their surface geometry.

Key Features:
- Reads and processes STEP files.
- Identifies faces with cylindrical geometry (potential holes).
- Outputs the count of detected holes per file.

Dependencies:
- OpenCascade (pythonOCC)
- Pandas
- OS module (for file handling)
"""

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
import os
import pandas as pd

def detect_holes(step_file_path):
    """
    Detects cylindrical holes in a given STEP file by analyzing face geometries.

    :param step_file_path: Path to the STEP file.
    :return: Count of cylindrical hole-like faces.
    """
    
    # Load STEP file
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(step_file_path)
    
    # Check if file reading was successful
    if status != 1:  
        print(f"Error reading file: {step_file_path}")
        return None

    step_reader.TransferRoots()
    shape = step_reader.Shape()

    # Initialize face explorer
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    hole_count = 0  # Counter for holes
    hole_faces = []  # List to store detected hole faces (optional)

    # Iterate over faces to identify cylindrical surfaces
    while explorer.More():
        face = explorer.Current()
        surface = BRepAdaptor_Surface(face)

        # Check if the face is a cylindrical surface (indicating a hole)
        if surface.GetType() == GeomAbs_Cylinder:
            hole_count += 1
            hole_faces.append(face)  # Storing the hole face (not used in output)

        explorer.Next()  # Move to the next face

    return hole_count  # Return total number of detected holes

# Example usage
folder_path = "Selected"  # Folder containing STEP files

# Retrieve all STEP file paths from the given folder
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".step")]

# Process each file and count the number of detected holes
count_hole = [detect_holes(fp) for fp in file_paths]

# Create a DataFrame to store results
df = pd.DataFrame({"File": file_paths, "Holes": count_hole})

# Print results
print(df)
