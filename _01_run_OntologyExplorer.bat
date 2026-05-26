@echo off
chcp 65001 >nul
title TscgOntologyExplorer

echo.
echo === TscgOntologyExplorer ===
echo.

cd instances/tscg-tools/TscgOntologyExplorer

npm start
