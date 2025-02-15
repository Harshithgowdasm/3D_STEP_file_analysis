"""
This script uses a variety of methods/techniques/algorithms to classify STEP files as either "Part" or "Assembly".  
It implements multiple classification methods, but only Method 3 (entity count in `classify_step_file` function)  
is validated and works accurately.  

Methods included:
1. Keyword-based search (disabled)
2. OCC-based geometric analysis (disabled)
3. Entity count-based classification (validated and accurate)

Only Method 3 is used for classification in this script.
"""

import os
import re
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopoDS import TopoDS_Compound

def is_assembly_by_keywords(file_path):
    """
    Check for assembly-specific keywords in the file content.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        if 'ASSEMBLY' in content or 'PRODUCT' in content:
            return True
        if 'MANIFOLD_SOLID_BREP' in content:
            return False
        return None  # Could not determine
    except Exception as e:
        print(f"Error reading file for keyword search: {e}")
        return None

def is_assembly_with_occ(file_path):
    """
    Use python-occ to determine if the file is an assembly.
    """
    try:
        reader = STEPControl_Reader()
        status = reader.ReadFile(file_path)
        if status == 1:  # File successfully read
            reader.TransferRoots()
            shape = reader.OneShape()
            # Assemblies are usually TopoDS_Compound (type 7)
            return shape.ShapeType() == TopoDS_Compound().ShapeType()
        else:
            print(f"Failed to read STEP file with OCC: {file_path}")
            return None
    except Exception as e:
        print(f"Error processing file with OCC: {e}")
        return None

def is_assembly_by_entity_count(file_path):
    """
    Count the number of PRODUCT entities in the STEP file.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        product_count = len(re.findall(r'PRODUCT\(', content))
        return product_count > 1  # More than one product indicates an assembly
    except Exception as e:
        print(f"Error counting entities in file: {e}")
        return None

def classify_step_file(file_path):
    """
    Classify the STEP file using multiple methods. Only Method 3 (Entity Count) accurtely classifies and used.
    """
    print(f"Classifying file: {file_path}")

    # Method 1: Keyword Search (disabled)
    # result_keywords = is_assembly_by_keywords(file_path)
    # print(f"Keyword Search Result: {result_keywords}")

    # Method 2: Using python-occ (disabled)
    # result_occ = is_assembly_with_occ(file_path)
    # print(f"OCC Analysis Result: {result_occ}")

    # Method 3: Entity Count (validated method)
    result_entity_count = is_assembly_by_entity_count(file_path)
    print(f"Entity Count Result: {result_entity_count}")

    # Combine results (only Method 3 is considered)
    if result_entity_count is not None:
        return "Assembly" if result_entity_count else "Part"

    return "Unknown"  # If all methods fail

def test_directory(directory_or_file):
    """
    Test and classify STEP files in a directory or classify a single file.
    """
    # Check if the input is a file or a directory
    if os.path.isfile(directory_or_file):
        # Single file classification
        file_path = directory_or_file
        classification = classify_step_file(file_path)
        print(f"File: {os.path.basename(file_path)}, Classification: {classification}")
        return {os.path.basename(file_path): classification}
    elif os.path.isdir(directory_or_file):
        # Directory classification
        step_files = [
            f for f in os.listdir(directory_or_file)
            if f.lower().endswith('.step') or f.lower().endswith('.stp')
        ]
        results = {}
        for file in step_files:
            file_path = os.path.join(directory_or_file, file)
            classification = classify_step_file(file_path)
            results[file] = classification
            print(f"File: {file}, Classification: {classification}")
        return results
    else:
        raise ValueError(f"The provided path is neither a file nor a directory: {directory_or_file}")

# Example usage
if __name__ == "__main__":
    directory = r"S:\03_HiWiS\Harshith\ILSC-APP\3D_STEP_file_analysis\Selected_Manually\ReviewedMaxim\Complex\00009985.step"  # Replace with your directory path
    results = test_directory(directory)

    print("\nClassification Results:")
    for file, classification in results.items():
        print(f"{file}: {classification}")
