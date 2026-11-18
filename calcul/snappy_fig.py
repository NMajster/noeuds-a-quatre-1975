"""Calculs SnapPy / spherogram sur la figure III-2 extraite (pd.json).
Lancer avec : C:\\dev\\topologie-exposes\\python snappy_fig.py"""
import json, itertools, snappy, spherogram
D = json.load(open("pd.json"))
coul = {int(k): v for k, v in D["couleurs"].items()}

def rapport(nom, pd):
    print(f"\n######## {nom} ########")
    L = spherogram.Link(pd)
    print("composantes :", len(L.link_components), "; croisements :", len(L.crossings))
    print("matrice d'enlacement :", L.linking_matrix())
    # chaque composante seule
    for i in range(len(L.link_components)):
        K = L.sublink([i]); K.simplify("global")
        E = K.exterior()
        try:
            ident = E.identify()
        except Exception as e:
            ident = f"(identify: {e})"
        print(f"  composante {i} : {len(K.crossings)} croisements après simplification ; identification : {ident}")
    # entrelacs entier
    L2 = L.copy(); L2.simplify("global")
    parts = L2.split_link_diagram()
    print("entrelacs entier : croisements après simplification", len(L2.crossings), "; morceaux disjoints du diagramme simplifié :", len(parts))
    M = L2.exterior()
    print("  extérieur : volume", M.volume(), "; type de solution :", M.solution_type())
    try:
        print("  identification :", M.identify())
    except Exception as e:
        print("  identification :", e)
    # sous-entrelacs de trois ronds
    for X in range(len(L.link_components)):
        S = [i for i in range(len(L.link_components)) if i != X]
        T = L.sublink(S); T.simplify("global")
        parts = T.split_link_diagram()
        print(f"  sans la composante {X} : croisements après simplification {len(T.crossings)} ; morceaux disjoints : {len(parts)} ; tailles {[len(p.crossings) for p in parts]}")
    return L

for nom in ("pd", "pd_noir_corrige"):
    rapport(nom, D[nom])
