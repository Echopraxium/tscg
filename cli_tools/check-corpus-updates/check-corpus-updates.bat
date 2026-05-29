@echo off
REM =============================================================
REM TSCG — cli-tools/check-corpus-updates/check-corpus-updates.bat
REM Checks corpus file versions against local repo
REM
REM Usage : double-click or run from cmd.exe
REM Options:
REM   --verbose   also show files that are in sync
REM   --json      output as JSON
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

@echo off
python "%~dp0check-corpus-updates.py" %*
pause
