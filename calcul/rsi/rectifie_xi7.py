"""Figure XI-7 de RSI : parmi les inversions d'un seul croisement, lesquelles donnent un noeud borromeen de quatre ronds
(tout triplet libre, les quatre tenant ensemble) ? Puis : les quatre ronds de la figure rectifiee jouent-ils le meme role ?
Usage : ../../../python rectifie_xi7.py"""
import json, itertools, snappy, spherogram
D = json.load(open("xi7.json")); PD = [tuple(x) for x in D["pd"]]; CC = D["comp_croisements"]; coul = D["couleurs"]
def morceaux(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings)
def borromeen(pd):
    L = spherogram.Link(pd); n = len(L.link_components)
    if n != 4: return False, L
    lm = L.linking_matrix()
    if any(lm[i][j] for i in range(4) for j in range(4) if i != j): return False, L
    if any(morceaux(L.sublink([i for i in range(4) if i != X])) != 0 for X in range(4)): return False, L
    return morceaux(L) > 0, L
print("figure imprimee : borromeenne a quatre ?", borromeen(PD)[0])
bons = []
for c in range(len(PD)):
    Q = list(PD); a, b, cc, d = Q[c]; Q[c] = (b, cc, d, a)
    ok, L = borromeen(Q)
    if ok: bons.append(c); print("   inversion du croisement", c, "(dessous :", coul[CC[c][0]], "composante", CC[c][0], "; dessus :", coul[CC[c][1]], "composante", CC[c][1], ") -> noeud borromeen de quatre ronds")
json.dump({"croisements_rectifiables": bons}, open("xi7_rectif.json", "w"))
for c in bons:
    Q = list(PD); a, b, cc, d = Q[c]; Q[c] = (b, cc, d, a); L = spherogram.Link(Q); L2 = L.copy(); L2.simplify("global"); M = L.exterior()
    for e in range(10):
        if M.solution_type() == "all tetrahedra positively oriented": break
        M.randomize()
    print("rectifiee au croisement", c, ":", len(L2.crossings), "croisements apres simplification |", M.solution_type(), "| volume %.4f" % float(M.volume()))
    for pente in ((1, 1), (-1, 1), (1, 2), (1, 3)):
        vols = []
        for k in range(4):
            N = M.copy(); N.dehn_fill(pente, k)
            try: F = N.filled_triangulation(); vols.append(round(float(F.volume()), 4))
            except Exception: vols.append(None)
        print("      torsion", pente, "le long de chaque rond, volume restant :", vols)
