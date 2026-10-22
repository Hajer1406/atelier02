CATEGORIES = ["facturation", "technique", "compte", "commercial"]
def accuracy(vrais, predits):
    if not vrais:
        return 0.0
    return sum(1 for v, p in zip(vrais, predits) if v == p) / len(vrais)
def scores_par_classe(vrais, predits, classes=CATEGORIES):
    resultat = {}
    for c in classes:
        vp = sum(1 for v, p in zip(vrais, predits) if v == c and p == c)
        fp = sum(1 for v, p in zip(vrais, predits) if v != c and p == c)
        fn = sum(1 for v, p in zip(vrais, predits) if v == c and p != c)

        precision = vp / (vp + fp) if (vp + fp) else 0.0
        recall = vp / (vp + fn) if (vp + fn) else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall)
            else 0.0
        )
        resultat[c] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": vp + fn,
        }
    return resultat
def f1_macro(scores):
    if not scores:
        return 0.0
    return sum(d["f1"] for d in scores.values()) / len(scores)
def taux_invalides(predits):
    if not predits:
        return 0.0
    invalides = sum(1 for p in predits if p not in CATEGORIES)
    return invalides / len(predits)
def matrice_confusion(vrais, predits):
    # Les lignes représentent les catégories réelles.
    # Les colonnes représentent les catégories prédites.
    # Une colonne supplémentaire compte les prédictions invalides.
    colonnes = CATEGORIES + ["invalide"]
    matrice = {
        vrai: {pred: 0 for pred in colonnes}
        for vrai in CATEGORIES
    }
    for vrai, predit in zip(vrais, predits):
        if vrai not in CATEGORIES:
            continue
        if predit not in CATEGORIES:
            predit = "invalide"
        matrice[vrai][predit] += 1
    return matrice
def afficher_rapport(etiquette, vrais, predits):
    scores = scores_par_classe(vrais, predits)
    rapport = {
        "etiquette": etiquette,
        "accuracy": accuracy(vrais, predits),
        "scores_par_classe": scores,
        "f1_macro": f1_macro(scores),
        "taux_invalides": taux_invalides(predits),
        "matrice_confusion": matrice_confusion(vrais, predits),
    }
    print(f"\n===== Rapport : {etiquette} =====")
    print(f"Accuracy : {rapport['accuracy']:.3f}")
    print(f"Macro-F1 : {rapport['f1_macro']:.3f}")
    print(f"Taux invalides : {rapport['taux_invalides']:.1%}")

    print("\nScores par catégorie :")
    for categorie, valeurs in scores.items():
        print(
            f"{categorie:<13} "
            f"Precision={valeurs['precision']:.3f} "
            f"Recall={valeurs['recall']:.3f} "
            f"F1={valeurs['f1']:.3f} "
            f"Support={valeurs['support']}"
        )
    print("\nMatrice de confusion (lignes = réel, colonnes = prédit) :")
    print(f"{'Réel / Prédit':<13}" + "".join(f"{c:>13}" for c in CATEGORIES + ["invalide"]))

    for categorie, ligne in rapport["matrice_confusion"].items():
        print(f"{categorie:<13}" + "".join(f"{ligne[c]:>13}" for c in CATEGORIES + ["invalide"]))
    return rapport