"""Étape 2 : appariement des extrémités d'arcs à travers les passages dessous,
identification de l'arc dessus, extrémités de bord (haut / bas).
Sortie : croisements.json"""
import json, math, numpy as np
arcs = [a for a in json.load(open("arcs.json")) if "chemin" in a]
for i, a in enumerate(arcs):
    a["id"] = i
    p = np.array(a["chemin"], float)
    a["P"] = p
def tangent(a, end):
    p = a["P"]
    k = min(8, len(p) - 1)
    if end == 0:
        return p[0], (p[0] - p[k]) / (np.linalg.norm(p[0] - p[k]) + 1e-9)
    return p[-1], (p[-1] - p[-1 - k]) / (np.linalg.norm(p[-1] - p[-1 - k]) + 1e-9)
E = []
for a in arcs:
    for end in (0, 1):
        pt, t = tangent(a, end)
        E.append({"arc": a["id"], "end": end, "pt": pt, "t": t, "col": a["couleur"]})
ys = [e["pt"][0] for e in E]
ytop, ybot = min(ys), max(ys)
for e in E:
    e["bord"] = "haut" if e["pt"][0] < ytop + 25 else ("bas" if e["pt"][0] > ybot - 25 else None)
inner = [i for i, e in enumerate(E) if e["bord"] is None]
def ang(u, v):
    return math.degrees(math.acos(max(-1, min(1, float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9))))))
cands = []
for i in inner:
    for j in inner:
        if j <= i or E[i]["col"] != E[j]["col"] or E[i]["arc"] == E[j]["arc"]:
            continue
        v = E[j]["pt"] - E[i]["pt"]; dist = np.linalg.norm(v)
        if not (8 < dist < 130):
            continue
        a1 = ang(E[i]["t"], v); a2 = ang(E[j]["t"], -v)
        if a1 < 40 and a2 < 40:
            cands.append((dist + 2 * (a1 + a2), i, j))
cands.sort()
used = set(); pairs = []
for s, i, j in cands:
    if i in used or j in used:
        continue
    used |= {i, j}; pairs.append((i, j, s))
unmatched = [i for i in inner if i not in used]
# arc dessus : arc (autre que les deux) dont le chemin passe au plus près du milieu
cross = []
for i, j, s in pairs:
    m = (E[i]["pt"] + E[j]["pt"]) / 2
    best = None
    for a in arcs:
        if a["id"] in (E[i]["arc"], E[j]["arc"]):
            continue
        dd = np.linalg.norm(a["P"] - m, axis=1); k = int(dd.argmin())
        if best is None or dd[k] < best[0]:
            best = (float(dd[k]), a["id"], k)
    cross.append({"sous_a": E[i]["arc"], "sous_a_end": E[i]["end"], "sous_b": E[j]["arc"], "sous_b_end": E[j]["end"],
                  "dessus": best[1], "dessus_idx": best[2], "dist_dessus": best[0], "milieu": m.tolist(), "score": s})
bords = [{"arc": e["arc"], "end": e["end"], "bord": e["bord"], "x": float(e["pt"][1]), "col": e["col"]} for e in E if e["bord"]]
json.dump({"croisements": cross, "bords": bords, "non_apparies": [{"arc": E[i]["arc"], "end": E[i]["end"], "col": E[i]["col"], "pt": E[i]["pt"].tolist()} for i in unmatched]},
          open("croisements.json", "w"), indent=0)
print("croisements :", len(cross), "; extrémités de bord :", len(bords), "; non appariées :", len(unmatched))
print("distance arc-dessus max :", max(c["dist_dessus"] for c in cross))
print("bords :", sorted((b["bord"], round(b["x"]), b["col"]) for b in bords))
for u in unmatched: print("NON APPARIÉE", E[u]["col"], E[u]["pt"].round().tolist())
