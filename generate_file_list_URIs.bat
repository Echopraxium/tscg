@echo off
REM generate-files-txt.bat
REM Genere files.txt avec les URLs raw.githubusercontent.com
REM Exclut les fichiers dans les dossiers: bin, obj, .vs, .git, packages, _archives

SETLOCAL EnableDelayedExpansion

SET REPO_URL=https://raw.githubusercontent.com/Echopraxium/tscg/main/

echo ============================================
echo Generation de files.txt avec URLs raw GitHub
echo ============================================
echo.
echo Dossiers exclus: bin, obj, .vs, .git, packages, _archives
echo.

REM Supprime l'ancien fichier s'il existe
if exist files.txt del files.txt

REM Initialise les compteurs
set /a file_count=0
set /a excluded_count=0

REM Liste tous les fichiers avec les extensions specifiees
for /r %%f in (*.cs *.fs *.md *.csproj *.fsproj *.jsonld *.bat *.txt) do (
    set "fullpath=%%f"
    set "relativepath=%%f"
    
    REM Convertit en chemin relatif
    set "relativepath=!relativepath:%CD%\=!"
    
    REM Flag pour savoir si on doit exclure ce fichier
    set "exclude=0"
    
    REM Test pour _archives SPECIFIQUEMENT (doit etre fait en premier)
    echo !relativepath! | findstr /i /c:"_archives" >nul
    if not errorlevel 1 (
        set "exclude=1"
        set /a excluded_count+=1
    )
    
    REM Si pas encore exclu, teste les autres dossiers
    if !exclude!==0 (
        for %%d in (bin obj .vs .git packages) do (
            if not !exclude!==1 (
                REM Test si le dossier est dans le chemin
                echo !relativepath! | findstr /i /c:"\%%d\" >nul
                if not errorlevel 1 (
                    set "exclude=1"
                    set /a excluded_count+=1
                )
                
                REM Test si le dossier est au debut du chemin
                if not !exclude!==1 (
                    echo !relativepath! | findstr /i /b "%%d\" >nul
                    if not errorlevel 1 (
                        set "exclude=1"
                        set /a excluded_count+=1
                    )
                )
            )
        )
    )
    
    REM Si pas exclu, on ajoute au fichier
    if !exclude!==0 (
        REM Remplace les backslashes par des slashes pour URL
        set "urlpath=!relativepath:\=/!"
        
        REM Encode les espaces pour URL
        set "urlpath=!urlpath: =%%20!"
        
        REM Ajoute l'URL au fichier
        echo %REPO_URL%!urlpath! >> files.txt
        
        REM Incremente le compteur
        set /a file_count+=1
    )
)

echo.
echo ============================================
echo Termine !
echo ============================================
echo.
echo URLs generees       : !file_count!
echo Fichiers exclus     : !excluded_count!
echo.
echo Fichier cree: files.txt
echo.
echo VERIFICATION: Recherche de lignes avec _archives...
findstr /i /c:"_archives" files.txt >nul
if errorlevel 1 (
    echo [OK] Aucune ligne avec _archives trouvee !
) else (
    echo [ATTENTION] Des lignes avec _archives sont encore presentes !
    echo.
    echo Lignes problematiques:
    findstr /i /c:"_archives" files.txt
)
echo.

ENDLOCAL
pause
