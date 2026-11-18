"""La construction de Lacan du 9 decembre 1975 : des trefles « homologues », c'est-a-dire le meme trefle recopie en parallele,
chacun passant dessus ou dessous les autres. Le trefle est la tresse a deux brins croises trois fois ; n trefles homologues
font une tresse a 2n brins ou, a chaque etape (trois etapes), le bloc de gauche croise le bloc de droite (tissage n x n).
Un croisement d'un trefle avec lui-meme garde le sens du trefle. Aux autres croisements, le sens est libre : signes[t][(i, j)]
= +1 si, a l'etape t, le brin de gauche (trefle i) passe sur le brin de droite (trefle j).

Usage : python lacan_homologues.py
"""
import itertools, json, sys, snappy, spherogram
def tissage(n):
    w = []
    for r in range(2 * n - 1):
        larg = r + 1 if r < n else 2 * n - 1 - r
        w += [n - larg + 1 + 2 * j for j in range(larg)]
    return w
def mot(n, signes):
    """signes : liste de 3 dictionnaires {(i, j): +1 ou -1}, i != j."""
    W = tissage(n); w = []
    for t in range(3):
        pos = list(range(n)) + list(range(n))                # trefle de chaque brin, de gauche a droite
        for g in W:
            i, j = pos[g - 1], pos[g]
            w.append(g * (1 if i == j else signes[t][(i, j)]))
            pos[g - 1], pos[g] = j, i
    return w
def regle(n, dessus):
    """Regle constante : dessus[(i, j)] = True si le trefle i passe toujours sur le trefle j."""
    s = {(i, j): (1 if dessus[(min(i, j), max(i, j))] == (i < j) else -1) for i in range(n) for j in range(n) if i != j}
    return [s, s, s]
def hyper(L):
    M = L.exterior()
    for e in range(8):
        if M.solution_type() == "all tetrahedra positively oriented": break
        M.randomize()
    return M.solution_type(), float(M.volume()), M
def decrit(w, n):
    L = spherogram.Link(braid_closure=w); nc = len(L.link_components)
    lm = L.linking_matrix(); nul = all(lm[i][j] == 0 for i in range(nc) for j in range(nc) if i != j)
    ronds = []
    for i in range(nc):
        K = L.sublink([i]); K.simplify("global"); ronds.append(len(K.crossings))
    sep = []
    for X in range(nc):
        T = L.sublink([i for i in range(nc) if i != X]); T.simplify("global")
        sep.append(sorted(len(p.crossings) for p in T.split_link_diagram()) if len(T.crossings) else [])
    L2 = L.copy(); L2.simplify("global"); parts = L2.split_link_diagram() if len(L2.crossings) else []
    st, vol, M = hyper(L2)
    return {"composantes": nc, "enlacements_nuls": nul, "ronds": ronds, "un_retire": sep, "croisements": (len(w), len(L2.crossings)), "morceaux": len(parts), "solution": st, "volume": round(vol, 4)}, M
if __name__ == "__main__":
    print("--- trois trefles homologues, regle de Lacan : 1 sur 2, 2 sur 3, 3 sur 1")
    for nom, d in (("cyclique", {(0, 1): True, (1, 2): True, (0, 2): False}), ("cyclique inverse", {(0, 1): False, (1, 2): False, (0, 2): True}), ("empile (1 sur 2 sur 3)", {(0, 1): True, (1, 2): True, (0, 2): True})):
        r, M = decrit(mot(3, regle(3, d)), 3); print(nom, ":", r, flush=True)
        if nom == "cyclique":
            for ref in ("dessin0", "dessin2"):
                D = json.load(open(f"soury3/{ref}.json")); w = [(i + 1) * (1 if dd == "G" else -1) for i, dd in D["mot"]] * 3
                R = spherogram.Link(braid_closure=w).exterior()
                try: print("   meme entrelacs que le", ref, "de Soury :", M.is_isometric_to(R), flush=True)
                except Exception as e: print("   comparaison avec", ref, "impossible")
