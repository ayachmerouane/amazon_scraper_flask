# 🕷️ Amazon Scraper Flask — ScraperAPI

Interface web Flask pour scraper des produits Amazon.

## 📁 Structure

```
amazon_scraper_flask/
├── app.py              ← Serveur Flask (routes)
├── scraper.py          ← Logique ScraperAPI
├── storage.py          ← Sauvegarde CSV
├── config.py           ← Clé API & paramètres
├── requirements.txt
├── templates/
│   └── index.html      ← Interface web
└── data/
    └── resultats.csv   ← Généré automatiquement
```

## 🚀 Installation & Lancement

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer votre clé API dans config.py
API_KEY = "votre_clé_scraperapi"

# 3. Lancer le serveur
python app.py

# 4. Ouvrir dans le navigateur
http://localhost:5000
```

## ✨ Fonctionnalités

- 🔍 Scraper un produit Amazon (titre, prix, note, avis, image…)
- 📋 Historique de tous les scrapes
- ⬇️ Export CSV en un clic
- 🎨 Interface sombre moderne
