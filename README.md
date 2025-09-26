# End-to-End PaddleOCR Training for Scene Text Recognition

This project provides a complete workflow for training custom text detection and recognition models using the PaddleOCR framework. It covers architecture study, dataset preparation (ICDAR 2019 MLT), model training, and evaluation, all packaged within a reproducible repository and a Kaggle/Colab notebook.



## 🚀 Features

- **Architecture Deep Dive:** Detailed notes on PP-OCRv3/v5 components (DB Detector, CRNN Recognizer).
- **Data Preparation:** A Python script to convert ICDAR 2019 MLT dataset annotations into the required PaddleOCR format.
- **Reproducible Training:** Custom configuration files for training detection and recognition models.
- **End-to-End Notebook:** A single notebook (`notebooks/PaddleOCR_Training_Workflow.ipynb`) that handles setup, data prep, training, and visualization.
- **Comprehensive Report:** A PDF report generated with LaTeX summarizing the methodology and findings.

## 📁 Repository Structure

.
├── PaddleOCR/              # Git submodule or clone of the official PaddleOCR repo
├── configs/                # Your custom training configuration files
│   ├── my_icdar_det_config.yml
│   └── my_icdar_rec_config.yml
├── data/                   # Dataset files (should be git-ignored)
│   ├── README.md           # Instructions on how to get and format the data
│   ├── train.txt           # Generated training labels
│   ├── val.txt             # Generated validation labels
│   └── icdar2019_mlt/      # Raw downloaded dataset lives here
│       └── ...
├── notebooks/              # Your Colab/Kaggle notebook(s)
│   └── PaddleOCR_Training_Workflow.ipynb
├── output/                 # Trained models, logs, visualizations (git-ignored)
│   ├── detection_model/
│   └── recognition_model/
├── report/                 # Your final PDF report and its source
│   ├── report.tex
│   ├── report.pdf
│   └── assets/
│       └── pipeline_diagram.drawio.png
├── scripts/                # Helper Python scripts
│   ├── prepare_icdar_data.py
│   └── visualize_results.py
├── .gitignore              # Specifies files for Git to ignore
└── README.md               # Main project README file

- **/PaddleOCR/**: A clone of the official PaddleOCR repository.
- **/configs/**: Custom YAML configuration files for training.
- **/data/**: Directory for storing and preparing datasets (see `data/README.md`).
- **/notebooks/**: Contains the main Jupyter/Colab notebook.
- **/output/**: Default location for saved models, logs, and visualizations (git-ignored).
- **/report/**: LaTeX source and final PDF report.
- **/scripts/**: Helper scripts for data preparation and result visualization.

## 🛠️ Setup and Usage

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/your-username/paddleocr-study.git](https://github.com/your-username/paddleocr-study.git)
    cd paddleocr-study
    ```

2.  **Clone the PaddleOCR repository:**
    ```bash
    git clone [https://github.com/PaddlePaddle/PaddleOCR.git](https://github.com/PaddlePaddle/PaddleOCR.git)
    ```

3.  **Set up the environment:**
    ```bash
    cd PaddleOCR
    pip install -r requirements.txt
    # Install paddlepaddle-gpu if you have a CUDA-enabled GPU
    # python3 -m pip install paddlepaddle-gpu
    cd ..
    ```

4.  **Download the dataset:**
    - Download the ICDAR 2019 MLT dataset from the official source.
    - Place the unzipped contents into the `data/icdar2019_mlt/` directory.

5.  **Run the Notebook:**
    - Open `notebooks/PaddleOCR_Training_Workflow.ipynb` in Google Colab, Kaggle, or a local Jupyter environment.
    - Follow the steps inside the notebook to prepare data, train the models, and evaluate the results.

##  deliverables

- **Code:** All scripts, configs, and notebooks are provided in this repository.
- **Report:** The final detailed report is available at `report/report.pdf`.
- **Trained Weights:** Sample trained model weights can be found in the `output/` directory after running the training pipeline.
