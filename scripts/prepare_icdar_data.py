# scripts/prepare_icdar_data.py
import os
import json
import random
from pathlib import Path

def create_ppocr_labels(dataset_path, output_path, val_split=0.1):
    """
    Converts ICDAR 2019 MLT training data to PaddleOCR detection format.
    The ground truth file is expected to be named 'train_gt.txt'.
    """
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)
    output_path.mkdir(exist_ok=True)

    gt_file = dataset_path / "train_gt.txt"
    if not gt_file.exists():
        print(f"Error: Ground truth file not found at {gt_file}")
        return

    image_annotations = {}
    print("Reading ground truth file...")
    with open(gt_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',', 9)
            image_name = f"train_{parts[0]}.jpg"
            points = [int(p) for p in parts[1:9]]
            transcription = parts[9]

            # Format points as [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            formatted_points = [[points[i], points[i+1]] for i in range(0, 8, 2)]

            # Ignore illegible text as per PaddleOCR convention
            if transcription == '###':
                continue

            annotation = {
                "transcription": transcription,
                "points": formatted_points
            }

            if image_name not in image_annotations:
                image_annotations[image_name] = []
            image_annotations[image_name].append(annotation)

    print(f"Processed {len(image_annotations)} unique images.")

    # Create train/val split
    image_names = list(image_annotations.keys())
    random.shuffle(image_names)
    split_idx = int(len(image_names) * (1 - val_split))
    train_keys = image_names[:split_idx]
    val_keys = image_names[split_idx:]

    # Write label files
    for split, keys in [("train", train_keys), ("val", val_keys)]:
        label_file = output_path / f"{split}.txt"
        with open(label_file, 'w', encoding='utf-8') as f:
            for key in keys:
                # The image path should be relative to where the training script is run
                # Or provide an absolute path. Here we assume the data dir is specified in the config.
                relative_image_path = os.path.join("icdar2019_mlt", "train", key)
                json_string = json.dumps(image_annotations[key], ensure_ascii=False)
                f.write(f"{relative_image_path}\t{json_string}\n")
        print(f"Successfully created {label_file} with {len(keys)} entries.")


if __name__ == '__main__':
    # These paths should be adjusted based on your project structure
    # Typically, the raw data is in data/icdar2019_mlt and labels are written to data/
    RAW_DATA_PATH = './data/icdar2019_mlt'
    OUTPUT_PATH = './data'
    create_ppocr_labels(RAW_DATA_PATH, OUTPUT_PATH)
