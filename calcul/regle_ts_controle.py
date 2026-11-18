"""Les solutions trouvees dans la disposition de Thome et Soury : sont-elles la figure rectifiee ? tiennent-elles (comptage exact) ?
Usage : python regle_ts_controle.py   (apres regle_dispositions.py TS)"""
import io, json, snappy, spherogram
src = io.open("coloriages_inv.py", encoding="utf-8").read(); exec(src.split("\nfor ", 1)[0].split("\nTESTS", 1)[0].split("\nCLASSES", 1)[0])
Tb = table(classe_transpositions(4))
B = json.load(open("regle_dispositions_TS.json"))
REF = spherogram.Link([tuple(x) for x in json.load(open("pd.json"))["pd_noir_corrige"]]).exterior()
M0 = json.load(open("motif_tresse.json")); ref_mot = [(i + 1) * (1 if d == "G" else -1) for i, d in M0["mot"]]
noms = ["noir", "brun", "rouge", "vert"]
for b in B:
    w = b["mot"] * 3; L = spherogram.Link(braid_closure=w); M = L.exterior(); rep = "?"
    for e in range(6):
        try: rep = M.is_isometric_to(REF); break
        except Exception: M.randomize()
    c = compte([tuple(x) for x in L.PD_code()], Tb)[0]
    g = {k: noms[v] for k, v in b["gagne"].items()}
    print("alternance", b["bits"], "| dessus :", g, "| motif identique a celui de la figure :", b["mot"] == ref_mot, "| meme entrelacs :", rep, "| volume %.4f" % float(M.volume()), "| coloriages", c, "(810000 si separes)", flush=True)
