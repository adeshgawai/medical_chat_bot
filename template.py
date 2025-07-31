import os
import logging
from pathlib import Path
import time

# Configure the logging settings
# This will create log messages with a timestamp, log level, and the message itself.
log_format = "[%(asctime)s] - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format
)

# The root directory for your project.
# This script will create the structure in the same directory where it is run.
project_name = "." 

# List of files and directories to create
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]

for filepath_str in list_of_files:
    # Convert the string path to a Path object for OS-agnostic handling
    filepath = Path(filepath_str)
    
    # Get the directory part of the file path
    filedir = filepath.parent
    
    # Create the directory if it doesn't exist
    # The check for filedir ensures we don't try to create a directory for top-level files
    if filedir and not os.path.exists(filedir):
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")
        
    # Create the file if it doesn't exist or if it's empty
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, "w") as f:
            pass  # Create an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filepath} already exists. Skipping.")

logging.info("Project structure setup is complete!")
