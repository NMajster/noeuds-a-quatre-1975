"""Lecture d'une figure de noeud en couleurs (figures I-8 et I-9 du Sinthome, lecon du 18 novembre 1975 ; XI-7 de RSI).
1. masque par couleur ; arcs = composantes connexes (un trait est interrompu la ou il passe dessous) ; squelette ; extremites.
2. appariement des extremites de meme couleur de part et d'autre de chaque interruption.
3. pour chaque interruption, les traits qui la traversent : zero (pointille, simple continuite), un, ou plusieurs croisements.
4. composantes, signes des croisements, code PD.
Sortie : <nom>.json (code PD, couleur de chaque composante, couple dessous/dessus de chaque croisement) et <nom>_controle.png.

Usage : python lire_figure.py <nom> <image> x0 y0 x1 y1
"""
import sys, json, math, cv2, numpy as np
nom = sys.argv[1]; img = sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7]); ech = 3
bgr = cv2.imread(img)[y0:y1, x0:x1]; bgr = cv2.resize(bgr, None, fx=ech, fy=ech, interpolation=cv2.INTER_CUBIC).astype(int)
rgb = bgr[:, :, ::-1]
REFS = {"noir": (0, 0, 0), "vert": (60, 163, 90), "rouge": (176, 0, 30), "brun": (224, 176, 122)}
dist = np.stack([np.sqrt(((rgb - np.array(c)) ** 2).sum(2)) for c in REFS.values()], 0)
proche = dist.argmin(0); encre = (np.sqrt(((rgb - 255) ** 2).sum(2)) > 110) & (dist.min(0) < 110)
masques = {c: (encre & (proche == k)) for k, c in enumerate(REFS)}
masques = {c: m for c, m in masques.items() if m.sum() > 400 * ech * ech}

def zhang_suen(im):
    im = im.copy().astype(np.uint8); changed = True
    while changed:
        changed = False
        for step in (0, 1):
            p = np.pad(im, 1)
            P2, P3, P4, P5 = p[:-2, 1:-1], p[:-2, 2:], p[1:-1, 2:], p[2:, 2:]
            P6, P7, P8, P9 = p[2:, 1:-1], p[2:, :-2], p[1:-1, :-2], p[:-2, :-2]
            nb = [P2, P3, P4, P5, P6, P7, P8, P9]; Bn = sum(nb)
            A = sum(((nb[i] == 0) & (nb[(i + 1) % 8] == 1)).astype(int) for i in range(8))
            c = (P2 * P4 * P6 == 0) & (P4 * P6 * P8 == 0) if step == 0 else (P2 * P4 * P8 == 0) & (P2 * P6 * P8 == 0)
            m = (im == 1) & (Bn >= 2) & (Bn <= 6) & (A == 1) & c
            if m.any(): im[m] = 0; changed = True
    return im
