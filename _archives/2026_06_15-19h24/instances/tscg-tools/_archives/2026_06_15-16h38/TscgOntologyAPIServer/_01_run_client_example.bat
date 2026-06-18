@echo off
REM =============================================================
REM TscgOntologyAPIServer — _01_run_client_example.bat
REM Runs the test client (tscg_api_client_example.py)
REM
REM Usage : double-click or run from cmd.exe
REM Location : instances\tscg-tools\TscgOntologyAPIServer\
REM
REM Prerequisites : server must be running
REM   - Via TscgOntologyExplorer (tscg-api-bridge plugin)
REM   - Or via _00_start_server.bat (in this same folder)
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

setlocal
cd /d "%~dp0"

REM ── Configuration ────────────────────────────────────────────
set HOST=127.0.0.1
set PORT=8000
set ONTOLOGY_DIR=E:\_00_Michel\_00_Lab\_00_GitHub\tscg\ontology

echo.
echo ============================================================
echo  TscgOntologyAPIServer -- Test Client
echo ============================================================
echo  Server    : http://%HOST%:%PORT%
echo  Ontology  : %ONTOLOGY_DIR%
echo ============================================================
echo.

python "%~dp0src\tscg_api_client_example.py" ^
    --host %HOST% ^
    --port %PORT% ^
    --ontology-dir "%ONTOLOGY_DIR%"

echo.
pause
endlocal
