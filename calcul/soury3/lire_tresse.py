"""Lecture d'un dessin de tresse en noir et blanc (dessins 0, 1, 2 du texte 66 de Soury, pages numerisees en haute definition).
1. arcs = composantes connexes de l'encre (un brin est interrompu la ou il passe dessous) ; squelette ; deux extremites.
2. appariement des extremites de part et d'autre de chaque passage dessous (alignement), et arc qui passe dessus.
3. brins suivis de haut en bas ; chaque passage dessous donne un croisement ; mot de tresse.
Sortie : <nom>.json (mot de tresse, controles) et <nom>_controle.png (ce que le programme a lu, a comparer a l'image).

On ne lit qu'une periode, prise au milieu du dessin, entre deux lignes horizontales ya et ya + T qui coupent
exactement le bon nombre de brins.

Usage : python lire_tresse.py <nom> <image> x0 y0 x1 y1 nb_brins [ya]
"""
import sys, json, math, cv2, numpy as np
nom, img = sys.argv[1], sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7]); ech = 2; NB = int(sys.argv[7]); YA = int(sys.argv[8]) if len(sys.argv) > 8 else None
g = cv2.imread(img, cv2.IMREAD_GRAYSCALE)[y0:y1, x0:x1]
g = cv2.resize(g, None, fx=ech, fy=ech, interpolation=cv2.INTER_CUBIC)
ink = (g < 128).astype(np.uint8); H, W = ink.shape

def zhang_suen(img):
    img = img.copy().astype(np.uint8); changed = True
    while changed:
        changed = False
        for step in (0, 1):
            p = np.pad(img, 1)
            P2, P3, P4, P5 = p[:-2, 1:-1], p[:-2, 2:], p[1:-1, 2:], p[2:, 2:]
            P6, P7, P8, P9 = p[2:, 1:-1], p[2:, :-2], p[1:-1, :-2], p[:-2, :-2]
            nb = [P2, P3, P4, P5, P6, P7, P8, P9]; B = sum(nb)
            A = sum(((nb[i] == 0) & (nb[(i + 1) % 8] == 1)).astype(int) for i in range(8))
            c = (P2 * P4 * P6 == 0) & (P4 * P6 * P8 == 0) if step == 0 else (P2 * P4 * P8 == 0) & (P2 * P6 * P8 == 0)
            m = (img == 1) & (B >= 2) & (B <= 6) & (A == 1) & c
            if m.any(): img[m] = 0; changed = True
    return img

n, cc, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
arcs = []; anomalies = []
for k in range(1, n):
    if stats[k, cv2.CC_STAT_AREA] < 12 * ech * ech: continue
    xx, yy, ww, hh = [int(v) for v in stats[k, :4]]
    comp = (cc[yy:yy + hh, xx:xx + ww] == k)
    sk = zhang_suen(np.pad(comp, 1))[1:-1, 1:-1]
    ys, xs = np.nonzero(sk); pts = set(zip(ys.tolist(), xs.tolist()))
    def nbr(q): return [(q[0] + a, q[1] + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a or b) and (q[0] + a, q[1] + b) in pts]
    ends = [q for q in pts if len(nbr(q)) == 1]
    if len(ends) < 2: anomalies.append((xx, yy, "sans extremites")); continue
    def bfs(s):
        prev = {s: None}; order = [s]
        for q in order:
            for r in nbr(q):
                if r not in prev: prev[r] = q; order.append(r)
        return prev, order[-1]
    prev, far = bfs(ends[0]); prev, far2 = bfs(far)
    path = []; q = far2
    while q is not None: path.append(q); q = prev[q]
    P = np.array([(y + yy, x + xx) for y, x in path], float)
    if P[0][0] > P[-1][0]: P = P[::-1]
    arcs.append({"P": P, "n_ext": len(ends)})
print("arcs :", len(arcs), "| a plus de deux extremites :", sum(a["n_ext"] > 2 for a in arcs), "| anomalies :", anomalies)

def tangente(P, bout):
    k = min(10 * ech, len(P) - 1)
    v = (P[0] - P[k]) if bout == 0 else (P[-1] - P[-1 - k])
    return v / (np.linalg.norm(v) + 1e-9)
