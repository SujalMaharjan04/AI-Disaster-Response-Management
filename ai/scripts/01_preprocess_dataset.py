import os
import shutil
import random
import cv2
import json
from pathlib import Path
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from ai.preprocessing.yolo_converter import convert_json_to_yolo

def setup_dirs(base_dir):
    """Creates the YOLO directory structure."""
    splits = ['train', 'val', 'test']
    for split in splits:
        (base_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
        (base_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)

def preprocess():
    # Configuration
    raw_labels_dir = Path("data/raw/xView2/train/labels")
    raw_images_dir = Path("data/raw/xView2/train/images")
    processed_dir = Path("data/processed/multi_hazards")

    target_events = ["flood", "earthquake"]

    if not raw_labels_dir.exists():
        print(f"Error: Labels directory {raw_labels_dir} not found.")
        return

    # 1. Identify target image-label pairs
    print("Filtering dataset for flood and earthquake events...")
    pairs = []
    all_jsons = list(raw_labels_dir.glob("*_post_disaster.json"))

    for jl in all_jsons:
        event_name = jl.name.split('_')[0]
        if any(k in event_name.lower() for k in target_events):
            img_name = jl.stem + ".png"
            img_path = raw_images_dir / img_name
            if img_path.exists():
                pairs.append((img_path, jl))

    print(f"Found {len(pairs)} valid target image-label pairs.")

    # 2. Split dataset (80% train, 10% val, 10% test)
    train_pairs, temp_pairs = train_test_split(pairs, train_size=0.8, random_state=42)
    val_pairs, test_pairs = train_test_split(temp_pairs, train_size=0.5, random_state=42)

    splits = {
        'train': train_pairs,
        'val': val_pairs,
        'test': test_pairs
    }

    setup_dirs(processed_dir)

    # 3. Process and move files
    for split, pair_list in splits.items():
        print(f"Processing {split} split ({len(pair_list)} images)...")
        for img_path, lbl_path in tqdm(pair_list):
            # Load image to get dimensions
            img = cv2.imread(str(img_path))
            if img is None:
                continue
            h, w = img.shape[:2]

            # Convert labels to YOLO format
            yolo_labels = convert_json_to_yolo(lbl_path, w, h)

            if not yolo_labels:
                continue # Skip images without valid building labels

            # Define output paths
            dest_img_path = processed_dir / 'images' / split / img_path.name
            dest_lbl_path = processed_dir / 'labels' / split / (lbl_path.stem + ".txt")

            # Save image
            shutil.copy(img_path, dest_img_path)

            # Save label
            with open(dest_lbl_path, 'w') as f:
                f.write("\n".join(yolo_labels))

    print("\nPreprocessing complete!")
    print(f"Processed data saved to: {processed_dir}")

if __name__ == "__main__":
    preprocess()
