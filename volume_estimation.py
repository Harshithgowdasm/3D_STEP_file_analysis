import os
import pandas as pd
import matplotlib.pyplot as plt
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps

# Function to extract volume from a STEP file
def get_volume(file_path):
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(file_path)
    step_reader.TransferRoots()
    shape = step_reader.Shape()
    
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    return props.Mass()

# Define folder path containing STEP files
folder_path = "abc_0000_data"

# List all STEP files in the folder
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".step")]

# Process each STEP file and get volumes
volumes = [get_volume(fp) for fp in file_paths]

# Store results in a DataFrame
df = pd.DataFrame({"File": file_paths, "Volume": volumes})
print(df)

# Plot the volumes
df.plot(kind="bar", x="File", y="Volume")
plt.xlabel("STEP File")
plt.ylabel("Volume")
plt.title("Volume of STEP Files")
plt.show()
