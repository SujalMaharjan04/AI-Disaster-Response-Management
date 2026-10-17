from pathlib import Path
import json

import cv2
import numpy as np
from PIL import Image
from shapely import wkt
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]      # works from any working dir
SRC = ROOT / "../data/processed/multi_hazards"
MASK_DIR = ROOT / "../data/processed/masks"
MASK_DIR.mkdir(parents=True, exist_ok=True)

CLASS_MAP = {"no-damage": 1, "minor-damage": 2,
             "major-damage": 3, "destroyed": 4}
IGNORE = 255                                    # un-classified buildings

def parts(geom):
    return list(geom.geoms) if hasattr(geom, "geoms") else [geom]

for label in tqdm(sorted((SRC / "labels").glob("*_post_disaster.json"))):
    img_path = SRC / "images" / f"{label.stem}.png"
    if not img_path.exists():
        continue
    w, h = Image.open(img_path).size
    mask = np.zeros((h, w), dtype=np.uint8)

    data = json.loads(label.read_text())
    for feat in data["features"]["xy"]:
        props = feat.get("properties", {})
        if props.get("feature_type") != "building":
            continue
        cls = CLASS_MAP.get(props.get("subtype"), IGNORE)
        for poly in parts(wkt.loads(feat["wkt"])):
            if poly.is_empty:
                continue
            pts = np.round(np.array(poly.exterior.coords)).astype(np.int32)
            cv2.fillPoly(mask, [pts], int(cls))

    cv2.imwrite(str(MASK_DIR / f"{label.stem}.png"), mask)