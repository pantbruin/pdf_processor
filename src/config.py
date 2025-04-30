from dotenv import load_dotenv
import os

def load_environment_variables():
    # Load environment variables from .env file
    load_dotenv()
    input_dir = os.getenv("INPUT_DIR")
    output_dir = os.getenv("OUTPUT_DIR")

    if input_dir and output_dir:
        return 'Input and output directories are set.'
    else:
        raise EnvironmentError("Environment variables INVOICE_DIR and OUTPUT_DIR are not set.")