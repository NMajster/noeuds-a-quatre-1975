"""Isomorphisme de deux diagrammes (codes PD) : meme dessin a deformation du plan pres, dessus/dessous respectes, sans miroir."""
from collections import deque
import periode as P
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
