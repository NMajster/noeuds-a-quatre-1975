"""Le motif d'une periode ecrit comme une tresse a 8 brins, tire du diagramme quotient.
Controle : la tresse repetee trois fois redonne, croisement pour croisement, le diagramme de la figure rectifiee.

Sortie : motif_tresse.json  (mot de tresse, couleur de chaque brin)
Usage : python motif_tresse.py
"""
import json
from collections import defaultdict, deque
import periode as P

D = json.load(open(r"pd.json"))
PD = D["pd_noir_corrige"]; coul = {int(k): v for k, v in D["couleurs"].items()}; CC = D["comp_croisements"]
A = P.automorphismes(PD); f = [g for g in A if P.ordre(g) == 3][0]
pair = P.structure(PD)

# --- quotient, en gardant le croisement d'origine de chaque croisement du quotient ---
def im(h): return (f[h[0]][0], (h[1] + f[h[0]][1]) % 4)
crep = {}; qc = []
for c in range(len(PD)):
    if c in crep: continue
    x = c
    while x not in crep: crep[x] = c; x = f[x][0]
    qc.append(c)
idx = {c: i for i, c in enumerate(qc)}
def q(h):
    x = h
    while x[0] != crep[h[0]]: x = im(x)
    return (idx[x[0]], x[1])
qpair = {q(h): q(h2) for h, h2 in pair.items()}
nq = len(qc); qface, nqf = P.faces(qpair)
face, nf = P.faces(pair)
fixes = {face[h] for h in pair if face[im(h)] == face[h]}
qfix = sorted({qface[q(h)] for h in pair if face[h] in fixes}); assert len(qfix) == 2
def couleur(h):               # h = demi-brin du quotient ; positions paires = brin dessous
    c0 = qc[h[0]]; return coul[CC[c0][0] if h[1] % 2 == 0 else CC[c0][1]]

def chemin(a, b):
    vois = defaultdict(list)
    for h, h2 in qpair.items(): vois[qface[h]].append((qface[h2], h))
    prev = {a: None}; file = deque([a])
    while file:
        x = file.popleft()
        for y, h in vois[x]:
            if y not in prev: prev[y] = (x, h); file.append(y)
    L = []; x = b
    while prev[x] is not None: x0, h = prev[x]; L.append(h); x = x0
    return L[::-1]

def tresse(a, b):
    ch = chemin(a, b); assert len(ch) == 8
    cur = [qpair[h] for h in ch]            # demi-brins par lesquels les 8 brins entrent, apres la coupe
    depart = list(cur)
    cols = [couleur(h) for h in cur]
    mot = []; fait = set()
    while len(fait) < nq:
        ok = False
        for i in range(7):
            (c, j), (c2, j2) = cur[i], cur[i + 1]
            if c == c2 and c not in fait and j2 == (j + 1) % 4:
                mot.append((i, "G" if j % 2 == 1 else "D"))      # brin qui passe dessus : celui de gauche (G) ou de droite (D)
                cur[i] = qpair[(c, (j + 3) % 4)]; cur[i + 1] = qpair[(c, (j + 2) % 4)]
                fait.add(c); ok = True; break
        if not ok: return None
    # retour a la coupe : les brins doivent arriver sur les demi-brins ch, dans l'ordre
    return (mot, cols) if cur == depart else ("retour", cur, depart)

def pd_de_tresse(mot, k):
    """Code PD de la tresse repetee k fois et refermee (repere : le flux monte, les positions croissent vers la droite)."""
    n = 0; cur = list(range(8)); n = 8; debut = list(cur); PDk = []
    for _ in range(k):
        for i, dessus in mot:
            a, b = cur[i], cur[i + 1]; no, ne = n, n + 1; n += 2     # no = sortie a gauche (NO), ne = sortie a droite (NE)
            if dessus == "G": PDk.append([b, ne, no, a])           # dessous : entre par le SE (b), sort au NO
            else: PDk.append([a, b, ne, no])                        # dessous : entre par le SO (a), sort au NE
            cur[i], cur[i + 1] = no, ne
    ren = {cur[i]: debut[i] for i in range(8)}
    return [tuple(ren.get(x, x) for x in X) for X in PDk]

if __name__ == "__main__":
    for a, b in ((qfix[0], qfix[1]), (qfix[1], qfix[0])):
        r = tresse(a, b)
        print("de la face", a, "a la face", b, ":", "bloque" if r is None else ("retour incorrect" if r[0] == "retour" else f"tresse de {len(r[0])} croisements"))
        if r and r[0] != "retour":
            mot, cols = r
            import axe_preuve_iso as I
            PD3 = pd_de_tresse(mot, 3)
            print("   couleurs des 8 brins :", cols)
            print("   tresse repetee 3 fois = diagramme de la figure rectifiee :", I.iso(PD3, [tuple(x) for x in PD]))
            json.dump({"mot": mot, "couleurs": cols}, open(r"motif_tresse.json", "w"))
            print("   mot :", " ".join(f"{i+1}{d}" for i, d in mot))
            break
