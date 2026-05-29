@echo off
REM =============================================================
REM TscgOntologyExplorer — _plugins_setup.bat
REM Installe ou met a jour les plugins dans le dossier AppData
REM de TscgOntologyExplorer, et desinstalle les anciens plugins.
REM
REM A placer a la racine de : TscgOntologyExplorer\
REM Usage : double-cliquer ou lancer depuis cmd.exe
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

setlocal
cd /d "%~dp0"

REM ── Chemins ──────────────────────────────────────────────────
set REPO_PLUGINS=%~dp0plugins
set APP_PLUGINS=%LOCALAPPDATA%\TscgOntologyExplorer\plugins

echo.
echo ============================================================
echo  TscgOntologyExplorer -- Plugins Setup
echo ============================================================
echo.
echo  Source  : %REPO_PLUGINS%
echo  Cible   : %APP_PLUGINS%
echo.

REM ── Creer le dossier cible si necessaire ─────────────────────
if not exist "%APP_PLUGINS%" (
    echo Création du dossier plugins AppData...
    mkdir "%APP_PLUGINS%"
)

REM ── Nettoyer AppData (supprime tous les plugins existants) ───
echo [1/3] Nettoyage des plugins AppData...

for /d %%P in ("%APP_PLUGINS%\*") do (
    echo   Suppression : %%~nxP
    rmdir /S /Q "%%P"
)
echo   AppData plugins : nettoye
echo.

REM ── Installer / mettre a jour les plugins ────────────────────
echo [2/3] Installation des plugins...

for /d %%P in ("%REPO_PLUGINS%\*") do (
    set PLUGIN_NAME=%%~nxP
    REM Ignorer les dossiers commencant par "_" (ex: _archives)
    echo %%~nxP | findstr /B "_" >nul
    if errorlevel 1 (
        echo   Installation : %%~nxP
        if exist "%APP_PLUGINS%\%%~nxP" (
            rmdir /S /Q "%APP_PLUGINS%\%%~nxP"
        )
        xcopy /E /I /Q "%%P" "%APP_PLUGINS%\%%~nxP"
        echo   OK
    ) else (
        echo   Ignore       : %%~nxP
    )
)
echo.

REM ── Verification ─────────────────────────────────────────────
echo [3/3] Plugins installes dans AppData :
echo.
for /d %%P in ("%APP_PLUGINS%\*") do (
    echo   + %%~nxP
    for %%F in ("%%P\*") do echo       %%~nxF
)

echo.
echo ============================================================
echo  Setup termine !
echo  Relancez TscgOntologyExplorer pour activer les plugins.
echo ============================================================
echo.

pause
endlocal
