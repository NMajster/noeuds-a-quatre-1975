import json, snappy, spherogram
def n_crois(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings)
for v in (0, 1):
    D = json.load(open(f"schema{v}.json")); L = spherogram.Link([tuple(x) for x in D["pd"]]); n = len(L.link_components); lm = L.linking_matrix()
    M = L.exterior(); S = []
    try: S = [[(snappy.Manifold(p).num_cusps(), round(float(snappy.Manifold(p).volume()), 3)) for p in M.split(s)] for s in M.splitting_surfaces()]
    except Exception as e: S = str(e)
    print("variante", v, ": composantes", n, D["couleurs"], "| croisements", len(L.crossings), "| enlacements nuls", not any(lm[i][j] for i in range(n) for j in range(n) if i != j),
          "| un rond retire :", [n_crois(L.sublink([i for i in range(n) if i != X])) for X in range(n)], "| tout :", n_crois(L), "| volume %.3f" % float(M.volume()), "| decoupe :", S)
