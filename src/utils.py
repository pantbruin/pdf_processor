import os
import sys

def are_env_variables_set():
    """
    Check if the required environment variables are set.
    
    Returns:
        bool: True if all required environment variables are set, False otherwise.
    """
    required_env_vars = [
        "INPUT_DIR",
        "OUTPUT_DIR",
    ]

    for env_var in required_env_vars:
        if not os.getenv(env_var):
            print(f"ERROR: Environment variable '{env_var}' is not set in batch script file.")
            input("Press the ENTER key to exit...")
            sys.exit(1)
    return True


def are_env_variables_valid():
    """
    Check if the environment variables are valid.
    
    Returns:
        bool: True if all environment variables are valid, False otherwise.
    """
    input_dir = os.getenv("INPUT_DIR")
    output_dir = os.getenv("OUTPUT_DIR")

    if not os.path.isdir(input_dir):
        print(f"Input directory '{input_dir}' does not exist or is not a directory.")
        return False

    if not os.path.isdir(output_dir):
        print(f"Output directory '{output_dir}' does not exist or is not a directory.")
        return False

    return True