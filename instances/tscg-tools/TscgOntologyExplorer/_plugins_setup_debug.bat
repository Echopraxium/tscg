@echo off
setlocal

set PLUGINS_DIR=%LOCALAPPDATA%\TscgOntologyExplorer\plugins

echo.
echo === TscgOntologyExplorer - Dev Plugins Setup ===
echo Target: %PLUGINS_DIR%
echo.

if not exist "%PLUGINS_DIR%" (
    mkdir "%PLUGINS_DIR%"
    echo [OK] Created plugins directory
)

echo [..] Installing tscg-dummy-server...
xcopy /E /I /Y dev\dummy-plugin-server "%PLUGINS_DIR%\tscg-dummy-server"
if %errorlevel%==0 (echo [OK] tscg-dummy-server installed) else (echo [ERR] tscg-dummy-server failed)

echo [..] Installing tscg-dummy-renderer...
xcopy /E /I /Y dev\dummy-plugin-renderer "%PLUGINS_DIR%\tscg-dummy-renderer"
if %errorlevel%==0 (echo [OK] tscg-dummy-renderer installed) else (echo [ERR] tscg-dummy-renderer failed)

echo [..] Installing tscg-python-bridge...
xcopy /E /I /Y dev\tscg-python-bridge "%PLUGINS_DIR%\tscg-python-bridge"
if %errorlevel%==0 (echo [OK] tscg-python-bridge installed) else (echo [ERR] tscg-python-bridge failed)

echo.
echo [..] Installing Python dependencies...
pip install -r dev\tscg-python-bridge\requirements.txt
if %errorlevel%==0 (echo [OK] Python dependencies installed) else (echo [ERR] pip install failed)

echo.
echo Done. Run "npm start" to test.
echo.
pause
