@echo off
REM =============================================================
REM TscgOntologyAPIServer — _run_tests.bat
REM Runs the test suite via tscg_api_cli.py test
REM
REM Usage: double-click or call from cmd.exe
REM Location: instances\tscg-tools\TscgOntologyAPIServer\src\
REM
REM Direct equivalent:
REM   python tscg_api_cli.py test              (all tests)
REM   python tscg_api_cli.py test -m iri       (IRI expansion)
REM   python tscg_api_cli.py test -m store     (TscgStore)
REM   python tscg_api_cli.py test -m endpoints (FastAPI)
REM   python tscg_api_cli.py test -v           (verbose)
REM   python tscg_api_cli.py test -k Process   (keyword filter)
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

setlocal
cd /d "%~dp0"

echo.
echo ============================================================
echo  TscgOntologyAPIServer -- Test Suite
echo ============================================================
echo.
echo  Available modules:
echo    1. All tests (full suite)
echo    2. test_expand_iri    - IRI expansion (18 tests)
echo    3. test_tscg_store    - TscgStore / pyoxigraph (20 tests)
echo    4. test_endpoints     - FastAPI endpoints (22 tests)
echo.

set /p CHOICE="Choice [1-4, default=1]: "

if "%CHOICE%"=="" set CHOICE=1
if "%CHOICE%"=="1" goto ALL
if "%CHOICE%"=="2" goto IRI
if "%CHOICE%"=="3" goto STORE
if "%CHOICE%"=="4" goto ENDPOINTS
goto ALL

:ALL
echo.
echo Running: all tests...
python tscg_api_cli.py test -v --tb short
goto END

:IRI
echo.
echo Running: test_expand_iri...
python tscg_api_cli.py test -m iri -v --tb short
goto END

:STORE
echo.
echo Running: test_tscg_store...
python tscg_api_cli.py test -m store -v --tb short
goto END

:ENDPOINTS
echo.
echo Running: test_endpoints...
python tscg_api_cli.py test -m endpoints -v --tb short
goto END

:END
echo.
pause
endlocal
