@echo off
REM =============================================================
REM TscgOntologyAPIServer — _setup.bat
REM Installation complete :
REM   1. Dependances Python (pip)
REM   2. Copie du plugin tscg-api-bridge dans AppData
REM
REM A placer sous : instances\tscg-tools\TscgOntologyAPIServer\
REM Usage : double-cliquer ou lancer depuis cmd.exe
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

setlocal
cd /d "%~dp0"

REM ── Chemins ──────────────────────────────────────────────────
set SRC_DIR=%~dp0src
set REPO_ROOT=%~dp0..\..\..\..
set PLUGIN_SRC=%REPO_ROOT%\TscgOntologyExplorer\plugins\tscg-api-bridge
set APP_PLUGINS=%LOCALAPPDATA%\TscgOntologyExplorer\plugins

echo.
echo ============================================================
echo  TscgOntologyAPIServer -- Setup complet
echo ============================================================
echo.

REM ── Verifier Python ──────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python introuvable dans le PATH.
    echo Installer Python 3.11+ depuis https://www.python.org/
    pause
    exit /b 1
)
echo Python :
python --version
echo.

REM ── Installer les dependances Python ─────────────────────────
echo [1/3] Installation des dependances Python...
echo.
pip install --upgrade pip --quiet
pip install "fastapi>=0.110.0" "uvicorn[standard]>=0.29.0" "pyoxigraph>=0.5.0" "rdflib>=6.3.0" "pydantic>=2.0.0" "requests>=2.31.0" "pytest>=8.0.0" "httpx>=0.27.0"

echo.
echo Verification des versions :
python -c "import fastapi;      print('  fastapi     :', fastapi.__version__)"
python -c "import uvicorn;      print('  uvicorn     :', uvicorn.__version__)"
python -c "import pyoxigraph;   print('  pyoxigraph  :', pyoxigraph.__version__)"
python -c "import rdflib;       print('  rdflib      :', rdflib.__version__)"
python -c "import pytest;       print('  pytest      :', pytest.__version__)"
echo.

REM ── Copier le plugin tscg-api-bridge dans AppData ────────────
echo [2/3] Installation du plugin tscg-api-bridge...
echo.

if not exist "%APP_PLUGINS%" (
    echo   Creation du dossier plugins AppData...
    mkdir "%APP_PLUGINS%"
)

REM Supprimer l'ancien plugin tscg-python-bridge si present
if exist "%APP_PLUGINS%\tscg-python-bridge" (
    echo   Suppression de l'ancien plugin tscg-python-bridge...
    rmdir /S /Q "%APP_PLUGINS%\tscg-python-bridge"
)

REM Copier tscg-api-bridge
if exist "%PLUGIN_SRC%" (
    if exist "%APP_PLUGINS%\tscg-api-bridge" (
        rmdir /S /Q "%APP_PLUGINS%\tscg-api-bridge"
    )
    xcopy /E /I /Q "%PLUGIN_SRC%" "%APP_PLUGINS%\tscg-api-bridge"
    echo   Plugin tscg-api-bridge installe dans :
    echo   %APP_PLUGINS%\tscg-api-bridge
) else (
    echo   [ATTENTION] Plugin source introuvable :
    echo   %PLUGIN_SRC%
    echo   Verifiez que TscgOntologyExplorer\plugins\tscg-api-bridge\ existe.
)
echo.

REM ── Verification finale ───────────────────────────────────────
echo [3/3] Verification :
echo.
if exist "%APP_PLUGINS%\tscg-api-bridge\index.js" (
    echo   tscg-api-bridge  : installe ✔
) else (
    echo   tscg-api-bridge  : ABSENT  ✗
)
if exist "%SRC_DIR%\tscg_api_server.py" (
    echo   tscg_api_server  : present ✔
) else (
    echo   tscg_api_server  : ABSENT  ✗
)
echo.

echo ============================================================
echo  Setup termine !
echo.
echo  Pour demarrer le serveur manuellement (CLI) :
echo    cd src
echo    python tscg_api_cli.py start
echo.
echo  Pour lancer les tests :
echo    cd src
echo    _run_tests.bat
echo.
echo  Relancez TscgOntologyExplorer pour activer le plugin.
echo ============================================================
echo.

pause
endlocal
