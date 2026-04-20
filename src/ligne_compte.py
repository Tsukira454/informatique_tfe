import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
extensions = [".py"]
total_lines = 0
total_files = 0

for fichier in ROOT.rglob("*"):
    if fichier.suffix in extensions:
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                nb_lines = len(lines)
                total_lines += nb_lines
                total_files += 1
                print(f"{fichier.relative_to(ROOT)} -> {nb_lines} lignes")
        except Exception as e:
            print(f"Erreur sur {fichier} : {e}")

print(f"\n{'='*40}")
print(f"Total : {total_files} fichiers | {total_lines} lignes")