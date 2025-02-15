"""
This script processes STEP files in a specified folder and extracts geometric information  
about the number of vertices, edges, and faces in each file.  

It uses `python-occ` (OCC) to read and analyze STEP files, extracting the following information:
- Number of vertices
- Number of edges
- Number of faces  

Each STEP file in the folder is processed, and the results are printed for each file.
"""

import os
import sys
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX, TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer

def count_elements(shape: TopoDS_Shape):
    """
    Count the number of vertices, edges, and faces in the given STEP file shape.

    :param shape: The geometric shape extracted from the STEP file.
    :return: A tuple containing the number of vertices, edges, and faces.
    """
    vertices = set()
    edges = set()
    faces = set()
    
    # Iterate through edges
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    while explorer.More():
        edges.add(explorer.Current())
        explorer.Next()

    # Iterate through vertices
    explorer.Init(shape, TopAbs_VERTEX)
    while explorer.More():
        vertices.add(explorer.Current())
        explorer.Next()

    # Iterate through faces
    explorer.Init(shape, TopAbs_FACE)
    while explorer.More():
        faces.add(explorer.Current())
        explorer.Next()

    return len(vertices), len(edges), len(faces)

def load_step_file(filename: str):
    """
    Load and parse a STEP file using python-occ.

    :param filename: The path to the STEP file.
    :return: The geometric shape extracted from the file, or None if reading fails.
    """
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    # Check if the file was successfully read
    if status != 1:  # IFSelect_ReturnStatus.IFSelect_RetDone is typically 1
        print(f"Error reading the STEP file: {filename}")
        return None

    # Transfer the root shape from the STEP file
    step_reader.TransferRoot()
    shape = step_reader.OneShape()

    return shape

def process_step_files(folder_path: str):
    """
    Process all STEP files in a given folder, extracting and displaying geometric information.

    :param folder_path: The directory containing STEP files.
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.step'):  # Ensure only STEP files are processed
            file_path = os.path.join(folder_path, filename)
            
            # Load the STEP file
            shape = load_step_file(file_path)
            if shape is not None:
                # Count vertices, edges, and faces
                vertices_count, edges_count, faces_count = count_elements(shape)
                
                # Print results
                print(f'File: {filename}')
                print(f'  Number of Vertices: {vertices_count}')
                print(f'  Number of Edges: {edges_count}')
                print(f'  Number of Faces: {faces_count}')
                print('')

if __name__ == "__main__":
    # Specify the folder containing STEP files
    folder_path = 'abc'  # Update with your actual folder path
    process_step_files(folder_path)
