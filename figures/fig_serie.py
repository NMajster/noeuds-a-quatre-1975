"""Figure : la serie. Ce que devient un rond du motif selon le nombre de tours autour de l'axe.
Un rond est fait de deux brins qui se croisent une fois par tour : 1 tour, un rond ; 3 tours, un trefle ; 5 tours, le noeud a cinq croisements ; 7 tours, a sept.
Usage : python fig_serie.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
OUT = r"../figures/"
def rond(ax, k, lw=2.2, r0=0.72, dr=0.5):
    u = np.linspace(0, 1, 60); s = (1 - np.cos(np.pi * u)) / 2
    def P(pos, niv):
        r = r0 + dr * np.asarray(pos, float); th = np.pi / 2 + 2 * np.pi * np.asarray(niv, float) / k; return r * np.cos(th), r * np.sin(th)
    for n in range(k):
        dessous = (1 - s, n + u); dessus = (s, n + u)
        ax.plot(*P(*dessous), color="#1e191e", lw=lw, solid_capstyle="butt", zorder=2)
        m = slice(22, 38)
        ax.plot(*P(dessus[0][m], dessus[1][m]), color="white", lw=lw * 3.2, solid_capstyle="butt", zorder=3)
        ax.plot(*P(*dessus), color="#1e191e", lw=lw, solid_capstyle="butt", zorder=4)
    ax.add_patch(Circle((0, 0), 0.07, fill=False, ec="#666666", lw=1.0)); ax.add_patch(Circle((0, 0), 0.02, color="#666666"))
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45)
fig, axes = plt.subplots(1, 4, figsize=(7.4, 2.3))
for ax, k, t1, t2 in zip(axes, (1, 3, 5, 7), ("1 tour", "3 tours", "5 tours", "7 tours"), ("un rond", "un trèfle", "cinq croisements", "sept croisements")):
    rond(ax, k); ax.set_title(t1, fontsize=10, pad=2); ax.text(0, -1.62, t2, ha="center", va="top", fontsize=9, color="#444444")
fig.tight_layout()
for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_serie." + ext, dpi=300, bbox_inches="tight", pad_inches=0.06)
