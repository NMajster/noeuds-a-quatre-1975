"""Preuve par diagrammes : le motif prive d'un rond, avec l'axe, est le meme entrelacs que trois ronds independants
enfiles deux fois sur l'axe. On simplifie les deux diagrammes et on cherche un isomorphisme de diagrammes
(meme dessin a deformation du plan pres, dessus/dessous respectes, sans miroir).

Usage : python axe_preuve.py   (apres axe.py)
"""
import json, itertools, random, snappy, spherogram
from collections import deque
import periode as P
import axe as AX     # relance axe.py (quelques secondes) et donne Q, ronds, axe

def iso(PD1, PD2):
    if len(PD1) != len(PD2): return False
    p1, p2 = P.structure(PD1), P.structure(PD2); n = len(PD1)
    for c1 in range(n):
        for r in (0, 2):
            f = {0: (c1, r)}; ok = True; file = deque([0])
            while file and ok:
                c = file.popleft(); d, rot = f[c]
                for i in range(4):
                    c2, j = p1[(c, i)]; d2, j2 = p2[(d, (i + rot) % 4)]; rot2 = (j2 - j) % 4
                    if rot2 not in (0, 2): ok = False; break
                    if c2 in f:
                        if f[c2] != (d2, rot2): ok = False; break
                    else: f[c2] = (d2, rot2); file.append(c2)
            if ok and len(f) == n and len({v[0] for v in f.values()}) == n: return True
    return False
def formes(L, essais=40):
    """Plusieurs diagrammes simplifies a 12 croisements du meme entrelacs."""
    F = []
    for e in range(essais):
        K = L.copy(); K.backtrack(steps=random.randint(0, 12)) if e else None; K.simplify("global")
        if len(K.crossings) == 12:
            pd = [tuple(x) for x in K.PD_code()]
            if not any(iso(pd, g) for g in F): F.append(pd)
    return F
random.seed(1)
axe_loop = [6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6]
T = {}
for eps in itertools.product((1, -1), repeat=3):
    if tuple(sorted(eps)) != eps: continue          # a permutation des ronds pres
    W = spherogram.Link(braid_closure=[eps[0] * 1, eps[1] * 3, eps[2] * 5] + axe_loop)
    T[eps] = formes(W); print("temoin", eps, ":", len(T[eps]), "forme(s) a 12 croisements")
Q, ronds, axe = AX.Q, AX.ronds, AX.axe
nc = len(Q.link_components)
for X in ronds:
    F = formes(Q.sublink([i for i in range(nc) if i != X]))
    trouve = [eps for eps, G in T.items() if any(iso(a, b) for a in F for b in G)]
    print(f"motif sans le rond {X}, avec l'axe : {len(F)} forme(s) ; meme diagramme que le temoin de signes {trouve}")
