"""
STEP File Volume Analysis Script

This script reads multiple STEP files from a specified folder, extracts their volume, 
and visualizes the results using a bar chart.

Functionality:
1. Extracts the volume of each STEP file using OpenCascade.
2. Stores the volume data in a Pandas DataFrame.
3. Plots a bar chart comparing the volumes of different STEP files.

"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps

# Function to extract volume from a STEP file
def get_volume(file_path):
    """
    Reads a STEP file and calculates its volume.

    Args:
        file_path (str): Path to the STEP file.

    Returns:
        float: Volume of the STEP file.
    """
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(file_path)  # Load the STEP file
    step_reader.TransferRoots()  # Transfer the shape
    shape = step_reader.Shape()  # Get the shape
    
    # Compute volume properties
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    
    return props.Mass()  # Return the computed volume

# Define the folder path containing STEP files
folder_path = "abc_0000_data"  # Modify this path as needed

# List all STEP files in the folder
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".step")]

# Process each STEP file and get volumes
volumes = [get_volume(fp) for fp in file_paths]

# Store results in a Pandas DataFrame
df = pd.DataFrame({"File": file_paths, "Volume": volumes})

# Print the DataFrame to view results
print(df)

# Plot the volumes using a bar chart
plt.figure(figsize=(12, 6))  # Set figure size for better visibility
df.plot(kind="bar", x="File", y="Volume", legend=False, color='b')

# Labeling the graph
plt.xlabel("STEP File")
plt.ylabel("Volume")
plt.title("Volume of STEP Files")
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability

# Display the plot
plt.show()
