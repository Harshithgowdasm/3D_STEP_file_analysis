from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
import os
import pandas as pd

def detect_holes(step_file_path):
    # Read the STEP file
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(step_file_path)
    if status != 1:  # Check if file reading was successful
        print(f"Error reading file: {step_file_path}")
        return None

    step_reader.TransferRoots()
    shape = step_reader.Shape()

    # Initialize explorer to iterate over faces
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    hole_count = 0
    hole_faces = []

    # Iterate over each face to detect cylindrical surfaces (holes)
    while explorer.More():
        face = explorer.Current()
        surface = BRepAdaptor_Surface(face)

        # Check if the surface is cylindrical, which often indicates a hole
        if surface.GetType() == GeomAbs_Cylinder:
            hole_count += 1
            hole_faces.append(face)  # Optionally, store the face representing the hole

        explorer.Next()

    return hole_count

# Example usage
folder_path = "abc_0000_data"

# List all STEP files in the folder
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".step")]

# Process each STEP file and get volumes
count_hole = [detect_holes(fp) for fp in file_paths]

# Store results in a DataFrame
df = pd.DataFrame({"File": file_paths, "holes": count_hole})
print(df)

