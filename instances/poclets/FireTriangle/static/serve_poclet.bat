@echo off
setlocal enabledelayedexpansion

set PORT=8080
cd /d "%~dp0"

:: Find first HTML file (excluding this bat's own name)
for %%f in (*.html) do (
    set HTML=%%~nxf
    goto :found
)
echo [TSCG] No .html file found. & pause & exit /b 1

:found
:: URL-encode spaces
set HTMLURL=!HTML: =%%20!

echo [TSCG] Folder:  %CD%
echo [TSCG] Opening: http://127.0.0.1:%PORT%/!HTMLURL!
echo [TSCG] Stop:    Ctrl+C
echo.

start /b powershell -WindowStyle Hidden -Command "Start-Sleep 2; Start-Process 'http://127.0.0.1:%PORT%/!HTMLURL!'"

python -m http.server %PORT% --bind 127.0.0.1
pause
