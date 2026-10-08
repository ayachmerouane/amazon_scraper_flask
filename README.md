# 🕷️ Amazon Scraper — Application Flask

Application web qui extrait les informations d'un produit Amazon à partir de son URL (titre, prix, note, nombre d'avis, image), conserve l'historique des recherches et permet de l'exporter en CSV.

<!-- Ajoute une capture d'écran de l'interface : -->
<!-- ![Aperçu de l'interface](docs/apercu.png) -->

## ✨ Fonctionnalités

- 🔍 Scraping d'un produit Amazon (.fr et .com) à partir de n'importe quelle URL
- 🧹 Normalisation automatique des URL (extraction de l'identifiant ASIN)
- 🔁 Retry automatique en cas de timeout
- 📋 Historique de tous les produits scrapés
- ⬇️ Export CSV en un clic
- 🎨 Interface web sombre et moderne

## ⚙️ Fonctionnement

```
Navigateur ──► Flask (app.py) ──► scraper.py ──► ScraperAPI ──► Amazon
                    │                  │
                    │                  └─► BeautifulSoup (extraction des données)
                    └─► storage.py ──► data/resultats.csv
```

L'application passe par **ScraperAPI**, qui gère les proxies et le rendu JavaScript, pour limiter les blocages.

## 🛠️ Stack technique

Python · Flask · Requests · BeautifulSoup · HTML/CSS · ScraperAPI

## 🚀 Lancer le projet

```bash
git clone https://github.com/ayachmerouane/amazon_scraper_flask.git
cd amazon_scraper_flask
pip install -r requirements.txt
```

Crée un fichier `config.py` (il n'est pas versionné) :

```python
API_KEY = "votre_clé_scraperapi"
```

Puis lance le serveur et ouvre http://localhost:5000 :

```bash
python app.py
```

## 📁 Structure

```
amazon_scraper_flask/
├── app.py              ← Serveur Flask (routes)
├── scraper.py          ← Appels ScraperAPI et extraction
├── storage.py          ← Sauvegarde CSV
├── config.py           ← Clé API (à créer, non versionné)
├── templates/
│   └── index.html      ← Interface web
└── requirements.txt
```

## ⚠️ Avertissement

Projet réalisé à des fins pédagogiques. Respectez les conditions d'utilisation d'Amazon.

## 👤 Auteur

**Merouane Ayach** — [GitHub](https://github.com/ayachmerouane)
