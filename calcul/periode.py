"""Periodicite du diagramme : recherche d'un automorphisme d'ordre 3 du diagramme (rotation de la tresse fermee),
diagramme quotient (une periode refermee) et revetements cycliques a k feuillets (le motif repete k fois).

Entree : pd.json (codes PD de la figure imprimee et de la figure rectifiee).
Convention PD : (a, b, c, d), a = entree du brin dessous, puis sens trigonometrique.
Un demi-brin est (croisement, position). Un automorphisme du diagramme respecte le dessus/dessous :
il envoie la position i sur i ou i + 2.

Usage : python periode.py
"""
import json, sys
from collections import defaultdict, deque

def structure(PD):
    """pair[(c, i)] = demi-brin a l'autre bout de l'arete."""
    occ = defaultdict(list)
    for c, X in enumerate(PD):
        for i, e in enumerate(X): occ[e].append((c, i))
    pair = {}
    for e, L in occ.items():
        assert len(L) == 2, (e, L)
        pair[L[0]] = L[1]; pair[L[1]] = L[0]
    return pair

def automorphismes(PD):
    """Tous les automorphismes du diagramme qui preservent l'orientation du plan et le dessus/dessous."""
    pair = structure(PD); n = len(PD); res = []
    for c1 in range(n):
        for r in (0, 2):
            f = {0: (c1, r)}; ok = True; file = deque([0])
            while file and ok:
                c = file.popleft(); d, rot = f[c]
                for i in range(4):
                    c2, j = pair[(c, i)]
                    d2, j2 = pair[(d, (i + rot) % 4)]
                    rot2 = (j2 - j) % 4
                    if rot2 not in (0, 2): ok = False; break
                    if c2 in f:
                        if f[c2] != (d2, rot2): ok = False; break
                    else:
                        f[c2] = (d2, rot2); file.append(c2)
            if ok and len(f) == n and len({v[0] for v in f.values()}) == n: res.append(f)
    return res

def ordre(f):
    n = len(f); g = {c: (c, 0) for c in f}; k = 0
    while True:
        g = {c: (f[g[c][0]][0], (g[c][1] + f[g[c][0]][1]) % 4) for c in g}; k += 1
        if all(g[c] == (c, 0) for c in g): return k
        if k > 400: return None

def faces(pair):
    """Face a gauche de chaque demi-brin (on part du croisement, on suit l'arete, on tourne a gauche)."""
    face = {}; nf = 0
    for h in pair:
        if h in face: continue
        cur = h
        while cur not in face:
            face[cur] = nf
            c2, j = pair[cur]
            cur = (c2, (j - 1) % 4)
        nf += 1
    return face, nf

def quotient(PD, f):
    """Diagramme quotient par l'automorphisme f, avec ses demi-brins, et les deux faces fixes."""
    pair = structure(PD)
    def im(h): return (f[h[0]][0], (h[1] + f[h[0]][1]) % 4)
    rep = {}                       # demi-brin -> representant d'orbite
    for h in pair:
        if h in rep: continue
        orb = [h]; x = im(h)
        while x != h: orb.append(x); x = im(x)
        for y in orb: rep[y] = h
    # croisements du quotient : orbites de croisements ; on choisit pour chacun un representant c0 et ses 4 positions
    crep = {}; qc = []
    for c in range(len(PD)):
        if c in crep: continue
        orb = [c]; x = f[c][0]
        while x != c: orb.append(x); x = f[x][0]
        for y in orb: crep[y] = c
        qc.append(c)
    idx = {c: i for i, c in enumerate(qc)}
    # demi-brin du quotient = (indice du croisement representant, position) ; image d'un demi-brin quelconque
    def q(h):
        r = rep[h]; c, i = r
        # ramener r sur le croisement representant de son orbite
        x = r
        while x[0] != crep[c]: x = im(x)
        return (idx[x[0]], x[1])
    qpair = {}
    for h, h2 in pair.items(): qpair[q(h)] = q(h2)
    face, nf = faces(pair)
    # faces fixes : orbite de la face sous f
    fim = {}
    for h in pair: fim[face[h]] = face[im(h)]
    fixes = [a for a in range(nf) if fim[a] == a]
    qface, nqf = faces(qpair)
    qfix = set()
    for h in pair:
        if face[h] in fixes: qfix.add(qface[q(h)])
    return qpair, len(qc), qface, nqf, sorted(qfix), (nf, fixes)

def chemin_dual(qpair, qface, a, b):
    """Plus court chemin de faces de a a b ; renvoie s[h] = +1 si le chemin traverse l'arete de la gauche de h vers sa droite."""
    vois = defaultdict(list)
    for h, h2 in qpair.items(): vois[qface[h]].append((qface[h2], h))   # de la face gauche de h a sa face droite
    prev = {a: None}; file = deque([a])
    while file:
        x = file.popleft()
        if x == b: break
        for y, h in vois[x]:
            if y not in prev: prev[y] = (x, h); file.append(y)
    s = defaultdict(int); x = b; L = 0
    while prev[x] is not None:
        x0, h = prev[x]; s[h] += 1; s[qpair[h]] -= 1; x = x0; L += 1
    return s, L

def revetement(qpair, nq, s, k):
    """Code PD du revetement cyclique a k feuillets du diagramme quotient (le motif repete k fois)."""
    lab = {}; n = 0
    PD = [[None] * 4 for _ in range(nq * k)]
    for m in range(k):
        for (c, i), (c2, j) in qpair.items():
            h = (c, i, m); h2 = (c2, j, (m + s[(c, i)]) % k)
            if h not in lab:
                lab[h] = lab[h2] = n; n += 1
            PD[c + nq * m][i] = lab[h]
    return [tuple(X) for X in PD]

if __name__ == "__main__":
    D = json.load(open(r"pd.json"))
    out = {}
    for cle in ("pd", "pd_noir_corrige"):
        PD = D[cle]; A = automorphismes(PD)
        ords = sorted(ordre(f) for f in A)
        print(cle, ": croisements", len(PD), "| automorphismes du diagramme :", len(A), "| ordres :", ords)
        pair = structure(PD); face, nf = faces(pair)
        print("   faces :", nf, "(attendu", len(PD) + 2, ")")
        f3 = [f for f in A if ordre(f) == 3]
        if f3:
            f = f3[0]
            qpair, nq, qface, nqf, qfix, (nf, fixes) = quotient(PD, f)
            print("   quotient : croisements", nq, "| faces", nqf, "| faces fixes en haut :", fixes, "-> dans le quotient :", qfix)
            s, L = chemin_dual(qpair, qface, qfix[0], qfix[1])
            print("   chemin d'une face fixe a l'autre : traverse", L, "brins")
            out[cle] = {"nq": nq, "qpair": [[list(a), list(b)] for a, b in qpair.items()], "s": [[list(h), v] for h, v in s.items() if v],
                        "orbites": None}
            for k in (1, 2, 3, 4, 5, 7):
                out[cle]["pd_k%d" % k] = revetement(qpair, nq, s, k)
    json.dump(out, open(r"periode.json", "w"))
