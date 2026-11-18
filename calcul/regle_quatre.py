"""La regle a quatre. Quatre trefles homologues (le meme trefle recopie en parallele : tissage 4 x 4 a chacune des trois etapes).
Entre deux trefles, il y a deux croisements par etape, six en tout. Reglages d'un couple qui laissent les deux trefles libres
(lacan_recherche.py) : 2 constants (l'un toujours sur l'autre) et 6 alternes.
On essaie tous les reglages ou un seul couple alterne, les cinq autres etant constants. Tout triplet se separe alors
(etabli pour trois trefles paralleles, quel que soit le reglage). Reste a voir si les quatre tiennent.

Usage : python regle_quatre.py [nombre de couples alternes, 1 par defaut]
"""
import sys, itertools, json, collections, snappy, spherogram
import lacan_homologues as LH
K = int(sys.argv[1]) if len(sys.argv) > 1 else 1
couples = [tuple(c) for c in json.load(open("lacan_couples.json"))]
const = [c for c in couples if all(c[2 * t] == c[0] and c[2 * t + 1] == -c[0] for t in range(3))]; alt = [c for c in couples if c not in const]
paires = [(i, j) for i in range(4) for j in range(i + 1, 4)]
def signes(choix): return [{**{(i, j): c[2 * t] for (i, j), c in choix.items()}, **{(j, i): c[2 * t + 1] for (i, j), c in choix.items()}} for t in range(3)]
def morceaux(L):
    L = L.copy(); L.simplify("global"); return sorted(len(p.crossings) for p in L.split_link_diagram()) if len(L.crossings) else []
bons = []; n = 0; res = collections.Counter()
for qui in itertools.combinations(range(6), K):
    for a in itertools.product(alt, repeat=K):
        for c in itertools.product(const, repeat=6 - K):
            it = iter(c); ia = iter(a); choix = {p: (next(ia) if k in qui else next(it)) for k, p in enumerate(paires)}
            w = LH.mot(4, signes(choix)); L = spherogram.Link(braid_closure=w); n += 1
            m = morceaux(L)
            if m == [3, 3, 3, 3]: res["les quatre se separent"] += 1; continue
            tri = all(morceaux(L.sublink([i for i in range(4) if i != X])) == [3, 3, 3] for X in range(4))
            res["les quatre tiennent, tout triplet se separe" if tri else "un triplet ne se separe pas"] += 1
            if tri: bons.append({"alterne": [paires[k] for k in qui], "choix": {str(p): v for p, v in choix.items()}, "mot": w, "croisements": len(m) and m}); print("  solution :", [paires[k] for k in qui], a, c, m, flush=True)
print("reglages essayes :", n, dict(res))
json.dump(bons, open(f"regle_quatre_k{K}.json", "w"))
