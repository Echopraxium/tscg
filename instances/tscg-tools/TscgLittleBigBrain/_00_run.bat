@echo off
title TSCG LittleBigBrain Benchmark
setlocal enabledelayedexpansion

echo ======================================================================
echo TSCG LittleBigBrain Benchmark
echo ======================================================================
echo.

REM Configuration
set API_HOST=localhost
set API_PORT=8000
set API_HEALTH_URL=http://%API_HOST%:%API_PORT%/health
set MAX_RETRIES=30
set RETRY_DELAY_SEC=2

REM Chemin du script de démarrage du serveur (à adapter si nécessaire)
set START_SERVER_BAT=..\TscgOntologyAPIServer\_00_start_server.bat

echo Vérification du serveur API...

call :check_server
if %errorlevel% equ 0 (
    echo Serveur API déjà actif.
    goto :run_benchmark
)

echo Serveur API non trouvé. Démarrage en cours...
if not exist "%START_SERVER_BAT%" (
    echo ERREUR: %START_SERVER_BAT% introuvable.
    pause
    exit /b 1
)

REM Lancer le serveur en arrière‑plan
echo Démarrage du serveur API...
start /b cmd /c "%START_SERVER_BAT%" > server.log 2>&1

REM Attendre que le serveur soit prêt
echo Attente du démarrage du serveur (max %MAX_RETRIES% tentatives)...
set retry=0
:wait_loop
timeout /t %RETRY_DELAY_SEC% /nobreak > nul
call :check_server
if %errorlevel% equ 0 (
    echo Serveur API prêt.
    goto :run_benchmark
)
set /a retry+=1
if %retry% lss %MAX_RETRIES% goto :wait_loop

echo ERREUR: Le serveur API n'a pas démarré dans le temps imparti.
echo Vérifiez le fichier server.log.
pause
exit /b 1

:run_benchmark
echo.
echo ======================================================================
echo Lancement du benchmark...
echo ======================================================================
echo.

REM Se placer dans le répertoire racine du projet (où se trouve ce batch)
cd /d "%~dp0"

REM Définir PYTHONPATH pour que les imports fonctionnent
set PYTHONPATH=%CD%

REM Exécuter le benchmark directement via le module (plus fiable)
python -m tests.test_benchmark --host %API_HOST% --port %API_PORT% --runs 5 --cycles 3

echo.
echo ======================================================================
echo Benchmark terminé.
echo ======================================================================
echo.

REM Optionnel : arrêter le serveur
set /p stop_server="Voulez-vous arrêter le serveur API ? (O/N) "
if /i "%stop_server%"=="O" (
    echo Arrêt du serveur API...
    curl -X POST http://%API_HOST%:%API_PORT%/shutdown > nul 2>&1
    if %errorlevel% equ 0 (
        echo Serveur arrêté.
    ) else (
        echo Impossible d'arrêter le serveur.
    )
)

echo Appuyez sur une touche pour fermer cette fenêtre.
pause > nul
exit /b 0

:check_server
curl -s -o nul "%API_HEALTH_URL%"
if %errorlevel% equ 0 exit /b 0
exit /b 1