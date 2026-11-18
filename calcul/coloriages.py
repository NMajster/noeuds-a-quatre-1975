"""Preuve elementaire de la non-separabilite du dessin corrige (sans structure hyperbolique).

Principe.
 (1) Chaque sous-entrelacs de trois ronds du dessin corrige est une union scindee de trois trefles
     (etabli par simplification du diagramme, voir snappy_fig.py).
 (2) Si l'entrelacs entier L etait scinde, une sphere separerait ses ronds en deux paquets A et B ;
     L serait l'union scindee de L_A et L_B ; chacun, ayant au plus trois ronds, est un sous-entrelacs
     d'un triplet, donc une union scindee de trefles. L serait donc l'union scindee de quatre trefles.
 (3) Le nombre de coloriages de Fox modulo p est un invariant d'entrelacs. Pour l'union scindee de
     quatre trefles, la nullite de la matrice de coloriage vaut 8 modulo 3 et 4 modulo tout p premier
     impair different de 3 (chaque trefle : determinant 3).
 (4) Si la nullite de L differe pour un p, L n'est pas cette union scindee ; donc L n'est pas scinde.

La matrice de coloriage se lit sur le code PD : a chaque croisement [a, b, c, d], les aretes a et c
sont celles du brin qui passe dessous, b et d celles du brin qui passe dessus ; la relation est
2*col(dessus) - col(a) - col(c) = 0, apres identification de b et d. Elle ne depend d'aucune
orientation ni d'aucun signe de croisement.

Usage : python coloriages.py
"""
import json, itertools
import spherogram

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 101, 1000003]

def nullite(pd, p):
    """Nullite modulo p de la matrice de coloriage du diagramme donne par son code PD."""
    aretes = sorted({e for x in pd for e in x})
    parent = {e: e for e in aretes}
    def find(e):
        while parent[e] != e:
            parent[e] = parent[parent[e]]; e = parent[e]
        return e
    for a, b, c, d in pd:
        parent[find(b)] = find(d)            # le brin de dessus ne change pas d'arc
    arcs = sorted({find(e) for e in aretes}); idx = {r: i for i, r in enumerate(arcs)}
    n = len(arcs); M = []
    for a, b, c, d in pd:
        row = [0] * n
        row[idx[find(b)]] += 2; row[idx[find(a)]] -= 1; row[idx[find(c)]] -= 1
        M.append([v % p for v in row])
    rang = 0
    for col in range(n):
        piv = next((r for r in range(rang, len(M)) if M[r][col]), None)
        if piv is None: continue
        M[rang], M[piv] = M[piv], M[rang]
        inv = pow(M[rang][col], -1, p)
        M[rang] = [(v * inv) % p for v in M[rang]]
        for r in range(len(M)):
            if r != rang and M[r][col]:
                f = M[r][col]; M[r] = [(x - f * y) % p for x, y in zip(M[r], M[rang])]
        rang += 1
    return n - rang

def pd_de(L):
    return [list(x) for x in L.PD_code()]

def ligne(nom, pd):
    print(f"{nom:<42} croisements {len(pd):>3} | nullite mod p :", {p: nullite(pd, p) for p in PRIMES})

# --- temoins connus ---
print("== Temoins ==")
tref = spherogram.Link("3_1"); ligne("trefle 3_1 (attendu : 2 mod 3, 1 sinon)", pd_de(tref))
borr = spherogram.Link("L6a4"); ligne("anneaux borromeens L6a4 (attendu : 1)", pd_de(borr))
hopf = spherogram.Link("L2a1"); ligne("entrelacs de Hopf (attendu : 1)", pd_de(hopf))

D = json.load(open("pd.json"))
for nom in ("pd_noir_corrige", "pd"):
    print(f"\n== {nom} ==")
    L = spherogram.Link(D[nom])
    ligne("entrelacs entier, diagramme extrait", D[nom])
    L2 = L.copy(); L2.simplify("global")
    ligne("entrelacs entier, diagramme simplifie", pd_de(L2))
    comps = list(range(len(L.link_components)))
    for k in (3, 2, 1):
        for S in itertools.combinations(comps, k):
            sub = L.sublink(list(S))
            ligne(f"sous-entrelacs {S}, non simplifie", pd_de(sub))
print("\nAttendu pour une union scindee de quatre trefles : 8 modulo 3, 4 modulo tout autre p impair.")
print("Attendu pour une union scindee de trois trefles : 6 modulo 3, 3 sinon ; de deux : 4 et 2 ; un trefle : 2 et 1.")
