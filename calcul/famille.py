"""La famille obtenue en repetant k fois le motif d'une periode (periode.json, produit par periode.py).
Pour chaque k : composantes, nature de chaque rond, enlacements, separation quand on retire un rond, tenue de l'ensemble.

Usage : python famille.py
"""
import json, snappy, spherogram
D = json.load(open(r"periode.json"))["pd_noir_corrige"]
REF = spherogram.Link([tuple(x) for x in json.load(open(r"pd.json"))["pd_noir_corrige"]])
def nom(K):
    K = K.copy(); K.simplify("global"); n = len(K.crossings)
    if n == 0: return "rond non noue (0 croisement)"
    try: idt = [str(x) for x in K.exterior().identify()][:2]
    except Exception as e: idt = ["?"]
    return f"{n} croisements apres simplification {idt}"
for k in (1, 2, 3, 4, 5, 7):
    L = spherogram.Link([tuple(x) for x in D["pd_k%d" % k]]); nc = len(L.link_components)
    print(f"\n===== motif repete {k} fois : {len(L.crossings)} croisements, {nc} composantes =====")
    lm = L.linking_matrix(); print("enlacements tous nuls :", all(lm[i][j] == 0 for i in range(nc) for j in range(nc) if i != j), lm if nc <= 4 else "")
    for i in range(nc): print("  rond", i, ":", nom(L.sublink([i])))
    if nc == 4:
        for X in range(4):
            T = L.sublink([i for i in range(4) if i != X]); T.simplify("global"); parts = T.split_link_diagram()
            print(f"  sans le rond {X} : {len(T.crossings)} croisements, morceaux disjoints {len(parts)}, tailles {[len(p.crossings) for p in parts]}")
        L2 = L.copy(); L2.simplify("global"); parts = L2.split_link_diagram()
        M = L2.exterior()
        for essai in range(6):
            if M.solution_type() == "all tetrahedra positively oriented": break
            M.randomize()
        print(f"  ensemble : {len(L2.crossings)} croisements apres simplification, morceaux {len(parts)} ; {M.solution_type()} ; volume {M.volume()}")
        if k == 3:
            print("  meme entrelacs que la figure rectifiee (isometrie des complementaires) :", M.is_isometric_to(REF.exterior()))
        try: print("  identification :", M.identify()[:3])
        except Exception as e: print("  identification : -")
