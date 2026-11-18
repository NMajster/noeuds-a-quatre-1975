"""Figure : l'axe. La tresse de Thome et Soury refermee en rond autour de son axe, vu en bout (un point au centre).
a. Un tour du motif : quatre ronds, dont chacun fait deux fois le tour de l'axe. Sans l'axe, ils sont libres.
b. Trois tours : quatre trefles.
Le mot de tresse vient de calcul/motif_tresse.json (repere : le flux monte, les rangs croissent vers la droite ;
on l'enroule en gardant ce repere : le rang devient le rayon, le flux tourne dans le sens inverse des aiguilles d'une montre).
Usage : python fig_axe.py"""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
OUT = r"../figures/"
COUL = {"noir": "#000000", "vert": "#3ca35a", "rouge": "#b0001e", "brun": "#e0b07a"}
M = json.load(open(r"motif_tresse.json")); mot = [(i, d) for i, d in M["mot"]]; cols0 = M["couleurs"]; NB = 8
def trace(ax, k, lw=1.6, r0=0.95, dr=0.2, axe=True):
    h = [0] * NB; NIV = []
    for i, d in mot:
        n = max(h[i], h[i + 1]); NIV.append(n); h[i] = h[i + 1] = n + 1
    H = max(h); tot = k * H; u = np.linspace(0, 1, 40); s = (1 - np.cos(np.pi * u)) / 2
    def P(pos, niv):
        r = r0 + dr * np.asarray(pos, float); th = np.pi / 2 + 2 * np.pi * np.asarray(niv, float) / tot; return r * np.cos(th), r * np.sin(th)
    cols = list(cols0); occ = {(n, i): d for (i, d), n in zip(mot, NIV)}
    for rep in range(k):
        for n in range(H):
            y0 = rep * H + n; pris = set()
            for i in range(NB - 1):
                if (n, i) in occ:
                    d = occ[(n, i)]; pris |= {i, i + 1}
                    g = (i + s, y0 + u, cols[i]); dr_ = (i + 1 - s, y0 + u, cols[i + 1]); dessus, dessous = (g, dr_) if d == "G" else (dr_, g)
                    ax.plot(*P(dessous[0], dessous[1]), color=COUL[dessous[2]], lw=lw, solid_capstyle="butt", zorder=2)
                    hw = 4 if k == 1 else 9; m = slice(20 - hw, 20 + hw)
                    ax.plot(*P(dessus[0][m], dessus[1][m]), color="white", lw=lw * 3.2, solid_capstyle="butt", zorder=3)
                    ax.plot(*P(dessus[0], dessus[1]), color=COUL[dessus[2]], lw=lw, solid_capstyle="butt", zorder=4)
                    cols[i], cols[i + 1] = cols[i + 1], cols[i]
            for i in range(NB):
                if i not in pris: ax.plot(*P(i + 0 * u, y0 - 0.02 + 1.04 * u), color=COUL[cols[i]], lw=lw, solid_capstyle="butt", zorder=2)
    if axe:
        ax.add_patch(Circle((0, 0), 0.11, fill=False, ec="#444444", lw=1.3)); ax.add_patch(Circle((0, 0), 0.03, color="#444444"))
        ax.text(0, -0.27, "axe", ha="center", va="top", fontsize=9, color="#444444")
    ax.set_aspect("equal"); ax.axis("off"); R = r0 + dr * (NB - 1) + 0.15; ax.set_xlim(-R, R); ax.set_ylim(-R, R)
if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.9))
    trace(axes[0], 1, lw=1.8); axes[0].set_title("a. Un tour : quatre ronds libres", fontsize=10)
    trace(axes[1], 3, lw=1.4); axes[1].set_title("b. Trois tours : quatre trèfles", fontsize=10)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_axe." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
    for k in (1, 3):
        f2, ax = plt.subplots(figsize=(8, 8)); trace(ax, k, lw=2.4, axe=False); f2.savefig(OUT + f"fig_axe_controle_{k}.png", dpi=200)
