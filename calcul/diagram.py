"""Étape 3 : diagramme complet de la figure III-2 et calculs.
- fermeture : extrémité haute de rang i reliée à l'extrémité basse de rang i (ordre des x) ;
- trois paires forcées (passages dessous sur des courbes, vérifiés à l'image : nonapp.png) ;
- composantes, orientations, signes des croisements ;
- nombres d'enlacement ; polynôme d'Alexander de chaque composante seule ;
- critère de séparation par étagement pour chaque sous-entrelacs de trois ronds ;
- polynôme d'Alexander à plusieurs variables (évaluation modulaire) : non nul => non scindé.
Toutes les conventions sont écrites ; aucune donnée du corpus n'est reproduite."""
import json, numpy as np, random, itertools, sympy as sp
from collections import defaultdict, Counter

arcs = [a for a in json.load(open("arcs.json")) if "chemin" in a]
for i, a in enumerate(arcs):
    a["id"] = i; a["P"] = np.array(a["chemin"], float)
D = json.load(open("croisements.json"))
cross = D["croisements"]

# --- paires forcées (extrémités non appariées par le critère d'angle) ---
def find_end(col, y, x):
    best = None
    for a in arcs:
        if a["couleur"] != col: continue
        for end, p in ((0, a["P"][0]), (1, a["P"][-1])):
            d = np.hypot(p[0] - y, p[1] - x)
            if best is None or d < best[0]: best = (d, a["id"], end)
    assert best[0] < 3, best
    return best[1], best[2]
def over_arc(m, excl):
    best = None
    for a in arcs:
        if a["id"] in excl: continue
        dd = np.linalg.norm(a["P"] - m, axis=1); k = int(dd.argmin())
        if best is None or dd[k] < best[0]: best = (float(dd[k]), a["id"], k)
    return best
FORCES = [("noir", (562, 1117), (581, 1082)), ("noir", (1433, 1095), (1440, 1057)), ("vert", (562, 535), (579, 573))]
for col, p1, p2 in FORCES:
    a1, e1 = find_end(col, *p1); a2, e2 = find_end(col, *p2)
    m = (np.array(p1) + np.array(p2)) / 2
    d, o, k = over_arc(m, {a1, a2})
    cross.append({"sous_a": a1, "sous_a_end": e1, "sous_b": a2, "sous_b_end": e2, "dessus": o, "dessus_idx": k,
                  "dist_dessus": d, "milieu": m.tolist(), "force": True})

# --- faux croisements : coupure de l'arc par un trait parasite (écart < 15 px, aucun brin dessus à < 20 px) ---
def gap_len(c):
    pa = arcs[c["sous_a"]]["P"][0 if c["sous_a_end"] == 0 else -1]
    pb = arcs[c["sous_b"]]["P"][0 if c["sous_b_end"] == 0 else -1]
    return float(np.linalg.norm(pa - pb))
faux = [c for c in cross if gap_len(c) < 15 and c["dist_dessus"] > 20]
cross = [c for c in cross if c not in faux]
print("faux croisements (continuités) :", [(arcs[c["sous_a"]]["couleur"], [round(v) for v in c["milieu"]]) for c in faux])

# --- graphe des extrémités : arête interne d'arc, arête de passage dessous, arête de fermeture ---
adj = defaultdict(list)
for a in arcs:
    adj[(a["id"], 0)].append(("arc", (a["id"], 1))); adj[(a["id"], 1)].append(("arc", (a["id"], 0)))
for ci, c in enumerate(cross + faux):
    u, v = (c["sous_a"], c["sous_a_end"]), (c["sous_b"], c["sous_b_end"])
    adj[u].append(("gap", v, ci)); adj[v].append(("gap", u, ci))
B = D["bords"]
haut = sorted([b for b in B if b["bord"] == "haut"], key=lambda b: b["x"])
bas = sorted([b for b in B if b["bord"] == "bas"], key=lambda b: b["x"])
assert len(haut) == len(bas) == 8
for h, b in zip(haut, bas):
    assert h["col"] == b["col"], (h, b)
    u, v = (h["arc"], h["end"]), (b["arc"], b["end"])
    adj[u].append(("ferm", v)); adj[v].append(("ferm", u))
bad = [k for k, v in adj.items() if len(v) != 2]
assert not bad, ("degrés", bad)

