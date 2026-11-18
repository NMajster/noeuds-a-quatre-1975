"""Figure : la meme regle sur trois ronds et sur trois trefles.
a. Le noeud borromeen ordinaire : le noir passe sur le vert, le vert sur le rouge, le rouge sur le noir.
b. Les trois trefles de Lacan (dessin 1 de Soury), referme en rond : meme regle.
Le panneau b est trace a partir du mot de tresse lu sur le dessin 1 de Soury (calcul/soury3/dessin1.json), enroule sur un tour.
Il est aussi enregistre seul (controle) pour etre relu par lire_figure.py et calcule.

Usage : python fig_ronds_trefles.py
"""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = r"../figures/"
COL = ["#1e191e", "#3cb44b", "#eb1e28"]            # noir, vert, rouge : le premier passe sur le deuxieme, etc.
mot = [tuple(x) for x in json.load(open(r"soury3/dessin1.json"))["mot"]]
NB = 6
def niveaux(mot):
    h = [0] * NB; L = []
    for i, d in mot:
        n = max(h[i], h[i + 1]); L.append(n); h[i] = h[i + 1] = n + 1
    return L, max(h)
NIV, H = niveaux(mot)
def trefles(ax, lw=2.0, r0=0.75, dr=0.26):
    """Tresse du dessin 1 repetee trois fois et enroulee : rayon = rang du brin, angle = niveau (sens des aiguilles d'une montre)."""
    tot = 3 * H; u = np.linspace(0, 1, 40); s = (1 - np.cos(np.pi * u)) / 2
    def P(pos, niv):
        r = r0 + dr * np.asarray(pos, float); th = np.pi / 2 - 2 * np.pi * np.asarray(niv, float) / tot
        return r * np.cos(th), r * np.sin(th)
    rond = [min(k, NB - 1 - k) for k in range(NB)]; occ = {(n, i): d for (i, d), n in zip(mot, NIV)}
    for rep in range(3):
        for n in range(H):
            y0 = rep * H + n; pris = set()
            for i in range(NB - 1):
                if (n, i) in occ:
                    d = occ[(n, i)]; pris |= {i, i + 1}
                    g = (i + s, y0 + u, rond[i]); dr_ = (i + 1 - s, y0 + u, rond[i + 1])
                    dessus, dessous = (g, dr_) if d == "G" else (dr_, g)
                    ax.plot(*P(dessous[0], dessous[1]), color=COL[dessous[2]], lw=lw, solid_capstyle="butt", zorder=2)
                    m = slice(11, 29)
                    ax.plot(*P(dessus[0][m], dessus[1][m]), color="white", lw=lw * 3.2, solid_capstyle="butt", zorder=3)
                    ax.plot(*P(dessus[0], dessus[1]), color=COL[dessus[2]], lw=lw, solid_capstyle="butt", zorder=4)
                    rond[i], rond[i + 1] = rond[i + 1], rond[i]
            for i in range(NB):
                if i not in pris: ax.plot(*P(i + 0 * u, y0 - 0.02 + 1.04 * u), color=COL[rond[i]], lw=lw, solid_capstyle="butt", zorder=2)
    ax.set_aspect("equal"); ax.axis("off"); R = r0 + dr * (NB - 1) + 0.15; ax.set_xlim(-R, R); ax.set_ylim(-R, R)
def ronds(ax, lw=2.4):
    d = 0.62; cen = [d * np.array([np.cos(a), np.sin(a)]) for a in np.radians([90, 210, 330])]; t = np.radians(np.linspace(0, 360, 400))
    cs = [(c[0] + np.cos(t), c[1] + np.sin(t)) for c in cen]
    for k in (2, 1, 0):                                                              # rouge, puis vert dessus, puis noir dessus : noir sur vert, vert sur rouge
        ax.plot(*cs[k], color="white", lw=lw * 3.0, zorder=2 * (2 - k)); ax.plot(*cs[k], color=COL[k], lw=lw, zorder=2 * (2 - k) + 1)
    def inter(c1, c2):
        v = c2 - c1; L = np.linalg.norm(v); m = (c1 + c2) / 2; h = np.sqrt(1 - L * L / 4); w = np.array([-v[1], v[0]]) / L; return [m + h * w, m - h * w]
    for p in inter(cen[2], cen[0]):                                                  # et le rouge sur le noir
        x, y = cs[2]; msk = (x - p[0]) ** 2 + (y - p[1]) ** 2 < 0.16 ** 2; idx = np.nonzero(msk)[0]
        for g in np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1):
            ax.plot(x[g], y[g], color="white", lw=lw * 3.0, solid_capstyle="butt", zorder=8); ax.plot(x[g], y[g], color=COL[2], lw=lw, solid_capstyle="butt", zorder=9)
    for k, c in enumerate(cen):
        for p in inter(c, cen[(k + 1) % 3]):
            pass
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.75, 1.75)
if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.1), gridspec_kw={"width_ratios": [1, 1.3]})
    ronds(axes[0]); axes[0].set_title("a. Trois ronds", fontsize=10)
    trefles(axes[1], lw=1.7); axes[1].set_title("b. Trois trèfles", fontsize=10)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_ronds_trefles." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
    f2, ax = plt.subplots(figsize=(7, 7)); trefles(ax, lw=2.6); f2.savefig(OUT + "fig_ronds_trefles_controle.png", dpi=200)
    f3, ax = plt.subplots(figsize=(5, 5)); ronds(ax, lw=3.0); f3.savefig(OUT + "fig_ronds_controle.png", dpi=200)
    print("niveaux par periode :", H)
