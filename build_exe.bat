@echo off
REM ─── Clean out previous builds
rd /s /q dist 2>nul
rd /s /q build 2>nul

REM ─── Bundle into one EXE (no .spec involved)
python -m PyInstaller ^
 --noconfirm ^
 --clean ^
 --onefile ^
 --name pdf_processor ^
 --paths src ^
 --add-data "src;src" ^
 run_app.py

REM ─── Report result
if %ERRORLEVEL% EQU 0 (
  echo.
  echo ✅ Build succeeded → dist\pdf_processor.exe
) else (
  echo.
  echo ❌ Build failed with errorlevel %ERRORLEVEL%
)

pause
