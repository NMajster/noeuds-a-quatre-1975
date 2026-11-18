"""Lecture d'une figure de noeud en couleurs (figures I-8 et I-9 du Sinthome, lecon du 18 novembre 1975 ; aussi XI-7 de RSI).
Les traits en pointilles (passages caches) sont suivis comme des traits pleins : une interruption sans brin qui la croise est une continuite.
1. masques par couleur ; arcs = composantes connexes (un trait est interrompu la ou il passe dessous) ; squelette ; extremites.
2. appariement des extremites de meme couleur de part et d'autre de chaque passage dessous ; arc qui passe dessus.
3. composantes, signes des croisements, code PD.
Sortie : xi7.json (code PD, couleur de chaque composante) et xi7_controle.png.

Usage : python figure_couleurs.py <nom> <image> x0 y0 x1 y1
"""
import sys, json, math, cv2, numpy as np
from collections import defaultdict
nom = sys.argv[1]; img = sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7]); ech = 3
bgr = cv2.imread(img)[y0:y1, x0:x1]; bgr = cv2.resize(bgr, None, fx=ech, fy=ech, interpolation=cv2.INTER_CUBIC).astype(int)
B, G, R = bgr[:, :, 0], bgr[:, :, 1], bgr[:, :, 2]
REFS = {"noir": (30, 25, 30), "bleu": (60, 135, 200), "vert": (60, 180, 75), "rouge": (235, 30, 40), "magenta": (236, 0, 140)}
rgb = np.stack([R, G, B], 2); dist = np.stack([np.sqrt(((rgb - np.array(c)) ** 2).sum(2)) for c in REFS.values()], 0)
proche = dist.argmin(0); encre = (np.sqrt(((rgb - 255) ** 2).sum(2)) > 110) & (dist.min(0) < 110)
masques = {c: (encre & (proche == k)) for k, c in enumerate(REFS)}
masques = {c: m for c, m in masques.items() if m.sum() > 400 * ech * ech}

def zhang_suen(img):
    img = img.copy().astype(np.uint8); changed = True
    while changed:
        changed = False
        for step in (0, 1):
            p = np.pad(img, 1)
            P2, P3, P4, P5 = p[:-2, 1:-1], p[:-2, 2:], p[1:-1, 2:], p[2:, 2:]
            P6, P7, P8, P9 = p[2:, 1:-1], p[2:, :-2], p[1:-1, :-2], p[:-2, :-2]
            nb = [P2, P3, P4, P5, P6, P7, P8, P9]; Bn = sum(nb)
            A = sum(((nb[i] == 0) & (nb[(i + 1) % 8] == 1)).astype(int) for i in range(8))
            c = (P2 * P4 * P6 == 0) & (P4 * P6 * P8 == 0) if step == 0 else (P2 * P4 * P8 == 0) & (P2 * P6 * P8 == 0)
            m = (img == 1) & (Bn >= 2) & (Bn <= 6) & (A == 1) & c
            if m.any(): img[m] = 0; changed = True
    return img
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
        if len(ends) < 2: print("   composante sans extremite ignoree :", coul, xx // ech + x0, yy // ech + y0, int(stats[k, cv2.CC_STAT_AREA])); continue
        def bfs(s):
            prev = {s: None}; order = [s]
            for q in order:
                for r in nbr(q):
                    if r not in prev: prev[r] = q; order.append(r)
            return prev, order[-1]
        prev, far = bfs(ends[0]); prev, far2 = bfs(far); path = []; q = far2
        while q is not None: path.append(q); q = prev[q]
        arcs.append({"coul": coul, "P": np.array([(y + yy, x + xx) for y, x in path], float), "n_ext": len(ends)})
print("arcs :", len(arcs), {c: sum(a["coul"] == c for a in arcs) for c in masques}, "| a plus de deux extremites :", sum(a["n_ext"] > 2 for a in arcs))
def tang(P, b):
    k = min(8 * ech, len(P) - 1); v = (P[0] - P[k]) if b == 0 else (P[-1] - P[-1 - k]); return v / (np.linalg.norm(v) + 1e-9)
EX = [{"arc": i, "b": b, "pt": (a["P"][0] if b == 0 else a["P"][-1]), "t": tang(a["P"], b), "coul": a["coul"]} for i, a in enumerate(arcs) for b in (0, 1)]
def ang(u, v): return math.degrees(math.acos(max(-1, min(1, float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9))))))
cands = []
for i in range(len(EX)):
    for j in range(i + 1, len(EX)):
        if EX[i]["coul"] != EX[j]["coul"] or (EX[i]["arc"] == EX[j]["arc"] and len(arcs[EX[i]["arc"]]["P"]) < 60 * ech): continue
        v = EX[j]["pt"] - EX[i]["pt"]; d = np.linalg.norm(v)
        if not (1 * ech < d < 30 * ech): continue
        a1, a2 = ang(EX[i]["t"], v), ang(EX[j]["t"], -v)
        if a1 < 45 and a2 < 45: cands.append((d + ech * (a1 + a2) / 6, i, j))
