@echo off
setlocal

set PORT=8080
set REPO=E:\_00_Michel\_00_Lab\_00_GitHub\tscg
set TARGET=index.html

:: Kill any process already using the port
echo [TSCG] Freeing port %PORT%...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT%') do (
    taskkill /PID %%a /F >nul 2>&1
)

if not exist "%REPO%\%TARGET%" (
    echo [TSCG] ERROR: %REPO%\%TARGET% not found.
    echo [TSCG] Run _Generate_Index-html.bat first.
    pause & exit /b 1
)

echo [TSCG] Root:    %REPO%
echo [TSCG] Opening: http://127.0.0.1:%PORT%/%TARGET%
echo [TSCG] Stop:    Ctrl+C
echo.

start /b powershell -WindowStyle Hidden -Command "Start-Sleep 2; Start-Process 'http://127.0.0.1:%PORT%/%TARGET%'"

node "%REPO%\serve.js" %PORT% "%REPO%"
pause
