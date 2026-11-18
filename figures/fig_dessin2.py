"""Figure : les deux noeuds de trois trefles de Soury, refermes en rond. a. dessin 1 (45 croisements). b. dessin 2 (33 croisements).
Meme regle dans les deux : le noir passe sur le vert, le vert sur le rouge, le rouge sur le noir.
Usage : python fig_dessin2.py"""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = r"../figures/"; COL = ["#1e191e", "#3cb44b", "#eb1e28"]; NB = 6
def charge(nom): return [tuple(x) for x in json.load(open(rf"soury3/{nom}.json"))["mot"]]
def ronds_de(mot):
    pos = list(range(NB))
    for _ in range(3):
        for i, d in mot: pos[i], pos[i + 1] = pos[i + 1], pos[i]
    arrive = {pos[r]: r for r in range(NB)}            # le brin parti du rang s arrive au rang arrive[s]
    rond = {}; k = 0
    for s in range(NB):
        if s in rond: continue
        x = s
        while x not in rond: rond[x] = k; x = arrive[x]
        k += 1
    return [rond[s] for s in range(NB)]
def trace(ax, mot, lw=1.7, r0=0.75, dr=0.26):
    h = [0] * NB; NIV = []
    for i, d in mot:
        n = max(h[i], h[i + 1]); NIV.append(n); h[i] = h[i + 1] = n + 1
    H = max(h); tot = 3 * H; u = np.linspace(0, 1, 40); s = (1 - np.cos(np.pi * u)) / 2
    def P(pos, niv):
        r = r0 + dr * np.asarray(pos, float); th = np.pi / 2 - 2 * np.pi * np.asarray(niv, float) / tot; return r * np.cos(th), r * np.sin(th)
    rond = ronds_de(mot); occ = {(n, i): d for (i, d), n in zip(mot, NIV)}
    for rep in range(3):
        for n in range(H):
            y0 = rep * H + n; pris = set()
            for i in range(NB - 1):
                if (n, i) in occ:
                    d = occ[(n, i)]; pris |= {i, i + 1}
                    g = (i + s, y0 + u, rond[i]); dr_ = (i + 1 - s, y0 + u, rond[i + 1]); dessus, dessous = (g, dr_) if d == "G" else (dr_, g)
                    ax.plot(*P(dessous[0], dessous[1]), color=COL[dessous[2]], lw=lw, solid_capstyle="butt", zorder=2)
                    m = slice(11, 29)
                    ax.plot(*P(dessus[0][m], dessus[1][m]), color="white", lw=lw * 3.2, solid_capstyle="butt", zorder=3)
                    ax.plot(*P(dessus[0], dessus[1]), color=COL[dessus[2]], lw=lw, solid_capstyle="butt", zorder=4)
                    rond[i], rond[i + 1] = rond[i + 1], rond[i]
            for i in range(NB):
                if i not in pris: ax.plot(*P(i + 0 * u, y0 - 0.02 + 1.04 * u), color=COL[rond[i]], lw=lw, solid_capstyle="butt", zorder=2)
    ax.set_aspect("equal"); ax.axis("off"); R = r0 + dr * (NB - 1) + 0.15; ax.set_xlim(-R, R); ax.set_ylim(-R, R)
if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.8))
    trace(axes[0], charge("dessin1")); axes[0].set_title("a. Dessin 1 : 45 croisements", fontsize=10)
    trace(axes[1], charge("dessin2")); axes[1].set_title("b. Dessin 2 : 33 croisements", fontsize=10)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_deux_noeuds_de_trois_trefles." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
    f2, ax = plt.subplots(figsize=(7, 7)); trace(ax, charge("dessin2"), lw=2.6); f2.savefig(OUT + "fig_dessin2_controle.png", dpi=200)
