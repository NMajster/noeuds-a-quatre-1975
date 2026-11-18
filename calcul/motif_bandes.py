"""Motifs par bandes. Une tresse a 2n brins produit de n bandes (chaque bande = un croisement entre deux brins,
conjugue par un mot w) se referme toujours en n ronds libres. On conjugue une seule bande, celle d'un rond central,
par un commutateur itere de tours complets autour d'UN brin de chacun des autres ronds : si l'on retire un rond,
le commutateur disparait et les ronds restants sont independants autour de l'axe.

Usage : python motif_bandes.py
"""
import json, snappy, spherogram
def inv(w): return [-x for x in reversed(w)]
def comm(a, b): return a + b + inv(a) + inv(b)
def A(i, j):                       # le brin j fait un tour complet autour du brin i (i < j)
    up = list(range(j - 1, i, -1)); return up + [i, i] + inv(up)
C3 = comm(A(2, 3), A(3, 5))                       # le brin 3 tourne autour du brin 2, puis autour du brin 5
C4 = comm(C3, A(3, 7))                            # ... puis autour du brin 7
MOTIFS = {
  "F n=3 (s1 s3 s5 . C3)": (6, [1, 3, 5] + C3),
  "G n=3 (bande conjuguee)": (6, [1, 5] + C3 + [3] + inv(C3)),
  "F n=4 (s1 s3 s5 s7 . C4)": (8, [1, 3, 5, 7] + C4),
  "G n=4 (bande conjuguee)": (8, [1, 5, 7] + C4 + [3] + inv(C4)),
}
def hyper(L):
    M = L.exterior()
    for e in range(8):
        if M.solution_type() == "all tetrahedra positively oriented": break
        M.randomize()
    return M.solution_type(), float(M.volume())
def rapport(nom, m, w, k):
    L = spherogram.Link(braid_closure=w * k); nc = len(L.link_components); n = m // 2
    lm = L.linking_matrix(); nul = all(lm[i][j] == 0 for i in range(nc) for j in range(nc) if i != j)
    ronds = []
    for i in range(nc):
        K = L.sublink([i]); K.simplify("global"); ronds.append(len(K.crossings))
    sep = []
    for X in range(nc):
        T = L.sublink([i for i in range(nc) if i != X]); T.simplify("global")
        sep.append(sorted(len(p.crossings) for p in T.split_link_diagram()) if len(T.crossings) else [0] * (nc - 1))
    L2 = L.copy(); L2.simplify("global"); parts = L2.split_link_diagram() if len(L2.crossings) else []
    st, vol = hyper(L2) if len(L2.crossings) else ("-", 0.0)
    print(f"{nom} tours={k} : {len(w)} crois. par tour ; composantes {nc} ; enlacements nuls {nul} ; ronds seuls {ronds} ; un rond retire -> {sep} ; tout : {len(L2.crossings)} crois., morceaux {len(parts)}, {st}, volume {vol:.5f}", flush=True)
if __name__ == "__main__":
    for nom, (m, w) in MOTIFS.items():
        for k in (1, 3):
            rapport(nom, m, w, k)
        axe = list(range(m, 0, -1)) + list(range(1, m + 1))
        Q = spherogram.Link(braid_closure=w + axe); print("   motif + axe :", hyper(Q), flush=True)
