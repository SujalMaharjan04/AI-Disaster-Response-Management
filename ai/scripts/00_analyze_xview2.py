import json
import os
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm
import pandas as pd

def analyze_xview2():
    # Paths
    labels_dir = Path("data/raw/xView2/train/labels")

    if not labels_dir.exists():
        print(f"Error: Labels directory {labels_dir} not found.")
        return

    # Filter keywords
    target_events = ["flood", "earthquake"]

    # Statistics containers
    event_counts = defaultdict(int)
    class_distribution = defaultdict(int)
    total_images = 0

    # List all json files
    json_files = list(labels_dir.glob("*.json"))
    print(f"Found {len(json_files)} total label files.")

    for json_file in tqdm(json_files, desc="Analyzing labels"):
        # Extract event name from filename: event-name_index_disaster_type.json
        filename = json_file.name
        event_name = filename.split('_')[0]

        # Only process flood and earthquake
        if not any(keyword in event_name.lower() for keyword in target_events):
            continue

        # Only process post-disaster images for damage assessment
        if "post_disaster" not in filename:
            continue

        total_images += 1
        event_counts[event_name] += 1

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # xView2 format usually has a list of buildings with damage classes
            # We expect a structure where building labels are provided
            if 'buildings' in data:
                for b in data['buildings']:
                    damage_class = b.get('damage_class')
                    if damage_class is not None:
                        class_distribution[damage_class] += 1
            elif 'polygons' in data: # Some versions use polygons list
                for p in data['polygons']:
                    damage_class = p.get('damage_class')
                    if damage_class is not None:
                        class_distribution[damage_class] += 1
            else:
                # If the structure differs, we might need to adjust this.
                # Some xView2 labels are in a different format.
                pass

        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Print Summary Report
    print("\n" + "="*40)
    print("XVIEW2 DATASET ANALYSIS REPORT")
    print("="*40)
    print(f"Total Target Images (Flood/Earthquake, Post-Disaster): {total_images}")

    print("\n--- Event Distribution ---")
    # Sort by count descending
    sorted_events = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
    for event, count in sorted_events:
        print(f"{event: <30} | {count} images")

    print("\n--- Damage Class Distribution ---")
    # Classes: 0: No Damage, 1: Minor, 2: Major, 3: Destroyed
    class_map = {0: "No Damage", 1: "Minor Damage", 2: "Major Damage", 3: "Destroyed"}
    for cls in sorted(class_distribution.keys()):
        count = class_distribution[cls]
        percentage = (count / sum(class_distribution.values())) * 100 if class_distribution else 0
        print(f"{class_map.get(cls, f'Class {cls}'): <20} | {count: >8} ({percentage:.2f}%)")

    print("="*40)

if __name__ == "__main__":
    analyze_xview2()
