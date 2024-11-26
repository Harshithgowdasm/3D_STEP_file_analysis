import os
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
from OCC.Core.BRepGProp import brepgprop_VolumeProperties


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
    brepgprop_VolumeProperties(shape, props)
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



def run_analysis_for_folder(folder_path):
    all_results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".step"):
            file_path = os.path.join(folder_path, filename)
            face_edge_result = analyze_step_file(file_path)
            curvature_result = analyze_complexity_by_curvature(file_path)
            volume = get_volume(file_path)
            holes = detect_holes(file_path)

            combined_result = {
                "File Name": filename,
                **face_edge_result,
                **curvature_result,
                "Volume": volume,
                "Hole Count": holes
            }
            all_results.append(combined_result)

    df = pd.DataFrame(all_results)
    return df

def criteria_count(row):
    criteria = [
        10 <= row["Total Faces"] <= 150,
        2 <= row["Curved Faces"] <= 50,
        100 <= row["Total Edges"] <= 1500,
        100 <= row["Vertices"] <= 2500,
        row["Bounding Box Volume"] < 0.2e6,
        0 > row["Mean Curvature"] >= -0.15,
        0 < row["Curvature Std Dev"] <= 0.2,
        1e5 <= row["Volume"] <= 0.13e6,
        5 <= row["Hole Count"] <= 50
        # file size filter 
        # 

    ]

    return sum(criteria)


def file_selection(folder_path, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    data = run_analysis_for_folder(folder_path)
    data['Criteria Met'] = data.apply(criteria_count, axis=1)
    filtered_data = data[data['Criteria Met'] >= 7]
    
    if not filtered_data.empty:
        #print(f"Rows meeting at least 7 criteria:")
        #print(filtered_data[['File Name', 'Criteria Met']])  

        for _, row in filtered_data.iterrows():
            file_path = os.path.join(folder_path, row['File Name'])
            print(f"File meets {row['Criteria Met']} criteria: {row['File Name']}")
            shutil.copy(file_path, os.path.join(destination_folder, row['File Name']))
    else:
        print(f"No files meet at least 7 criteria.")
    
    return data
