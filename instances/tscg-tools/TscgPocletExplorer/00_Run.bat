Copier

@echo off
REM ================================================================
REM  TSCG Poclet Explorer — Launcher
REM  Author: Echopraxium with the collaboration of Claude AI
REM
REM  Location: system-models/tscg-tools/tscg-poclet-explorer/
REM  Usage   : double-click this file, or call from any folder
REM
REM  Remonte 3 niveaux jusqu'a la racine tscg/ pour executer
REM  "npm run tscg-poclet-explorer" depuis le bon package.json
REM  tscg-poclet-explorer\ -> tscg-tools\ -> system-models\ -> tscg\
REM ================================================================
 
REM Calcule la racine du repo (3 niveaux au-dessus de ce .bat)
pushd "%~dp0..\..\..\"
 
echo [TSCG] Repo root : %CD%
echo [TSCG] Launching : npm run tscg-poclet-explorer
echo.
 
npm run tscg-poclet-explorer
 
popd