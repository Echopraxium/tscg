@echo off
REM =============================================================
REM TscgOntologyAPIServer — _setup.bat
REM Installe les prerequis Python pour tscg_api_server.py,
REM tscg_api_cli.py et tscg_api_client_example.py
REM
REM Usage: double-cliquer ou lancer depuis cmd.exe
REM Chemin attendu: instances\tscg-tools\TscgOntologyAPIServer\src\
REM
REM Author: Echopraxium with the collaboration of Claude AI
REM =============================================================

setlocal
cd /d "%~dp0"

echo.
echo ============================================================
echo  TscgOntologyAPIServer -- Installation des prerequis Python
echo ============================================================
echo.

REM -- Verifier que Python est disponible ----------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas trouve dans le PATH.
    echo Installer Python 3.11+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo Python trouve :
python --version
echo.

REM -- Installer les dependances --------------------------------
echo Installation des dependances depuis requirements.txt ...
echo.

pip install --upgrade pip
echo.

pip install "fastapi>=0.110.0"
pip install "uvicorn[standard]>=0.29.0"
pip install "pyoxigraph>=0.5.0"
pip install "rdflib>=6.3.0"
pip install "pydantic>=2.0.0"
pip install "requests>=2.31.0"

echo.
echo ============================================================
echo  Verification des versions installees
echo ============================================================
echo.

python -c "import fastapi;     print('fastapi     :', fastapi.__version__)"
python -c "import uvicorn;     print('uvicorn     :', uvicorn.__version__)"
python -c "import pyoxigraph;  print('pyoxigraph  :', pyoxigraph.__version__)"
python -c "import rdflib;      print('rdflib      :', rdflib.__version__)"
python -c "import pydantic;    print('pydantic    :', pydantic.__version__)"
python -c "import requests;    print('requests    :', requests.__version__)"

echo.
echo ============================================================
echo  Installation terminee !
echo.
echo  Pour demarrer le serveur (CLI):
echo    python tscg_api_cli.py start
echo.
echo  Pour demarrer avec auto-chargement de l'ontologie:
echo    python tscg_api_cli.py start --ontology-dir ..\..\..\..\ontology
echo.
echo  Swagger UI (apres demarrage):
echo    http://127.0.0.1:8000/docs
echo ============================================================
echo.

pause
endlocal
