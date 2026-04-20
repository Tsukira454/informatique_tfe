@echo off
chcp 65001 >nul
title Nexus Extraction - Launcher

echo.
echo +--------------------------------------------------+
echo ^|         Nexus Extraction - Launcher             ^|
echo +--------------------------------------------------+
echo.

:: === Verification Python 3.12 ===
echo [1/3] Verification de Python 3.12...

python --version 2>nul | findstr /C:"Python 3.12" >nul
if %errorlevel% neq 0 (
    py -3.12 --version 2>nul | findstr /C:"Python 3.12" >nul
    if %errorlevel% neq 0 (
        echo.
        echo [ERREUR] Python 3.12 n'est pas installe !
        echo Telechargez-le sur : https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON=py -3.12
    )
) else (
    set PYTHON=python
)

echo [OK] Python 3.12 detecte !
echo.

:: === Installation des dependances ===
echo [2/3] Installation des dependances...
echo.

%PYTHON% -m pip install --upgrade pip --quiet
%PYTHON% -m pip install pygame --quiet
%PYTHON% -m pip install cryptography --quiet
%PYTHON% -m pip install requests --quiet

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Impossible d'installer les dependances !
    echo Verifiez votre connexion internet.
    echo.
    pause
    exit /b 1
)

echo [OK] Dependances installees !
echo.

:: === Lancement du jeu ===
echo [3/3] Lancement de Nexus Extraction...
echo.

cd /d "%~dp0"
%PYTHON% src/data/main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Le jeu a plante ! Consultez les logs dans src/data/logs/
    echo.
    pause
)