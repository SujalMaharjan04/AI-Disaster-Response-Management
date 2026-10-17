import json
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def normalize_polygon(polygon, width, height):
    """
    Normalize polygon coordinates to [0, 1] relative to image size.
    polygon: list of [x, y] pairs
    """
    normalized = []
    for x, y in polygon:
        nx = x / width
        ny = y / height
        # Clip to [0, 1] to avoid YOLO errors
        nx = max(0.0, min(1.0, nx))
        ny = max(0.0, min(1.0, ny))
        normalized.append(f"{nx:.6f} {ny:.6f}")

    return " ".join(normalized)

def convert_json_to_yolo(json_path, image_width, image_height):
    """
    Converts an xView2 JSON label file to YOLO segmentation format.
    Returns a list of strings, one for each building.
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Extract buildings from either 'buildings' or 'polygons' key
        buildings = data.get('buildings', []) if 'buildings' in data else data.get('polygons', [])

        yolo_lines = []
        for b in buildings:
            damage_class = b.get('damage_class')
            polygon = b.get('polygon')

            if damage_class is not None and polygon is not None:
                # Ensure damage_class is within [0, 3]
                if 0 <= damage_class <= 3:
                    norm_poly = normalize_polygon(polygon, image_width, image_height)
                    yolo_lines.append(f"{damage_class} {norm_poly}")

        return yolo_lines
    except Exception as e:
        logger.error(f"Error converting {json_path}: {e}")
        return []
