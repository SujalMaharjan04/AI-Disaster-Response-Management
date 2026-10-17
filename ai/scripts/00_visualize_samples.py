import json
import os
import random
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def visualize_xview2_samples():
    # Paths
    images_dir = Path("data/raw/xView2/train/images")
    labels_dir = Path("data/raw/xView2/train/labels")
    output_dir = Path("ai/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Target event types
    target_events = ["flood", "earthquake"]

    # Find all post-disaster json files
    all_labels = list(labels_dir.glob("*_post_disaster.json"))

    # Filter labels by target events
    filtered_labels = [l for l in all_labels if any(k in l.name.lower() for k in target_events)]

    if not filtered_labels:
        print("No target labels found for visualization.")
        return

    # Pick a few random samples
    samples = random.sample(filtered_labels, min(4, len(filtered_labels)))

    # Damage class colors: 0: Green, 1: Yellow, 2: Orange, 3: Red
    colors = {
        0: (0, 255, 0),   # Green - No Damage
        1: (0, 255, 255), # Yellow - Minor
        2: (0, 165, 255), # Orange - Major
        3: (0, 0, 255)    # Red - Destroyed
    }

    for idx, label_path in enumerate(samples):
        # Construct image path
        # label: event-name_index_post_disaster.json -> image: event-name_index_post_disaster.png
        img_name = label_path.stem + ".png"
        img_path = images_dir / img_name

        if not img_path.exists():
            print(f"Image not found: {img_path}")
            continue

        # Load image
        image = cv2.imread(str(img_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Load label
        with open(label_path, 'r') as f:
            data = json.load(f)

        # Process labels
        # Depending on xView2 JSON structure, we look for building polygons
        buildings = data.get('buildings', []) if 'buildings' in data else data.get('polygons', [])

        for b in buildings:
            damage_class = b.get('damage_class')
            poly = b.get('polygon') # Expecting list of [x, y]

            if damage_class is not None and poly is not None:
                pts = np.array(poly, np.int32).reshape((-1, 1, 2))
                color = colors.get(damage_class, (255, 255, 255))
                cv2.polylines(image, [pts], isClosed=True, color=color, thickness=2)

        # Plot
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.title(f"Sample {idx+1}: {label_path.name}\nColors: 0-Green, 1-Yellow, 2-Orange, 3-Red")
        plt.axis('off')

        # Save
        save_path = output_dir / f"sample_{idx+1}_{label_path.stem}.png"
        plt.savefig(save_path)
        plt.close()
        print(f"Saved visualization to {save_path}")

if __name__ == "__main__":
    visualize_xview2_samples()