arcs = []
for coul, mk in masques.items():
    mk = cv2.morphologyEx(mk.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, cc, stats, _ = cv2.connectedComponentsWithStats(mk, connectivity=8)
    for k in range(1, n):
        if stats[k, cv2.CC_STAT_AREA] < 14 * ech * ech: continue
        xx, yy, ww, hh = [int(v) for v in stats[k, :4]]
        sk = zhang_suen(np.pad(cc[yy:yy + hh, xx:xx + ww] == k, 1))[1:-1, 1:-1]
        ys, xs = np.nonzero(sk); pts = set(zip(ys.tolist(), xs.tolist()))
        def nbr(q): return [(q[0] + a, q[1] + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a or b) and (q[0] + a, q[1] + b) in pts]
        ends = [q for q in pts if len(nbr(q)) == 1]
        if len(ends) < 2: print("   composante sans extremite ignoree :", coul, xx // ech + x0, yy // ech + y0); continue
        def bfs(s):
            prev = {s: None}; order = [s]
            for q in order:
                for r in nbr(q):
                    if r not in prev: prev[r] = q; order.append(r)
            return prev, order[-1]
        prev, far = bfs(ends[0]); prev, far2 = bfs(far); path = []; q = far2
        while q is not None: path.append(q); q = prev[q]
        if len(path) < 5 * ech: continue                               # un point de pointille : ignore, ses voisins se raccordent par-dessus
        arcs.append({"coul": coul, "P": np.array([(y + yy, x + xx) for y, x in path], float), "n_ext": len(ends)})
print("arcs :", len(arcs), {c: sum(a["coul"] == c for a in arcs) for c in masques}, "| a plus de deux extremites :", sum(a["n_ext"] > 2 for a in arcs))
def tang(P, b):
    k = min(8 * ech, len(P) - 1); v = (P[0] - P[k]) if b == 0 else (P[-1] - P[-1 - k]); return v / (np.linalg.norm(v) + 1e-9)
EX = [{"arc": i, "b": b, "pt": (a["P"][0] if b == 0 else a["P"][-1]), "t": tang(a["P"], b), "coul": a["coul"]} for i, a in enumerate(arcs) for b in (0, 1)]
def ang(u, v): return math.degrees(math.acos(max(-1, min(1, float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9))))))
def long_(i): return len(arcs[EX[i]["arc"]]["P"]) > 60 * ech
pris = set(); paires = []
for dmax, amax in ((30, 45), (70, 60), (70, 85)):                     # trois passes, de la plus stricte a la plus tolerante
    cands = []
    for i in range(len(EX)):
        for j in range(i + 1, len(EX)):
            if i in pris or j in pris or EX[i]["coul"] != EX[j]["coul"] or (EX[i]["arc"] == EX[j]["arc"] and not long_(i)): continue
            v = EX[j]["pt"] - EX[i]["pt"]; d = np.linalg.norm(v)
            if not (ech < d < dmax * ech): continue
            a1, a2 = ang(EX[i]["t"], v), ang(EX[j]["t"], -v)
            if a1 < amax and a2 < amax: cands.append((d + ech * (a1 + a2) / 6, i, j))
    for s, i, j in sorted(cands):
        if i in pris or j in pris: continue
        pris |= {i, j}; paires.append((i, j))
print("interruptions appariees :", len(paires), "| extremites non appariees :", len(EX) - 2 * len(paires))
if len(EX) != 2 * len(paires):
    for i in range(len(EX)):
        if i not in pris: print("   NON APPARIEE :", EX[i]["coul"], "point (page)", int(EX[i]["pt"][1] / ech) + x0, int(EX[i]["pt"][0] / ech) + y0)
    sys.exit(1)
def dist_seg(P, a, b):
    ab = b - a; tt = np.clip(((P - a) @ ab) / (ab @ ab + 1e-9), 0, 1); proj = a + tt[:, None] * ab
    d = np.linalg.norm(P - proj, axis=1); k = int(d.argmin()); return float(d[k]), k, float(tt[k])
gaps = []; cross = []
for i, j in paires:
    a, b = EX[i]["pt"], EX[j]["pt"]; L = []
    for k, arc in enumerate(arcs):
        P = arc["P"]; dec = 0
        if k in (EX[i]["arc"], EX[j]["arc"]):
            # le trait qui s'interrompt ici peut repasser dessus un peu plus loin : on ne retire que ses bouts
            g0 = 12 * ech if (EX[i]["arc"] == k and EX[i]["b"] == 0) or (EX[j]["arc"] == k and EX[j]["b"] == 0) else 0
            g1 = 12 * ech if (EX[i]["arc"] == k and EX[i]["b"] == 1) or (EX[j]["arc"] == k and EX[j]["b"] == 1) else 0
            if len(P) < g0 + g1 + 20: continue
            P = P[g0:len(P) - g1]; dec = g0
        d, q, tt = dist_seg(P, a, b)
        if d < 5.0 * ech and 0.0 < tt < 1.0: L.append((tt, k, q + dec, d))
    L.sort(); ids = []
    for tt, k, q, d in L:
        ids.append(len(cross)); cross.append({"gap": len(gaps), "dessus": k, "idx": q, "m": a + tt * (b - a), "de": i, "vers": j})
    gaps.append({"i": i, "j": j, "x": ids})