# --- parcours des composantes ---
seen = set(); comps = []
for a in arcs:
    if (a["id"], 0) in seen: continue
    seq = []  # liste d'arcs orientés (id, sens) ; sens 0 = de l'extrémité 0 vers 1
    start = (a["id"], 0); cur = start
    while True:
        aid, end = cur
        seen.add((aid, 0)); seen.add((aid, 1))
        seq.append((aid, 0 if end == 0 else 1))
        other = (aid, 1 - end)
        nxt = [e for e in adj[other] if e[0] != "arc"][0]
        cur = nxt[1]
        if cur == start: break
        if cur[0] == aid: break
    comps.append(seq)
col_of = {a["id"]: a["couleur"] for a in arcs}
print("composantes :", len(comps), [Counter(col_of[i] for i, _ in s) for s in comps])
comp_of, sens_of = {}, {}
for k, s in enumerate(comps):
    for aid, sens in s:
        comp_of[aid] = k; sens_of[aid] = sens
couleur_comp = {k: Counter(col_of[i] for i, _ in s).most_common(1)[0][0] for k, s in enumerate(comps)}

# --- signes : direction de passage du brin dessous et du brin dessus (repère mathématique : x à droite, y en haut) ---
def dirvec(aid, idx):
    P = arcs[aid]["P"]; n = len(P)
    i0, i1 = max(0, idx - 3), min(n - 1, idx + 3)
    v = P[i1] - P[i0]
    if sens_of[aid] == 1: v = -v
    return np.array([v[1], -v[0]])  # (x, y_math)
for c in faux:
    c["comp_sous"] = None
for c in cross:
    # brin dessous : de l'extrémité quittée vers l'extrémité retrouvée, dans le sens de parcours
    a, ea, b, eb = c["sous_a"], c["sous_a_end"], c["sous_b"], c["sous_b_end"]
    # on quitte l'arc a par son extrémité de sortie si (sens 0 et end 1) ou (sens 1 et end 0)
    sort_a = (sens_of[a] == 0 and ea == 1) or (sens_of[a] == 1 and ea == 0)
    pa, pb = arcs[a]["P"][0 if ea == 0 else -1], arcs[b]["P"][0 if eb == 0 else -1]
    u = (pb - pa) if sort_a else (pa - pb)
    u = np.array([u[1], -u[0]])
    o = dirvec(c["dessus"], c["dessus_idx"])
    c["signe"] = int(np.sign(o[0] * u[1] - o[1] * u[0]))
    c["comp_sous"] = comp_of[a]; c["comp_dessus"] = comp_of[c["dessus"]]
    assert comp_of[a] == comp_of[b]
print("croisements :", len(cross), "; signes nuls :", sum(1 for c in cross if c["signe"] == 0))

# --- enlacements ---
lk = defaultdict(int); selfc = Counter(); writhe = Counter()
for c in cross:
    i, j = c["comp_sous"], c["comp_dessus"]
    if i == j: selfc[i] += 1; writhe[i] += c["signe"]
    else: lk[tuple(sorted((i, j)))] += c["signe"]
print("couleurs :", couleur_comp)
print("croisements propres :", dict(selfc), "; vrilles (writhe) :", dict(writhe))
print("enlacements (somme des signes / 2) :", {k: v / 2 for k, v in lk.items()})

# --- présentation de Wirtinger d'un sous-ensemble de composantes ---
def wirtinger(S):
    """Générateurs = arcs maximaux du sous-diagramme (coupés seulement aux passages dessous
    dont le brin dessus est dans S). Relation à chaque tel croisement."""
    keep = [c for c in cross if c["comp_sous"] in S and c["comp_dessus"] in S]
    cut = {id(c) for c in keep}
    gen = {}; g = 0
    for k in S:
        seq = comps[k]
        # position de départ : juste après un passage coupé, s'il y en a
        n = len(seq)
        # liste des passages entre arcs consécutifs du parcours
        links = []
        for t in range(n):
            aid = seq[t][0]; nxt = seq[(t + 1) % n][0]
            # quel croisement relie la sortie de aid à nxt ?
            cc = None
            for c in cross:
                if {c["sous_a"], c["sous_b"]} == {aid, nxt} and (c["comp_sous"] == k): cc = c
            links.append(cc)
        starts = [t for t in range(n) if links[t - 1] is not None and id(links[t - 1]) in cut] or [0]
        t0 = starts[0]
        cur = None
        for s in range(n):
            t = (t0 + s) % n
            if s == 0 or (links[t - 1] is not None and id(links[t - 1]) in cut):
                cur = g; g += 1
            gen[seq[t][0]] = cur
    rel = []
    for c in keep:
        a, b = c["sous_a"], c["sous_b"]
        # orienter : entrée -> sortie
        ea = c["sous_a_end"]
        sort_a = (sens_of[a] == 0 and ea == 1) or (sens_of[a] == 1 and ea == 0)
        gin, gout = (gen[a], gen[b]) if sort_a else (gen[b], gen[a])
        rel.append((gin, gout, gen[c["dessus"]], c["signe"]))
    comp_gen = {}
    for aid, gg in gen.items(): comp_gen[gg] = comp_of[aid]
    return g, rel, comp_gen

