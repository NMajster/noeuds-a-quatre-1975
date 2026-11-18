"""Figure : la premiere construction de Lacan (Encore, 15 mai 1973). Une chaine de ronds plies : un rond simple, un rond passe
dedans et plie (il presente deux oreilles de chaque cote), un autre rond plie, et un dernier rond simple qui prend les deux oreilles.
Les ronds sont des courbes de l'espace ; le dessus/dessous du dessin vient de leur hauteur. Le meme calcul donne le code PD,
controle par SnapPy (controle_chaine_1973.py).
Usage : python fig_chaine_1973.py"""
import io, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
src = io.open(r"../figures/fig_simples.py", encoding="utf-8").read(); exec(src[:src.index("codes = {}")])
def plie(xl, xr, w, h, n=1200):
    """Rond plie : il suit les quatre aretes longues d'une boite ; demi-tours a gauche dans les plans y = +-w, a droite dans les plans z = +-h."""
    s = np.linspace(0, np.pi, 80); P = []
    def droit(a, b): return [np.array(a) + (np.array(b) - np.array(a)) * u for u in np.linspace(0, 1, 60, endpoint=False)]
    P += droit((xr, w, h), (xl, w, h)); P += [np.array((xl - h * np.sin(x), w, h * np.cos(x))) for x in s[:-1]]
    P += droit((xl, w, -h), (xr, w, -h)); P += [np.array((xr + w * np.sin(x), w * np.cos(x), -h)) for x in s[:-1]]
    P += droit((xr, -w, -h), (xl, -w, -h)); P += [np.array((xl - h * np.sin(x), -w, -h * np.cos(x))) for x in s[:-1]]
    P += droit((xl, -w, h), (xr, -w, h)); P += [np.array((xr + w * np.sin(x), -w * np.cos(x), h)) for x in s[:-1]]
    P = np.array(P); d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.vstack([P, P[:1]]), axis=0), axis=1))]
    u = np.linspace(0, d[-1], n, endpoint=False) + 0.0137; Q = np.vstack([P, P[:1]])
    return np.stack([np.interp(u, d, Q[:, k]) for k in range(3)], 1)
def rond_xy(cx, R, n=1200):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False) + 0.0031; return np.stack([cx + R * np.cos(a), R * np.sin(a), 0 * a], 1)
def rond_xz(cx, R, n=1200):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False) + 0.0031; return np.stack([cx + R * np.cos(a), 0 * a, R * np.sin(a)], 1)
def vue(P, phi=52, psi=9):
    f, g = np.radians(phi), np.radians(psi); x, y, z = P[:, 0], P[:, 1], P[:, 2]
    y, z = y * np.cos(f) - z * np.sin(f), y * np.sin(f) + z * np.cos(f)
    x, z = x * np.cos(g) + z * np.sin(g), -x * np.sin(g) + z * np.cos(g)
    return np.stack([x, y, z], 1)
from scipy.interpolate import splprep, splev
def ferme(points, n=1200):
    """Courbe fermee lisse passant par les points donnes."""
    P = np.array(points, float); tck, u = splprep([P[:, 0], P[:, 1], P[:, 2]], s=0, per=True, k=3)
    x, y, z = splev(np.linspace(0, 1, n, endpoint=False) + 0.00041, tck); return np.stack([x, y, z], 1)
R0 = 1.1
A = rond_xy(-0.9 - R0, R0); B = plie(-0.9, 0.7, 0.55, 0.22); C = plie(1.40, 3.0, 0.22, 0.55); Dd = rond_xz(3.0 + R0, R0)
# chaine refermee : un seul rond prend les deux oreilles de gauche du premier rond plie et les deux oreilles de droite du second
E = ferme([(-0.93, -1.0, 0), (-0.93, -0.5, 0), (-0.93, 0, 0), (-0.93, 0.5, 0), (-0.93, 1.0, 0), (-0.6, 1.9, 0.5), (0.6, 2.5, 1.3), (2.0, 2.1, 1.9), (2.9, 1.0, 1.9),
           (3.03, 0.25, 1.4), (3.03, 0, 0.8), (3.03, 0, 0.3), (3.03, 0, -0.3), (3.03, 0, -0.8), (3.03, -0.25, -1.4), (2.9, -1.0, -1.9), (2.0, -2.1, -1.9), (0.6, -2.5, -1.3), (-0.6, -1.9, -0.5), (-0.93, -1.0, 0)][:-1])
COL = ["#1e191e", "#3c87c8", "#3cb44b", "#eb1e28"]
D3 = rond_xz(0.7 + 0.08 + R0, R0)
if __name__ == "__main__":
    codes = {}
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 4.6))
    for ax, (cle, ronds, cols, titre) in zip(axes, [("trois", [A, B, D3], [COL[0], COL[1], COL[3]], "a. Trois ronds : un rond, un rond plié, un rond"),
                                                    ("ouverte", [A, B, C, Dd], COL, "b. Quatre ronds : un rond, deux ronds pliés, un rond")]):
        Rr = [vue(P) for P in ronds]; pd, vr, nx = dessine(ax, Rr, cols, lw=2.0, trou=0.10, titre=titre); codes[cle] = {"pd": pd, "croisements": nx}
        ax.set_xlim(-3.4, 5.6)
    Rr = [vue(P) for P in [E, B, C]]; f2, ax2 = plt.subplots(); pd, vr, nx = dessine(ax2, Rr, COL[:3]); codes["fermee"] = {"pd": pd, "croisements": nx}; plt.close(f2)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_chaine_1973." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
    json.dump(codes, open(OUT + "codes_pd_chaine_1973.json", "w"))
