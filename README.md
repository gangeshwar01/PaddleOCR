# End-to-End PaddleOCR Training for Scene Text Recognition

This repository provides a complete, reproducible workflow for training custom scene text detection models using the powerful **PaddleOCR** framework. It guides you from initial setup and data preparation to model training and inference, using the ICDAR 2019 MLT dataset as a primary example.

## 🚀 Features

  * **Architecture Deep Dive:** Detailed notes on PP-OCR system components (DB Detector, CRNN Recognizer).
  * **Automated Data Handling:** Includes Python scripts to download and prepare datasets for training.
  * **Reproducible Training:** Provides custom configuration files tailored for stable and efficient training.
  * **Comprehensive Workflow:** A clear, step-by-step guide covering the entire process from setup to a fully trained model.
  * **Troubleshooting Guide:** Includes solutions for common errors related to paths, dependencies, and environment setup.

-----

## 📁 Repository Structure

The project is organized to keep custom scripts and configurations separate from the official PaddleOCR library code.

```
.
├── PaddleOCR/              # A clone of the official PaddleOCR repository
│   ├── ppocr/              # The core library code
│   ├── tools/
│   │   └── train.py        # The main training script
│   └── setup.py
│
├── configs/                # Your custom training configuration files
│   └── my_icdar_det_config.yml
│
├── data/                   # Directory for datasets (git-ignored)
│   └── icdar2019_mlt/      # Raw dataset lives here
│
├── scripts/                # Helper Python scripts
│   ├── download.py         # Script to download the dataset
│   └── prepare_icdar_data.py # Script to format labels
│
├── output/                 # Saved models and logs (git-ignored)
├── venv/                   # Python virtual environment (git-ignored)
└── README.md               # This guide
```

-----

## 🛠️ Complete Training Workflow

Follow these steps in order to set up the project and train your model. All commands are intended for a PowerShell terminal on Windows.

### Step 1: Initial Setup

First, clone this repository and the official PaddleOCR repository inside it.

```powershell
# Clone your project repository
git clone https://github.com/your-username/paddleocr-study.git
cd paddleocr-study

# Clone the official PaddleOCR repository into a subfolder
git clone https://github.com/PaddlePaddle/PaddleOCR.git
```

### Step 2: Environment Setup

We'll create an isolated Python virtual environment to manage dependencies.

```powershell
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate

# Install PaddleOCR and all its dependencies in editable mode
# This is the most reliable way to ensure all modules are found.
cd PaddleOCR
pip install -e .

# Recommended: Upgrade PaddlePaddle to the latest version to avoid errors
pip install --upgrade paddlepaddle
```

### Step 3: Download the Dataset

Run the provided script to automatically download and unzip the ICDAR 2019 MLT dataset.

```powershell
# IMPORTANT: Navigate back to your project's root directory first
cd ..

# Run the download script
python scripts/download.py
```

### Step 4: Prepare Data Labels

This script converts the raw dataset labels into the format required by PaddleOCR.

```powershell
# Run the preparation script from the root directory
python scripts/prepare_icdar_data.py
```

This will generate `train.txt` and `val.txt` inside the `data/` folder.

### Step 5: Download Pre-trained Backbone

For best results, we start with a model pre-trained on ImageNet.

```powershell
# Navigate into the PaddleOCR directory
cd PaddleOCR

# Create the directory for pre-trained models
New-Item -ItemType Directory -Force -Path ./pretrain_models

# Download the model weights using PowerShell
Invoke-WebRequest -Uri https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/MobileNetV3_large_x0_5_pretrained.pdparams -OutFile ./pretrain_models/MobileNetV3_large_x0_5_pretrained.pdparams
```

### Step 6: Start Training\!

You are now ready to train the model.

```powershell
# Ensure you are still inside the D:\...\paddleocr-study\PaddleOCR> directory
# Run the training script, pointing it to your custom config file
python tools/train.py -c ../configs/my_icdar_det_config.yml
```

You will see the training process begin, with the loss decreasing over time. Your trained models will be saved in the `output/` directory.

-----

## 🚨 Troubleshooting

If you encounter an error, check here first.

  * **`FileNotFoundError: ... tools/train.py`**

      * **Cause:** You are in the wrong directory.
      * **Solution:** You must be **inside** the `PaddleOCR` folder when you run the training command. Use `cd PaddleOCR`.

  * **`ModuleNotFoundError: No module named 'ppocr'` or `'yaml'`**

      * **Cause:** Dependencies are not installed correctly in your virtual environment.
      * **Solution:** Make sure your `venv` is activated. Navigate into the `PaddleOCR` folder and run `pip install -e .`.

  * **`ImportError: cannot import name ...`**

      * **Cause:** The installed `paddlepaddle` version is out of sync with the PaddleOCR library.
      * **Solution:** Run `pip install --upgrade paddlepaddle` to get the latest version.

  * **Script processes "0 images"**

      * **Cause:** The dataset folder structure is incorrect.
      * **Solution:** Ensure your data is located at `data/icdar2019_mlt/` and that the `TrainImages` and `TrainGT` folders are directly inside it.
