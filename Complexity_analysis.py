import os
import pandas as pd
import numpy as np
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties


def analyze_step_file(file_path):
    # Load STEP file
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(file_path)
    if status != 1:
        raise ValueError("Error reading STEP file")

    step_reader.TransferRoots()
    shape = step_reader.Shape()

    # Initialize counters
    face_count = 0
    curved_face_count = 0
    edge_count = 0
    vert_count = 0

    # Explore vertices
    vertices_explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
    while vertices_explorer.More():
        vertices = vertices_explorer.Current()
        vert_count += 1
        vertices_explorer.Next()

    # Count faces and edges
    face_explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while face_explorer.More():
        face = face_explorer.Current()
        face_count += 1
        
        # Check if the face is curved or planar
        surface = BRepAdaptor_Surface(face)
        if surface.GetType() != GeomAbs_Plane:
            curved_face_count += 1
        
        face_explorer.Next()

    # Count edges
    edge_explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    while edge_explorer.More():
        edge = edge_explorer.Current()
        edge_count += 1
        edge_explorer.Next()

    # Determine complexity based on thresholds
    complexity = "Simple" if face_count < 20 and curved_face_count < 9 and vert_count<60 else "Complex"

    # Return results as dictionary
    return {
        "Total Faces": face_count,
        "Curved Faces": curved_face_count,
        "Total Edges": edge_count,
        "Vertices" : vert_count,
        "Complexity (Face/Edge)": complexity
    }

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

def get_volume(file_path):
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(file_path)
    step_reader.TransferRoots()
    shape = step_reader.Shape()
    
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    return props.Mass()

def analyze_complexity_by_curvature(file_path):
    # Load STEP file
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(file_path)
    if status != 1:
        raise ValueError("Error reading STEP file")
    
    step_reader.TransferRoots()
    shape = step_reader.Shape()
    
    # Initialize bounding box and curvature data
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    bbox_volume = (xmax - xmin) * (ymax - ymin) * (zmax - zmin)
    
    curvatures = []
    face_explorer = TopExp_Explorer(shape, TopAbs_FACE)
    
    # Calculate curvature variation on each face
    while face_explorer.More():
        face = face_explorer.Current()
        
        # Get the Geom_Surface using BRep_Tool
        geom_surface = BRep_Tool.Surface(face)
        
        # Adapt it to use BRepAdaptor_Surface for bounds
        surface = BRepAdaptor_Surface(face)
        u_min, u_max, v_min, v_max = surface.FirstUParameter(), surface.LastUParameter(), surface.FirstVParameter(), surface.LastVParameter()
        
        # Sample curvature at midpoint
        u_sample, v_sample = (u_min + u_max) / 2, (v_min + v_max) / 2
        props = GeomLProp_SLProps(geom_surface, u_sample, v_sample, 2, 0.01)
        
        if props.IsCurvatureDefined():
            curvatures.append(props.MeanCurvature())
        
        face_explorer.Next()
    
    # Analyze curvature variation
    curvature_std_dev = np.std(curvatures)
    curvature_mean = np.mean(curvatures)
    complexity = "Simple" if curvature_std_dev < 0.1 and bbox_volume < 1.0 else "Complex"

    # Return results as dictionary
    return {
        "Bounding Box Volume": bbox_volume,
        "Mean Curvature": curvature_mean,
        "Curvature Std Dev": curvature_std_dev,
        "Complexity (Curvature)": complexity
    }

# Run analysis and store results in DataFrame
def run_analysis_for_folder(folder_path):
    all_results = []
    
    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".step"):  # Check if file is a STEP file
            file_path = os.path.join(folder_path, filename)
            
            # Run analysis for each file
            face_edge_result = analyze_step_file(file_path)
            curvature_result = analyze_complexity_by_curvature(file_path)
            volume = get_volume(file_path)
            holes = detect_holes(file_path)
            
            # Combine results with filename
            combined_result = {
                "File Name": filename,
                **face_edge_result,
                **curvature_result,
                "Volume": volume,
                "Hole Count": holes
            }
            all_results.append(combined_result)
    
    # Create DataFrame from all results
    df = pd.DataFrame(all_results)
    return df

# Example usage
folder_path = "All"
result_df = run_analysis_for_folder(folder_path)
result_df.to_csv('analysis_df.csv')
print(result_df)
