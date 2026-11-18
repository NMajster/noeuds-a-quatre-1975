import io, json, snappy, spherogram
src = io.open("coloriages_inv.py", encoding="utf-8").read(); exec(src.split("\nfor ", 1)[0].split("\nTESTS", 1)[0].split("\nCLASSES", 1)[0])
D = json.load(open("rsi/trefles3b.json")); L = spherogram.Link([tuple(x) for x in D["pd"]]); n = len(L.link_components)
def nc(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings), len(K.split_link_diagram()) if len(K.crossings) else 0
import collections
C = collections.Counter((D["couleurs"][a], D["couleurs"][b]) for a, b in D["comp_croisements"])
print("composantes", n, D["couleurs"], "| croisements", len(L.crossings), "| ronds seuls", [nc(L.sublink([i])) for i in range(n)], "| couples", [nc(L.sublink([i for i in range(n) if i != X])) for X in range(n)])
print("dessous -> dessus :", dict(C))
print("coloriages S4 :", compte([tuple(x) for x in L.PD_code()], table(classe_transpositions(4)))[0], "(408 pour le dessin 2 de Soury selon la contre-lecture ; 27000 si separes)")
