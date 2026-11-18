"""Trefles homologues (recopies en parallele) : recherche de toutes les facons de regler dessus/dessous, etape par etape.
1. Deux trefles : parmi les reglages d'enlacement nul, lesquels se separent ?
2. Trois trefles : parmi les reglages ou chaque couple se separe, lesquels tiennent a trois (noeud borromeen de trois trefles) ?
3. Quatre trefles : reglages ou chaque triplet se separe et ou les quatre tiennent.

Usage : python lacan_recherche.py
"""
import itertools, json, snappy, spherogram
import lacan_homologues as LH
def separe(w, k):
    """True si le diagramme se simplifie en k trefles disjoints (preuve de separation)."""
    L = spherogram.Link(braid_closure=w); L.simplify("global")
    P = L.split_link_diagram() if len(L.crossings) else []
    return sorted(len(p.crossings) for p in P) == [3] * k
# 1. couples : signes (etape t, (0,1)) et (etape t, (1,0)), somme nulle
couples = []
for s in itertools.product((1, -1), repeat=6):
    if sum(s) != 0: continue
    sg = [{(0, 1): s[2 * t], (1, 0): s[2 * t + 1]} for t in range(3)]
    if separe(LH.mot(2, sg), 2): couples.append(s)
print("reglages d'un couple, enlacement nul : 20 ; qui se separent :", len(couples), flush=True)
for s in couples: print("   ", s, "(constant)" if all(s[2 * t] == s[0] and s[2 * t + 1] == -s[0] for t in range(3)) else "")
json.dump(couples, open("lacan_couples.json", "w"))
# 2. triplets
def signes(n, choix):                       # choix[(i, j)] pour i < j : un reglage de couple
    return [{**{(i, j): c[2 * t] for (i, j), c in choix.items()}, **{(j, i): c[2 * t + 1] for (i, j), c in choix.items()}} for t in range(3)]
tri = []
for c in itertools.product(couples, repeat=3):
    choix = {(0, 1): c[0], (0, 2): c[1], (1, 2): c[2]}; w = LH.mot(3, signes(3, choix))
    if not separe(w, 3): tri.append(c)
print("reglages de trois trefles ou chaque couple se separe :", len(couples) ** 3, "; qui ne se separent pas a trois :", len(tri), flush=True)
for c in tri[:12]:
    r, M = LH.decrit(LH.mot(3, signes(3, {(0, 1): c[0], (0, 2): c[1], (1, 2): c[2]})), 3); print("   ", c, r["croisements"], r["solution"], r["volume"], flush=True)
json.dump(tri, open("lacan_triplets.json", "w"))
