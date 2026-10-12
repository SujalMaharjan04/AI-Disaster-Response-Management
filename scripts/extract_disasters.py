from pathlib import Path
import shutil

SOURCE = Path("data/raw/xView2/train")

IMAGE_DIR = SOURCE / "images"
LABEL_DIR = SOURCE / "labels"

OUTPUT = Path("data/processed/multi_hazards")

DISASTERS = [
    "flood",
    "earthquake"
]

for folder in ["images", "labels"]:
    (OUTPUT / folder).mkdir(parents=True, exist_ok=True)

for image in IMAGE_DIR.glob("*.png"):
    name = image.name.lower()

    if not any(d in name for d in DISASTERS):
        continue

    shutil.copy2(image, OUTPUT / "images" / image.name)

    label = LABEL_DIR / image.with_suffix(".json").name

    if label.exists():
        shutil.copy2(label, OUTPUT / "labels" / label.name)


print("Extraction Complete")