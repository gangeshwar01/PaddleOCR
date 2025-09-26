import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Debug dataset paths for PaddleOCR.")
parser.add_argument("--data_path", type=str, required=True, help="Path to the root of the dataset.")
args = parser.parse_args()

data_path = Path(args.data_path)
train_images_dir = data_path / "TrainImages"
train_gt_dir = data_path / "TrainGT"

print("--- DEBUGGING FILE PATHS ---")

# 1. Check if the main directories exist
print(f"\n[1] Checking for directories...")
print(f"Image directory path: '{train_images_dir}' | Exists: {train_images_dir.exists()}")
print(f"Annotation directory path: '{train_gt_dir}' | Exists: {train_gt_dir.exists()}")

# 2. List first 5 items in the image directory
print("\n[2] Listing first 5 items in the Image Directory:")
if train_images_dir.exists():
    image_items = list(train_images_dir.iterdir())[:5]
    if not image_items:
        print("  -> DIRECTORY IS EMPTY!")
    for item in image_items:
        print(f"  -> Found: {item.name}")
else:
    print("  -> Directory not found.")

# 3. List first 5 items in the annotation directory
print("\n[3] Listing first 5 items in the Annotation Directory:")
if train_gt_dir.exists():
    gt_items = list(train_gt_dir.iterdir())[:5]
    if not gt_items:
        print("  -> DIRECTORY IS EMPTY!")
    for item in gt_items:
        print(f"  -> Found: {item.name}")
else:
    print("  -> Directory not found.")

# 4. Attempt to match one file to see the logic
print("\n[4] Attempting to match the first image to its annotation:")
if train_images_dir.exists():
    first_image = next(train_images_dir.glob("*.jpg"), None)
    if not first_image:
        first_image = next(train_images_dir.glob("*.png"), None)
    
    if first_image:
        print(f"  -> Found an image file: '{first_image.name}'")
        expected_gt_name = first_image.stem + ".txt"
        expected_gt_path = train_gt_dir / expected_gt_name
        print(f"  -> Script expects a corresponding annotation named: '{expected_gt_name}'")
        print(f"  -> Checking if it exists at '{expected_gt_path}' | Exists: {expected_gt_path.exists()}")
    else:
        print("  -> Could not find any .jpg or .png images in the Image Directory.")
else:
    print("  -> Image directory not found.")

print("\n--- END OF DEBUG ---")