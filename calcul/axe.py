"""Le motif d'une periode, referme, avec l'axe autour duquel on le repete.
L'axe est ajoute au diagramme quotient : il passe dessus les 8 brins a l'aller, dessous au retour.
On regarde : les 4 ronds sans l'axe ; les 4 ronds avec l'axe ; 3 ronds avec l'axe, compares au temoin
(trois ronds independants, chacun enfile deux fois sur l'axe).

Usage : python axe.py
"""
import json, snappy, spherogram
from collections import deque, defaultdict
import periode as P

def chemin_ordonne(qpair, qface, a, b):
    vois = defaultdict(list)
    for h, h2 in qpair.items(): vois[qface[h]].append((qface[h2], h))
    prev = {a: None}; file = deque([a])
    while file:
        x = file.popleft()
        if x == b: break
        for y, h in vois[x]:
            if y not in prev: prev[y] = (x, h); file.append(y)
    L = []; x = b
    while prev[x] is not None: x0, h = prev[x]; L.append(h); x = x0
    return L[::-1]

def avec_axe(qpair, nq, chemin):
    """Renvoie le code PD du diagramme auquel on a ajoute l'axe (composante supplementaire)."""
    pair = dict(qpair); n = len(chemin)
    XO = [nq + 2 * i for i in range(n)]; XR = [nq + 2 * i + 1 for i in range(n)]
    def lie(u, v): pair[u] = v; pair[v] = u
    for i, h in enumerate(chemin):
        h2 = qpair[h]
        lie(h, (XO[i], 0)); lie((XO[i], 2), (XR[i], 3)); lie((XR[i], 1), h2)
    for i in range(n - 1):
        lie((XO[i], 1), (XO[i + 1], 3)); lie((XR[i + 1], 2), (XR[i], 0))
    lie((XO[0], 3), (XR[0], 2)); lie((XO[n - 1], 1), (XR[n - 1], 0))
    lab = {}; k = 0; PD = [[None] * 4 for _ in range(nq + 2 * n)]
    for h, h2 in pair.items():
        if h not in lab: lab[h] = lab[h2] = k; k += 1
        PD[h[0]][h[1]] = lab[h]
    return [tuple(X) for X in PD]

def temoin(m):
    """m ronds independants, chacun enfile deux fois sur l'axe : tresse s1 s3 s5... refermee, avec son axe."""
    # diagramme annulaire : pour chaque rond, un croisement entre ses deux brins
    qpair = {}
    for r in range(m):
        # croisement r : brins 0 (dessous entrant), 2 (dessous sortant), 1 et 3 (dessus). Fermeture : 2 -> 3 et 1 -> 0 (deux tours)
        qpair[(r, 2)] = (r, 3); qpair[(r, 3)] = (r, 2); qpair[(r, 1)] = (r, 0); qpair[(r, 0)] = (r, 1)
    return qpair, m

D = json.load(open(r"pd.json"))
PD = D["pd_noir_corrige"]; A = P.automorphismes(PD); f = [g for g in A if P.ordre(g) == 3][0]
qpair, nq, qface, nqf, qfix, _ = P.quotient(PD, f)
ch = chemin_ordonne(qpair, qface, qfix[0], qfix[1]); print("brins traverses par l'axe :", len(ch))
Q = spherogram.Link(avec_axe(qpair, nq, ch)); nc = len(Q.link_components)
print("motif + axe : composantes", nc, "; croisements", len(Q.crossings)); lm = Q.linking_matrix(); print("enlacements :", lm)
axe = [i for i in range(nc) if sum(abs(x) for x in lm[i]) == max(sum(abs(x) for x in r) for r in lm)][0]; print("l'axe est la composante", axe)
M = Q.exterior()
for e in range(6):
    if M.solution_type() == "all tetrahedra positively oriented": break
    M.randomize()
print("motif + axe :", M.solution_type(), "volume", M.volume())
def desc(L, nom):
    L = L.copy(); L.simplify("global"); parts = L.split_link_diagram()
    M = L.exterior()
    print(f"{nom} : {len(L.crossings)} croisements apres simplification, morceaux {len(parts)} ; {M.solution_type()} ; volume {float(M.volume()):.6f} ; H1 {M.homology()}")
    return L
ronds = [i for i in range(nc) if i != axe]
desc(Q.sublink(ronds), "les 4 ronds sans l'axe")
res = []
for X in ronds:
    res.append(desc(Q.sublink([i for i in range(nc) if i != X]), f"sans le rond {X} (3 ronds + axe)"))
# temoin : trois ronds independants enfiles deux fois sur l'axe = tresse s1 s3 s5 sur 6 brins, l'axe etant un 7e brin qui fait le tour
W = spherogram.Link(braid_closure=[1, 3, 5, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6])
print("temoin : composantes", len(W.link_components), "enlacements", W.linking_matrix())
Wd = desc(W, "temoin (3 ronds independants + axe)")
json.dump({"temoin": Wd.PD_code(), "sans": [L.PD_code() for L in res]}, open(r"axe.json", "w"))
