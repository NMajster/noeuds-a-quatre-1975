import json, snappy, spherogram
def nc(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings), len(K.split_link_diagram()) if len(K.crossings) else 0
for k in (5, 7):
    D = json.load(open(f"rsi/axe_{k}.json")); L = spherogram.Link([tuple(x) for x in D["pd"]]); m = len(L.link_components); lm = L.linking_matrix()
    print("dessin a", k, "tours : ronds", m, "| croisements lus", len(L.crossings), "| enlacements nuls", not any(lm[i][j] for i in range(m) for j in range(m) if i != j),
          "| chaque rond seul (croisements, morceaux)", [nc(L.sublink([i])) for i in range(m)], "| un rond retire", [nc(L.sublink([i for i in range(m) if i != X])) for X in range(m)], "| tout", nc(L), flush=True)
