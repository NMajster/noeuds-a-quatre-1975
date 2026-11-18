"""La figure XI-7 de RSI (trois cercles et un quatrieme rond) : est-ce un noeud borromeen de quatre ronds ? ses quatre ronds jouent-ils le meme role ?
Usage : ../../../python calcule_xi7.py"""
import json, itertools, snappy, spherogram
D = json.load(open("xi7.json")); L = spherogram.Link([tuple(x) for x in D["pd"]]); n = len(L.link_components)
# nom de chaque composante de spherogram : par ses croisements
CC = D["comp_croisements"]; noms0 = ["noir (le quatrieme)", "cercle du haut", "cercle de gauche", "cercle du bas"]
def morceaux(K):
    K = K.copy(); K.simplify("global"); return (len(K.crossings), len(K.split_link_diagram()) if len(K.crossings) else 0)
print("composantes :", n, "| croisements :", len(L.crossings), "| enlacements :", L.linking_matrix())
for i in range(n): print("   rond", i, "seul :", morceaux(L.sublink([i])), "(croisements, morceaux apres simplification)")
for X in range(n): print("   sans le rond", X, ":", morceaux(L.sublink([i for i in range(n) if i != X])))
for a, b in itertools.combinations(range(n), 2): print("   couple", a, b, ":", morceaux(L.sublink([a, b])))
print("ensemble :", morceaux(L))
M = L.exterior()
for e in range(10):
    if M.solution_type() == "all tetrahedra positively oriented": break
    M.randomize()
print("structure :", M.solution_type(), "| volume", M.volume())
try:
    G = M.symmetry_group(); perms = sorted({tuple(i.cusp_images()) for i in M.is_isometric_to(M, return_isometries=True)})
    print("symetries :", G, "| permutations des ronds :", perms)
    print("classes de ronds equivalents :", sorted({tuple(sorted({p[i] for p in perms})) for i in range(n)}))
except Exception as e: print("symetries non calculables :", e)
# epreuve independante : on tord l'espace le long du disque borde par un rond (chirurgie de pente 1 puis -1) ; le volume de ce qui reste distingue les ronds
for pente in ((1, 1), (-1, 1), (1, 2)):
    vols = []
    for c in range(n):
        N = M.copy(); N.dehn_fill(pente, c)
        try: F = N.filled_triangulation(); vols.append((round(float(F.volume()), 4), F.solution_type()[:12]))
        except Exception as e: vols.append("?")
    print("remplissage", pente, "de chaque rond :", vols)
