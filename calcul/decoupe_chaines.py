"""Une chaine borromeenne de ronds ordinaires se laisse-t-elle decouper en morceaux par des tores ? Quels ronds vont ensemble ?
On cherche les tores incompressibles (surfaces normales de SnapPy), on decoupe, et on identifie chaque morceau.
Usage : python decoupe_chaines.py"""
import snappy, spherogram, json
def inv(w): return [-x for x in reversed(w)]
def comm(a, b): return a + b + inv(a) + inv(b)
def A(i, j):
    up = list(range(j - 1, i, -1)); return up + [i, i] + inv(up)
def decrit(nom, L):
    M = L.exterior(); print(nom, "| composantes", M.num_cusps(), "| volume %.4f" % float(M.volume()), M.solution_type(), flush=True)
    try: S = M.splitting_surfaces()
    except Exception as e: print("   surfaces de decoupe : non calculables (", e, ")"); return
    print("   tores de decoupe trouves :", len(S))
    for k, s in enumerate(S):
        try:
            P = M.split(s)
            for p in P:
                Q = snappy.Manifold(p); 
                for e in range(6):
                    if Q.solution_type() == "all tetrahedra positively oriented": break
                    Q.randomize()
                try: idt = [str(x) for x in Q.identify()][:3]
                except Exception: idt = []
                print(f"      tore {k} : morceau a {Q.num_cusps()} bords, volume {float(Q.volume()):.4f}, {Q.solution_type()[:28]}, {idt}")
        except Exception as e: print("      tore", k, ": decoupe impossible :", e)
decrit("anneaux borromeens", spherogram.Link(braid_closure=[1, -2] * 3))
decrit("chaine de quatre ronds", spherogram.Link(braid_closure=comm(comm(A(1, 2), A(2, 3)), A(3, 4))))
decrit("chaine de cinq ronds", spherogram.Link(braid_closure=comm(comm(comm(A(1, 2), A(2, 3)), A(3, 4)), A(4, 5))))
D = json.load(open("pd.json")); decrit("quatre trefles de Thome et Soury", spherogram.Link([tuple(x) for x in D["pd_noir_corrige"]]))
