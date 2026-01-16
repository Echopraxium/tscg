@echo off
REM generate-files.bat
REM Genere files.txt avec les URLs raw.githubusercontent.com

SETLOCAL EnableDelayedExpansion

SET REPO_URL=https://raw.githubusercontent.com/Echopraxium/tscg/main/

echo Generation de files.txt avec URLs raw GitHub...

REM Supprime l'ancien fichier s'il existe
if exist files.txt del files.txt

REM Liste tous les fichiers avec les extensions specifiees
REM en excluant bin, obj, .vs, .git, packages, _archives

for /r %%f in (*.cs *.fs *.md *.csproj *.fsproj *.jsonld) do (
    set "filepath=%%f"
    set "filepath=!filepath:%CD%\=!"
    
    REM Flag pour savoir si on doit exclure ce fichier
    set "exclude=0"
    
    REM Test pour _archives (test separe pour plus de fiabilite)
    echo !filepath! | findstr /i "_archives" >nul
    if not errorlevel 1 set "exclude=1"
    
    REM Test pour les autres dossiers exclus
    echo !filepath! | findstr /i /c:"\bin\" /c:"\obj\" /c:"\.vs\" /c:"\.git\" /c:"\packages\" >nul
    if not errorlevel 1 set "exclude=1"
    
    REM Si pas exclu, on ajoute au fichier
    if !exclude!==0 (
        REM Remplace les backslashes par des slashes
        set "filepath=!filepath:\=/!"
        
        REM Remplace les espaces par %%20
        set "filepath=!filepath: =%%20!"
        
        echo %REPO_URL%!filepath! >> files.txt
    )
)

echo.
echo Termine ! Fichier files.txt genere avec URLs raw GitHub.
echo.

REM Compte le nombre de lignes
set /a count=0
for /f %%a in ('type "files.txt" ^| find /c /v ""') do set count=%%a
echo Nombre d'URLs generees : %count%

ENDLOCAL

pause