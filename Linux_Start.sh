#!/bin/bash

echo ""
echo "+--------------------------------------------------+"
echo "|         Nexus Extraction - Launcher             |"
echo "+--------------------------------------------------+"
echo ""

# === Verification Python 3.12 ===
echo "[1/3] Verification de Python 3.12..."

if python3.12 --version &>/dev/null; then
    PYTHON=python3.12
elif python3 --version 2>/dev/null | grep -q "Python 3.12"; then
    PYTHON=python3
else
    echo ""
    echo "[ERREUR] Python 3.12 n'est pas installe !"
    echo "Installez-le avec : sudo apt install python3.12"
    echo "Ou telechargez-le sur : https://www.python.org/downloads/"
    echo ""
    read -p "Appuyez sur Entree pour quitter..."
    exit 1
fi

echo "[OK] Python 3.12 detecte !"
echo ""

# === Installation des dependances ===
echo "[2/3] Installation des dependances..."
echo ""

$PYTHON -m pip install --upgrade pip --quiet
$PYTHON -m pip install pygame --quiet
$PYTHON -m pip install cryptography --quiet
$PYTHON -m pip install requests --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERREUR] Impossible d'installer les dependances !"
    echo "Verifiez votre connexion internet."
    echo ""
    read -p "Appuyez sur Entree pour quitter..."
    exit 1
fi

echo "[OK] Dependances installees !"
echo ""

# === Lancement du jeu ===
echo "[3/3] Lancement de Nexus Extraction..."
echo ""

cd "$(dirname "$0")"
$PYTHON src/data/main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERREUR] Le jeu a plante ! Consultez les logs dans src/data/logs/"
    echo ""
    read -p "Appuyez sur Entree pour quitter..."
fi