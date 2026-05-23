@echo off
setlocal

set PLUGINS_DIR=%LOCALAPPDATA%\TscgOntologyExplorer\plugins
set BRIDGE_SRC=dev\tscg-python-bridge

echo.
echo === TscgOntologyExplorer - Dev Plugins Setup ===
echo Target: %PLUGINS_DIR%
echo.

if not exist "%PLUGINS_DIR%" (
    mkdir "%PLUGINS_DIR%"
    echo [OK] Created plugins directory
)

echo [..] Installing tscg-dummy-server...
xcopy /E /I /Y dev\dummy-plugin-server "%PLUGINS_DIR%\tscg-dummy-server" >nul
if %errorlevel%==0 (echo [OK] tscg-dummy-server installed) else (echo [ERR] tscg-dummy-server failed)

echo [..] Installing tscg-dummy-renderer...
xcopy /E /I /Y dev\dummy-plugin-renderer "%PLUGINS_DIR%\tscg-dummy-renderer" >nul
if %errorlevel%==0 (echo [OK] tscg-dummy-renderer installed) else (echo [ERR] tscg-dummy-renderer failed)

echo [..] Installing tscg-python-bridge...
xcopy /E /I /Y "%BRIDGE_SRC%" "%PLUGINS_DIR%\tscg-python-bridge" >nul
if %errorlevel%==0 (echo [OK] tscg-python-bridge installed) else (echo [ERR] tscg-python-bridge failed)

echo.
echo [..] Installing Python dependencies...
pip install -r "%BRIDGE_SRC%\requirements.txt"
if %errorlevel%==0 (echo [OK] Python dependencies installed) else (echo [ERR] pip install failed)

echo.
echo [..] Installing pyoxigraph (Phase 2 triple store - required for /corpus/* endpoints)...
pip show pyoxigraph >nul 2>&1
if %errorlevel%==0 (
    echo [OK] pyoxigraph already installed
) else (
    pip install pyoxigraph
    if %errorlevel%==0 (
        echo [OK] pyoxigraph installed
    ) else (
        echo [WARN] pyoxigraph installation failed
        echo        /corpus/* endpoints will be unavailable but the bridge will still run
        echo        Retry manually: pip install pyoxigraph
    )
)

echo.
echo [..] Installing test dependencies (pytest, httpx)...
pip install pytest pytest-asyncio httpx --quiet
if %errorlevel%==0 (echo [OK] Test dependencies installed) else (echo [WARN] Test dependencies failed)

echo.
echo === Setup complete. Run "npm start" to launch. ===
echo.
echo Tip: for persistent triple store across sessions, start the bridge with:
echo   python bridge_server.py --port 7432 --corpus-db "%%APPDATA%%\tscg\corpus.db"
echo.

REM ── Optional: run unit tests ─────────────────────────────────────
echo Run unit tests now? [Y/N]
set /p RUN_TESTS="> "
if /i "%RUN_TESTS%"=="Y" (
    echo.
    echo === Running unit tests ===
    cd "%BRIDGE_SRC%"
    pytest tests\ -v --tb=short
    set TEST_RESULT=%errorlevel%
    cd ..\..
    echo.
    if %TEST_RESULT%==0 (
        echo [OK] All tests passed ^^!
    ) else (
        echo [WARN] Some tests failed - see output above
    )
    echo.
    echo Useful test commands:
    echo   All tests        : cd %BRIDGE_SRC% ^& pytest tests\ -v
    echo   One module       : cd %BRIDGE_SRC% ^& pytest tests\test_expand_iri.py -v
    echo   Stop on 1st fail : cd %BRIDGE_SRC% ^& pytest tests\ -x
    echo   With coverage    : cd %BRIDGE_SRC% ^& pytest tests\ --cov=bridge_server --cov-report=term-missing
    echo.
)

pause
