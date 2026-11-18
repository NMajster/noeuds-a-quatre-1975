"""Les tresses lues sur les dessins 0, 1 et 2 de Soury (trois trefles) : ce qu'elles donnent, repetees k fois.
Usage : ../../../python calcule.py"""
import json, snappy, spherogram
def hyper(L):
    M = L.exterior()
    for e in range(8):
        if M.solution_type() == "all tetrahedra positively oriented": break
        M.randomize()
    return M.solution_type(), float(M.volume()), M
def mot(nom):
    D = json.load(open(nom + ".json")); return [(i + 1) * (1 if d == "G" else -1) for i, d in D["mot"]]
def rapport(nom, w, k):
    L = spherogram.Link(braid_closure=w * k); nc = len(L.link_components)
    lm = L.linking_matrix(); nul = all(lm[i][j] == 0 for i in range(nc) for j in range(nc) if i != j)
    ronds = []
    for i in range(nc):
        K = L.sublink([i]); K.simplify("global"); ronds.append(len(K.crossings))
    sep = []
    for X in range(nc):
        T = L.sublink([i for i in range(nc) if i != X]); T.simplify("global")
        sep.append(sorted(len(p.crossings) for p in T.split_link_diagram()) if len(T.crossings) else [0] * (nc - 1))
    L2 = L.copy(); L2.simplify("global"); parts = L2.split_link_diagram() if len(L2.crossings) else []
    st, vol, M = hyper(L2) if len(L2.crossings) else ("-", 0.0, None)
    print(f"{nom} x{k} : {len(w) * k} crois. ; composantes {nc} ; enlacements nuls {nul} ; ronds seuls {ronds} ; un rond retire -> {sep} ; tout : {len(L2.crossings)} crois., morceaux {len(parts)}, {st}, volume {vol:.5f}", flush=True)
    return M
M = {}
for nom in ("dessin0", "dessin1", "dessin2"):
    w = mot(nom); print(nom, "mot :", w)
    for k in (1, 3, 5): M[(nom, k)] = rapport(nom, w, k)
    axe = list(range(6, 0, -1)) + list(range(1, 7))
    print("   motif + axe :", hyper(spherogram.Link(braid_closure=w + axe))[:2], flush=True)
for a, b in ((("dessin0", 3), ("dessin1", 3)), (("dessin0", 3), ("dessin2", 3)), (("dessin1", 3), ("dessin2", 3))):
    try: print(a, "meme entrelacs que", b, ":", M[a].is_isometric_to(M[b]))
    except Exception as e: print(a, b, "comparaison impossible :", e)
