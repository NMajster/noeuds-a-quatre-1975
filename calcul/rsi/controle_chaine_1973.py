import json, snappy, spherogram
C = json.load(open(r"../figures/codes_pd_chaine_1973.json"))
BOR = spherogram.Link(braid_closure=[1, -2] * 3).exterior()
def nc(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings)
for cle, v in C.items():
    L = spherogram.Link([tuple(x) for x in v["pd"]]); m = len(L.link_components); lm = L.linking_matrix(); M = L.exterior()
    s = f"{cle} : ronds {m} | croisements {len(L.crossings)} | enlacements nuls {not any(lm[i][j] for i in range(m) for j in range(m) if i != j)} | chaque rond seul {[nc(L.sublink([i])) for i in range(m)]} | un rond retire {[nc(L.sublink([i for i in range(m) if i != X])) for X in range(m)]} | tout {nc(L)} | volume {float(M.volume()):.4f}"
    if m == 3:
        try: s += f" | meme noeud que le noeud borromeen : {M.is_isometric_to(BOR)}"
        except Exception as e: s += " | comparaison impossible"
    print(s)
