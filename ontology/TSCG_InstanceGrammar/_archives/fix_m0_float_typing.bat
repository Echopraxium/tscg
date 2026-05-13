@echo off
REM Fix XSD Float Typing in TSCG M0 Poclet Files
REM Author: Echopraxium with the collaboration of Claude AI
REM Date: 2026-04-18

setlocal enabledelayedexpansion

echo ============================================================
echo TSCG Float Typing Fix - M0 Poclets
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python 3.7+ or add it to your PATH
    pause
    exit /b 1
)

REM Set repository root
set REPO_ROOT=E:\_00_Michel\_00_Lab\_00_GitHub\tscg

REM Check if repository exists
if not exist "%REPO_ROOT%" (
    echo Error: Repository not found at %REPO_ROOT%
    pause
    exit /b 1
)

echo Repository: %REPO_ROOT%
echo.

REM Check if fix script exists
set SCRIPT_PATH=%REPO_ROOT%\fix_float_typing.py
if not exist "%SCRIPT_PATH%" (
    echo Error: Script not found at %SCRIPT_PATH%
    echo Please ensure fix_float_typing.py is in the repository root
    pause
    exit /b 1
)

REM Ask for confirmation
echo This will modify all M0_*.jsonld files in instances/poclets/
echo.
set /p CONFIRM="Continue? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Cancelled by user
    pause
    exit /b 0
)

echo.
echo Processing files...
echo.

REM Process all M0_*.jsonld files in poclets subdirectories
cd /d "%REPO_ROOT%"

REM Collect all M0_*.jsonld files
set FILES=
for /r instances\poclets %%F in (M0_*.jsonld) do (
    set FILES=!FILES! "%%F"
)

REM Check if any files found
if not defined FILES (
    echo Warning: No M0_*.jsonld files found in instances\poclets\
    pause
    exit /b 1
)

REM Run Python script
python "%SCRIPT_PATH%" %FILES%

echo.
echo ============================================================
echo Done!
echo ============================================================
echo.
echo Next step: Run SHACL validation to verify fixes:
echo pyshacl -s ontology\M0_Instances_Schema.shacl.ttl -df json-ld instances\poclets\FireTriangle\M0_FireTriangle.jsonld
echo.

pause
