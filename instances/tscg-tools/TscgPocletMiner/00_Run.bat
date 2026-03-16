@echo off
REM ================================================================
REM  TSCG Poclet Miner — Launcher
REM  Author: Echopraxium with the collaboration of Claude AI
REM
REM  Location: instances/tscg-tools/TscgPocletMiner/
REM  Usage   : double-click this file, or call from any folder
REM
REM  Remonte 3 niveaux jusqu'a la racine tscg/ pour executer
REM  "npm run sim:TscgPocletMiner" depuis le bon package.json
REM  TscgPocletMiner\ -> tscg-tools\ -> instances\ -> tscg\
REM ================================================================
 
REM Calcule la racine du repo (3 niveaux au-dessus de ce .bat)
pushd "%~dp0..\..\..\"
 
echo [TSCG] Repo root : %CD%
echo [TSCG] Launching : npm run sim:TscgPocletMiner
echo.
 
npm run sim:TscgPocletMiner
 
popd