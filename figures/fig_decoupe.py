"""Figure : le noeud a quatre ronds se decoupe en deux noeuds a trois.
a. Un noeud borromeen a trois : I, R et un troisieme rond, dessine epais.
b. Le troisieme rond est une chambre a air (un tube) : elle contient le sinthome et S, accroches l'un a l'autre aux deux bouts.
Le dessin b, sans le tube, est aussi enregistre seul (controle) pour etre relu par lire_figure.py et calcule.

Usage : python fig_decoupe.py [variante]     variante = 0 ou 1 (sens de l'accrochage du bas)
"""
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
OUT = r"../figures/"
VAR = int(sys.argv[1]) if len(sys.argv) > 1 else 0
COL = {"I": "#1e191e", "R": "#3c87c8", "X": "#3cb44b", "Y": "#eb1e28"}      # noir, bleu, vert (sinthome), rouge (S)
d = 0.62; cen = {k: d * np.array([np.cos(a), np.sin(a)]) for k, a in zip("ABC", np.radians([90, 210, 330]))}
def cercle(c, r=1.0, a0=0, a1=360, n=400):
    t = np.radians(np.linspace(a0, a1, n)); return c[0] + r * np.cos(t), c[1] + r * np.sin(t)
def inter(c1, c2, r=1.0):
    v = c2 - c1; L = np.linalg.norm(v); m = (c1 + c2) / 2; h = np.sqrt(r * r - L * L / 4); u = np.array([-v[1], v[0]]) / L
    return [m + h * u, m - h * u]
def boucle(c, r_in, r_out, a0, a1, n=300):
    """Boucle allongee : arc exterieur de a0 a a1, calotte au-dela de a1, arc interieur de a1 a a0, calotte en deca de a0."""
    t = np.radians(np.linspace(a0, a1, n)); rm, rc = (r_in + r_out) / 2, (r_out - r_in) / 2; s = np.linspace(0, np.pi, 40)
    def pol(r, ang): return c[0] + r * np.cos(ang), c[1] + r * np.sin(ang)
    xo, yo = pol(r_out, t); xi, yi = pol(r_in, t[::-1])
    c1 = np.array(pol(rm, np.radians(a1))); c0 = np.array(pol(rm, np.radians(a0)))
    x1, y1 = c1[0] + rc * np.cos(np.radians(a1) + s), c1[1] + rc * np.sin(np.radians(a1) + s)
    x0, y0 = c0[0] + rc * np.cos(np.radians(a0) + np.pi + s), c0[1] + rc * np.sin(np.radians(a0) + np.pi + s)
    return np.concatenate([xo, x1, xi, x0, xo[:1]]), np.concatenate([yo, y1, yi, y0, yo[:1]])
def pres(ax, xy, pt, coul, lw, rayon=0.085, z=10):
    """Redessine, avec un liseré blanc, le morceau de la courbe xy qui passe pres du point pt (ce brin passe dessus)."""
    x, y = xy; m = (x - pt[0]) ** 2 + (y - pt[1]) ** 2 < rayon ** 2
    idx = np.nonzero(m)[0]
    if len(idx) == 0: return
    for g in np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1):
        ax.plot(x[g], y[g], color="white", lw=lw * 3.0, solid_capstyle="butt", zorder=z); ax.plot(x[g], y[g], color=coul, lw=lw, solid_capstyle="butt", zorder=z + 1)
def dessus(ax, xy, coul, lw, z):
    ax.plot(*xy, color="white", lw=lw * 3.0, solid_capstyle="butt", zorder=z); ax.plot(*xy, color=coul, lw=lw, solid_capstyle="butt", zorder=z + 1)
A, B, C = cen["A"], cen["B"], cen["C"]
ri, ro = 0.78, 1.22
def polar(c, r, a): return c + r * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
def panneau(ax, mode, lw=2.2, lwf=1.5):
    """mode : 'trois' (tube plein, sans contenu), 'quatre' (tube clair et son contenu), 'controle' (contenu seul)."""
    a = cercle(A); b = cercle(B)
    ax.plot(*a, color=COL["I"], lw=lw, zorder=1)                                   # I dessous le tube
    if mode != "controle":
        t = np.radians(np.linspace(0, 360, 400)); ext = np.c_[C[0] + ro * np.cos(t), C[1] + ro * np.sin(t)]; itr = np.c_[C[0] + ri * np.cos(t[::-1]), C[1] + ri * np.sin(t[::-1])]
        ax.add_patch(Polygon(np.vstack([ext, itr]), closed=True, fc=("#bdbdbd" if mode == "trois" else "#eeeeee"), ec="none", zorder=2))
        for r in (ri, ro): ax.plot(*cercle(C, r), color="#8a8a8a", lw=0.8, zorder=3)
    if mode != "trois":
        X = boucle(C, 0.88, 1.04, 75, 285); Y = boucle(C, 0.96, 1.12, 255, 465)
        dessus(ax, X, COL["X"], lwf, 4)                                              # passent sur I
        dessus(ax, Y, COL["Y"], lwf, 6)                                              # Y sur X partout, puis on retablit X dessus ou il faut
        dg = np.degrees
        haut_calX = polar(C, 0.96, 75 - dg(0.08 / 0.96)); bas_calX = polar(C, 0.96, 285 + dg(0.08 / 0.96)); bas_calY = polar(C, 1.04, 255 - dg(0.08 / 1.04))
        pres(ax, X, haut_calX, COL["X"], lwf, rayon=0.045, z=8)                        # en haut : la calotte de X passe sur Y, la calotte de Y passe sur X
        pres(ax, X, bas_calX if VAR == 0 else bas_calY, COL["X"], lwf, rayon=0.045, z=8)
    # R passe sur le tube et son contenu
    if mode == "controle": dessus(ax, b, COL["R"], lw, 12)
    else:
        ax.plot(*b, color="white", lw=lw * 3.0, zorder=12) if mode != "trois" else None
        ax.plot(*b, color=COL["R"], lw=lw, zorder=13)
    # I passe sur R
    for p in inter(A, B): pres(ax, a, p, COL["I"], lw, rayon=0.16, z=14)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.75, 1.9); ax.set_ylim(-1.75, 1.75)
if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
    panneau(axes[0], "trois"); axes[0].set_title("a. Un nœud à trois", fontsize=10)
    panneau(axes[1], "quatre"); axes[1].set_title("b. Le troisième rond contient deux ronds", fontsize=10)
    axes[0].text(*(A + np.array([-1.12, 0.35])), "I", ha="center", fontsize=10); axes[0].text(*(B + np.array([-1.12, -0.2])), "R", ha="center", color=COL["R"], fontsize=10)
    axes[1].text(*(A + np.array([-1.12, 0.35])), "I", ha="center", fontsize=10); axes[1].text(*(B + np.array([-1.12, -0.2])), "R", ha="center", color=COL["R"], fontsize=10)
    axes[1].text(*(C + np.array([-0.40, -0.42])), "Σ", ha="center", va="center", color=COL["X"], fontsize=10); axes[1].text(*(C + np.array([1.36, 0.0])), "S", ha="center", va="center", color=COL["Y"], fontsize=10)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_decoupe." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
    f2, ax = plt.subplots(figsize=(6, 6)); panneau(ax, "controle", lw=3.0, lwf=2.2); f2.savefig(OUT + "fig_decoupe_controle.png", dpi=200)
