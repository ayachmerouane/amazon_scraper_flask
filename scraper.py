import requests
from bs4 import BeautifulSoup
import time
import config
import re
from urllib.parse import urlparse

def nettoyer_url_amazon(url):
    if not url.startswith("http"):
        url = "https://" + url
    parsed = urlparse(url)
    domaine = parsed.netloc.replace("www.", "") or "amazon.fr"
    match = re.search(r'/(dp|gp/product)/([A-Z0-9]{10})', url)
    if match:
        return f"https://{domaine}/dp/{match.group(2)}", domaine
    return url, domaine

def fetch_page(url: str, domaine: str, use_render: str = "true", tentatives: int = 3) -> requests.Response | None:
    """Appelle ScraperAPI avec un système de retry automatique en cas de timeout."""
    pays = "us" if ".com" in domaine else "fr"
    params = {
        "api_key": config.API_KEY,
        "url": url,
        "render": use_render,
        "country_code": pays,
    }

    for i in range(tentatives):
        try:
            print(f"📡 Tentative {i+1}/{tentatives} pour : {url[:50]}...")
            # Timeout de 60s par tentative
            response = requests.get(config.BASE_URL, params=params, timeout=60)
            if response.status_code == 200:
                return response
            elif response.status_code == 403:
                print("⚠️ Clé API invalide ou limite atteinte.")
                break
        except Exception as e:
            print(f"❌ Erreur sur tentative {i+1} : {e}")
        
        # Attendre un peu avant de réessayer
        time.sleep(2)
        
    return None

def extraire(soup: BeautifulSoup, url: str) -> dict:
    titre_el = soup.select_one("#productTitle")
    titre = titre_el.get_text(strip=True) if titre_el else "N/A"

    prix_raw = "N/A"
    p_el = soup.select_one(".a-price .a-offscreen") or soup.select_one("#price_inside_buybox")
    if p_el:
        prix_raw = p_el.get_text(strip=True)
    
    # Formatage : Chiffre puis Symbole à droite
    prix_clean = prix_raw.replace("€", "").replace("$", "").replace("\xa0", "").strip()
    
    if prix_clean != "N/A":
        prix = f"{prix_clean} $" if ".com" in url else f"{prix_clean} €"
    else:
        prix = "N/A"

    img_el = soup.select_one("#landingImage") or soup.select_one("#imgBlkFront")
    image = img_el["src"] if img_el else ""

    return {
        "url": url,
        "titre": titre,
        "marque": (soup.select_one("#bylineInfo") or soup.select_one("#brand")).get_text(strip=True) if soup.select_one("#bylineInfo") else "N/A",
        "prix": prix,
        "note": soup.select_one(".a-icon-alt").get_text(strip=True) if soup.select_one(".a-icon-alt") else "N/A",
        "nb_avis": soup.select_one("#acrCustomerReviewText").get_text(strip=True) if soup.select_one("#acrCustomerReviewText") else "0 avis",
        "disponibilite": (soup.select_one("#availability")).get_text(strip=True) if soup.select_one("#availability") else "En stock",
        "image": image,
    }

def scraper_produit(url: str) -> dict:
    url_propre, domaine = nettoyer_url_amazon(url)
    res = fetch_page(url_propre, domaine, use_render="true", tentatives=2)
    if not res: return {"erreur": "Délai dépassé après plusieurs tentatives."}
    
    soup = BeautifulSoup(res.text, "html.parser")
    if not soup.select_one("#productTitle"):
        return {"erreur": "Amazon a bloqué la page produit."}
    return extraire(soup, url_propre)

def scraper_par_nom(nom: str) -> dict:
    query = nom.replace(' ', '+')
    search_url = f"https://www.amazon.fr/s?k={query}"
    
    # Recherche rapide sans JS pour éviter le timeout
    res = fetch_page(search_url, "amazon.fr", use_render="false", tentatives=3)
    
    if not res: 
        return {"erreur": "La recherche Amazon est inaccessible pour le moment."}
    
    soup = BeautifulSoup(res.text, "html.parser")
    a_tag = soup.select_one('h2 a.a-link-normal')
    
    if not a_tag:
        for link in soup.find_all('a', href=True):
            if "/dp/" in link['href'] and "customerReviews" not in link['href']:
                a_tag = link
                break

    if a_tag and "/dp/" in a_tag['href']:
        path = a_tag['href'].split("?")[0]
        target = "https://www.amazon.fr" + path if path.startswith("/") else path
        return scraper_produit(target)
    
    return {"erreur": "Aucun produit trouvé."}