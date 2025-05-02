@echo off
setlocal ENABLEDELAYEDEXPANSION

:: ─── 1. ENVIRONMENT VARIABLES ───────────────────────────────────────────────
set "INPUT_PATH=<input_path>"
set "OUTPUT_DIR=<output_dir>"

REM Launch the EXE
"%~dp0./pdf_processor.exe" %*

endlocal
