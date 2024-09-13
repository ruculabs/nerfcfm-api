# NeRF Pipeline Scripts

This repository provides a set of scripts for processing data, training NeRF models, and exporting 3D objects using Nerfstudio. These scripts wrap the Nerfstudio CLI commands to streamline the workflow for NeRF-based 3D reconstruction.

## Requirements

These scripts work with the Nerfstudio package. You can install it using pip:

```bash
pip install nerfstudio
```
### Current Version Information

The scripts have been tested with the following version of Nerfstudio:

- **Nerfstudio Version**: 1.1.4
- **Python Version**: 3.8 (inside a conda environment)

To check your version of Nerfstudio, use the following command:

```bash
pip show nerfstudio
```

For more information, please refer to the [Nerfstudio documentation](https://docs.nerf.studio/quickstart/installation.html).

## Project Structure

The project is organized as follows:

```bash
scripts/
  nerf_data/
    process_data.py       # Script for processing raw data into Nerfstudio format
    utils.py              # Utilities for data processing
  nerf_models/
    train_model.py        # Script for training NeRF models
    utils.py              # Utilities for model training
  nerf_objects/
    export_object.py      # Script for exporting trained models to 3D objects
    utils.py              # Utilities for object exporting
  main.py                 # Main entry point to the pipeline
```

### Usage

1. Data Processing

    To process raw data (either images or video), use the following command:

    ```bash
    python main.py process_data --data_type video --data_path /path/to/video --output_dir /path/to/processed_data
    ```

    Supported data types:

    - `images`: A folder containing images of the scene.
    - `video`: A video file to extract frames from.

2. Training NeRF Models

    To train a NeRF model using the processed data:

    ```bash
    python main.py train_model --model_type nerfacto --data_dir /path/to/processed_data --output_dir /path/to/model_output --num_epochs 20
    ```

    Supported model types:

    - `nerfacto`
    - `instant-ngp`
    - `splatfacto`

3. Exporting 3D Objects

    To export the trained model to a 3D object (e.g., TSDF Fusion or Poisson surface reconstruction):

    ```bash
    python main.py export_object --export_type tsdf --config_path /path/to/model/CONFIG.yml --output_dir /path/to/export_output
    ```

    Supported export types:

    - `tsdf`: TSDF Fusion for mesh export.
    - `poisson`: Poisson surface reconstruction for high-quality mesh export.
    - `pointcloud`: Export as a point cloud.

### Conda Environment Setup

To ensure all dependencies are properly installed, use a **conda environment**. Here's a basic setup:

```bash
conda create -n nerfstudio python=3.8
conda activate nerfstudio
pip install nerfstudio
```

Make sure the ffmpeg path is properly set in your environment. You can add the following line to your .bashrc or .zshrc file:

```bash
export PATH="$HOME/nerf/nerf_playground/ffmpeg_build/bin:$PATH"
```

## License

The scripts are licensed under the Apache 2.0 License, following the same licensing as Nerfstudio.
