"""Certification de la non-séparabilité (structure hyperbolique) pour les deux versions de la figure.
Un extérieur d'entrelacs hyperbolique est irréductible : l'entrelacs n'est pas scindé."""
import json, snappy, spherogram
D = json.load(open("pd.json"))
for nom in ("pd", "pd_noir_corrige"):
    L = spherogram.Link(D[nom]); L.simplify("global")
    M = L.exterior()
    ok = M.solution_type() == "all tetrahedra positively oriented"
    essais = 0
    while not ok and essais < 200:
        M.randomize(); essais += 1
        ok = M.solution_type() == "all tetrahedra positively oriented"
    print(f"\n{nom} : {len(L.crossings)} croisements ; tétraèdres {M.num_tetrahedra()} ; solution {M.solution_type()} après {essais} randomisations ; volume {M.volume()}")
    try:
        r = M.verify_hyperbolicity()
        print("  verify_hyperbolicity :", r[0] if isinstance(r, tuple) else r)
    except Exception as e:
        print("  verify_hyperbolicity indisponible ou échec :", type(e).__name__, str(e)[:200])
    print("  homologie :", M.homology(), "; nombre de pointes :", M.num_cusps())
