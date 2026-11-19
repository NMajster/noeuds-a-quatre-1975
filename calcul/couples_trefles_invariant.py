"""Les trois partages des quatre trefles en deux couples sont-ils distingues par le noeud lui-meme ?
Pour chaque couple de trefles, on comble ces deux trefles le long de leur longitude (operation qui ne depend ni du dessin
ni du miroir) et on calcule le volume de ce qui reste. Deux couples que le noeud ne distingue pas donnent le meme volume.
Usage : venv-snappy/Scripts/python.exe couples_trefles_invariant.py"""
import json, itertools, snappy, spherogram
D = json.load(open("../donnees/pd.json")); L = spherogram.Link([tuple(x) for x in D["pd_noir_corrige"]]); coul = D["couleurs"]; CC = D["comp_croisements"]
noms = []
for comp in L.link_components:
    cs = {ce.crossing.label for ce in comp}; k = next(i for i, (a, b) in enumerate(CC) if a == b and i in cs); noms.append(coul[str(CC[k][0])])
def vol(pente, paire):
    best = None
    for essai in range(8):
        M = L.exterior()
        for e in range(essai): M.randomize()
        for i in paire: M.dehn_fill(pente, i)
        if M.solution_type() in ("all tetrahedra positively oriented", "contains negatively oriented tetrahedra"):
            v = float(M.volume())
            if M.solution_type() == "all tetrahedra positively oriented": return round(v, 6), "sûr"
            best = (round(v, 6), "à confirmer")
    return best or (None, M.solution_type())
for pente in ((0, 1), (1, 1), (-1, 1), (1, 2), (-1, 2)):
    print("comblement de pente", pente)
    for i, j in itertools.combinations(range(4), 2):
        print("   ", noms[i] + "-" + noms[j], vol(pente, (i, j)))
