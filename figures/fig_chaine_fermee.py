"""Figure : la chaine refermee de 1973. Les deux ronds simples des bouts sont reunis en un seul, qui fait le tour de la chaine
et prend les quatre oreilles (« de quatre a un »). Courbes de l'espace ; le code PD est controle par SnapPy.
Usage : python fig_chaine_fermee.py"""
import io, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ns = {}
src = io.open(r"../figures/fig_chaine_1973.py", encoding="utf-8").read(); exec(src.split('if __name__ == "__main__":')[0], ns)
plie, vue, dessine, ferme, OUT, COL = ns["plie"], ns["vue"], ns["dessine"], ns["ferme"], ns["OUT"], ns["COL"]
B = plie(-0.9, 0.7, 0.55, 0.22); C = plie(1.40, 3.0, 0.22, 0.55); R0 = 1.1
ca, cd = -0.9 - R0, 3.0 + R0                                   # centres des deux anciens ronds des bouts
P = []
for a in np.radians(np.linspace(0, 165, 12)): P.append((ca + R0 * np.cos(a), R0 * np.sin(a), 0))              # demi-rond de gauche, cote y > 0
P += [(-3.55, 1.25, 0.0), (-2.6, 2.55, 0.05), (-0.5, 3.0, 0.2), (2.0, 3.0, 0.5), (4.3, 2.6, 0.9), (5.45, 1.5, 1.0), (5.55, 0.5, 0.75)]
for a in np.radians(np.linspace(20, 340, 22)): P.append((cd + R0 * np.cos(a), 0, R0 * np.sin(a)))              # rond de droite, de haut en bas par le brin qui prend les oreilles
P += [(5.55, -0.5, -0.75), (5.45, -1.5, -1.0), (4.3, -2.6, -0.9), (2.0, -3.0, -0.5), (-0.5, -3.0, -0.2), (-2.6, -2.55, -0.05), (-3.55, -1.25, 0.0)]
for a in np.radians(np.linspace(195, 345, 11)): P.append((ca + R0 * np.cos(a), R0 * np.sin(a), 0))             # demi-rond de gauche, cote y < 0
E = ferme(P)
if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    R = [vue(X) for X in (E, B, C)]; pd, vr, nx = dessine(ax, R, [COL[0], COL[1], COL[2]], lw=2.0, trou=0.10)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_chaine_fermee." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
    json.dump({"fermee": {"pd": pd, "croisements": nx}}, open(OUT + "codes_pd_chaine_fermee.json", "w")); print("croisements :", nx)
    # figure reunie : la chaine ouverte a quatre ronds, puis la chaine refermee
    A, Dd = ns["A"], ns["Dd"]
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 5.6), gridspec_kw={"height_ratios": [1, 1.45]})
    dessine(axes[0], [vue(X) for X in (A, B, C, Dd)], COL, lw=2.0, trou=0.10, titre="a. La chaîne ouverte : un rond, deux ronds pliés, un rond")
    dessine(axes[1], [vue(X) for X in (E, B, C)], [COL[0], COL[1], COL[2]], lw=2.0, trou=0.10, titre="b. La chaîne refermée : un seul rond prend les quatre oreilles")
    axes[0].set_xlim(-4.2, 6.3); axes[1].set_xlim(-4.2, 6.3)
    fig.tight_layout()
    for ext in ("png", "svg", "pdf"): fig.savefig(OUT + "fig_chaines_1973." + ext, dpi=300, bbox_inches="tight", pad_inches=0.05)
