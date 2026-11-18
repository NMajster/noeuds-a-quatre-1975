"""Nombre de coloriages d'un diagramme par un quandle involutif (version rapide).

Meme invariant que coloriages_s4.py : a chaque croisement, arc_sortant = o * arc_entrant * o, ou o est la
couleur du brin de dessus, prise dans une classe d'involutions d'un groupe fini. La regle ne depend ni de
l'orientation ni du signe. Le nombre de coloriages est un invariant d'entrelacs, multiplicatif pour les
unions scindees.

Methode : on choisit des arcs generateurs (ceux dont les couleurs determinent toutes les autres par
propagation), on enumere leurs couleurs en profondeur, et a chaque etape on execute les deductions et
les verifications devenues possibles.

Usage : python coloriages_inv.py
"""
import json, itertools, sys, time
import spherogram

def perm_mul(p, q):
    return tuple(p[i] for i in q)

def classe_transpositions(n):
    out = []
    for i, j in itertools.combinations(range(n), 2):
        p = list(range(n)); p[i], p[j] = p[j], p[i]; out.append(tuple(p))
    return out

def classe_doubles_transpositions(n):
    out = set()
    for a, b, c, d in itertools.permutations(range(n), 4):
        p = list(range(n)); p[a], p[b] = p[b], p[a]; p[c], p[d] = p[d], p[c]; out.add(tuple(p))
    return sorted(out)

def table(classe):
    idx = {p: i for i, p in enumerate(classe)}
    return [[idx[perm_mul(perm_mul(o, x), o)] for x in classe] for o in classe]

def croisements_arcs(pd):
    aretes = sorted({e for x in pd for e in x})
    parent = {e: e for e in aretes}
    def find(e):
        while parent[e] != e:
            parent[e] = parent[parent[e]]; e = parent[e]
        return e
    for a, b, c, d in pd:
        parent[find(b)] = find(d)
    arcs = sorted({find(e) for e in aretes}); idx = {r: i for i, r in enumerate(arcs)}
    return len(arcs), [(idx[find(b)], idx[find(a)], idx[find(c)]) for a, b, c, d in pd]

def plan(n, X):
    """Etapes : (generateur, [deductions (cible, dessus, source)], [verifications (dessus, u, v)])."""
    connu = set(); verifie = set(); etapes = []
    def cloture(connu, verifie):
        ded, ver = [], []
        change = True
        while change:
            change = False
            for k, (o, u, v) in enumerate(X):
                if k in verifie or o not in connu: continue
                if u in connu and v in connu:
                    ver.append((o, u, v)); verifie.add(k); change = True
                elif u in connu:
                    ded.append((v, o, u)); connu.add(v); verifie.add(k); change = True
                elif v in connu:
                    ded.append((u, o, v)); connu.add(u); verifie.add(k); change = True
        return ded, ver
    while len(connu) < n:
        meilleur, gain = None, -1
        for a in range(n):
            if a in connu: continue
            c2 = set(connu) | {a}; v2 = set(verifie); cloture(c2, v2)
            if len(c2) > gain: meilleur, gain = a, len(c2)
        connu.add(meilleur)
        ded, ver = cloture(connu, verifie)
        etapes.append((meilleur, ded, ver))
    assert len(verifie) == len(X)
    return etapes

def compte(pd, T):
    n, X = croisements_arcs(pd)
    etapes = plan(n, X); q = len(T); col = [0] * n
    def rec(i):
        if i == len(etapes): return 1
        g, ded, ver = etapes[i]; tot = 0
        for c in range(q):
            col[g] = c
            for t, o, s in ded: col[t] = T[col[o]][col[s]]
            ok = True
            for o, u, v in ver:
                if T[col[o]][col[u]] != col[v]: ok = False; break
            if ok: tot += rec(i + 1)
        return tot
    return rec(0), len(etapes)

QUANDLES = [
    ("transpositions de S3 (coloriages de Fox modulo 3)", table(classe_transpositions(3))),
    ("transpositions de S4", table(classe_transpositions(4))),
    ("doubles transpositions de A5", table(classe_doubles_transpositions(5))),
    ("transpositions de S5", table(classe_transpositions(5))),
]
pd_tref = [list(x) for x in spherogram.Link("3_1").PD_code()]
pd_borr = [list(x) for x in spherogram.Link("L6a4").PD_code()]
D = json.load(open("pd.json"))
for nom, T in QUANDLES:
    t, _ = compte(pd_tref, T); b, _ = compte(pd_borr, T)
    print(f"\n== {nom} ({len(T)} couleurs) ==", flush=True)
    print(f"  trefle : {t} ; union scindee de quatre trefles : {t**4} ; de trois trefles et un rond non noue : {t**3 * len(T)}", flush=True)
    print(f"  anneaux borromeens (temoin) : {b} ; trois ronds separes : {len(T)**3}", flush=True)
    for cle in ("pd_noir_corrige", "pd"):
        t0 = time.time(); c, g = compte(D[cle], T)
        print(f"  {cle} : {c} coloriages ({g} arcs generateurs, {time.time()-t0:.0f} s)", flush=True)
