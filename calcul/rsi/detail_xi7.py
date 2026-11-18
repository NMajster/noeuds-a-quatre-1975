import json, io, contextlib, spherogram, snappy
with contextlib.redirect_stdout(io.StringIO()): import rectifie_xi7 as R
PD = R.PD
def etat(Q):
    L = spherogram.Link(Q); lm = L.linking_matrix(); s = []
    for X in range(4):
        K = L.sublink([i for i in range(4) if i != X]); K.simplify("global"); s.append(len(K.crossings))
    K = L.copy(); K.simplify("global"); M = K.exterior() if len(K.crossings) else None
    return [lm[0][1], lm[0][2], lm[0][3]], s, len(K.crossings), (round(float(M.volume()), 3) if M else 0)
print("imprimee :", etat(PD))
for c in range(14):
    Q = list(PD); a, b, cc, d = Q[c]; Q[c] = (b, cc, d, a); print("inversion", c, R.CC[c], ": enlacements du noir", *etat(Q))
