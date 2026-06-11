@echo off
setlocal enabledelayedexpansion

if not "%~1"=="" (
    set PROJECT=%~1
    goto run
)

echo.
echo Usage: _02_run_pipeline.bat [project_name]
echo.
echo Available projects:
python run_pipeline.py --list
echo.
set /p PROJECT="Project name: "

:run
echo.
echo Running pipeline for project: %PROJECT%
echo.
python run_pipeline.py %PROJECT%
echo.
pause
