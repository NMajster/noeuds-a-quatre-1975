"""Controle du mot que le contre-lecteur dit avoir lu sur le dessin 3 de Soury (11 niveaux, 28 croisements par periode) :
repete trois fois, donne-t-il le noeud de la figure rectifiee ?
Usage : python controle_astra2.py"""
import io, json, snappy, spherogram
src = io.open("coloriages_inv.py", encoding="utf-8").read(); exec(src.split("\nfor ", 1)[0].split("\nTESTS", 1)[0].split("\nCLASSES", 1)[0])
niveaux = "1G 3G 5G 7G / 2D 6G / 2D 6G / 1D 3D 5D 7D / 4G / 3G 5G / 2D 4D 6D / 1G 3G 5D 7D / 2G 4G 6G / 3D 5D / 4D"
mot = [int(x[:-1]) * (1 if x[-1] == "G" else -1) for x in niveaux.replace("/", " ").split()]
print("croisements par periode :", len(mot))
REF = spherogram.Link([tuple(x) for x in json.load(open("pd.json"))["pd_noir_corrige"]]); IMP = spherogram.Link([tuple(x) for x in json.load(open("pd.json"))["pd"]])
Tb = table(classe_transpositions(4))
for nom, w in (("mot lu, G = +", mot), ("mot lu, G = -", [-x for x in mot])):
    L = spherogram.Link(braid_closure=w * 3); ronds = []
    for i in range(len(L.link_components)):
        K = L.sublink([i]); K.simplify("global"); ronds.append(len(K.crossings))
    M = L.exterior()
    for e in range(8):
        if M.solution_type() == "all tetrahedra positively oriented": break
        M.randomize()
    rep = "?"
    for e in range(6):
        try: rep = M.is_isometric_to(REF.exterior()); break
        except Exception: M.randomize()
    print(nom, ": composantes", len(L.link_components), "| ronds seuls", ronds, "| coloriages S4", compte([tuple(x) for x in L.PD_code()], Tb)[0], "(rectifiee 144144, imprimee 45552) | volume %.4f" % float(M.volume()), "| meme complementaire que la figure rectifiee :", rep)
