import os
from pathlib import Path
import shutil

def verify_dataset_structure(dataset_path):
    """
    Verifies that the dataset follows the YOLO segmentation format.
    dataset_path: Path to 'data/processed/multi_hazards'
    """
    path = Path(dataset_path)
    required = [
        'images/train', 'images/val', 'images/test',
        'labels/train', 'labels/val', 'labels/test'
    ]

    missing = []
    for req in required:
        if not (path / req).exists():
            missing.append(req)

    if missing:
        return False, f"Missing directories: {', '.join(missing)}"

    return True, "Dataset structure verified."

def setup_colab_paths(drive_mount_point="/content/drive/MyDrive/xview2_processed"):
    """
    Ensures paths in dataset.yaml are updated to match Google Drive mounting point.
    """
    yaml_path = Path("ai/datasets/dataset.yaml")
    if not yaml_path.exists():
        return "Error: dataset.yaml not found."

    with open(yaml_path, 'r') as f:
        content = f.read()

    # Replace relative path with Colab Drive path
    new_content = content.replace("path: data/processed/multi_hazards", f"path: {drive_mount_point}")

    with open(yaml_path, 'w') as f:
        f.write(new_content)

    return f"Updated dataset.yaml path to {drive_mount_point}"
