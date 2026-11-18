"""Figure : la regle a trois (Lacan, 9 decembre 1975) et la regle a quatre (figure de Thome et Soury).
Une fleche de A vers B veut dire : A passe toujours sur B.  Usage : python fig_regles.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
OUT = r"../figures/"
C = {"noir": "#000000", "vert": "#3ca35a", "rouge": "#b0001e", "brun": "#c9924f", "gris": "#555555"}
def rond(ax, xy, coul, nom, r=0.33):
    ax.add_patch(Circle(xy, r, fill=False, ec=coul, lw=2.6)); ax.text(xy[0], xy[1], nom, ha="center", va="center", fontsize=9, color=coul)
def fleche(ax, a, b, r=0.40, rad=0.0, style="-|>", coul="#555555", ls="-"):
    a, b = np.array(a, float), np.array(b, float); u = (b - a) / np.linalg.norm(b - a)
    ax.add_patch(FancyArrowPatch(a + r * u, b - r * u, arrowstyle=style, mutation_scale=13, lw=1.3, color=coul, connectionstyle=f"arc3,rad={rad}", linestyle=ls))
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
ax = axes[0]; P = {k: (1.5 * np.cos(a), 1.5 * np.sin(a)) for k, a in zip("ABC", np.radians([90, 210, 330]))}
for k, c in zip("ABC", ("#000000", "#3ca35a", "#b0001e")): rond(ax, P[k], c, "")
fleche(ax, P["A"], P["B"]); fleche(ax, P["B"], P["C"]); fleche(ax, P["C"], P["A"])
ax.set_title("a. La règle à trois", fontsize=10)
ax = axes[1]; R, B = (0, 1.5), (0, -1.6); N, V = (-0.95, -0.05), (0.95, -0.05)
ax.add_patch(FancyBboxPatch((-1.55, -0.58), 3.1, 1.06, boxstyle="round,pad=0.02,rounding_size=0.25", fill=False, ec="#999999", lw=0.9, ls=(0, (4, 3))))
[rond(ax, p, C[k], k, r=0.42) for p, k in ((R, "rouge"), (B, "brun"), (N, "noir"), (V, "vert"))]
[fleche(ax, p, q, r=0.50) for p, q in ((R, N), (R, V), (N, B), (V, B))]
ax.add_patch(FancyArrowPatch((0.42, -1.72), (0.44, 1.56), arrowstyle="-|>", mutation_scale=13, lw=1.3, color="#555555", connectionstyle="arc3,rad=1.05"))
fleche(ax, N, V, r=0.50, style="<|-|>", ls=(0, (2, 2)))
ax.text(0, 0.22, "alternent", ha="center", va="bottom", fontsize=8, color="#555555")
ax.set_title("b. La règle à quatre", fontsize=10)
for ax in axes: ax.set_xlim(-2.6, 3.0); ax.set_ylim(-2.3, 2.2); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_regles." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
