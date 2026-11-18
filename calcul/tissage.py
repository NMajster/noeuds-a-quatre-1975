"""Regle tiree du dessin 1 de Soury (trois trefles) : le motif a l'ombre du demi-tour sur 2n brins (chaque brin croise
chaque autre une fois par periode), ecrit en trois morceaux : demi-tour du bloc de gauche, demi-tour du bloc de droite,
tissage carre n x n. Le dessus/dessous ne depend que du rang du croisement (signe e_i attache au generateur s_i).
On cherche, pour n donne, les ecritures du demi-tour et les signes qui donnent n trefles noues borromeennement.

Usage : python tissage.py n
"""
import sys, itertools, json, snappy, spherogram
n = int(sys.argv[1]); m = 2 * n

def mots_reduits(k):
    """Tous les mots reduits du demi-tour sur k brins (generateurs 1..k-1)."""
    res = []
    def rec(perm, mot):
        desc = [i for i in range(k - 1) if perm[i] < perm[i + 1]]
        if not desc: res.append(tuple(mot)); return
        for i in desc:
            p = list(perm); p[i], p[i + 1] = p[i + 1], p[i]; rec(p, mot + [i + 1])
    rec(list(range(k)), []); return res
def tissage(n):
    """Tissage carre n x n, en losange : rangees successives de generateurs."""
    w = []
    for r in range(2 * n - 1):
        larg = r + 1 if r < n else 2 * n - 1 - r
        w += [n - larg + 1 + 2 * j for j in range(larg)]
    return w
def anneaux_ok(w, eps):
    """Pre-filtre rapide : enlacements nuls (somme des signes des 4 croisements entre deux ronds)."""
    pos = list(range(m)); s = {}
    for g in w:
        a, b = pos[g - 1], pos[g]; ra, rb = min(a, m - 1 - a), min(b, m - 1 - b)
        if ra != rb: s[(min(ra, rb), max(ra, rb))] = s.get((min(ra, rb), max(ra, rb)), 0) + eps[g - 1]
        pos[g - 1], pos[g] = b, a
    return all(v == 0 for v in s.values())
def examine(w):
    L = spherogram.Link(braid_closure=w * 3); nc = len(L.link_components)
    if nc != n: return None
    for i in range(n):
        K = L.sublink([i]); K.simplify("global")
        if len(K.crossings) != 3: return None
    for X in range(n):
        T = L.sublink([i for i in range(n) if i != X]); T.simplify("global")
        P = T.split_link_diagram() if len(T.crossings) else []
        if sorted(len(p.crossings) for p in P) != [3] * (n - 1): return None
    L2 = L.copy(); L2.simplify("global")
    if len(L2.split_link_diagram()) != 1: return None
    M = L2.exterior()
    for e in range(6):
        if M.solution_type() == "all tetrahedra positively oriented": break
        M.randomize()
    return (M.solution_type(), round(float(M.volume()), 4), len(L2.crossings))
W = tissage(n); gauches = mots_reduits(n); vus = set(); bons = []
print("n =", n, "| ecritures du demi-tour d'un bloc :", len(gauches), "| tissage :", W, flush=True)
for g in gauches:
    d = tuple(m - x for x in g)
    base = list(g) + list(d) + W
    for eps in itertools.product((1, -1), repeat=m - 1):
        if eps[0] != 1: continue                      # a miroir pres
        if not anneaux_ok(base, eps): continue
        w = [x * eps[x - 1] for x in base]
        r = examine(w)
        if r: bons.append({"gauche": g, "eps": eps, "mot": w, "res": r}); print("  ", g, eps, r, flush=True)
print("solutions :", len(bons), "| volumes distincts :", sorted({b["res"][1] for b in bons}))
json.dump(bons, open(f"tissage_n{n}.json", "w"))
