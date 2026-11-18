"""Quels ronds vont ensemble dans les figures I-8 et I-9 ?  Torsion de pente 1/2 le long de deux ronds a la fois :
deux ronds de morceaux differents donnent 6,138 + 6,138 = 12,276 ; deux ronds du meme morceau donnent autre chose."""
import io, contextlib, itertools, json, snappy, spherogram
with contextlib.redirect_stdout(io.StringIO()): import calcule_figures as C
def noms_de(L, D):
    CC = D["comp_croisements"]; noms = []
    for comp in L.link_components:
        cnt = {}
        for ce in comp:
            c = ce.crossing.label
            if isinstance(c, int) and c < len(CC):
                k = CC[c][0] if ce.strand_index in (0, 2) else CC[c][1]; cnt[k] = cnt.get(k, 0) + 1
        noms.append(D["couleurs"][max(cnt, key=cnt.get)])
    return noms
cas = [("chaine temoin", C.T, ["rond 1", "rond 2", "rond 3", "rond 4"])]
for f, t in (("I8.json", "figure I-8 (noir = I, bleu = R, vert = sinthome, rouge = S)"), ("I9.json", "figure I-9")):
    L, D = C.charge(f); cas.append((t, L, noms_de(L, D)))
for titre, L, noms in cas:
    M = L.exterior(); print(titre)
    for a, b in itertools.combinations(range(4), 2):
        v = []
        for p in ((1, 2), (1, 3)):
            N = M.copy(); N.dehn_fill(p, a); N.dehn_fill(p, b); v.append(C.vol(N.filled_triangulation()))
        print("   ", noms[a], "et", noms[b], ": volumes restants", v, flush=True)
