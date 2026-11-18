"""Le noeud de trois trefles selon la regle de Lacan (disposition emboitee) : est-ce celui des dessins 0 et 1 de Soury ?
tient-il a trois (preuve exacte par comptage de coloriages) ?
Usage : python lacan_trois_preuve.py"""
import io, sys, json, snappy, spherogram
src = io.open("coloriages_inv.py", encoding="utf-8").read()
exec(src[:src.index("\n", src.index("def compte"))].rsplit("def compte", 1)[0] + "def compte" + src.split("def compte", 1)[1].split("\nfor ", 1)[0].split("\nTESTS", 1)[0].split("\nCLASSES", 1)[0])
sys.argv = ["x", "3"]
import contextlib
with contextlib.redirect_stdout(io.StringIO()): import lacan_quatre as Q
T = dict(zip(Q.paires, (True, False, True)))
for g in ((1, 2, 1), (2, 1, 2)):
    w = Q.mot_emboite(g, T); L = spherogram.Link(braid_closure=w); pd = [tuple(x) for x in L.PD_code()]
    M = L.exterior()
    for nom in ("dessin0", "dessin1"):
        D = json.load(open(f"soury3/{nom}.json")); ws = [(i + 1) * (1 if dd == "G" else -1) for i, dd in D["mot"]] * 3
        R = spherogram.Link(braid_closure=ws).exterior(); rep = "?"
        for essai in range(6):
            try: rep = M.is_isometric_to(R); break
            except Exception: M.randomize(); R.randomize()
        print("regle de Lacan, ecriture", g, ": meme entrelacs que le", nom, "de Soury :", rep, "| volumes", round(float(M.volume()), 4), round(float(R.volume()), 4))
    tr = [tuple(x) for x in spherogram.Link(braid_closure=[1, 1, 1]).PD_code()]
    for nomc, cl in (("transpositions de S3", classe_transpositions(3)), ("transpositions de S4", classe_transpositions(4))):
        Tb = table(cl); c3 = compte(tr, Tb); c = compte(pd, Tb)
        if isinstance(c, tuple): c3, c = c3[0], c[0]
        print(f"   coloriages par les {nomc} : un trefle {c3} ; trois trefles separes {c3 ** 3} ; ce noeud {c} ->", "ne se separe pas (exact)" if c != c3 ** 3 else "ne tranche pas")
