# 3D STEP File Analysis

This repository provides tools for analyzing 3D STEP files, enabling extraction and inspection of geometrical properties such as curvature, volume, and hole detection for applications in engineering and data processing.

## Installation

### Step 1: Download Dataset

Download the recommended [ABC dataset](https://deep-geometry.github.io/abc-dataset/) to access a variety of CAD models for analysis. The ABC dataset includes a large collection of CAD models that can be used for geometrical and topological data analysis, allowing for diverse applications of the tools provided in this repository. Follow the instructions on their page for downloading and setting up the dataset locally.

### Step 2: Set Up Environment and Install `pythonocc-core`

1. **Install Anaconda or Miniconda** if you haven’t already using [Anaconda](https://docs.anaconda.com/anaconda/install/).
2. **Create a new Conda environment**:
   ```bash
   conda create -n cad_env python=3.8
   conda activate cad_env
3. **Install `pythonocc-core` from conda-forge**:
    ```bash
    conda install -c conda-forge pythonocc-core
4. **Verify the Installation: Run the following command to check if `pythonocc-core`is installed correctly:**
    ```bash
    python -c "from OCC.Core.STEPControl import STEPControl_Reader; print('OCC is working')"


