@echo off
chcp 65001 > nul
echo ========================================
echo  TSCG v6.0 - Conversion HTML + PDF
echo ========================================
echo.

REM Genere un HTML standalone avec style preprint
REM --from markdown-tex_math_dollars : desactive l'interpretation LaTeX math
REM    (evite que _^ et | soient interpretes comme du TeX)
pandoc TSCG_Research_Paper_Draft_v6.md ^
  --standalone ^
  --from markdown-tex_math_dollars ^
  --toc ^
  --toc-depth=3 ^
  --number-sections ^
  --metadata title="TSCG: The Transdisciplinary System Construction Game" ^
  --css=preprint.css ^
  --syntax-highlighting=kate ^
  -o TSCG_Research_Paper_Draft_v6.html

if %ERRORLEVEL% NEQ 0 (
    echo ERREUR - Pandoc absent : https://pandoc.org/installing.html
    pause
    exit /b 1
)

echo.
echo OK - TSCG_Research_Paper_Draft_v6.html genere.
echo.
echo ========================================
echo  ETAPES POUR GENERER LE PDF :
echo ========================================
echo  1. Le fichier HTML va s'ouvrir dans votre navigateur
echo  2. Appuyez Ctrl+P (Imprimer)
echo  3. Destination : "Enregistrer en PDF"
echo  4. Mise en page : Portrait, A4
echo  5. Marges : Normales (ou Personnalisees : 1.5cm)
echo  6. Cochez "Graphiques d'arriere-plan"
echo  7. Decochez "En-tetes et pieds de page"
echo  8. Cliquez "Enregistrer"
echo ========================================
echo.

start TSCG_Research_Paper_Draft_v6.html
pause
