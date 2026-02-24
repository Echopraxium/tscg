@echo off
REM ============================================================================
REM TSCG JSON-LD to OWL Turtle Converter - Windows Batch Script
REM ============================================================================
REM Author: Echopraxium with the collaboration of Claude AI
REM Date: 2026-02-15
REM Version: 1.0.0
REM ============================================================================

echo.
echo ======================================================================
echo TSCG JSON-LD to OWL Turtle Converter
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if rdflib is installed
python -c "import rdflib" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: rdflib not found. Installing...
    echo.
    pip install rdflib
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install rdflib
        echo Please run manually: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM Run conversion
echo Starting conversion...
echo.

python jsonld_to_turtle.py --skip-errors

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo SUCCESS: Conversion completed!
    echo ======================================================================
    echo.
    echo All .jsonld files have been converted to .ttl format.
    echo You can now open them in Protege or use with OWL reasoners.
    echo.
) else (
    echo.
    echo ======================================================================
    echo WARNING: Conversion completed with errors
    echo ======================================================================
    echo.
    echo Check the log file for details.
    echo.
)

pause
