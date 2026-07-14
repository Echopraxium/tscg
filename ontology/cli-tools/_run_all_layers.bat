@echo off
REM ============================================================================
REM  TSCG - acceptance gate launcher
REM  Author: Echopraxium with the collaboration of Claude AI
REM
REM  Double-click safe. Four things this handles:
REM
REM   1. CRLF line endings. cmd.exe REQUIRES them. A .bat saved with Unix LF gets
REM      chopped mid-command ('@echo off' is read as '@echo' + 'on'), which prints
REM      garbage AND silently skips logic. Never edit this file with a tool that
REM      normalises to LF.
REM
REM   2. cd /d "%~dp0" - launched from Explorer, the working directory is NOT the
REM      script's folder.
REM
REM   3. NO 'start' - it spawns a window that CLOSES the instant the script ends.
REM      The whole point of a gate is to be READ.
REM
REM   4. chcp 65001 - the gate prints box-drawing characters.
REM ============================================================================

cd /d "%~dp0"
chcp 65001 >nul 2>&1

python run_all_layers.py %*
set GATE_EXIT=%ERRORLEVEL%

echo.
if "%GATE_EXIT%"=="0" goto :pass
if "%GATE_EXIT%"=="2" goto :layout
goto :fail

:pass
echo   ---- GATE: PASS  (exit 0) ----
goto :done

:layout
echo   #### LAYOUT ERROR (exit 2) - a REQUIRED instance compartment is missing.
echo   #### The totals above are NOT comprehensive. Do not trust any number.
goto :done

:fail
echo   #### GATE: FAIL (exit %GATE_EXIT%) - a count moved.
echo   ####
echo   ####   UP   = a new defect was introduced.
echo   ####   DOWN = either a deliberate fix (then run: run_all_layers.py --update-golden)
echo   ####          or a validator that STOPPED BITING.
echo   ####
echo   ####   A shrinking error count is the most dangerous signal in this repo:
echo   ####   it LOOKS LIKE PROGRESS.
goto :done

:done
echo.
pause
exit /b %GATE_EXIT%
