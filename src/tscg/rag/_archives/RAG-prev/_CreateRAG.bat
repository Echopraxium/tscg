:: _CreateRAG.bat
@echo off
echo ========================================
echo  TSCG RAG - Creation de la base
echo ========================================
echo.

echo Choisissez le mode:
echo  [1] Mode local (recommandé)
echo  [2] Mode API Google (avancé)
echo  [3] Annuler
echo.

set /p choice="Votre choix [1-3]: "

if "%choice%"=="1" (
    echo Mode LOCAL selectionne
    python create_RAG_lan.py local
    pause
) else if "%choice%"=="2" (
    echo Mode API Google selectionne
    echo.
    set /p project="Entrez le Google Cloud Project ID: "
    python create_RAG_lan.py api --project "%project%"
    pause
) else (
    echo Operation annulee
    pause
)