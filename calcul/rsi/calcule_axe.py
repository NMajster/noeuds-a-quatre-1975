import io, json, snappy, spherogram
src = io.open("coloriages_inv.py", encoding="utf-8").read(); exec(src.split("\nfor ", 1)[0].split("\nTESTS", 1)[0].split("\nCLASSES", 1)[0])
def nc(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings)
for k in (1, 3):
    D = json.load(open(f"rsi/axe_{k}.json")); L = spherogram.Link([tuple(x) for x in D["pd"]]); m = len(L.link_components)
    print("dessin a", k, "tour(s) : ronds", D["couleurs"], "| croisements lus", len(L.crossings), "| chaque rond seul", [nc(L.sublink([i])) for i in range(m)], "| tout", nc(L),
          "| un rond retire", [nc(L.sublink([i for i in range(m) if i != X])) for X in range(m)],
          ("| coloriages S4 %d (144144 pour le noeud de Thome et Soury)" % compte([tuple(x) for x in L.PD_code()], table(classe_transpositions(4)))[0]) if k == 3 else "")
