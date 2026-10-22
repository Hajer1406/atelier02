
import csv
import json
import sys
import time
from pathlib import Path
from classifieur import CONSIGNE, classer
from evaluation import afficher_rapport
PAUSE = 2.1
BASE_DIR = Path(__file__).resolve().parent.parent
DOSSIER_RESULTATS = BASE_DIR / "resultats"
def charger(chemin=None):
    if chemin is None:
        chemin = BASE_DIR / "data" / "tickets.csv"
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    if len(lignes) != 72:
        print(f"Attention : {len(lignes)} tickets ont été chargés, et non 72.")
    if not lignes:
        raise ValueError("Le fichier tickets.csv est vide.")
    return lignes
def evaluer(modele, lignes, consigne=CONSIGNE, etiquette=None):
    etiquette = etiquette or modele
    vrais = []
    predits = []
    debut = time.time()
    print(f"=== {etiquette} ===")
    print(f"Nombre de tickets : {len(lignes)}")
    for i, ligne in enumerate(lignes, start=1):
        prediction = classer(
            ligne["texte"],
            modele,
            consigne=consigne,
        )
        predits.append(prediction)
        vrais.append(ligne["categorie"].strip().lower())
        print(f"[{i}/{len(lignes)}] {ligne['id']} -> {prediction}")
        if i < len(lignes):
            time.sleep(PAUSE)
    resume = afficher_rapport(etiquette, vrais, predits)
    resume.update({
        "modele": modele,
        "etiquette": etiquette,
        "duree_s": round(time.time() - debut, 1),
        "predits": predits,
        "ids": [ligne["id"] for ligne in lignes],
    })
    DOSSIER_RESULTATS.mkdir(parents=True, exist_ok=True)
    nom_fichier = (
    etiquette.replace("/", "_")
    .replace(" ", "_")
    .replace("+", "plus")
    + ".json"
)
    fichier_sortie = DOSSIER_RESULTATS / nom_fichier
    with open(fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)
    print(f"\nRésultats enregistrés dans : {fichier_sortie}")
    return resume
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Utilisation : "
            "python .\\code\\evaluer.py openai/gpt-oss-20b"
        )
        sys.exit(1)
    evaluer(sys.argv[1], charger())
