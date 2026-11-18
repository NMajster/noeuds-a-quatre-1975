"""Figure XI-7 : inversions de deux croisements donnant un noeud borromeen de quatre ronds."""
import json, itertools, io, contextlib, spherogram
with contextlib.redirect_stdout(io.StringIO()): import rectifie_xi7 as R
PD, CC, coul = R.PD, R.CC, R.coul
def flip(Q, c): a, b, cc, d = Q[c]; Q[c] = (b, cc, d, a)
print("croisements (dessous, dessus) :", [(i, CC[i][0], CC[i][1]) for i in range(len(PD))], "| composantes :", coul)
L = spherogram.Link(PD); print("enlacements imprimes :", L.linking_matrix())
for k in (2, 3):
    bons = []
    for cs in itertools.combinations(range(len(PD)), k):
        Q = list(PD)
        for c in cs: flip(Q, c)
        if R.borromeen(Q)[0]: bons.append(cs)
    print(k, "inversions :", len(bons), "solutions", bons[:20])
    if bons: break
