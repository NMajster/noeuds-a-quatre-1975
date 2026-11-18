"""Pour une tresse refermee (mot avec G = le brin de gauche passe dessus, D = celui de droite), repetee trois fois :
entre deux ronds, qui passe dessus, et combien de fois ?  Une relation constante = l'un des deux est toujours dessus."""
import json, sys, collections
def analyse(nom, mot, nb, k=3):
    pos = list(range(nb)); ev = []
    for _ in range(k):
        for i, d in mot:
            a, b = pos[i], pos[i + 1]; ev.append((a, b) if d == "G" else (b, a)); pos[i], pos[i + 1] = b, a
    # ronds = cycles de la permutation des brins
    perm = {pos[r]: r for r in range(nb)}            # le brin s finit au rang r, et repart comme brin de rang r
    rond = {}; nr = 0
    for s in range(nb):
        if s in rond: continue
        x = s
        while x not in rond: rond[x] = nr; x = perm[x]
        nr += 1
    # identite des brins au fil des periodes : le brin etiquete s est suivi sur les k periodes, donc pas de recollage a faire si k periodes referment
    C = collections.Counter((rond[a], rond[b]) for a, b in ev)
    print(nom, ": ronds", nr, "| croisements d'un rond avec lui-meme :", [C[(r, r)] for r in range(nr)])
    for a in range(nr):
        for b in range(a + 1, nr):
            print(f"    rond {a} sur rond {b} : {C[(a, b)]} fois ; rond {b} sur rond {a} : {C[(b, a)]} fois", "-> constant" if 0 in (C[(a, b)], C[(b, a)]) else "")
if __name__ == "__main__":
    for nom in ("dessin0", "dessin1", "dessin2"):
        D = json.load(open(f"soury3/{nom}.json")); analyse(nom + " de Soury", [tuple(x) for x in D["mot"]], 6)
    M = json.load(open("motif_tresse.json")); analyse("figure de quatre trefles (rectifiee)", [tuple(x) for x in M["mot"]], 8)
