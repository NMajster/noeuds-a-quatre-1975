"""Le noeud borromeen ordinaire est-il un motif repete trois fois autour d'un axe ? Que donne le motif apres un seul tour ?
Motif : la tresse a trois brins s1 s2^-1.  Usage : python borromeen_axe.py"""
import snappy, spherogram
import periode as P
for k in (1, 2, 3):
    L = spherogram.Link(braid_closure=[1, -2] * k); K = L.copy(); K.simplify("global"); m = len(L.link_components)
    s = f"motif repete {k} fois : ronds {m} | croisements apres simplification {len(K.crossings)}"
    if len(K.crossings):
        M = L.exterior(); s += f" | volume {float(M.volume()):.4f} | {[str(x) for x in M.identify()][:2]}"
    print(s)
B = spherogram.Link(braid_closure=[1, -2] * 3); pd = [tuple(x) for x in B.PD_code()]
A = P.automorphismes(pd); print("symetries du dessin a 6 croisements :", len(A), "| ordres :", sorted(P.ordre(f) for f in A))
L1 = spherogram.Link(braid_closure=[1, -2, 3, 2, 1, 1, 2, 3])            # un tour du motif, avec l'axe comme quatrieme brin
print("un tour avec l'axe : ronds", len(L1.link_components), "| enlacement du rond avec l'axe :", abs(L1.linking_matrix()[0][1]))
