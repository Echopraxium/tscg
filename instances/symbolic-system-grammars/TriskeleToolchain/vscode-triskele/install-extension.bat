@echo off
:: install-extension.bat
:: Author: Echopraxium with the collaboration of Claude AI
:: Installs the triskele-debug VS Code extension for TriskeleVM debugging.
:: Also copies launch.json to the workspace .vscode\ folder automatically.
::
:: Usage: double-click install-extension.bat  (or run from cmd)
:: Requirements: VS Code installed

setlocal EnableDelayedExpansion

set EXT_NAME=triskele-debug
set EXT_VERSION=0.1.0
set EXT_FOLDER=%EXT_NAME%-%EXT_VERSION%
set TARGET="%USERPROFILE%\.vscode\extensions\%EXT_FOLDER%"

echo.
echo  TriskeleVM Debugger -- VS Code Extension Installer
echo  ====================================================
echo.

:: ── Check VS Code is installed ───────────────────────────────────────────────
where code >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  [ERROR] VS Code not found in PATH.
    echo          Please install VS Code from https://code.visualstudio.com
    echo          and ensure "Add to PATH" was selected during installation.
    goto :fail
)

:: ── Locate source folder (same directory as this .bat) ───────────────────────
set SRC=%~dp0
:: Remove trailing backslash
if "%SRC:~-1%"=="\" set SRC=%SRC:~0,-1%

if not exist "%SRC%\package.json" (
    echo  [ERROR] package.json not found next to this script.
    echo          Make sure install-extension.bat is in the vscode-triskele\ folder.
    goto :fail
)

:: ── Workspace root = parent of vscode-triskele\ ──────────────────────────────
:: SRC = ...\TriskeleToolchain\vscode-triskele
:: WORKSPACE = ...\TriskeleToolchain
for %%I in ("%SRC%\..") do set WORKSPACE=%%~fI
set VSCODE_DIR=%WORKSPACE%\.vscode

:: ── Create .vscode in workspace if needed ────────────────────────────────────
if not exist "%VSCODE_DIR%" (
    echo  Creating %VSCODE_DIR% ...
    mkdir "%VSCODE_DIR%"
)

:: ── Copy launch.json to workspace .vscode\ ───────────────────────────────────
if exist "%SRC%\launch.json" (
    if exist "%VSCODE_DIR%\launch.json" (
        echo  Backing up existing launch.json to launch.json.bak ...
        copy /Y "%VSCODE_DIR%\launch.json" "%VSCODE_DIR%\launch.json.bak" >nul
    )
    echo  Copying launch.json to %VSCODE_DIR%\ ...
    copy /Y "%SRC%\launch.json" "%VSCODE_DIR%\launch.json" >nul
    if %ERRORLEVEL% neq 0 (
        echo  [ERROR] Failed to copy launch.json.
        goto :fail
    )
    echo  [OK] launch.json installed.
) else (
    echo  [WARN] launch.json not found in %SRC% -- skipped.
)

:: ── Create VS Code extensions directory if needed ────────────────────────────
if not exist "%USERPROFILE%\.vscode\extensions" (
    echo  Creating %USERPROFILE%\.vscode\extensions ...
    mkdir "%USERPROFILE%\.vscode\extensions"
)

:: ── Remove previous version if present ───────────────────────────────────────
if exist %TARGET% (
    echo  Removing previous installation: %TARGET%
    rmdir /S /Q %TARGET%
)

:: ── Copy extension files ──────────────────────────────────────────────────────
echo  Installing extension to %TARGET% ...
xcopy /E /I /Q "%SRC%" %TARGET%
if %ERRORLEVEL% neq 0 (
    echo  [ERROR] Extension copy failed.
    goto :fail
)

:: ── Done ─────────────────────────────────────────────────────────────────────
echo.
echo  [OK] triskele-debug %EXT_VERSION% installed successfully.
echo.
echo  Next steps:
echo    1. Restart VS Code  (or Ctrl+Shift+P -^> Developer: Reload Window)
echo    2. Run:  cargo run -p tsk-dbg -- src\wolf3d_v2_clean.tvmx --symbols src\wolf3d_v2_clean.sym
echo    3. Press F5 in VS Code -^> "Debug wolf3d"
echo.
pause
exit /b 0

:fail
echo.
echo  Installation aborted.
pause
exit /b 1
