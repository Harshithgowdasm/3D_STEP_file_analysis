import os
import re
import shutil
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
from OCC.Core.BRepGProp import brepgprop


def analyze_step_file(file_path):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(file_path)
    if status != 1:
        raise ValueError("Error reading STEP file")

    step_reader.TransferRoots()
    shape = step_reader.Shape()

    face_count = 0
    curved_face_count = 0
    edge_count = 0
    vert_count = 0

    vertices_explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
    while vertices_explorer.More():
        vertices_explorer.Next()
        vert_count += 1

    face_explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while face_explorer.More():
        face = face_explorer.Current()
        face_count += 1
        surface = BRepAdaptor_Surface(face)
        if surface.GetType() != GeomAbs_Plane:
            curved_face_count += 1
        face_explorer.Next()

    edge_explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    while edge_explorer.More():
        edge_explorer.Next()
        edge_count += 1

    return {
        "Total Faces": face_count,
        "Curved Faces": curved_face_count,
        "Total Edges": edge_count,
        "Vertices": vert_count,
    }


def detect_holes(step_file_path):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(step_file_path)
    if status != 1:
        print(f"Error reading file: {step_file_path}")
        return None

    step_reader.TransferRoots()
    shape = step_reader.Shape()

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    hole_count = 0

    while explorer.More():
        face = explorer.Current()
        surface = BRepAdaptor_Surface(face)
        if surface.GetType() == GeomAbs_Cylinder:
            hole_count += 1
        explorer.Next()

    return hole_count


def get_volume(file_path):
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(file_path)
    step_reader.TransferRoots()
    shape = step_reader.Shape()

    props = GProp_GProps()
    brepgprop.VolumeProperties(shape, props)
    return props.Mass()


def analyze_complexity_by_curvature(file_path):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(file_path)
    if status != 1:
        raise ValueError("Error reading STEP file")

    step_reader.TransferRoots()
    shape = step_reader.Shape()

    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    bbox_volume = (xmax - xmin) * (ymax - ymin) * (zmax - zmin)

    curvatures = []
    face_explorer = TopExp_Explorer(shape, TopAbs_FACE)

    while face_explorer.More():
        face = face_explorer.Current()
        geom_surface = BRep_Tool.Surface(face)
        surface = BRepAdaptor_Surface(face)
        u_min, u_max = surface.FirstUParameter(), surface.LastUParameter()
        v_min, v_max = surface.FirstVParameter(), surface.LastVParameter()
        u_sample, v_sample = (u_min + u_max) / 2, (v_min + v_max) / 2
        props = GeomLProp_SLProps(geom_surface, u_sample, v_sample, 2, 0.01)
        if props.IsCurvatureDefined():
            curvatures.append(props.MeanCurvature())
        face_explorer.Next()

    curvature_std_dev = np.std(curvatures)
    curvature_mean = np.mean(curvatures)

    return {
        "Bounding Box Volume": bbox_volume,
        "Mean Curvature": curvature_mean,
        "Curvature Std Dev": curvature_std_dev,
    }


def is_assembly_by_entity_count(file_path):
    """
    Check if the STEP file is an assembly by counting PRODUCT entities.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        product_count = len(re.findall(r'PRODUCT\(', content))
        return product_count > 1  # More than one product indicates an assembly
    except Exception as e:
        print(f"Error reading file for entity count: {e}")
        return None

def run_analysis_for_folder(folder_path):
    all_results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".step"):
            file_path = os.path.join(folder_path, filename)
            file_size_kb = os.path.getsize(file_path) / 1024  # Get file size in KB
            
            # Skip files larger than 5MB
            if file_size_kb > 5 * 1024:  # 20MB = 20 * 1024 KB
                print(f"Skipping file (size > 5MB): {filename}")
                continue

            # Determine if the file is a part or an assembly
            is_assembly = is_assembly_by_entity_count(file_path)
            ispart = 0 if is_assembly else 1

            # Proceed with analysis if the file is within size limits
            face_edge_result = analyze_step_file(file_path)
            curvature_result = analyze_complexity_by_curvature(file_path)
            volume = get_volume(file_path)
            holes = detect_holes(file_path)

            combined_result = {
                "File Name": filename,
                **face_edge_result,
                **curvature_result,
                "Volume": volume,
                "Hole Count": holes,
                "size": file_size_kb,
                "ispart": ispart
            } 
            all_results.append(combined_result)
            print(f"Analysis successful for {filename} file")

    df = pd.DataFrame(all_results)
    return df

def criteria_count(row):
    criteria = [
        20 <= row["Total Faces"] <= 120, 
        5 <= row["Curved Faces"] <= 50, 
        100 <= row["Total Edges"] <= 700, 
        200 <= row["Vertices"] <= 1500,  
        1e3 <= row["Volume"] <= 1.5e5, 
        5 <= row["Hole Count"] <= 50,
        25 <= row["size"] <= 500,  # file size filter  
        row["ispart"] == 1 
    ]

    return sum(criteria)

def file_selection(folder_path, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    data = run_analysis_for_folder(folder_path)
    data['Criteria Met'] = data.apply(criteria_count, axis=1)
    filtered_data = data[data['Criteria Met'] >= 8]
    
    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            file_path = os.path.join(folder_path, row['File Name'])
            print(f"File meets {row['Criteria Met']} criteria: {row['File Name']}")
            shutil.copy(file_path, os.path.join(destination_folder, row['File Name']))
    else:
        print(f"No files meet at least 7 criteria.")
    
    return data
