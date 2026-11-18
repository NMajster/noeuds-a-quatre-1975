"""Les quatre trefles de la figure rectifiee jouent-ils le meme role dans le noeud ? Symetries du complementaire et leur action sur les ronds.
Usage : python symetries.py"""
import json, snappy, spherogram
D = json.load(open("pd.json")); L = spherogram.Link([tuple(x) for x in D["pd_noir_corrige"]]); coul = D["couleurs"]
CC = D["comp_croisements"]
# couleur de chaque composante de spherogram : par un croisement propre
noms = []
for comp in L.link_components:
    cs = {ce.crossing.label for ce in comp}
    k = next(i for i, (a, b) in enumerate(CC) if a == b and i in cs) if all(isinstance(c, int) for c in cs) else None
    noms.append(coul[str(CC[k][0])] if k is not None else "?")
print("composantes :", noms)
M = L.exterior()
for e in range(8):
    if M.solution_type() == "all tetrahedra positively oriented": break
    M.randomize()
print(M.solution_type(), M.volume())
G = M.symmetry_group(); print("groupe de symetrie :", G, "| ordre", G.order(), "| amphicheiral :", G.is_amphicheiral() if hasattr(G, "is_amphicheiral") else "?")
perms = set()
for iso in M.is_isometric_to(M, return_isometries=True):
    perms.add((tuple(iso.cusp_images()), iso.extends_to_link()))
for p in sorted(perms): print("   permutation des ronds :", [noms[i] + "->" + noms[j] for i, j in enumerate(p[0])], "| respecte les meridiens :", p[1])
