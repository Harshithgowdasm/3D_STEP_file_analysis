import os
import sys
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX, TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer

def count_elements(shape: TopoDS_Shape):
    vertices = set()
    edges = set()
    faces = set()
    
    # Use TopExp_Explorer to iterate through edges, vertices, and faces
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    while explorer.More():
        edges.add(explorer.Current())
        explorer.Next()

    explorer.Init(shape, TopAbs_VERTEX)
    while explorer.More():
        vertices.add(explorer.Current())
        explorer.Next()

    explorer.Init(shape, TopAbs_FACE)
    while explorer.More():
        faces.add(explorer.Current())
        explorer.Next()

    return len(vertices), len(edges), len(faces)

def load_step_file(filename: str):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    if status != 1:  # IFSelect_ReturnStatus.IFSelect_RetDone is typically 1
        print(f"Error reading the STEP file: {filename}")
        return None

    step_reader.TransferRoot()
    shape = step_reader.OneShape()

    return shape

def process_step_files(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith('.step'):
            file_path = os.path.join(folder_path, filename)
            shape = load_step_file(file_path)
            if shape is not None:
                vertices_count, edges_count, faces_count = count_elements(shape)
                print(f'File: {filename}')
                print(f'  Number of Vertices: {vertices_count}')
                print(f'  Number of Edges: {edges_count}')
                print(f'  Number of Faces: {faces_count}')
                print('')

if __name__ == "__main__":
    # Specify the folder containing STEP files
    folder_path = 'abc_0000'  # Update with your actual folder path
    process_step_files(folder_path)