def fox_matrix(ngen, rel, comp_gen, tval):
    """Relation x_out = x_over^{e} x_in x_over^{-e} (e = signe, convention de Wirtinger).
    Ligne de Fox abélianisée : d/dx_in, d/dx_out, d/dx_over."""
    M = [[0] * ngen for _ in rel]
    for r, (gi, go, gv, e) in enumerate(rel):
        t = tval[comp_gen[gv]]
        # relation r = x_over^e x_in x_over^-e x_out^-1 ; dérivées de Fox abélianisées (x_k -> t_comp)
        if e == 1:
            M[r][gi] += t; M[r][gv] += 1 - tval[comp_gen[gi]]; M[r][go] += -1
        else:
            tinv = t ** -1 if not isinstance(t, int) else None
            M[r][gi] += tinv; M[r][gv] += -tinv + tinv * tval[comp_gen[gi]]; M[r][go] += -1
    return M

def det_mod(M, p):
    A = [[x % p for x in row] for row in M]; n = len(A); det = 1
    for i in range(n):
        piv = next((r for r in range(i, n) if A[r][i]), None)
        if piv is None: return 0
        if piv != i: A[i], A[piv] = A[piv], A[i]; det = -det
        det = det * A[i][i] % p; inv = pow(A[i][i], p - 2, p)
        for r in range(i + 1, n):
            f = A[r][i] * inv % p
            if f:
                for cidx in range(i, n): A[r][cidx] = (A[r][cidx] - f * A[i][cidx]) % p
    return det % p

class Fp(int):
    pass
def alexander_nonzero(S, essais=6, p=1_000_000_007):
    ngen, rel, comp_gen = wirtinger(S)
    res = []
    for _ in range(essais):
        tv = {k: random.randrange(2, p - 1) for k in S}
        # travailler modulo p : t^-1 = inverse modulaire
        M = [[0] * ngen for _ in rel]
        for r, (gi, go, gv, e) in enumerate(rel):
            t = tv[comp_gen[gv]]; ti = tv[comp_gen[gi]]
            if e == 1:
                M[r][gi] += t; M[r][gv] += 1 - ti; M[r][go] += -1
            else:
                tinv = pow(t, p - 2, p)
                M[r][gi] += tinv; M[r][gv] += -tinv + tinv * ti; M[r][go] += -1
        # mineur : supprimer une ligne et une colonne
        Mm = [row[1:] for row in M[1:]]
        res.append(det_mod(Mm, p))
    return ngen, len(rel), res

def alexander_knot(k):
    ngen, rel, comp_gen = wirtinger([k])
    t = sp.symbols("t")
    M = sp.zeros(len(rel), ngen)
    for r, (gi, go, gv, e) in enumerate(rel):
        if e == 1:
            M[r, gi] += t; M[r, gv] += 1 - t; M[r, go] += -1
        else:
            M[r, gi] += 1 / t; M[r, gv] += -1 / t + 1; M[r, go] += -1
    if ngen == 0 or len(rel) == 0:
        return ngen, len(rel), sp.Integer(1)
    Mm = M[1:, 1:]
    d = sp.factor(sp.simplify(Mm.det(method="berkowitz")))
    return ngen, len(rel), d

print("\n== Chaque composante seule (croisements propres seulement) ==")
for k in range(len(comps)):
    ng, nr, d = alexander_knot(k)
    num, den = sp.fraction(sp.together(d))
    print(couleur_comp[k], ": générateurs", ng, "relations", nr, "; Alexander =", sp.factor(num), "/", den, "; |Δ(-1)| =", abs(d.subs(sp.Symbol('t'), -1)))

