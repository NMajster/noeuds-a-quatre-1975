import json, itertools, snappy, spherogram
def nc(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings)
for n in "ab":
    D = json.load(open(f"rsi/imp_{n}.json")); L = spherogram.Link([tuple(x) for x in D["pd"]]); m = len(L.link_components)
    print("panneau", n, ": ronds", D["couleurs"], "| croisements", len(L.crossings), "| tout, apres simplification :", nc(L),
          "| en retirant un rond :", [nc(L.sublink([i for i in range(m) if i != X])) for X in range(m)])
