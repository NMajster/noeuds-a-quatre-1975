"""Les figures I-8 et I-9 du Sinthome (noeud a quatre ronds, 18 novembre 1975) : sont-elles borromeennes a quatre ?
se decoupent-elles par un tore ? quels ronds vont ensemble ?  Comparaison avec la chaine temoin et avec la figure XI-7 de RSI.
Pour savoir quels ronds vont ensemble : on tord l'espace le long de deux ronds a la fois ; le volume restant n'est pas le meme
selon que les deux ronds sont dans le meme morceau ou dans deux morceaux differents.
Usage : ../../../python calcule_figures.py"""
import json, itertools, snappy, spherogram
def inv(w): return [-x for x in reversed(w)]
def comm(a, b): return a + b + inv(a) + inv(b)
def A(i, j):
    up = list(range(j - 1, i, -1)); return up + [i, i] + inv(up)
def n_crois(K):
    K = K.copy(); K.simplify("global"); return len(K.crossings)
def vol(F):
    best = None
    for e in range(8):
        v = float(F.volume())
        if F.solution_type() == "all tetrahedra positively oriented": return round(v, 3)
        best = v if best is None else best; F.randomize()
    return "~%.2f" % best
def etude(nom, L, noms):
    n = len(L.link_components); lm = L.linking_matrix()
    print("=====", nom, "| composantes", n, "| croisements", len(L.crossings), flush=True)
    print("   enlacements non nuls :", [(noms[i], noms[j], lm[i][j]) for i in range(n) for j in range(i + 1, n) if lm[i][j]])
    print("   chaque rond seul (croisements apres simplification) :", [n_crois(L.sublink([i])) for i in range(n)])
    tri = {noms[X]: n_crois(L.sublink([i for i in range(n) if i != X])) for X in range(n)}
    print("   un rond retire, croisements restants :", tri, "| ensemble :", n_crois(L))
    borro = all(v == 0 for v in tri.values()) and n_crois(L) > 0 and not any(lm[i][j] for i in range(n) for j in range(n) if i != j)
    print("   noeud borromeen de quatre ronds :", borro)
    M = L.exterior(); print("   volume", vol(M.copy()))
    try:
        S = M.splitting_surfaces(); print("   tores de decoupe :", len(S), [[(snappy.Manifold(p).num_cusps(), vol(snappy.Manifold(p))) for p in M.split(s)] for s in S])
    except Exception as e: print("   decoupe non calculable :", e)
    if borro:
        for a, b in itertools.combinations(range(n), 2):
            N = M.copy(); N.dehn_fill((1, 1), a); N.dehn_fill((1, 1), b)
            print("      torsion le long de", noms[a], "et", noms[b], ": volume restant", vol(N.filled_triangulation()), flush=True)
    return borro
def charge(f):
    D = json.load(open(f)); L = spherogram.Link([tuple(x) for x in D["pd"]])
    # nom de chaque composante de spherogram : on retrouve sa couleur par un croisement ou elle passe dessous
    return L, D
T = spherogram.Link(braid_closure=comm(comm(A(1, 2), A(2, 3)), A(3, 4))); etude("chaine temoin de quatre ronds", T, ["rond 1", "rond 2", "rond 3", "rond 4"])
for f, titre in (("I8.json", "figure I-8 du Sinthome"), ("I9.json", "figure I-9 du Sinthome"), ("XI7c.json", "figure XI-7 de RSI")):
    L, D = charge(f)
    # correspondance composantes de spherogram -> couleurs : par les aretes
    pd = D["pd"]; CC = D["comp_croisements"]; noms = []
    for comp in L.link_components:
        labs = {ce.crossing.label for ce in comp}; cnt = {}
        for ce in comp:
            c = ce.crossing.label
            if isinstance(c, int) and c < len(CC):
                k = CC[c][0] if ce.strand_index in (0, 2) else CC[c][1]; cnt[k] = cnt.get(k, 0) + 1
        k = max(cnt, key=cnt.get) if cnt else 0; noms.append(D["couleurs"][k] + ("" if D["couleurs"].count(D["couleurs"][k]) == 1 else str(k)))
    etude(titre, L, noms)
