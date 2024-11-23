import os 
import logging 
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)  # Split directory and file name

    # Ensure the directory exists
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)  # Create only the directory
        logging.info(f"Creating directory {filedir} for the file {filename}")

    # Create the file if it doesn't exist or if it is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, 'w') as f:
            pass  # Create an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
