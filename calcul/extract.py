"""Extraction du diagramme de la figure III-2 (édition numérisée du *Sinthome*, p. 57).
Étape 1 : masques par couleur, arcs (composantes connexes), squelettes, extrémités.
Sortie : arcs.json (pour chaque arc : couleur, chemin ordonné du squelette, extrémités)."""
import cv2, numpy as np, json, sys
from scipy import ndimage as ndi

P = r"PAGES-DES-EDITIONS/S23/S23-page-044.png"
im = cv2.imread(P).astype(int)
Y0, Y1, X0, X1 = 300, 1880, 230, 1420          # cadre de la figure (sans légende ni folio)
roi = im[Y0:Y1, X0:X1]
REF = {"noir": (0, 0, 0), "vert": (64, 160, 96), "rouge": (32, 0, 224), "brun": (64, 128, 192)}
H, W = roi.shape[:2]
d = np.stack([np.sqrt(((roi - np.array(c)) ** 2).sum(2)) for c in REF.values()], 0)
lab = d.argmin(0)
dmin = d.min(0)
ink = dmin < 90
names = list(REF)

def zhang_suen(img):
    img = img.copy().astype(np.uint8)
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            p = np.pad(img, 1)
            P2, P3, P4, P5 = p[:-2, 1:-1], p[:-2, 2:], p[1:-1, 2:], p[2:, 2:]
            P6, P7, P8, P9 = p[2:, 1:-1], p[2:, :-2], p[1:-1, :-2], p[:-2, :-2]
            nb = [P2, P3, P4, P5, P6, P7, P8, P9]
            B = sum(nb)
            A = sum(((nb[i] == 0) & (nb[(i + 1) % 8] == 1)).astype(int) for i in range(8))
            if step == 0:
                c = (P2 * P4 * P6 == 0) & (P4 * P6 * P8 == 0)
            else:
                c = (P2 * P4 * P8 == 0) & (P2 * P6 * P8 == 0)
            m = (img == 1) & (B >= 2) & (B <= 6) & (A == 1) & c
            if m.any():
                img[m] = 0
                changed = True
    return img

arcs = []
for ci, name in enumerate(names):
    mask = (ink & (lab == ci)).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, cc = cv2.connectedComponents(mask, connectivity=8)
    for k in range(1, n):
        comp = (cc == k)
        if comp.sum() < 150:          # bruit
            continue
        sk = zhang_suen(comp)
        ys, xs = np.nonzero(sk)
        pts = set(zip(ys.tolist(), xs.tolist()))
        nbr = lambda q: [(q[0] + a, q[1] + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a or b) and (q[0] + a, q[1] + b) in pts]
        ends = [q for q in pts if len(nbr(q)) == 1]
        if len(ends) < 2:
            arcs.append({"couleur": name, "anomalie": "pas_deux_extremites", "n_ext": len(ends), "taille": int(comp.sum())})
            continue
        # chemin le plus long : BFS depuis une extrémité, puis depuis la plus lointaine
        def bfs(s):
            prev = {s: None}; order = [s]
            for q in order:
                for r in nbr(q):
                    if r not in prev:
                        prev[r] = q; order.append(r)
            return prev, order[-1]
        prev, far = bfs(ends[0])
        prev, far2 = bfs(far)
        path = []; q = far2
        while q is not None:
            path.append(q); q = prev[q]
        path = [(int(y + Y0), int(x + X0)) for y, x in path]  # coordonnées page
        arcs.append({"couleur": name, "chemin": path[::3] + [path[-1]], "n_ext": len(ends), "taille": int(comp.sum())})

json.dump(arcs, open("arcs.json", "w"), indent=0)
from collections import Counter
print("arcs par couleur :", Counter(a["couleur"] for a in arcs if "chemin" in a))
print("anomalies :", [a for a in arcs if "anomalie" in a])
print("arcs à plus de 2 extrémités :", sum(1 for a in arcs if a.get("n_ext", 2) > 2))
