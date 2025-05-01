import os
import sys
import pymupdf
from pathlib import Path

def are_env_variables_set():
    """
    Check if the required environment variables are set.
    
    Returns:
        bool: True if all required environment variables are set, False otherwise.
    """
    required_env_vars = [
        "INPUT_PATH",
        "OUTPUT_DIR",
    ]

    for env_var in required_env_vars:
        if not os.getenv(env_var):
            print(f"ERROR: Environment variable '{env_var}' is not set in batch script file.")
            input("Press the ENTER key to exit...")
            sys.exit(1)
    return True


def input_path_is_valid():
    input_path = os.getenv("INPUT_PATH")
    # 1) Check that the input path exists and is a file
    if not os.path.exists(input_path) or not os.path.isfile(input_path):
        print(f"ERROR: The input path '{input_path}' does not exist or is not a file.")
        return False

    # 2) Try opening it as a PDF
    try:
        doc = pymupdf.open(str(input_path), filetype="pdf")
        doc.close()
        return True
    except Exception:
            print(f"ERROR: Could not open the input file '{input_path}' as a PDF.")
            print("Please check the file format and try again.")
            input("Press the ENTER key to exit...")
            sys.exit(1)


def verify_output_path() -> Path:
    """
    Ensure the given path
     - exists (or can be created),
     - is a directory,
     Returns a Path object on success or exits the program with an error.
    """
    output_path = os.getenv("OUTPUT_DIR")
    p = Path(f'{output_path}/ProcessedInvoices/')

    # 1) If it doesn’t exist, try to create it (mkdir -p behavior)
    if not p.exists():
        try:
            p.mkdir(parents=True, exist_ok=True)
            print(f"INFO: Created output directory {p.resolve()}.")
        except Exception as e:
            sys.exit(f"ERROR: Could not create output directory {p!r}: {e}")

    # 2) It must be a directory
    if not p.is_dir():
        sys.exit(f"ERROR: Output path {p!r} exists but is not a directory.")

    #set environment variable to the new path
    os.environ["OUTPUT_DIR"] = p.resolve()
    return p