"""Les ronds d'un entrelacs jouent-ils le meme role ?  Epreuve : on tord l'espace le long du disque que borde un rond
(chirurgie de pente 1/q sur ce rond, qui est non noue et non enlace aux autres) et on mesure le volume de ce qui reste.
Deux ronds echanges par une symetrie donnent les memes volumes (au signe de q pres si la symetrie renverse l'orientation).
Des volumes differents prouvent (numeriquement) que les deux ronds ne jouent pas le meme role.

Usage : python roles_des_ronds.py
"""
import json, snappy, spherogram
def inv(w): return [-x for x in reversed(w)]
def comm(a, b): return a + b + inv(a) + inv(b)
def A(i, j):
    up = list(range(j - 1, i, -1)); return up + [i, i] + inv(up)
def profil(L, pentes=((1, 1), (-1, 1), (1, 2), (-1, 2), (1, 3), (-1, 3))):
    M = L.exterior(); n = M.num_cusps(); P = []
    for c in range(n):
        v = []
        for p in pentes:
            best = None
            for essai in range(6):
                N = M.copy(); N.dehn_fill(p, c); F = N.filled_triangulation()
                for e in range(essai): F.randomize()
                if F.solution_type() == "all tetrahedra positively oriented": best = round(float(F.volume()), 3); break
                best = best if best is not None else ("~%.2f" % float(F.volume()))
            v.append(best)
        P.append(v)
    return P
CAS = {"anneaux borromeens": spherogram.Link(braid_closure=[1, -2] * 3),
       "chaine de quatre ronds [[A12, A23], A34]": spherogram.Link(braid_closure=comm(comm(A(1, 2), A(2, 3)), A(3, 4))),
       "chaine de quatre ronds [(s1 s2^-1)^3, s3^2]": spherogram.Link(braid_closure=comm([1, -2] * 3, [3, 3])),
       "chaine de cinq ronds [[[A12, A23], A34], A45]": spherogram.Link(braid_closure=comm(comm(comm(A(1, 2), A(2, 3)), A(3, 4)), A(4, 5)))}
for nom, L in CAS.items():
    print(nom, "| composantes", len(L.link_components), flush=True)
    for c, v in enumerate(profil(L)): print("   rond", c, ": volumes apres torsion (pentes 1, -1, 1/2, -1/2, 1/3, -1/3) :", v, flush=True)
