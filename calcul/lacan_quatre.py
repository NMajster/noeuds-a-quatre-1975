"""La regle de Lacan (9 decembre 1975) : entre deux trefles, l'un passe toujours sur l'autre. Peut-elle nouer quatre trefles ?
Une telle regle est un « tournoi » entre les quatre trefles (pour chaque couple, lequel est dessus) : 64 tournois.
- 24 sont des empilements (ordre total) : les quatre trefles se separent, sans calcul.
- pour les 40 autres, on calcule, dans deux dispositions :
  (P) quatre trefles recopies en parallele (tissage 4 x 4 a chaque etape) ;
  (E) quatre trefles emboites, disposition des dessins 0 et 1 de Soury (chaque brin croise chaque autre une fois par tour),
      pour les 16 ecritures du demi-tour de chaque bloc.
Dans chaque cas : chaque triplet se separe-t-il ? les quatre tiennent-ils ?

Usage : python lacan_quatre.py n      (n = 3 ou 4)
"""
import sys, itertools, json, collections, snappy, spherogram
import lacan_homologues as LH
n = int(sys.argv[1]); m = 2 * n
paires = [(i, j) for i in range(n) for j in range(i + 1, n)]
def transitif(T):
    sc = sorted(sum(1 for (i, j), v in T.items() if (i == a and v) or (j == a and not v)) for a in range(n))
    return sc == list(range(n))
def morceaux(L):
    L = L.copy(); L.simplify("global"); return sorted(len(p.crossings) for p in L.split_link_diagram()) if len(L.crossings) else []
def examine(w):
    L = spherogram.Link(braid_closure=w)
    if len(L.link_components) != n: return "pas %d ronds" % n
    tri = [morceaux(L.sublink([i for i in range(n) if i != X])) == [3] * (n - 1) for X in range(n)]
    tout = morceaux(L)
    if tout == [3] * n: return "tout se separe"
    if all(tri): return "BORROMEEN : chaque sous-ensemble se separe, le tout tient (%s)" % tout
    return "un sous-ensemble de %d ne se separe pas" % (n - 1)
def mots_reduits(k):
    res = []
    def rec(perm, mot):
        desc = [i for i in range(k - 1) if perm[i] < perm[i + 1]]
        if not desc: res.append(tuple(mot)); return
        for i in desc:
            p = list(perm); p[i], p[i + 1] = p[i + 1], p[i]; rec(p, mot + [i + 1])
    rec(list(range(k)), []); return res
def mot_emboite(g, T):
    """Disposition emboitee : ombre = demi-tour gauche g, demi-tour droit (miroir), tissage ; rond du brin de rang s : min(s, m-1-s).
    Dessus/dessous par le tournoi T ; un rond se croise lui-meme toujours dans le meme sens."""
    base = list(g) + [m - x for x in g] + LH.tissage(n); w = []; pos = list(range(m))
    for t in range(3):
        for x in base:
            a, b = pos[x - 1], pos[x]; ra, rb = min(a, m - 1 - a), min(b, m - 1 - b)
            if ra == rb: s = 1
            else: s = 1 if (T[(ra, rb)] if ra < rb else not T[(rb, ra)]) else -1          # +1 : le brin de gauche passe dessus
            w.append(x * s); pos[x - 1], pos[x] = b, a
    return w
res = collections.Counter(); bons = []
for vals in itertools.product((True, False), repeat=len(paires)):
    T = dict(zip(paires, vals))
    if transitif(T): res[("empilement", "tout se separe (sans calcul)")] += 1; continue
    r = examine(LH.mot(n, LH.regle(n, T))); res[("P parallele", r)] += 1
    if r.startswith("BORR"): bons.append(("P", vals))
    for g in mots_reduits(n):
        r = examine(mot_emboite(g, T)); res[("E emboite", r)] += 1
        if r.startswith("BORR"): bons.append(("E", g, vals))
for k, v in sorted(res.items()): print(v, k, flush=True)
print("solutions :", bons)
json.dump([list(map(str, b)) for b in bons], open(f"lacan_quatre_n{n}.json", "w"))
