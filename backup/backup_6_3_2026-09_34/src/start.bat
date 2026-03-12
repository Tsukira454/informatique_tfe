@echo off
title Lancement du script Python

REM Vérification de Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non detecte. Installation en cours...
    winget install -e --id Python.Python.3 --silent
    if %errorlevel% neq 0 (
        echo Erreur lors de l'installation de Python.
        echo Essayer d'installer python 3.13.11 manuellement
        pause
        exit /b
    )
)

echo Python detecte.
echo Lancement du script...
python "%~dp0main.py"

pause
