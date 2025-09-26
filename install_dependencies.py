# install_dependencies.py
import subprocess
import sys
import os

def install_requirements(requirements_path="requirements.txt"):
    """
    Reads a requirements.txt file and installs the packages using pip.

    Args:
        requirements_path (str): The path to the requirements.txt file.
    """
    if not os.path.exists(requirements_path):
        print(f"Error: The file '{requirements_path}' was not found.")
        print("Please make sure you are running this script from the main PaddleOCR directory.")
        return

    try:
        print(f"--- Installing packages from {requirements_path} ---")
        
        # Using sys.executable ensures we use the pip from the correct virtual environment
        # The command will be, for example: C:\path\to\venv\python.exe -m pip install -r requirements.txt
        command = [sys.executable, "-m", "pip", "install", "-r", requirements_path]

        # Execute the command
        subprocess.check_call(command)

        print("\n--- ✅ All required libraries have been successfully installed. ---")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    install_requirements()