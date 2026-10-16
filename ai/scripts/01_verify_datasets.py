from pathlib import Path
from PIL import Image
from tqdm import tqdm
import json


# ---------------------------------------------------
# Dataset location
# ---------------------------------------------------

DATASET_ROOT = Path("../data/processed/multi_hazards")

IMAGE_DIR = DATASET_ROOT / "images"
LABEL_DIR = DATASET_ROOT / "labels"


# ---------------------------------------------------
# Counters
# ---------------------------------------------------

pre_images = 0
post_images = 0
labels = 0

missing_labels = []
corrupted_images = []
invalid_json = []


# ---------------------------------------------------
# Verify folders
# ---------------------------------------------------

print("=" * 60)
print("VERIFYING MULTI HAZARD DATASET")
print("=" * 60)


if not IMAGE_DIR.exists():
    raise FileNotFoundError(
        f"Missing image folder: {IMAGE_DIR}"
    )


if not LABEL_DIR.exists():
    raise FileNotFoundError(
        f"Missing label folder: {LABEL_DIR}"
    )


# ---------------------------------------------------
# Check images
# ---------------------------------------------------

image_files = list(IMAGE_DIR.glob("*"))

print(f"\nFound {len(image_files)} files")


for image_path in tqdm(image_files):

    filename = image_path.stem


    # Count images

    if "pre_disaster" in filename:
        pre_images += 1

    elif "post_disaster" in filename:

        post_images += 1


        # Check corresponding label

        label_path = LABEL_DIR / f"{filename}.json"


        if label_path.exists():

            labels += 1


            try:

                with open(label_path) as f:
                    json.load(f)

            except Exception:

                invalid_json.append(
                    str(label_path)
                )


        else:

            missing_labels.append(
                str(label_path)
            )


    # Verify image

    try:

        img = Image.open(image_path)
        img.verify()

    except Exception:

        corrupted_images.append(
            str(image_path)
        )


# ---------------------------------------------------
# Report
# ---------------------------------------------------

print("\n")
print("=" * 60)
print("DATASET SUMMARY")
print("=" * 60)

print(f"Pre-disaster images  : {pre_images}")
print(f"Post-disaster images : {post_images}")
print(f"JSON labels          : {labels}")

print("=" * 60)

print(
    f"Missing labels       : {len(missing_labels)}"
)

print(
    f"Corrupted images     : {len(corrupted_images)}"
)

print(
    f"Invalid JSON         : {len(invalid_json)}"
)

print("=" * 60)


if missing_labels:
    print("\nExample missing labels:")
    for item in missing_labels[:5]:
        print(item)


if invalid_json:
    print("\nExample invalid JSON:")
    for item in invalid_json[:5]:
        print(item)


print("\nVerification complete.")