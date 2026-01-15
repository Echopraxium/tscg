@echo off
:: uuid: c3d4e5f6-a7b8-5901-c2d3-e4f5a6b7c8d9
:: This script runs the Integrity Suite only (No Server/CLI launch).
:: It focuses on displaying test traces and pauses for verification.

:: Define paths relative to the root folder
set TEST_PROJECT=src/TSCP.Tests/TSCP.Tests.fsproj

:: Define the PowerShell logic
:: 1. Run Tests on the specific Test Project
:: 2. Display specific success/failure messages
:: 3. Always Pause (Read-Host) to allow the user to read the traces
set "PS_LOGIC=Write-Host '--- TSCP CORE 5 INTEGRITY SUITE (TEST ONLY) ---' -Fore Cyan; Write-Host '[1/1] Verifying Systemic Axioms (M3/M2)...' -Fore Gray; dotnet test %TEST_PROJECT% --nologo; if ($LASTEXITCODE -eq 0) { Write-Host ''; Write-Host 'SUCCESS: Axioms VALIDATED.' -Fore Green } else { Write-Host ''; Write-Host 'FAILURE: Axioms broken. Review errors above.' -Fore Red }; Write-Host ''; Read-Host 'Press Enter to exit...'"

:: Launch PowerShell
start powershell -NoExit -Command "& { %PS_LOGIC% }"