#!/usr/bin/env python3
"""
run_app.py

Entry-point for the Invoice Processing application.
This script loads environment variables and then invokes core logic.
"""
from src.config import load_environment_variables
from src.pdf_processor import main as process_master_pdf

def main():
    """
    Main entry-point of the application.
    """
    load_environment_variables()
    process_master_pdf()

if __name__ == "__main__":
    main()

