@echo off
REM ============================================================================
REM  TSCG - acceptance gate launcher (stays open, no frills)
REM  Author: Echopraxium with the collaboration of Claude AI
REM  MUST stay CRLF (.gitattributes: *.bat text eol=crlf).
REM ============================================================================
cd /d "%~dp0"
chcp 65001 >nul 2>&1

python run_all_layers.py %*
set GATE_EXIT=%ERRORLEVEL%

echo.
echo ============================================================
if "%GATE_EXIT%"=="0"  echo   GATE: PASS  (exit 0)
if "%GATE_EXIT%"=="2"  echo   LAYOUT ERROR (exit 2) - a required compartment is missing.
if not "%GATE_EXIT%"=="0" if not "%GATE_EXIT%"=="2" echo   GATE: FAIL (exit %GATE_EXIT%) - a count moved.
echo ============================================================
echo.
REM cmd /k = the window NEVER closes on its own, even if pause is skipped
REM or python was not found. Type EXIT to close it.
cmd /k