EX = [{"arc": i, "bout": b, "pt": (a["P"][0] if b == 0 else a["P"][-1]), "t": tangente(a["P"], b)} for i, a in enumerate(arcs) for b in (0, 1)]
ytop = min(e["pt"][0] for e in EX); ybot = max(e["pt"][0] for e in EX); marge = 14 * ech
for e in EX: e["bord"] = "haut" if e["pt"][0] < ytop + marge else ("bas" if e["pt"][0] > ybot - marge else None)
inner = [i for i, e in enumerate(EX) if e["bord"] is None]
def ang(u, v): return math.degrees(math.acos(max(-1, min(1, float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9))))))
cands = []
for i in inner:
    for j in inner:
        if j <= i or EX[i]["arc"] == EX[j]["arc"]: continue
        v = EX[j]["pt"] - EX[i]["pt"]; dist = np.linalg.norm(v)
        if not (3 * ech < dist < 48 * ech): continue
        a1, a2 = ang(EX[i]["t"], v), ang(EX[j]["t"], -v)
        if a1 < 45 and a2 < 45: cands.append((dist + 1.5 * ech * (a1 + a2) / 10, i, j))
cands.sort(); pris = set(); paires = []
for s, i, j in cands:
    if i in pris or j in pris: continue
    pris |= {i, j}; paires.append((i, j))
# seconde passe : simples interruptions du trait (extremites tres proches, sans condition d'alignement)
reste = [i for i in inner if i not in pris]; c2 = sorted((float(np.linalg.norm(EX[i]["pt"] - EX[j]["pt"])), i, j) for i in reste for j in reste if j > i and EX[i]["arc"] != EX[j]["arc"])
for dd, i, j in c2:
    if dd < 12 * ech and i not in pris and j not in pris: pris |= {i, j}; paires.append((i, j))
seuls = [i for i in inner if i not in pris]
def page(pt): return (round(float(pt[1] / ech)) + x0, round(float(pt[0] / ech)) + y0)
print("passages dessous apparies :", len(paires), "| extremites non appariees :", [page(EX[i]["pt"]) for i in seuls],
      "| bords haut/bas :", sum(e["bord"] == "haut" for e in EX), sum(e["bord"] == "bas" for e in EX))
suite = {}
for i, j in paires:
    suite[(EX[i]["arc"], EX[i]["bout"])] = (EX[j]["arc"], EX[j]["bout"]); suite[(EX[j]["arc"], EX[j]["bout"])] = (EX[i]["arc"], EX[i]["bout"])
# periode : autocorrelation des lignes d'encre
prof = ink.sum(1).astype(float); prof -= prof.mean(); best = None
for T in range(int(H / 3 * 0.93), int(H / 3 * 1.07)):
    c = float((prof[:-T] * prof[T:]).sum() / (np.linalg.norm(prof[:-T]) * np.linalg.norm(prof[T:]) + 1e-9))
    if best is None or c > best[0]: best = (c, T)
T = best[1]; print("periode :", T / ech, "pixels de la page (correlation %.2f)" % best[0])
def coupe(y):
    """arcs coupes par la ligne horizontale y : liste (x, arc), ou None si la ligne passe dans un passage dessous."""
    L = []
    for i, a in enumerate(arcs):
        P = a["P"]; k = np.nonzero((P[:-1, 0] - y) * (P[1:, 0] - y) <= 0)[0]
        if len(k) > 1 and np.ptp(k) > 3: return None
        if len(k): L.append((float(P[k[0], 1]), i))
    for i, j in paires:
        if (EX[i]["pt"][0] - y) * (EX[j]["pt"][0] - y) <= 0: return None
    return sorted(L)
