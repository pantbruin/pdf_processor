@echo off
setlocal ENABLEDELAYEDEXPANSION

:: ─── 1. ENVIRONMENT VARIABLES ───────────────────────────────────────────────
set "INPUT_PATH=./invoices.pdf"
REM Final output folder named ProcessedInvoices will automatically be created in specified OUTPUT_DIR
set "OUTPUT_DIR=<output_path_here>"

REM Launch the EXE
"%~dp0./pdf_processor.exe" %*

endlocal
