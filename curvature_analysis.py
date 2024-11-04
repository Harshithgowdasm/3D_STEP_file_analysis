from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRep import BRep_Tool
from OCC.Core.GeomAbs import GeomAbs_CurveType
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepTools import breptools_UVBounds
from OCC.Core.BRepLProp import BRepLProp_SLProps
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
import matplotlib.pyplot as plt
import numpy as np

def curvature_analysis(step_file_path):
    # Read the STEP file
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(step_file_path)
    step_reader.TransferRoots()
    shape = step_reader.Shape()

    # Go through each face in the shape
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    mean_curvatures = []
    gaussian_curvatures = []
    
    while explorer.More():
        face = explorer.Current()
        surface = BRepAdaptor_Surface(face)
        u_min, u_max, v_min, v_max = breptools_UVBounds(face)

        # Compute curvature at the midpoint (u, v)
        u_mid, v_mid = (u_min + u_max) / 2, (v_min + v_max) / 2
        props = BRepLProp_SLProps(surface, u_mid, v_mid, 2, 1e-6)
        if props.IsCurvatureDefined():
            mean_curvature = props.MeanCurvature()
            gaussian_curvature = props.GaussianCurvature()
            mean_curvatures.append(mean_curvature)
            gaussian_curvatures.append(gaussian_curvature)
        
        explorer.Next()

    return mean_curvatures, gaussian_curvatures

# List of STEP files to analyze
file_paths = ['abc_0000_data/abc_00000001.step', 'abc_0000_data/abc_00000002.step', 'abc_0000_data/abc_00000003.step', 'abc_0000_data/abc_00000004.step','abc_0000_data/abc_00000005.step', 'abc_0000_data/abc_00000006.step', 'abc_0000_data/abc_00000007.step', 'abc_0000_data/abc_00000008.step']  # replace with your file paths
curvature_data = {}

# Process each file and store its curvature data
for file_path in file_paths:
    mean_curvatures, gaussian_curvatures = curvature_analysis(file_path)
    curvature_data[file_path] = (mean_curvatures, gaussian_curvatures)

print(curvature_data['abc_0000_data/abc_00000003.step'])

# Visualize the curvature comparison
fig, ax = plt.subplots(2, 1, figsize=(14, 10))

# Plot Mean Curvature for each file
for file_path, (mean_curvatures, _) in curvature_data.items():
    ax[0].plot(range(len(mean_curvatures)), mean_curvatures, label=file_path)
ax[0].set_title("Mean Curvature Comparison")
ax[0].set_xlabel("Face Index")
ax[0].set_ylabel("Mean Curvature")
ax[0].legend()

# Plot Gaussian Curvature for each file
for file_path, (_, gaussian_curvatures) in curvature_data.items():
    ax[1].plot(range(len(gaussian_curvatures)), gaussian_curvatures, label=file_path)
ax[1].set_title("Gaussian Curvature Comparison")
ax[1].set_xlabel("Face Index")
ax[1].set_ylabel("Gaussian Curvature")
ax[1].legend()

plt.tight_layout()
plt.show()
