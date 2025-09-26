# Dataset Setup: ICDAR 2019 MLT

This directory is intended to hold the raw and processed datasets for the PaddleOCR training pipeline. The raw data is not checked into Git.

## 1. Data Source

The primary dataset used for this project is the **ICDAR 2019 Multilingual Scene Text Dataset (MLT)**.

- **Official Website:** [ICDAR 2019 Robust Reading Challenge](https://rrc.cvc.uab.es/?ch=15)
- **Task:** Task 1 - Text in the Wild (Multi-lingual)

You will need to register on the site to download the training images and ground truth files.

## 2. Setup Instructions

1.  **Download:** Download the "Training Set images" and "Training Set ground truth" from the challenge website.
2.  **Unzip:** Unzip the contents. You should have a folder with all the training images (`train_*.jpg`) and a `train_gt.txt` file.
3.  **Organize:** Create a directory `data/icdar2019_mlt/` and place the `train_gt.txt` file and a sub-folder containing all training images inside it. The structure should look like this:
    ```
    data/
    └── icdar2019_mlt/
        ├── train/
        │   ├── train_00001.jpg
        │   └── ...
        └── train_gt.txt
    ```

## 3. Formatting

After setting up the raw data, run the preparation script from the root directory:

```bash
python scripts/prepare_icdar_data.py