cands.sort(); pris = set(); paires = []
for s, i, j in cands:
    if i in pris or j in pris: continue
    pris |= {i, j}; paires.append((i, j))
reste = [i for i in range(len(EX)) if i not in pris]          # seconde passe, plus tolerante (traits courbes)
c2 = sorted((float(np.linalg.norm(EX[i]["pt"] - EX[j]["pt"])), i, j) for i in reste for j in reste if j > i and EX[i]["coul"] == EX[j]["coul"] and (EX[i]["arc"] != EX[j]["arc"] or len(arcs[EX[i]["arc"]]["P"]) > 60 * ech))
for d, i, j in c2:
    if d < 45 * ech and i not in pris and j not in pris and ang(EX[i]["t"], EX[j]["pt"] - EX[i]["pt"]) < 80 and ang(EX[j]["t"], EX[i]["pt"] - EX[j]["pt"]) < 80: pris |= {i, j}; paires.append((i, j))
print("passages dessous :", len(paires), "| extremites non appariees :", len(EX) - 2 * len(paires))
if len(EX) != 2 * len(paires):
    for i in range(len(EX)):
        if i not in pris: print("   NON APPARIEE :", EX[i]["coul"], "arc", EX[i]["arc"], "point (page)", int(EX[i]["pt"][1] / ech) + x0, int(EX[i]["pt"][0] / ech) + y0, "longueur de l'arc", len(arcs[EX[i]["arc"]]["P"]))
    dbg = np.full(bgr.shape, 255, np.uint8)
    for a in arcs: cv2.polylines(dbg, [a["P"][:, ::-1].astype(np.int32).reshape(-1, 1, 2)], False, (0, 0, 0), 2)
    for i in range(len(EX)):
        if i not in pris: cv2.circle(dbg, (int(EX[i]["pt"][1]), int(EX[i]["pt"][0])), 14, (0, 0, 255), 3)
    cv2.imwrite(nom + "_debug.png", dbg); sys.exit(1)
cross = []
for i, j in paires:
    m = (EX[i]["pt"] + EX[j]["pt"]) / 2; best = None
    for k, a in enumerate(arcs):
        if k in (EX[i]["arc"], EX[j]["arc"]) and EX[i]["arc"] != EX[j]["arc"]: continue
        dd = np.linalg.norm(a["P"] - m, axis=1); q = int(dd.argmin())
        if k == EX[i]["arc"] and min(q, len(a["P"]) - 1 - q) < 12 * ech: continue      # un arc qui se referme sur lui-meme : ignorer ses bouts
        if best is None or dd[q] < best[0]: best = (float(dd[q]), k, q)
    cross.append({"u": (EX[i]["arc"], EX[i]["b"]), "v": (EX[j]["arc"], EX[j]["b"]), "dessus": best[1], "idx": best[2], "dist": best[0], "m": m})
