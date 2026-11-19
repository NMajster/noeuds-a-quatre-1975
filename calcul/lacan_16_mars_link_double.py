# Lacan, 16 mars 1976 : le « link » de Milnor (un rond et un huit, qui se defont si le huit se traverse),
# puis le meme avec chaque element double : « radicalement impossible de separer les quatre elements ».
# Controle : invariants de Milnor a indices distincts (developpement de Magnus), qui decident
# si un entrelacs se defait quand chaque rond peut se traverser lui-meme (Milnor 1954).
import itertools, snappy, spherogram
from collections import defaultdict
DEG = 3
def smul(a, b):
    r = defaultdict(int)
    for wa, ca in a.items():
        for wb, cb in b.items():
            if len(wa) + len(wb) <= DEG: r[wa + wb] += ca * cb
    return {w: c for w, c in r.items() if c}
def sinv(s):
    u = {w: -c for w, c in s.items() if w != ()}; r = {(): 1}; p = {(): 1}
    for k in range(DEG):
        p = smul(p, u)
        for w, c in p.items(): r[w] = r.get(w, 0) + c
    return {w: c for w, c in r.items() if c}
def milnor(L):
    comps = L.link_components; n = len(comps)
    # arcs : (composante, rang) ; un arc change a chaque passage dessous (entree 0 du croisement)
    arc_of = {}; passages = []
    for k, comp in enumerate(comps):
        debut = next(i for i, cep in enumerate(comp) if cep.strand_index == 0)
        comp = comp[debut:] + comp[:debut]      # on part d'un passage dessous
        a = -1; seq = []
        for cep in comp:
            if cep.strand_index == 0: a += 1; seq.append(cep.crossing)
            else: arc_of[cep.crossing] = (k, a)   # brin du dessus de ce croisement
        passages.append(seq)                      # croisements passes dessous, dans l'ordre ; l'arc a commence apres seq[a]
    E = {}
    for k in range(n):
        for a in range(len(passages[k])): E[(k, a)] = {(): 1, (k,): 1}
    for it in range(DEG + 4):
        N = {}
        for k in range(n):
            cur = {(): 1, (k,): 1}; N[(k, 0)] = cur
            for a in range(1, len(passages[k])):
                c = passages[k][a]; w = E[arc_of[c]] if c.sign == 1 else sinv(E[arc_of[c]])
                cur = smul(smul(w, cur), sinv(w)); N[(k, a)] = cur
        stable = N == E; E = N
    res = {}
    for k in range(n):
        lam = {(): 1}
        for a in list(range(1, len(passages[k]))) + [0]:
            c = passages[k][a]; w = E[arc_of[c]] if c.sign == 1 else sinv(E[arc_of[c]])
            lam = smul(w, lam)
        res[k] = {w: c for w, c in lam.items() if w and k not in w and len(set(w)) == len(w)}
    return res, stable
def rapport(nom, L):
    M = L.exterior()
    res, stable = milnor(L)
    print(f"\n== {nom} : {len(L.link_components)} ronds, {len(L.crossings)} croisements, enlacements {L.linking_matrix()}")
    try: print("   volume", round(float(M.volume()), 6), "| identification :", M.identify()[:3])
    except Exception as e: print("   (volume :", e, ")")
    print("   iterations stables :", stable)
    for k, d in res.items(): print("   longitude du rond", k, ": coefficients a indices distincts non nuls :", d if d else "aucun")
    return res
def tresse_doublee(mot, brins, torsions):
    # chaque brin i (1..brins) devient la paire (2i-1, 2i) ; sigma_i devient quatre croisements de meme signe
    out = []
    for g in mot:
        i, s = abs(g), (1 if g > 0 else -1)
        out += [s * 2 * i, s * (2 * i - 1), s * (2 * i + 1), s * 2 * i]
    for i, t in torsions.items():      # t tours complets entre les deux brins de la paire i, places au debut
        out = [(1 if t > 0 else -1) * (2 * i - 1)] * (2 * abs(t)) + out
    return out
# controles
rapport("controle : noeud borromeen", spherogram.Link(braid_closure=[1, -2, 1, -2, 1, -2]))
rapport("controle : deux ronds enlaces", spherogram.Link(braid_closure=[1, 1]))
W = [1, -2, 1, -2, -2]
LW = spherogram.Link(braid_closure=W)
rapport("le link a deux elements (candidat : chaine de Whitehead)", LW)
print("   composantes et brins :", [sorted({cep.crossing.label for cep in c}) for c in LW.link_components])
import json
for nom, tors in (("double, parallele du dessin (sans torsion ajoutee)", {}),):
    L = spherogram.Link(braid_closure=tresse_doublee(W, 3, tors)); rapport(nom, L)
# torsions a ajouter pour que les deux copies de chaque element ne soient pas enlacees : on les cherche
best = None
for t in itertools.product(range(-3, 4), repeat=3):
    L = spherogram.Link(braid_closure=tresse_doublee(W, 3, {1: t[0], 2: t[1], 3: t[2]}))
    if len(L.link_components) != 4: continue
    m = L.linking_matrix()
    if all(m[i][j] == 0 for i in range(4) for j in range(4) if i != j):
        if best is None or sum(map(abs, t)) < sum(map(abs, best)): best = t
print("\ntorsions qui annulent tous les enlacements :", best)
L0 = spherogram.Link(braid_closure=tresse_doublee(W, 3, dict(zip((1, 2, 3), best))))
r = rapport("double, les deux copies de chaque element non enlacees (dessin corrige de l'edition)", L0)
# Les coefficients de longueur 1 et 2 a indices distincts sont tous nuls dans les quatre longitudes :
# enlacements et invariants triples s'annulent, donc les invariants de longueur 4 sont bien definis.
# Ils ne sont pas nuls : l'entrelacs double ne se defait pas par auto-traversee.
