import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOSSIER_RESULTATS = BASE_DIR / "resultats"

FICHIERS_MODELES = {
    "GPT-OSS-120B": "openai_gpt-oss-120b.json",
    "GPT-OSS-20B": "openai_gpt-oss-20b.json",
    "Qwen sans exemples": "qwen_qwen3.8-27b_sans_exemples.json",
    "Qwen avec 4 exemples": "qwen_qwen3.8-27b_plus_4_exemples.json",
}


def charger_resultats():
    resultats = {}

    for nom_modele, nom_fichier in FICHIERS_MODELES.items():
        chemin = DOSSIER_RESULTATS / nom_fichier

        if not chemin.exists():
            print(f"Fichier manquant : {nom_fichier}")
            continue

        try:
            with open(chemin, encoding="utf-8") as fichier:
                donnees = json.load(fichier)

            resultats[nom_modele] = donnees

        except (json.JSONDecodeError, OSError) as erreur:
            print(f"Impossible de lire {nom_fichier} : {erreur}")

    return resultats


def afficher_tableau(resultats):
    print("\n=== TABLEAU COMPARATIF ===")
    print(
        f"{'Modèle':28} "
        f"{'Accuracy':>10} "
        f"{'F1 macro':>10} "
        f"{'Invalides':>10}"
    )

    for modele, donnees in resultats.items():
        accuracy = donnees.get("accuracy", "N/D")
        f1_macro = donnees.get("f1_macro", "N/D")
        invalides = donnees.get("taux_invalides", "N/D")

        if isinstance(accuracy, (int, float)):
            accuracy = f"{accuracy:.3f}"

        if isinstance(f1_macro, (int, float)):
            f1_macro = f"{f1_macro:.3f}"

        if isinstance(invalides, (int, float)):
            invalides = f"{invalides:.3f}"

        print(
            f"{modele:28} "
            f"{str(accuracy):>10} "
            f"{str(f1_macro):>10} "
            f"{str(invalides):>10}"
        )


def comparer_tickets(resultats):
    if len(resultats) < 2:
        print("\nIl faut au moins deux fichiers de résultats valides.")
        return

    predictions_par_modele = {}

    for modele, donnees in resultats.items():
        ids = donnees.get("ids", [])
        predictions = donnees.get("predits", [])

        if len(ids) != len(predictions):
            print(f"Attention : IDs et prédictions incohérents pour {modele}.")

        predictions_par_modele[modele] = dict(zip(ids, predictions))

    premier_modele = next(iter(predictions_par_modele))
    ids_reference = list(
        predictions_par_modele[premier_modele].keys()
    )

    ids_communs = set(ids_reference)

    for predictions in predictions_par_modele.values():
        ids_communs &= set(predictions.keys())

    divergences = []

    for ticket_id in ids_reference:
        if ticket_id not in ids_communs:
            continue

        valeurs = {
            modele: predictions[ticket_id]
            for modele, predictions in predictions_par_modele.items()
        }

        if len(set(valeurs.values())) > 1:
            divergences.append((ticket_id, valeurs))

    print("\n=== TICKETS SUR LESQUELS LES MODÈLES DIVERGENT ===")
    print(f"Nombre de tickets communs : {len(ids_communs)}")
    print(f"Nombre de tickets divergents : {len(divergences)}")

    for ticket_id, valeurs in divergences:
        print(f"\nTicket {ticket_id}")
        for modele, prediction in valeurs.items():
            print(f"  {modele} : {prediction}")

    tous_different = [
        (ticket_id, valeurs)
        for ticket_id, valeurs in divergences
        if len(set(valeurs.values())) == len(resultats)
    ]

    print(
        "\nTickets où les quatre configurations donnent "
        f"des prédictions toutes différentes : {len(tous_different)}"
    )

    for ticket_id, valeurs in tous_different:
        print(f"  {ticket_id} : {valeurs}")


if __name__ == "__main__":
    resultats = charger_resultats()

    if resultats:
        afficher_tableau(resultats)
        comparer_tickets(resultats)