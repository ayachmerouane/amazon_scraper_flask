from flask import Flask, render_template, request, jsonify, send_file
import scraper, storage, config, os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", historique=storage.charger_historique())

@app.route("/scraper", methods=["POST"])
def scraper_route():
    data = request.get_json()
    entree = data.get("url", "").strip()
    
    if not entree:
        return jsonify({"erreur": "Saisie vide"}), 400

    if entree.startswith("http"):
        resultat = scraper.scraper_produit(entree)
    else:
        resultat = scraper.scraper_par_nom(entree)

    if "erreur" in resultat:
        return jsonify(resultat), 500

    storage.sauvegarder(resultat)
    return jsonify(resultat)

@app.route("/historique")
def historique_route():
    return jsonify(storage.charger_historique())

@app.route("/export")
def export_csv():
    if not os.path.isfile(config.OUTPUT_FILE):
        return "Fichier introuvable", 404
    return send_file(os.path.abspath(config.OUTPUT_FILE), as_attachment=True)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, port=5000)