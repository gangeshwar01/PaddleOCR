# scripts/prepare_icdar_data.py
import os
import json
import random
import argparse # New: Imported argparse to handle command-line arguments
from pathlib import Path

def create_ppocr_labels_from_individual_files(dataset_path, output_path, val_split=0.1):
    """
    Scans for images and their corresponding individual .txt annotation files,
    then converts them into PaddleOCR's required label format.
    """
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)
    output_path.mkdir(exist_ok=True)

    # Define paths based on the described folder structure
    train_images_dir = dataset_path / "TrainImages"
    train_gt_dir = dataset_path / "TrainGT"

    if not train_images_dir.exists() or not train_gt_dir.exists():
        print(f"Error: Could not find 'TrainImages' or 'TrainGT' inside the path: {dataset_path}")
        print("Please ensure your --data_path is correct and contains these subfolders.")
        return

    image_annotations = {}
    print(f"Reading images from: {train_images_dir}")
    print(f"Reading annotations from: {train_gt_dir}")

    # Iterate through all image files in the training directory
    image_files = list(train_images_dir.glob("*.jpg"))
    if not image_files:
        image_files = list(train_images_dir.glob("*.png"))

    for img_path in image_files:
        # Construct the path for the corresponding annotation file
        gt_filename = img_path.stem + ".txt"
        gt_path = train_gt_dir / gt_filename
        
        if not gt_path.exists():
            continue

        annotations_for_image = []
        with open(gt_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    parts = line.split(',', 8)
                    points = [int(p) for p in parts[0:8]]
                    transcription = parts[8]

                    if transcription in ('###', '---'):
                        continue

                    formatted_points = [[points[i], points[i+1]] for i in range(0, 8, 2)]
                    
                    annotation = {
                        "transcription": transcription,
                        "points": formatted_points
                    }
                    annotations_for_image.append(annotation)
                except (ValueError, IndexError):
                    print(f"Warning: Malformed line in {gt_path.name}, skipping line: '{line}'")

        if annotations_for_image:
            # IMPORTANT: For PaddleOCR, the image paths in the label file must be correct
            # We will use the absolute path to avoid any issues.
            image_annotations[str(img_path.resolve())] = annotations_for_image

    print(f"Successfully processed {len(image_annotations)} images with annotations.")

    image_paths = list(image_annotations.keys())
    random.shuffle(image_paths)
    split_idx = int(len(image_paths) * (1 - val_split))
    train_paths = image_paths[:split_idx]
    val_paths = image_paths[split_idx:]

    for split, paths in [("train", train_paths), ("val", val_paths)]:
        label_file = output_path / f"{split}.txt"
        with open(label_file, 'w', encoding='utf-8') as f:
            for path in paths:
                json_string = json.dumps(image_annotations[path], ensure_ascii=False)
                f.write(f"{path}\t{json_string}\n")
        print(f"Successfully created {label_file} with {len(paths)} entries.")

if __name__ == '__main__':
    # New: Use argparse to get paths from the command line
    parser = argparse.ArgumentParser(description="Prepare dataset for PaddleOCR.")
    parser.add_argument("--data_path", type=str, required=True, help="Path to the root of the dataset (containing TrainImages and TrainGT).")
    parser.add_argument("--output_path", type=str, default="./data", help="Path to save the generated train.txt and val.txt files.")
    args = parser.parse_args()

    create_ppocr_labels_from_individual_files(args.data_path, args.output_path)