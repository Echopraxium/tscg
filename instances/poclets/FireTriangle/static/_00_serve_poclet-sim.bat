@echo off
setlocal

set PORT=8080

:: Root = folder where this .bat lives (the static/ folder of the poclet)
set ROOT=%~dp0
:: Remove trailing backslash
if "%ROOT:~-1%"=="\" set ROOT=%ROOT:~0,-1%

:: Auto-detect the M0_*.html file in this folder
set TARGET=
for %%f in ("%ROOT%\M0_*.html") do (
    set TARGET=%%~nxf
    goto :found
)

echo [TSCG] ERROR: No M0_*.html file found in:
echo [TSCG]   %ROOT%
pause & exit /b 1

:found

:: Kill any process already using the port
echo [TSCG] Freeing port %PORT%...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT%') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo [TSCG] Root:    %ROOT%
echo [TSCG] Opening: http://127.0.0.1:%PORT%/%TARGET%
echo [TSCG] Stop:    Ctrl+C
echo.

start /b powershell -WindowStyle Hidden -Command "Start-Sleep 2; Start-Process 'http://127.0.0.1:%PORT%/%TARGET%'"

node "%ROOT%\..\..\..\..\serve.js" %PORT% "%ROOT%"
pause
