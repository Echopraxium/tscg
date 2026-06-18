@echo off
setlocal
:: ============================================================
::  TSCG — M0_Counterpoint
::  Download WebAudioFont instrument samples
::  Author: Echopraxium with the collaboration of Claude AI
:: ============================================================

set BASE=https://surikov.github.io/webaudiofontdata/sound
set DEST=%~dp0sounds

if not exist "%DEST%" mkdir "%DEST%"
echo [TSCG] Downloading instrument samples to %DEST%
echo.

:: WebAudioFontPlayer runtime
curl -L -o "%DEST%\..\WebAudioFontPlayer.js" ^
  "https://surikov.github.io/webaudiofont/npm/dist/WebAudioFontPlayer.js"
echo [OK] WebAudioFontPlayer.js

:: Organ (0190)
curl -L -o "%DEST%\0190_GeneralUserGS_sf2_file.js" ^
  "%BASE%/0190_GeneralUserGS_sf2_file.js"
echo [OK] Organ

:: Piano (0000)
curl -L -o "%DEST%\0000_JCLive_sf2_file.js" ^
  "%BASE%/0000_JCLive_sf2_file.js"
echo [OK] Piano

:: Harpsichord (0060)
curl -L -o "%DEST%\0060_GeneralUserGS_sf2_file.js" ^
  "%BASE%/0060_GeneralUserGS_sf2_file.js"
echo [OK] Harpsichord

:: Flute (0730)
curl -L -o "%DEST%\0730_JCLive_sf2_file.js" ^
  "%BASE%/0730_JCLive_sf2_file.js"
echo [OK] Flute

:: Strings (0490)
curl -L -o "%DEST%\0490_GeneralUserGS_sf2_file.js" ^
  "%BASE%/0490_GeneralUserGS_sf2_file.js"
echo [OK] Strings

:: Choir (0520)
curl -L -o "%DEST%\0520_GeneralUserGS_sf2_file.js" ^
  "%BASE%/0520_GeneralUserGS_sf2_file.js"
echo [OK] Choir

:: Trumpet (0560)
curl -L -o "%DEST%\0560_GeneralUserGS_sf2_file.js" ^
  "%BASE%/0560_GeneralUserGS_sf2_file.js"
echo [OK] Trumpet

echo.
echo [TSCG] Done. Structure:
echo   static\
echo     WebAudioFontPlayer.js
echo     sounds\
echo       0000_JCLive_sf2_file.js       (Piano)
echo       0060_GeneralUserGS_sf2_file.js (Harpsichord)
echo       0190_GeneralUserGS_sf2_file.js (Organ)
echo       0490_GeneralUserGS_sf2_file.js (Strings)
echo       0520_GeneralUserGS_sf2_file.js (Choir)
echo       0560_GeneralUserGS_sf2_file.js (Trumpet)
echo       0730_JCLive_sf2_file.js       (Flute)
echo.
pause
