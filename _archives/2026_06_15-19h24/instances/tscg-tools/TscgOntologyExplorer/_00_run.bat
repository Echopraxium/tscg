@echo off
REM =============================================================
REM TscgOntologyExplorer — _00_run.bat
REM Smart launcher — detects port conflicts before npm start
REM
REM Usage : double-click
REM Location : instances/tscg-tools/TscgOntologyExplorer/
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

set LAUNCHER=%~dp0src\launcher.py
start "TscgOntologyExplorer" /D "%~dp0" cmd /K python "%LAUNCHER%"