print("\n== Étagement des sous-entrelacs de trois ronds (critère suffisant de séparation) ==")
for X in range(len(comps)):
    S = [k for k in range(len(comps)) if k != X]
    rel = Counter()
    for c in cross:
        i, j = c["comp_sous"], c["comp_dessus"]
        if i in S and j in S and i != j: rel[(i, j)] += 1  # (dessous, dessus)
    pairs = {}
    ok = True
    for i, j in itertools.combinations(S, 2):
        a, b = rel[(i, j)], rel[(j, i)]
        pairs[(couleur_comp[i], couleur_comp[j])] = (a, b)
        if a and b: ok = False
    # acyclicité de l'ordre « dessous -> dessus »
    import networkx as nx
    G = nx.DiGraph(); G.add_nodes_from(S); G.add_edges_from([e for e, v in rel.items() if v])
    print("sans", couleur_comp[X], ": (i sous j, j sous i) par paire =", pairs, "; étagé =", ok and nx.is_directed_acyclic_graph(G))

print("\n== Polynôme d'Alexander à plusieurs variables, évaluations modulo p ==")
print("entrelacs complet :", alexander_nonzero(list(range(len(comps)))))
for X in range(len(comps)):
    S = [k for k in range(len(comps)) if k != X]
    print("sans", couleur_comp[X], ":", alexander_nonzero(S))
json.dump({"croisements": [{k: v for k, v in c.items() if k != "milieu"} for c in cross]}, open("diagramme.json", "w"), default=float, indent=0)

print("\n== Contrôle sans signes : déterminant de coloriage (2·dessus − entrée − sortie) ==")
for k in range(len(comps)):
    ngen, rel, comp_gen = wirtinger([k])
    M = sp.zeros(len(rel), ngen)
    for r, (gi, go, gv, e) in enumerate(rel):
        M[r, gv] += 2; M[r, gi] -= 1; M[r, go] -= 1
    print(couleur_comp[k], ": |det mineur| =", abs(M[1:, 1:].det()) if ngen > 1 else 1)

print("\n== Suite dessus / dessous le long de chaque composante (croisements propres seulement) ==")
for k in range(len(comps)):
    ev = []
    for t, (aid, sens) in enumerate(comps[k]):
        P = arcs[aid]["P"]; n = len(P)
        evs = []
        for ci, c in enumerate(cross):
            if c["comp_sous"] == k and c["comp_dessus"] == k and c["dessus"] == aid:
                pos = c["dessus_idx"] if sens == 0 else n - 1 - c["dessus_idx"]
                evs.append((pos, f"D{ci}"))
        evs.sort()
        ev += [e for _, e in evs]
        # passage dessous à la sortie de l'arc
        nxt = comps[k][(t + 1) % len(comps[k])][0]
        for ci, c in enumerate(cross):
            if c["comp_sous"] == k and c["comp_dessus"] == k and {c["sous_a"], c["sous_b"]} == {aid, nxt}:
                ev.append(f"S{ci}")
    print(couleur_comp[k], " ".join(ev))

# ===================== Invariants de Milnor par développement de Magnus =====================
# Séries non commutatives tronquées au degré DEG, variables X_c (une par composante).
DEG = 3
def smul(a, b):
    r = defaultdict(int)
    for wa, ca in a.items():
        for wb, cb in b.items():
            if len(wa) + len(wb) <= DEG:
                r[wa + wb] += ca * cb
    return {w: c for w, c in r.items() if c}
def sinv_gen(c, e):
    # (1+X)^e pour e = ±1, tronqué
    if e == 1: return {(): 1, (c,): 1}
    return {tuple([c] * k): (-1) ** k for k in range(DEG + 1)}
def sconj_inv(s):
    # inverse d'une série 1 + ... : somme (-u)^k
    u = {w: c for w, c in s.items() if w != ()}
    r = {(): 1}; p = {(): 1}
    for k in range(1, DEG + 1):
        p = smul(p, {w: -c for w, c in u.items()})
        for w, c in p.items(): r[w] = r.get(w, 0) + c
    return {w: c for w, c in r.items() if c}

OW = None  # calculé après la table des transitions
ncomp = len(comps)
E = {a["id"]: {(): 1, (comp_of[a["id"]],): 1} for a in arcs if a["id"] in comp_of}
trans = {}
for c in cross:
    trans[(c["sous_a"], c["sous_a_end"], c["sous_b"], c["sous_b_end"])] = c
    trans[(c["sous_b"], c["sous_b_end"], c["sous_a"], c["sous_a_end"])] = c
