"""La regle a quatre, dans une disposition donnee (l'ombre d'une tresse a 8 brins, deux brins par trefle, repetee trois fois).
Reglage essaye : cinq couples de trefles en relation constante (l'un passe toujours sur l'autre) et UN couple qui alterne
(a chacun de ses croisements dans la periode, l'un ou l'autre passe dessus, le meme choix etant repete a chaque tour).
On garde les reglages ou tout triplet se separe et ou les quatre ne se separent pas.

Dispositions :
  E  emboitee (celle de Lacan et des dessins 0 et 1 de Soury) : chaque brin croise chaque autre une fois par tour ; 16 ecritures.
  TS celle de la figure de Thome et Soury (28 croisements par tour).

Usage : python regle_dispositions.py E|TS
"""
import sys, itertools, json, collections, snappy, spherogram
import lacan_homologues as LH

def mots_reduits(k):
    res = []
    def rec(perm, mot):
        desc = [i for i in range(k - 1) if perm[i] < perm[i + 1]]
        if not desc: res.append(tuple(mot)); return
        for i in desc:
            p = list(perm); p[i], p[i + 1] = p[i + 1], p[i]; rec(p, mot + [i + 1])
    rec(list(range(k)), []); return res

def croisements(ombre, rond):
    """Pour une periode : liste (generateur, rond du brin de gauche, rond du brin de droite). Le rond d'un brin est donne par son rang au debut."""
    pos = list(range(len(rond))); L = []
    for g in ombre:
        a, b = pos[g - 1], pos[g]; L.append((g, rond[a], rond[b])); pos[g - 1], pos[g] = b, a
    assert all(rond[pos[r]] == rond[r] for r in range(len(rond))), "les ronds ne se retrouvent pas apres un tour"
    return L
def tresse(X, propre, dessus):
    """dessus[k] = rond qui passe dessus au croisement k de la periode (croisements entre ronds differents) ; propre[k] = signe d'un croisement d'un rond avec lui-meme."""
    w = [g * (propre[k] if a == b else (1 if dessus[k] == a else -1)) for k, (g, a, b) in enumerate(X)]
    return w * 3
def sous_tresse(w, rond, garde):
    """Retire les brins des ronds absents de `garde`."""
    n = len(rond); pos = list(range(n)); out = []
    for x in w:
        g = abs(x); a, b = pos[g - 1], pos[g]
        if rond[a % n] in garde and rond[b % n] in garde:
            rang = sum(1 for r in range(g - 1) if rond[pos[r] % n] in garde) + 1
            out.append(rang if x > 0 else -rang)
        pos[g - 1], pos[g] = b, a
    return out
memo = {}
def morceaux(w):
    k = tuple(w)
    if k not in memo:
        L = spherogram.Link(braid_closure=list(w)); L.simplify("global")
        memo[k] = tuple(sorted(len(p.crossings) for p in L.split_link_diagram())) if len(L.crossings) else ()
    return memo[k]

def cherche(nom, ombre, rond, propre_de):
    X = croisements(ombre, rond); nr = 4; res = collections.Counter(); bons = []
    propre = [propre_de(k) for k in range(len(X))]
    paires = [(i, j) for i in range(nr) for j in range(i + 1, nr)]
    for (a, b) in paires:
        ks = [k for k, (g, x, y) in enumerate(X) if {x, y} == {a, b}]
        autres = [p for p in paires if p != (a, b)]
        for bits in itertools.product((0, 1), repeat=len(ks)):
            if len(set(bits)) == 1: continue                                  # ce serait un couple constant
            # enlacement nul du couple qui alterne : somme des signes
            if sum((1 if (a if bt else b) == X[k][1] else -1) for k, bt in zip(ks, bits)) != 0: res["couple alterne enlace"] += 1; continue
            for vals in itertools.product((0, 1), repeat=len(autres)):
                gagne = {p: (p[0] if v else p[1]) for p, v in zip(autres, vals)}
                dessus = {}
                for k, (g, x, y) in enumerate(X):
                    if x == y: continue
                    p = (min(x, y), max(x, y))
                    dessus[k] = (a if bits[ks.index(k)] else b) if p == (a, b) else gagne[p]
                # enlacements nuls des couples constants
                if any(sum((1 if dessus[k] == X[k][1] else -1) for k in dessus if {X[k][1], X[k][2]} == set(p)) != 0 for p in autres): res["couple constant enlace"] += 1; continue
                w = tresse(X, propre, dessus)
                if not all(morceaux(sous_tresse(w, rond, set(range(nr)) - {r})) == (3, 3, 3) for r in range(nr)): res["un triplet ne se separe pas"] += 1; continue
                m = morceaux(w)
                if m == (3, 3, 3, 3): res["les quatre se separent"] += 1; continue
                res["SOLUTION"] += 1; bons.append({"disposition": nom, "alterne": (a, b), "bits": bits, "gagne": {str(p): v for p, v in gagne.items()}, "mot": w[:len(w) // 3]})
                print("   solution :", nom, "| couple qui alterne", (a, b), bits, "| dessus pour les autres couples", gagne, "| croisements apres simplification", m, flush=True)
    return res, bons

if __name__ == "__main__":
    mode = sys.argv[1]; tout = collections.Counter(); B = []
    if mode == "E":
        for g in mots_reduits(4):
            ombre = list(g) + [8 - x for x in g] + LH.tissage(4); rond = [min(s, 7 - s) for s in range(8)]
            r, b = cherche("emboitee " + str(g), ombre, rond, lambda k: 1); tout += r; B += b
            print("ecriture", g, dict(r), flush=True)
    else:
        M = json.load(open("motif_tresse.json")); noms = ["noir", "brun", "rouge", "vert"]
        # motif_tresse.json est ecrit dans un repere ou le flux monte ; on garde ses signes tels quels (G = +)
        ombre = [i + 1 for i, d in M["mot"]]; rond = [noms.index(c) for c in M["couleurs"]]; sg = [1 if d == "G" else -1 for i, d in M["mot"]]
        r, b = cherche("Thome et Soury", ombre, rond, lambda k: sg[k]); tout += r; B += b
    print("TOTAL", dict(tout)); json.dump(B, open(f"regle_dispositions_{mode}.json", "w"))