print("croisements :", len(cross), "| interruptions sans croisement (pointilles) :", sum(not g["x"] for g in gaps), "| interruptions a plusieurs croisements :", sum(len(g["x"]) > 1 for g in gaps))
suite = {}
for k, g in enumerate(gaps):
    u, v = (EX[g["i"]]["arc"], EX[g["i"]]["b"]), (EX[g["j"]]["arc"], EX[g["j"]]["b"])
    suite[u] = (v, k, +1); suite[v] = (u, k, -1)
vu = set(); comps = []
for a0 in range(len(arcs)):
    if a0 in vu: continue
    seq = []; a, b = a0, 0
    while True:
        vu.add(a); (a2, b2), k, sgn = suite[(a, 1 - b)]; seq.append((a, b, k, sgn)); a, b = a2, b2
        if (a, b) == (a0, 0): break
    comps.append(seq)
coul_comp = [arcs[s[0][0]]["coul"] for s in comps]
print("composantes :", len(comps), coul_comp)
comp_de = {a: k for k, s in enumerate(comps) for a, *_ in s}; sens = {a: b for s in comps for a, b, *_ in s}
ev = []
for s in comps:
    L = []
    for a, b, kg, sgn in s:
        n = len(arcs[a]["P"]); d = sorted(((c["idx"] if b == 0 else n - 1 - c["idx"]), i) for i, c in enumerate(cross) if c["dessus"] == a)
        L += [("D", i) for _, i in d] + [("S", i) for i in (gaps[kg]["x"] if sgn > 0 else gaps[kg]["x"][::-1])]
    ev.append(L)
inn, out = {}, {}; lab = 0
for L in ev:
    for t, e in enumerate(L): inn[e] = lab + t; out[e] = lab + (t + 1) % len(L)
    lab += len(L)
def direction(a, idx):
    P = arcs[a]["P"]; i0, i1 = max(0, idx - 4), min(len(P) - 1, idx + 4); v = P[i1] - P[i0]
    if sens[a] == 1: v = -v
    return np.array([v[1], -v[0]])
sens_gap = {kg: sgn for s in comps for a, b, kg, sgn in s}
PD = []
for i, c in enumerate(cross):
    u = (EX[c["vers"]]["pt"] - EX[c["de"]]["pt"]) * sens_gap[c["gap"]]; u = np.array([u[1], -u[0]]); o = direction(c["dessus"], c["idx"])
    s = int(np.sign(o[0] * u[1] - o[1] * u[0])); assert s != 0
    ai, ci, oi, oo = inn[("S", i)], out[("S", i)], inn[("D", i)], out[("D", i)]
    PD.append([ai, oo, ci, oi] if s == 1 else [ai, oi, ci, oo])
json.dump({"pd": PD, "couleurs": coul_comp, "comp_croisements": [[comp_de[EX[c["de"]]["arc"]], comp_de[c["dessus"]]] for c in cross]}, open(nom + ".json", "w"))
BGR = {"noir": (0, 0, 0), "brun": (120, 170, 220), "vert": (0, 150, 0), "rouge": (0, 0, 220)}
ctl = np.full(bgr.shape, 255, np.uint8)
for i, a in enumerate(arcs): cv2.polylines(ctl, [a["P"][:, ::-1].astype(np.int32).reshape(-1, 1, 2)], False, BGR[coul_comp[comp_de[i]]], 3)
for c in cross: cv2.circle(ctl, (int(c["m"][1]), int(c["m"][0])), 5 * ech, BGR[coul_comp[comp_de[c["dessus"]]]], 2)     # couleur du cercle = rond qui passe dessus
cv2.imwrite(nom + "_controle.png", ctl)
