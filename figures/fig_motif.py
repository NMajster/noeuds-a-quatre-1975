"""Figure : le motif d'une periode (tresse a 8 brins, 28 croisements) et ce motif repete trois fois.

Le mot de tresse vient de calcul/motif_tresse.json (motif_tresse.py), ou il est controle : repete trois fois,
il redonne croisement pour croisement le diagramme de la figure rectifiee.
Repere du calcul : le flux monte, les positions croissent vers la droite. Le dessin est ce repere tourne
d'un demi-tour (la tresse se lit de haut en bas), sans miroir.

Usage : python fig_motif.py
"""
import json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"../figures/"
COUL = {"noir": "#000000", "vert": "#3ca35a", "rouge": "#b0001e", "brun": "#e0b07a"}
M = json.load(open(r"motif_tresse.json"))
mot, cols0 = [(i, d) for i, d in M["mot"]], M["couleurs"]

def niveaux(mot):
    """Place chaque croisement au premier niveau libre (les croisements qui ne se touchent pas partagent un niveau)."""
    h = [0] * 8; L = []
    for i, d in mot:
        n = max(h[i], h[i + 1]); L.append(n); h[i] = h[i + 1] = n + 1
    return L, max(h)
NIV, H = niveaux(mot)

def trace(ax, k, lw, sep=True):
    cols = list(cols0); u = np.linspace(0, 1, 40); s = u * u * (3 - 2 * u)
    def P(x, y): return -np.asarray(x, float), -np.asarray(y, float)          # demi-tour
    for rep in range(k):
        y0 = rep * H
        occ = {}                                                             # (niveau, position) -> croisement
        for (i, d), n in zip(mot, NIV): occ[(n, i)] = d
        for n in range(H):
            pris = set()
            for i in range(7):
                if (n, i) in occ:
                    d = occ[(n, i)]; pris |= {i, i + 1}
                    g = (i + s, y0 + n + u, cols[i]); dr = (i + 1 - s, y0 + n + u, cols[i + 1])   # brin venu de gauche, brin venu de droite
                    dessus, dessous = (g, dr) if d == "G" else (dr, g)
                    ax.plot(*P(dessous[0], dessous[1]), color=COUL[dessous[2]], lw=lw, solid_capstyle="butt", zorder=2)
                    m = slice(11, 29)
                    ax.plot(*P(dessus[0][m], dessus[1][m]), color="white", lw=lw * 3.2, solid_capstyle="butt", zorder=3)
                    ax.plot(*P(dessus[0], dessus[1]), color=COUL[dessus[2]], lw=lw, solid_capstyle="butt", zorder=4)
                    cols[i], cols[i + 1] = cols[i + 1], cols[i]
            for i in range(8):
                if i not in pris: ax.plot(*P([i, i], [y0 + n - 0.01, y0 + n + 1.01]), color=COUL[cols[i]], lw=lw, solid_capstyle="butt", zorder=2)
        if sep and rep: ax.plot(*P([-0.6, 7.6], [y0, y0]), color="#888888", lw=0.6, ls=(0, (4, 3)), zorder=1)
    assert cols == cols0
    for i in range(8):                                                        # amorces en haut et en bas
        ax.plot(*P([i, i], [-0.7, 0]), color=COUL[cols0[i]], lw=lw, solid_capstyle="butt")
        ax.plot(*P([i, i], [k * H, k * H + 0.7]), color=COUL[cols0[i]], lw=lw, solid_capstyle="butt")
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-8.2, 1.2); ax.set_ylim(-(k * H + 1.0), 1.0)

fig = plt.figure(figsize=(6.6, 7.6))
a = fig.add_axes([0.02, 0.30, 0.50, 0.62]); b = fig.add_axes([0.58, 0.02, 0.38, 0.90])
trace(a, 1, lw=2.4); a.set_title("a. Le motif", fontsize=10, pad=4)
trace(b, 3, lw=1.5); b.set_title("b. Le motif répété trois fois", fontsize=10, pad=4)
for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig2_motif_trois_fois." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
print("niveaux par periode :", H, "| croisements par periode :", len(mot))
