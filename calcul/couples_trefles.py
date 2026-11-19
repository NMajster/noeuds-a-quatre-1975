"""Les couples de couleurs du 16 decembre 1975 (rouge-brun, vert-noir) appartiennent-ils au noeud des quatre trefles ?
On liste toutes les isometries du complementaire trouvees par SnapPy, leur action sur les quatre trefles, et si elles
conservent ou renversent l'orientation de l'espace. On regarde quels partages en deux couples sont conserves.
Usage : venv-snappy/Scripts/python.exe couples_trefles.py"""
import json, snappy, spherogram, collections
D = json.load(open("../donnees/pd.json")); L = spherogram.Link([tuple(x) for x in D["pd_noir_corrige"]]); coul = D["couleurs"]; CC = D["comp_croisements"]
noms = []
for comp in L.link_components:
    cs = {ce.crossing.label for ce in comp}
    k = next(i for i, (a, b) in enumerate(CC) if a == b and i in cs); noms.append(coul[str(CC[k][0])])
print("composantes :", noms)
partages = {"noir-vert / rouge-brun": [{"noir", "vert"}, {"rouge", "brun"}], "noir-brun / vert-rouge": [{"noir", "brun"}, {"vert", "rouge"}], "noir-rouge / vert-brun": [{"noir", "rouge"}, {"vert", "brun"}]}
bilan = collections.Counter(); ordres = set(); pleins = set()
for essai in range(12):
    M = L.exterior()
    for e in range(essai): M.randomize()
    if M.solution_type() != "all tetrahedra positively oriented": continue
    G = M.symmetry_group(); ordres.add(G.order()); pleins.add(G.is_full_group())
    for iso in M.is_isometric_to(M, return_isometries=True):
        p = tuple(iso.cusp_images()); dets = [m.det() for m in iso.cusp_maps()]
        sens = "conserve" if all(d == 1 for d in dets) else ("renverse" if all(d == -1 for d in dets) else "mixte")
        bilan[(p, sens, iso.extends_to_link())] += 1
print("ordres trouves :", ordres, "| groupe declare complet par SnapPy :", pleins, "|", G)
vus = collections.defaultdict(set)
for (p, sens, ext), n in sorted(bilan.items()):
    vus[p].add(sens)
for p, s in sorted(vus.items()):
    img = {noms[i]: noms[j] for i, j in enumerate(p)}
    cons = [nom for nom, (A, B) in partages.items() if {frozenset(img[x] for x in A), frozenset(img[x] for x in B)} == {frozenset(A), frozenset(B)}]
    print("  ", " ".join(f"{a}->{b}" for a, b in img.items()), "| orientation de l'espace :", sorted(s), "| partages conserves :", cons)
print("nombre de permutations distinctes des trefles :", len(vus))
