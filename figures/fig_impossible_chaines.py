"""Figure : pourquoi la regle « l'un passe toujours sur l'autre » ne peut pas donner quatre, montre sur des ronds.
a. Les quatre ronds s'empilent (le noir sur tous, puis le vert, le rouge, le bleu) : ils se separent.
b. Ils ne s'empilent pas : trois sont en cycle (noir sur vert, vert sur rouge, rouge sur noir) et tiennent ; le quatrieme, pose dessus, s'enleve sans les liberer.
Le panneau b est aussi enregistre seul pour etre relu par lire_figure.py et calcule.
Usage : python fig_impossible_chaines.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = r"../figures/"
COL = {"noir": "#1e191e", "vert": "#3cb44b", "rouge": "#eb1e28", "bleu": "#3c87c8"}
t = np.radians(np.linspace(0, 360, 500))
def cercle(c, r=1.0): return c[0] + r * np.cos(t), c[1] + r * np.sin(t)
def pose(ax, xy, coul, lw, z):                                   # un rond pose sur ce qui est deja dessine
    ax.plot(*xy, color="white", lw=lw * 3.0, zorder=z); ax.plot(*xy, color=coul, lw=lw, zorder=z + 1)
def repasse(ax, xy, pts, coul, lw, z, rayon=0.17):                # ce rond repasse dessus pres des points donnes
    x, y = xy
    for p in pts:
        idx = np.nonzero((x - p[0]) ** 2 + (y - p[1]) ** 2 < rayon ** 2)[0]
        for g in np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1):
            if len(g): ax.plot(x[g], y[g], color="white", lw=lw * 3.0, solid_capstyle="butt", zorder=z); ax.plot(x[g], y[g], color=coul, lw=lw, solid_capstyle="butt", zorder=z + 1)
def inter(c1, c2, r1=1.0, r2=1.0):
    v = np.array(c2) - np.array(c1); L = np.linalg.norm(v); a = (r1 * r1 - r2 * r2 + L * L) / (2 * L); h = np.sqrt(max(r1 * r1 - a * a, 0)); m = np.array(c1) + a * v / L; w = np.array([-v[1], v[0]]) / L
    return [m + h * w, m - h * w]
def empiles(ax, lw=2.4):
    cen = [(-0.95, 0.35), (-0.32, -0.35), (0.32, 0.35), (0.95, -0.35)]
    for k, nom in list(enumerate(("noir", "vert", "rouge", "bleu")))[::-1]: pose(ax, cercle(cen[k]), COL[nom], lw, 2 * (4 - k))
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.9, 1.9)
def cycle(ax, lw=2.4):
    d = 0.62; cen = [d * np.array([np.cos(a), np.sin(a)]) for a in np.radians([90, 210, 330])]; cs = [cercle(c) for c in cen]
    pose(ax, cs[2], COL["rouge"], lw, 2); pose(ax, cs[1], COL["vert"], lw, 4); pose(ax, cs[0], COL["noir"], lw, 6)      # noir sur vert, vert sur rouge
    repasse(ax, cs[2], inter(cen[2], cen[0]), COL["rouge"], lw, 8)                                                      # et rouge sur noir
    pose(ax, cercle((0.0, -0.05), 1.28), COL["bleu"], lw, 12)                                                           # le quatrieme, pose sur les trois
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.9, 1.9)
if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
    empiles(axes[0]); axes[0].set_title("a. Quatre ronds empilés", fontsize=10)
    cycle(axes[1]); axes[1].set_title("b. Trois ronds en cycle, et un quatrième", fontsize=10)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_impossible_chaines." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
    for nom, f in (("a", empiles), ("b", cycle)):
        f2, ax = plt.subplots(figsize=(6, 6)); f(ax, lw=3.0); f2.savefig(OUT + f"fig_impossible_controle_{nom}.png", dpi=200)
