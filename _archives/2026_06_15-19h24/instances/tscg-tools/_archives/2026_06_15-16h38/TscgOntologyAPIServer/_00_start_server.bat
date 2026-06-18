@echo off
REM =============================================================
REM TscgOntologyAPIServer — _00_start_server.bat
REM Starts the REST server standalone (without TscgOntologyExplorer)
REM
REM Usage : double-click or run from cmd.exe
REM Location : instances\tscg-tools\TscgOntologyAPIServer\
REM
REM Server accessible at :
REM   http://127.0.0.1:8000
REM   http://127.0.0.1:8000/docs  (Swagger UI)
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

setlocal
cd /d "%~dp0"

REM ── Configuration ────────────────────────────────────────────
set HOST=127.0.0.1
set PORT=8000
set LOG_LEVEL=warning
set ONTOLOGY_DIR=E:\_00_Michel\_00_Lab\_00_GitHub\tscg\ontology

REM Persistent store in AppData (same location as Electron plugin)
set STORE_PATH=%APPDATA%\tscg-ontology-explorer\tscg_store.oxg

echo.
echo ============================================================
echo  TscgOntologyAPIServer -- Standalone
echo ============================================================
echo  URL       : http://%HOST%:%PORT%
echo  Swagger   : http://%HOST%:%PORT%/docs
echo  Store     : %STORE_PATH%
echo  Ontology  : %ONTOLOGY_DIR%
echo ============================================================
echo.
echo  Press Ctrl+C to stop the server
echo.

python "%~dp0src\tscg_api_server.py" ^
    --host %HOST% ^
    --port %PORT% ^
    --log-level %LOG_LEVEL% ^
    --store-path "%STORE_PATH%" ^
    --ontology-dir "%ONTOLOGY_DIR%"

echo.
echo Server stopped.
pause
endlocal
