"""Parmi les 84 inversions possibles d'un seul croisement du dessin imprime, lesquelles donnent un dessin qui se repete trois fois ?
Usage : python periode_unicite.py"""
import json
import periode as P
D = json.load(open(r"pd.json")); PD = [tuple(x) for x in D["pd"]]; CC = D["comp_croisements"]; coul = D["couleurs"]
bons = []
for c in range(len(PD)):
    Q = list(PD); a, b, cc, d = Q[c]; Q[c] = (b, cc, d, a)        # le brin dessus passe dessous
    A = P.automorphismes(Q)
    if any(P.ordre(f) == 3 for f in A): bons.append(c)
print("dessin imprime : automorphismes", len(P.automorphismes(PD)))
print("inversions d'un seul croisement qui retablissent la repetition par trois :", bons, [(coul[str(CC[c][0])], coul[str(CC[c][1])]) for c in bons])
print("le croisement rectifie dans l'etude est le numero 25 :", bons == [25])
