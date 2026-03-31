@echo off
chcp 65001 > nul
echo Converting TSCG_Research_Paper_Draft_v4.md...
echo.

REM ============================================================
REM  Essai 1 : xelatex + polices Cambria (UTF-8 / symboles math)
REM  Necessite preamble.tex dans le meme dossier
REM ============================================================
where xelatex > nul 2>&1
if %ERRORLEVEL% == 0 (
    echo Engine: xelatex + Cambria/Cambria Math
    pandoc TSCG_Research_Paper_Draft_v4.md ^
      --pdf-engine=xelatex ^
      --include-in-header=preamble.tex ^
      --variable geometry:margin=2.5cm ^
      --variable fontsize=11pt ^
      --variable linestretch=1.15 ^
      --toc ^
      --number-sections ^
      -o TSCG_Research_Paper_Draft_v4.pdf
    goto :check
)

REM ============================================================
REM  Essai 2 : pdflatex (symboles via package textcomp/amssymb)
REM ============================================================
where pdflatex > nul 2>&1
if %ERRORLEVEL% == 0 (
    echo Engine: pdflatex
    pandoc TSCG_Research_Paper_Draft_v4.md ^
      --pdf-engine=pdflatex ^
      --variable geometry:margin=2.5cm ^
      --variable fontsize=11pt ^
      --variable linestretch=1.15 ^
      --toc ^
      --number-sections ^
      -o TSCG_Research_Paper_Draft_v4.pdf
    goto :check
)

REM ============================================================
REM  Fallback HTML -> Chrome/Edge -> Ctrl+P -> Enregistrer PDF
REM ============================================================
:html
echo Generation HTML (fallback)...
pandoc TSCG_Research_Paper_Draft_v4.md ^
  --standalone ^
  --toc ^
  --number-sections ^
  --metadata title="TSCG Research Paper v4.0" ^
  -o TSCG_Research_Paper_Draft_v4.html

if %ERRORLEVEL% == 0 (
    echo.
    echo OK - TSCG_Research_Paper_Draft_v4.html genere.
    echo Ouvrez dans Chrome/Edge puis Ctrl+P - Enregistrer en PDF.
    start TSCG_Research_Paper_Draft_v4.html
) else (
    echo ERREUR - Pandoc absent : https://pandoc.org/installing.html
)
goto :end

:check
if %ERRORLEVEL% == 0 (
    echo.
    echo OK - TSCG_Research_Paper_Draft_v4.pdf genere avec succes.
    goto :end
)
echo.
echo ERREUR PDF - Basculement vers HTML...
goto :html

:end
echo.
pause