def transition(k, t):
    seq = comps[k]; n = len(seq)
    aid, s = seq[t]; nxt, s2 = seq[(t + 1) % n]
    return trans.get((aid, 1 if s == 0 else 0, nxt, 0 if s2 == 0 else 1))
OW = {}
for k in range(len(comps)):
    L = []
    for t in range(len(comps[k])):
        c = transition(k, t)
        if c is not None and c["comp_sous"] == k:
            L.append((comps[k][t][0], comps[k][(t + 1) % len(comps[k])][0], c["dessus"], c["signe"]))
    OW[k] = L
for it in range(DEG + 3):
    newE = {}
    for k in range(ncomp):
        seq = comps[k]; n = len(seq)
        cur = {(): 1, (k,): 1}; newE[seq[0][0]] = cur
        for t in range(n - 1):
            nxt = seq[t + 1][0]
            c = transition(k, t)
            if c is not None and c["comp_sous"] == k:
                w = E[c["dessus"]] if c["signe"] == 1 else sconj_inv(E[c["dessus"]])
                cur = smul(smul(w, cur), sconj_inv(w))
            newE[nxt] = cur   # sans croisement (fermeture, faux croisement) : même générateur
    stable = all(newE[a] == E[a] for a in E)
    E = newE
print("\n== Invariants de Milnor (Magnus, degré ≤ 3) ; itérations stables :", stable, "==")
def longitude(k):
    lam = {(): 1}
    for (ain, aout, aov, e) in OW[k]:
        w = E[aov] if e == 1 else sconj_inv(E[aov])
        lam = smul(w, lam)
    return lam
nm = {k: couleur_comp[k] for k in range(ncomp)}
for k in range(ncomp):
    lam = longitude(k)
    autres = [j for j in range(ncomp) if j != k]
    l2 = {(nm[i], nm[j]): lam.get((i, j), 0) for i in autres for j in autres if i != j}
    l3 = {tuple(nm[x] for x in w): c for w, c in lam.items() if len(w) == 3 and k not in w and len(set(w)) == 3}
    print("longitude de", nm[k], ": μ(ij,k) =", {a: b for a, b in l2.items() if b}, "| μ(ijl,k) non nuls =", l3)

# ===================== Export en code PD (convention KnotTheory / spherogram) =====================
def evenements(k):
    """Suite ordonnée des passages de la composante k par les croisements : ('S', ci) dessous, ('D', ci) dessus."""
    seq = comps[k]; n = len(seq); ev = []
    idx_of = {id(c): i for i, c in enumerate(cross)}
    for t, (aid, s) in enumerate(seq):
        P = arcs[aid]["P"]; m = len(P); dess = []
        for ci, c in enumerate(cross):
            if c["dessus"] == aid:
                pos = c["dessus_idx"] if s == 0 else m - 1 - c["dessus_idx"]
                dess.append((pos, ci))
        ev += [("D", ci) for _, ci in sorted(dess)]
        c = transition(k, t)
        if c is not None:
            ev.append(("S", idx_of[id(c)]))
    return ev
def pd_code(flip=()):
    lab = 0; inn = {}; out = {}
    for k in range(ncomp):
        ev = evenements(k); n = len(ev); base = lab
        for t, e in enumerate(ev):
            inn[e] = base + t; out[e] = base + (t + 1) % n
        lab += n
    PD = []
    for ci, c in enumerate(cross):
        U, O = ("S", ci), ("D", ci)
        s = c["signe"]
        if ci in flip:            # inversion du croisement : le brin dessus passe dessous
            U, O = O, U; s = -s
        a, cc = inn[U], out[U]; oin, oout = inn[O], out[O]
        b, d = (oout, oin) if s == 1 else (oin, oout)
        PD.append([a, b, cc, d])
    return PD
json.dump({"pd": pd_code(), "pd_noir_corrige": pd_code(flip=(25,)), "couleurs": couleur_comp,
           "comp_croisements": [[c["comp_sous"], c["comp_dessus"]] for c in cross]}, open("pd.json", "w"))
print("\ncode PD écrit : pd.json (", len(cross), "croisements )")

print("\n== Invariants de Milnor à indices répétés (sous-entrelacs noir-vert), degré 3 ==")
for k in range(ncomp):
    lam = longitude(k)
    rep = {tuple(nm[x] for x in w): c for w, c in lam.items() if len(w) == 3 and len(set(w)) < 3}
    sel = {w: c for w, c in rep.items() if set(w) <= {"noir", "vert"}}
    print("longitude de", nm[k], ":", sel)
