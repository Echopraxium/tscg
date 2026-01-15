@echo off
:: uuid: e8f4a2b1-c3d4-4b1e-9a2f-7c8b9d0e1f2a
:: Script de Rebuild Sécurisé (Deep Clean + Build)
:: Protection contre les verrous de fichiers (File Locks)

:: 1. Définition des cibles à surveiller (Les applications qui pourraient verrouiller les DLLs)
::    Note: On inclut TSCP.Doc2B64z qui est notre nouvel outil.
set "TARGETS='TSCG.CLI','TSCG.Server','TSCG.GUI','TSCG.Doc2B64z'"

:: 2. Construction de la logique PowerShell
::    - Vérifie si les processus tournent.
::    - Si OUI : Alerte rouge + Liste les coupables + STOP.
::    - Si NON : Nettoyage (bin/obj/.vs) + Rebuild.

set "PS_LOGIC=$targets = %TARGETS%; Write-Host '--- TSCP REBUILD SHIELD ---' -Fore Cyan; $running = Get-Process -Name $targets -ErrorAction SilentlyContinue; if ($running) { Write-Host '' ; Write-Host 'BLOCAGE CRITIQUE : Des processus TSCP sont actifs !' -Fore Red; Write-Host 'Impossible de recompiler car les fichiers sont verrouilles.' -Fore Red; Write-Host 'Veuillez fermer les fenetres suivantes :' -Fore Yellow; $running | ForEach-Object { Write-Host (' [X] ' + $_.ProcessName + ' (ID: ' + $_.Id + ')') -Fore Yellow }; Write-Host ''; Read-Host 'Appuyez sur Entree pour quitter sans rien faire...'; return }; Write-Host 'Aucun verrou detecte. Demarrage du nettoyage...' -Fore Green; Get-ChildItem -Path . -Include bin,obj -Recurse | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; if (Test-Path .\.vs) { Remove-Item -Path .\.vs -Recurse -Force -ErrorAction SilentlyContinue; Write-Host 'Cache Visual Studio (.vs) nettoye.' -Fore Gray }; Write-Host 'Lancement de dotnet build...' -Fore Cyan; dotnet clean; dotnet restore; dotnet build; if ($LASTEXITCODE -eq 0) { Write-Host '' ; Write-Host 'SUCCES : La solution est a jour.' -Fore Green } else { Write-Host '' ; Write-Host 'ECHEC du build.' -Fore Red }; Read-Host 'Appuyez sur Entree pour fermer...'"

:: 3. Exécution dans une nouvelle fenêtre PowerShell
start "TSCG Builder" powershell -NoExit -Command "& { %PS_LOGIC% }"