"""Dans une chaine borromeenne de quatre ronds ordinaires, les quatre ronds jouent-ils le meme role ?
Deux chaines temoins (tresses pures brunniennes refermees) et, pour comparaison, les anneaux borromeens.
Usage : python symetries_chaines.py"""
import snappy, spherogram
def inv(w): return [-x for x in reversed(w)]
def comm(a, b): return a + b + inv(a) + inv(b)
def A(i, j):
    up = list(range(j - 1, i, -1)); return up + [i, i] + inv(up)
CH = {"anneaux borromeens (s1 s2^-1)^3": [1, -2] * 3,
      "quatre ronds : [[A12, A23], A34]": comm(comm(A(1, 2), A(2, 3)), A(3, 4)),
      "quatre ronds : [(s1 s2^-1)^3, s3^2]": comm([1, -2] * 3, [3, 3])}
for nom, w in CH.items():
    L = spherogram.Link(braid_closure=w); L.simplify("global"); M = L.exterior()
    for e in range(10):
        if M.solution_type() == "all tetrahedra positively oriented": break
        M.randomize()
    print(nom, "| composantes", len(L.link_components), "| croisements", len(L.crossings), "|", M.solution_type(), "volume %.4f" % float(M.volume()))
    try:
        G = M.symmetry_group(); perms = sorted({tuple(i.cusp_images()) for i in M.is_isometric_to(M, return_isometries=True)})
        orb = {frozenset(p[i] for p in perms) for i in range(M.num_cusps())}
        print("   symetries :", G, "| classes de ronds equivalents :", sorted(sorted(o) for o in orb))
    except Exception as e: print("   symetries non calculables :", e)