for c in cross: c["reel"] = c["dist"] < 3.5 * ech
print("interruptions :", len(cross), "| vrais croisements :", sum(c["reel"] for c in cross), "| continuites (pointilles) :", sum(not c["reel"] for c in cross), "| distances douteuses :", sorted(round(c["dist"] / ech, 1) for c in cross if 2 * ech < c["dist"] < 8 * ech))
suite = {}
for k, c in enumerate(cross): suite[c["u"]] = (c["v"], k); suite[c["v"]] = (c["u"], k)
# composantes : suite d'arcs orientes
vu = set(); comps = []
for a0 in range(len(arcs)):
    if a0 in vu: continue
    seq = []; a, b = a0, 0
    while True:
        vu.add(a); seq.append((a, b))                         # on entre dans l'arc a par son bout b
        (a2, b2), k = suite[(a, 1 - b)]; seq[-1] = (a, b, k)
        a, b = a2, b2
        if (a, b) == (a0, 0): break
    comps.append(seq)
print("composantes :", len(comps), [arcs[s[0][0]]["coul"] for s in comps])
comp_de = {a: k for k, s in enumerate(comps) for a, b, _ in s}; sens = {a: b for s in comps for a, b, _ in s}
# evenements le long de chaque composante
ev = []
for k, s in enumerate(comps):
    L = []
    for a, b, kc in s:
        n = len(arcs[a]["P"]); d = sorted(((c["idx"] if b == 0 else n - 1 - c["idx"]), i) for i, c in enumerate(cross) if c["dessus"] == a and c["reel"])
        L += [("D", i) for _, i in d] + ([("S", kc)] if cross[kc]["reel"] else [])
    ev.append(L)
inn, out = {}, {}; lab = 0
for L in ev:
    for t, e in enumerate(L): inn[e] = lab + t; out[e] = lab + (t + 1) % len(L)
    lab += len(L)
def direction(a, idx):
    P = arcs[a]["P"]; i0, i1 = max(0, idx - 4), min(len(P) - 1, idx + 4); v = P[i1] - P[i0]
    if sens[a] == 1: v = -v
    return np.array([v[1], -v[0]])                           # (x, y vers le haut)
PD = []
for i, c in enumerate(cross):
    if not c["reel"]: continue
    (a, ba), (b_, bb) = c["u"], c["v"]
    sort_a = (sens[a] == 0 and ba == 1) or (sens[a] == 1 and ba == 0)       # on quitte l'arc a par le bout ba ?
    pa, pb = arcs[a]["P"][0 if ba == 0 else -1], arcs[b_]["P"][0 if bb == 0 else -1]
    u = (pb - pa) if sort_a else (pa - pb); u = np.array([u[1], -u[0]]); o = direction(c["dessus"], c["idx"])
    s = int(np.sign(o[0] * u[1] - o[1] * u[0])); assert s != 0
    ai, ci, oi, oo = inn[("S", i)], out[("S", i)], inn[("D", i)], out[("D", i)]
    PD.append([ai, oo, ci, oi] if s == 1 else [ai, oi, ci, oo])
json.dump({"pd": PD, "couleurs": [arcs[s[0][0]]["coul"] for s in comps], "comp_croisements": [[comp_de[c["u"][0]], comp_de[c["dessus"]]] for c in cross if c["reel"]]}, open(nom + ".json", "w"))
print("croisements :", len(PD))
ctl = np.full(bgr.shape, 255, np.uint8); BGR = {"noir": (0, 0, 0), "bleu": (200, 120, 0), "vert": (0, 150, 0), "rouge": (0, 0, 220), "magenta": (200, 0, 200)}; PAL = [BGR[arcs[s[0][0]]["coul"]] for s in comps] + [(0, 0, 0)] * 5
for i, a in enumerate(arcs): cv2.polylines(ctl, [a["P"][:, ::-1].astype(np.int32).reshape(-1, 1, 2)], False, PAL[comp_de[i] % 5], 3)
for i, c in enumerate(cross):
    if not c["reel"]: continue
    cv2.circle(ctl, (int(c["m"][1]), int(c["m"][0])), 5 * ech, PAL[comp_de[c["dessus"]] % 5], 2)       # couleur du cercle = rond qui passe dessus
cv2.imwrite(nom + "_controle.png", ctl)
