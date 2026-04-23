# storage.py — Sauvegarde et lecture CSV

import csv
import os
from datetime import datetime
import config

COLONNES = ["date", "titre", "marque", "prix", "note", "nb_avis", "disponibilite", "url"]


def sauvegarder(produit: dict):
    os.makedirs("data", exist_ok=True)
    existe = os.path.isfile(config.OUTPUT_FILE)
    produit["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(config.OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES)
        if not existe:
            writer.writeheader()
        writer.writerow({col: produit.get(col, "N/A") for col in COLONNES})


def charger_historique() -> list:
    if not os.path.isfile(config.OUTPUT_FILE):
        return []
    with open(config.OUTPUT_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
