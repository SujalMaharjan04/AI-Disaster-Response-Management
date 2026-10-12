from pathlib import Path
from collections import Counter

IMAGE_DIR = Path("data/raw/xView2/train/images")

events = Counter()


for image in IMAGE_DIR.glob("*.png"):
    name = image.name

    event = (
        name.replace("_pre_disaster.png", "").replace("_post_disaster.png", "")
    )

    event = event.rsplit("_", 1)[0]

    events[event] += 1

print("\nDisaster Event Found:")
print("------------------------")

for event, count in events.items():
    print(f"{event}: {count}")