"""Figures simples, dessinees a partir de courbes de l'espace : trefles, noeud borromeen, exemple de Milnor.

Chaque rond est une courbe fermee (x, y, z). On la projette sur le plan (x, y). A chaque croisement, le brin
le plus bas (z) est interrompu. Le meme calcul produit le code PD du dessin, ecrit dans codes_pd.json, pour
que chaque figure soit controlee par SnapPy (voir controle_simples.py) : on dessine donc ce qu'on a verifie.

Usage : python fig_simples.py
"""
import json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"../figures/"
N = 1200                                   # points par rond

def croisements(ronds):
    """Liste des croisements : (rond i, indice de segment a, parametre s, rond j, indice b, parametre t, point)."""
    X = []
    for i, P in enumerate(ronds):
        for j, Q in enumerate(ronds):
            if j < i: continue
            A0, A1 = P[:, :2], np.roll(P[:, :2], -1, axis=0)
            B0, B1 = Q[:, :2], np.roll(Q[:, :2], -1, axis=0)
            for a in range(len(P)):
                d1 = A1[a] - A0[a]
                d2 = B1 - B0
                den = d1[0] * d2[:, 1] - d1[1] * d2[:, 0]
                w = B0 - A0[a]
                with np.errstate(divide="ignore", invalid="ignore"):
                    s = (w[:, 0] * d2[:, 1] - w[:, 1] * d2[:, 0]) / den
                    t = (w[:, 0] * d1[1] - w[:, 1] * d1[0]) / den
                ok = (den != 0) & (s >= 0) & (s < 1) & (t >= 0) & (t < 1)
                for b in np.nonzero(ok)[0]:
                    if i == j and (b <= a + 1 or (a == 0 and b == len(P) - 1)): continue
                    X.append((i, a, float(s[b]), j, int(b), float(t[b]), A0[a] + s[b] * d1))
    return X

def analyse(ronds):
    """Pour chaque croisement : brin de dessus et de dessous, directions ; puis code PD."""
    X = croisements(ronds)
    passages = {i: [] for i in range(len(ronds))}       # par rond : (position le long du rond, n° de croisement, 'dessus'|'dessous')
    infos = []
    for k, (i, a, s, j, b, t, pt) in enumerate(X):
        P, Q = ronds[i], ronds[j]
        zi = P[a, 2] + s * (P[(a + 1) % len(P), 2] - P[a, 2])
        zj = Q[b, 2] + t * (Q[(b + 1) % len(Q), 2] - Q[b, 2])
        assert abs(zi - zj) > 1e-3, "croisement ambigu"
        di = P[(a + 1) % len(P), :2] - P[a, :2]; dj = Q[(b + 1) % len(Q), :2] - Q[b, :2]
        if zi > zj: haut, bas = (i, a + s, di), (j, b + t, dj)
        else:       haut, bas = (j, b + t, dj), (i, a + s, di)
        infos.append({"pt": pt, "haut": haut, "bas": bas})
        passages[haut[0]].append((haut[1], k, "dessus")); passages[bas[0]].append((bas[1], k, "dessous"))
    # numerotation des aretes : le long de chaque rond, une arete entre deux passages consecutifs
    arete_avant, arete_apres, n = {}, {}, 0
    for i in passages:
        L = sorted(passages[i]); m = len(L)
        for r, (pos, k, role) in enumerate(L):
            arete_avant[(k, role)] = n + r                    # arete qui arrive au passage
            arete_apres[(k, role)] = n + (r + 1) % m          # arete qui en repart
        n += m
    pd = []
    for k, c in enumerate(infos):
        u, o = c["bas"][2], c["haut"][2]
        a, cc = arete_avant[(k, "dessous")], arete_apres[(k, "dessous")]
        vers_la_gauche = u[0] * o[1] - u[1] * o[0] > 0        # le brin de dessus va de la droite vers la gauche du brin de dessous
        b, d = (arete_avant[(k, "dessus")], arete_apres[(k, "dessus")]) if vers_la_gauche else (arete_apres[(k, "dessus")], arete_avant[(k, "dessus")])
        pd.append([a + 1, b + 1, cc + 1, d + 1])
    vrille = sum(1 if (c["bas"][2][0] * c["haut"][2][1] - c["bas"][2][1] * c["haut"][2][0]) < 0 else -1 for c in infos)
    return infos, pd, vrille

