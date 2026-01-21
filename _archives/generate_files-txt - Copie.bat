@echo off
REM generate-files.bat
REM Genere files.txt avec les URLs raw.githubusercontent.com

SETLOCAL EnableDelayedExpansion

SET REPO_URL=https://raw.githubusercontent.com/Echopraxium/tscg/main/

echo Generation de files.txt avec URLs raw GitHub...

REM Supprime l'ancien fichier s'il existe
if exist files.txt del files.txt

REM Initialise le compteur
set /a file_count=0

REM Liste tous les fichiers avec les extensions specifiees
for /r %%f in (*.cs *.fs *.md *.csproj *.fsproj *.jsonld) do (
    set "fullpath=%%f"
    set "relativepath=%%f"
    
    REM Convertit en chemin relatif
    set "relativepath=!relativepath:%CD%\=!"
    
    REM Flag pour savoir si on doit exclure ce fichier
    set "exclude=0"
    
    REM Test des dossiers exclus avec backslashes seulement
    for %%d in (bin obj .vs .git packages _archives) do (
        if not !exclude!==1 (
            REM Test si le dossier est dans le chemin (avec backslash avant et après)
            echo !relativepath! | findstr /i /c:"\%%d\" >nul
            if not errorlevel 1 set "exclude=1"
            
            REM Test si le dossier est à la fin du chemin
            if not !exclude!==1 (
                echo !relativepath! | findstr /i /c:"\%%d " >nul
                if not errorlevel 1 set "exclude=1"
            )
            
            REM Test si le dossier est au début du chemin
            if not !exclude!==1 (
                echo !relativepath! | findstr /i /b "%%d\" >nul
                if not errorlevel 1 set "exclude=1"
            )
        )
    )
    
    REM Si pas exclu, on ajoute au fichier
    if !exclude!==0 (
        REM Remplace les backslashes par des slashes pour URL (seulement pour l'URL finale)
        set "urlpath=!relativepath:\=/!"
        
        REM Encode les espaces pour URL
        set "urlpath=!urlpath: =%%20!"
        
        REM Ajoute l'URL au fichier
        echo %REPO_URL%!urlpath! >> files.txt
        
        REM Incrémente le compteur
        set /a file_count+=1
        
        REM Affiche le fichier ajouté (optionnel, pour debug)
        REM echo Ajoute: !relativepath!
    )
)

echo.
echo Termine ! Fichier files.txt genere avec URLs raw GitHub.
echo.
echo Nombre d'URLs generees : !file_count!

ENDLOCAL
pause