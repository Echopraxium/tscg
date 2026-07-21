@echo off
REM ============================================================================
REM  verify_session_2026-07-18.bat
REM  Verifie que les fichiers du working tree correspondent aux livrables du
REM  zip Claude (session 2026-07-18), via git hash-object (insensible CRLF/LF).
REM  Place dans ontology/cli-tools/. Lancer depuis la RACINE du repo:
REM      ontology\cli-tools\verify_session_2026-07-18.bat
REM  OK   = fichier local identique au livrable  -> ne rien copier
REM  DIFF = contenu different (version obsolete)  -> recopier depuis le zip
REM  MISS = fichier absent                        -> copier depuis le zip
REM ============================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0\..\.."
set OK=0
set KO=0
echo(
echo   STATUS  DEBUT..FIN   FICHIER
echo   ------  ----------   -------
call :check "ontology\M1_CoreConcepts.jsonld" 4822 2e5c
call :check "ontology\M1_CoreConcepts_README.md" dad4 3dda
call :check "ontology\M2_GenericConcepts.jsonld" 680d f6a3
call :check "ontology\M2_GenericConcepts_README.md" e4bc a71f
call :check "ontology\cli-tools\check-M1\M1_Schema_shacl.ttl" 92e8 dcb5
call :check "ontology\M1_Domains.jsonld" 6ad0 d04c
call :check "ontology\M1_Domains_README.md" 2424 35a6
call :check "ontology\M3_BicephalousPerspective.jsonld" 0fc9 1b71
call :check "ontology\M3_BicephalousPerspective_README.md" 4789 eaf1
call :check "ontology\M3_GrammarFoundation.jsonld" fc88 bcbb
call :check "ontology\M3_GrammarFoundation_README.md" adf4 8788
call :check "instances\tscg-tools\TscgOntologyValidator\M0_TscgOntologyValidator_README.md" 9003 f854
echo(
echo   OK=%OK%   DIFF/MISS=%KO%
echo(
if %KO% GTR 0 (echo   ^>^> Recopier depuis le zip les fichiers marques DIFF ou MISS, puis relancer.) else (echo   ^>^> Tout est aligne sur le zip.)
endlocal
goto :eof

:check
set "F=%~1"
set "RDEB=%~2"
set "RFIN=%~3"
if not exist "%F%" (
  echo   MISS    %RDEB%..%RFIN%   %F%
  set /a KO+=1
  goto :eof
)
for /f "delims=" %%H in ('git hash-object "%F%"') do set "HASH=%%H"
set "LDEB=!HASH:~0,4!"
set "LFIN=!HASH:~-4!"
if "!LDEB!"=="%RDEB%" if "!LFIN!"=="%RFIN%" (
  echo   OK      !LDEB!..!LFIN!   %F%
  set /a OK+=1
  goto :eof
)
echo   DIFF    !LDEB!..!LFIN!   %F%   ^(attendu %RDEB%..%RFIN%^)
set /a KO+=1
goto :eof
