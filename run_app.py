#!/usr/bin/env python3
"""
run_app.py

Entry-point for the Invoice Processing application.
This script loads environment variables and then invokes core logic.
"""
from src.pdf_processor import main as process_input_pdf
from src.validators import main as run_validators

def main():
    """
    Main entry-point of the application.
    """
    # Check environment variables
    run_validators()
    process_input_pdf()

if __name__ == "__main__":
    main()

