@echo off
setlocal enabledelayedexpansion

if not "%~1"=="" (
    set ZIP_PATH=%~1
    goto run
)

set ZIP_PATH=
for %%f in ("*.zip") do (
    if "!ZIP_PATH!"=="" set ZIP_PATH=%%~ff
)

if "!ZIP_PATH!"=="" (
    set /p ZIP_PATH="Chemin du zip: "
)

:run
echo Zip: %ZIP_PATH%
python update_toolchain.py "%ZIP_PATH%" "%CD%"
echo.
pause