ya = None
for y in ([YA * ech - y0 * ech] if YA else range(H // 2 - T // 2 - T // 4, H // 2 - T // 2 + T // 4)):
    A_, B_ = coupe(y), coupe(y + T)
    if A_ and B_ and len(A_) == NB and len(B_) == NB and max(abs(a[0] - b[0]) for a, b in zip(A_, B_)) < 8 * ech: ya = y; break
assert ya is not None, "pas de ligne de coupe trouvee"
yb = ya + T; print("lignes de coupe (y page) :", ya / ech + y0, yb / ech + y0)
dep = coupe(ya); arr = coupe(yb)
brins = []; passages = []; arcs_de = {}
for s, (x, a) in enumerate(dep):
    P = arcs[a]["P"]; k = int(np.nonzero((P[:-1, 0] - ya) * (P[1:, 0] - ya) <= 0)[0][0]); poly = [P[k:]]; b = 1; vu = 0
    while True:
        arcs_de.setdefault(a, s)
        nx = suite.get((a, b))
        if poly[-1][-1][0] > yb + 20 * ech or nx is None or vu > 60: break
        Q = arcs[nx[0]]["P"]; Q = Q if nx[1] == 0 else Q[::-1]
        passages.append({"brin": s, "a": poly[-1][-1], "b": Q[0], "arcs": (a, nx[0])})
        a = nx[0]; b = 1 - nx[1]; poly.append(Q); vu += 1
    brins.append(np.vstack(poly))
fin = [sorted(range(NB), key=lambda r: abs(arr[r][0] - brins[s][int(np.abs(brins[s][:, 0] - yb).argmin()), 1]))[0] for s in range(NB)]
print("brins :", len(brins), "| permutation sur une periode (rang de depart -> rang d'arrivee) :", fin, "| tous arrives :", all(B[-1][0] >= yb for B in brins))
def x_en(s, y):
    B = brins[s]; k = int(np.abs(B[:, 0] - y).argmin()); return B[k, 1]
def dist_seg(P, a, b):
    ab = b - a; tt = np.clip(((P - a) @ ab) / (ab @ ab + 1e-9), 0, 1); proj = a + tt[:, None] * ab
    d = np.linalg.norm(P - proj, axis=1); k = int(d.argmin()); return float(d[k]), proj[k]
X = []; pb = []
for p in passages:
    for i, arc in enumerate(arcs):
        if i in p["arcs"]: continue
        d, pt = dist_seg(arc["P"], p["a"], p["b"])
        if d < 2.5 * ech and ya <= pt[0] < yb: X.append({"m": pt, "dessous": p["brin"], "arc_dessus": i})
X.sort(key=lambda c: c["m"][0]); mot = []
ordre = list(range(NB))                                     # ordre des brins de gauche a droite, mis a jour a chaque croisement
for c in X:
    cands = [s for s in range(NB) if s != c["dessous"] and abs(x_en(s, c["m"][0]) - c["m"][1]) < 6 * ech]
    ru = ordre.index(c["dessous"]); ro = None
    for s in cands:
        if abs(ordre.index(s) - ru) == 1: ro = ordre.index(s)
    if ro is None: pb.append(page(c["m"]) + (ru, [ordre.index(s) for s in cands])); continue
    i = min(ru, ro); mot.append((i, "G" if ro < ru else "D")); ordre[i], ordre[i + 1] = ordre[i + 1], ordre[i]; c["ok"] = True
print("croisements dans la periode :", len(mot), "| douteux :", pb, "| ordre final :", ordre, "(attendu : brin s au rang fin[s])", [ordre.index(s) for s in range(NB)] == fin)
print("mot :", " ".join(f"{i+1}{d}" for i, d in mot))
json.dump({"mot": mot, "brins": NB, "douteux": pb, "permutation": fin, "coherent": [ordre.index(s) for s in range(NB)] == fin}, open(nom + ".json", "w"))
ctl = cv2.cvtColor((255 - ink * 90).astype(np.uint8), cv2.COLOR_GRAY2BGR)
PAL = [(200, 0, 0), (0, 140, 0), (0, 0, 200), (0, 160, 200), (180, 0, 180), (120, 80, 0), (0, 0, 0), (90, 90, 90)]
for s, B in enumerate(brins): cv2.polylines(ctl, [B[:, ::-1].astype(np.int32).reshape(-1, 1, 2)], False, PAL[s % len(PAL)], 2)
for c, (i, d) in zip([c for c in X if c.get("ok")], mot):
    cv2.circle(ctl, (int(c["m"][1]), int(c["m"][0])), 5 * ech, (0, 0, 255) if d == "G" else (255, 0, 0), 2)
for y in (ya, yb): cv2.line(ctl, (0, int(y)), (W, int(y)), (0, 200, 0), 1)
for i in seuls: cv2.drawMarker(ctl, (int(EX[i]["pt"][1]), int(EX[i]["pt"][0])), (0, 200, 255), cv2.MARKER_CROSS, 12, 2)
cv2.imwrite(nom + "_controle.png", ctl[max(0, int(ya) - 60):int(yb) + 60])