def dessine(ax, ronds, couleurs, lw=2.6, trou=0.16, titre=None):
    infos, pd, vrille = analyse(ronds)
    for i, P in enumerate(ronds):
        garde = np.ones(len(P), bool)
        for c in infos:
            if c["bas"][0] == i:
                loin = np.abs((np.arange(len(P)) - c["bas"][1] + len(P) / 2) % len(P) - len(P) / 2) > len(P) / 8
                garde &= (np.linalg.norm(P[:, :2] - c["pt"], axis=1) > trou) | loin      # seul le passage de dessous est interrompu
        idx = np.arange(len(P))
        # decoupe en morceaux continus (le rond est ferme)
        debut = [k for k in idx if garde[k] and not garde[k - 1]] or [0]
        for k0 in debut:
            morceau = [k0]
            k = (k0 + 1) % len(P)
            while garde[k] and k != k0:
                morceau.append(k); k = (k + 1) % len(P)
            if k == k0: morceau.append(k0)
            Q = P[morceau]
            ax.plot(Q[:, 0], Q[:, 1], color=couleurs[i], lw=lw, solid_capstyle="butt")
    ax.set_aspect("equal"); ax.axis("off")
    if titre: ax.set_title(titre, fontsize=10, pad=4)
    return pd, vrille, len(infos)

t = np.linspace(0, 2 * np.pi, N, endpoint=False) + 0.00037   # leger decalage : aucun croisement ne tombe sur un point d'echantillonnage
def trefle(main):
    return np.stack([np.sin(t) + 2 * np.sin(2 * t), np.cos(t) - 2 * np.cos(2 * t), main * -np.sin(3 * t)], 1)
def borromeen():
    """Trois cercles en triangle. Chaque cercle passe dessus le suivant et dessous le precedent, aux deux croisements."""
    R, d, h = 1.0, 0.62, 0.5
    # sur chaque cercle, les quatre croisements se suivent a environ 60 degres : on alterne dessus et dessous
    a0 = np.radians(150) - np.arccos(d * np.sqrt(3) / (2 * R))
    L = []
    for k in range(3):
        th = np.pi / 2 + k * 2 * np.pi / 3
        L.append(np.stack([d * np.cos(th) + R * np.cos(t), d * np.sin(th) + R * np.sin(t), h * np.cos(3 * (t - th - a0))], 1))
    return L
def milnor(traverse):
    """Un « huit » et un ovale (entrelacs de Whitehead). traverse=True : le huit s'est traverse lui-meme."""
    s = -1.0 if traverse else 1.0
    huit = np.stack([2.2 * np.sin(t), 1.1 * np.sin(2 * t), s * 0.5 * np.cos(t)], 1)
    ovale = np.stack([1.05 * np.cos(t), 1.75 * np.sin(t), 0.9 * np.sin(2 * t)], 1)
    return [huit, ovale]

codes = {}
NOIR, VERT, ROUGE = "#000000", "#3ca35a", "#b0001e"

fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6))
for ax, (cle, ronds, coul, titre) in zip(axes, [
        ("trefle_a", [trefle(+1)], [NOIR], "a. Un nœud de trèfle"),
        ("trefle_b", [trefle(-1)], [NOIR], "b. Son image en miroir"),
        ("borromeen", borromeen(), [NOIR, VERT, ROUGE], "c. Le nœud borroméen")]):
    pd, vr, nx = dessine(ax, ronds, coul, titre=titre)
    codes[cle] = {"pd": pd, "vrille": vr, "croisements": nx}
fig.tight_layout()
for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig1_trefles_borromeen." + ext, dpi=300)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.9))
for ax, (cle, ronds, titre) in zip(axes, [
        ("milnor_noue", milnor(False), "a. Le « huit » et l'ovale"),
        ("milnor_traverse", milnor(True), "b. Après que le huit s'est traversé")]):
    pd, vr, nx = dessine(ax, ronds, [NOIR, ROUGE], titre=titre, trou=0.14)
    codes[cle] = {"pd": pd, "vrille": vr, "croisements": nx}
fig.tight_layout()
for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig3_milnor." + ext, dpi=300)
plt.close(fig)

json.dump(codes, open(OUT + "codes_pd.json", "w"), indent=1)
for k, v in codes.items(): print(k, ": croisements", v["croisements"], "| vrille", v["vrille"])
