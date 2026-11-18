"""Controle de deux affirmations du rapport de contre-lecture (Astra, 18/11/2026).
1. Contre-exemple : la tresse s1 . u . s3 . u^-1 avec u = (2, -1, -1, 3, 3, -2) donne deux cercles non noues, d'enlacement nul, non separes.
2. Famille F : dimension de l'espace des coloriages de Fox modulo 3 pour n = 3 a 6, contre 2n pour n trefles separes.
Usage : python controle_astra.py"""
import io, contextlib, snappy, spherogram
src = io.open("coloriages.py", encoding="utf-8").read(); exec(src[:src.index("PRIMES = [")] + "PRIMES = [3]\n" + src[src.index("def nullite"):].split("\nD = json", 1)[0].split("\nif __name__", 1)[0].split("\ndata = ", 1)[0])
def inv(w): return [-x for x in reversed(w)]
u = [2, -1, -1, 3, 3, -2]; w = [1] + u + [3] + inv(u); L = spherogram.Link(braid_closure=w)
K = L.copy(); K.simplify("global")
print("contre-exemple : composantes", len(L.link_components), "| enlacement", L.linking_matrix()[0][1], "| chaque rond seul :", [len((lambda k: (k.simplify('global'), k)[1])(L.sublink([i])).crossings) for i in range(2)],
      "| croisements du tout apres simplification :", len(K.crossings), "| nullite de Fox mod 3 :", nullite([tuple(x) for x in L.PD_code()], 3), "(2 pour deux cercles separes)")
import motif_bandes as B
with contextlib.redirect_stdout(io.StringIO()): pass
C = B.C3; mots = {3: [1, 3, 5] + B.C3, 4: [1, 3, 5, 7] + B.C4}
C5 = B.comm(B.C4, B.A(3, 9)); mots[5] = [1, 3, 5, 7, 9] + C5
C6 = B.comm(C5, B.A(3, 11)); mots[6] = [1, 3, 5, 7, 9, 11] + C6
for n, w in mots.items():
    L = spherogram.Link(braid_closure=w * 3)
    print("famille F, n =", n, ": croisements par tour", len(w), "| composantes", len(L.link_components), "| nullite de Fox mod 3 :", nullite([tuple(x) for x in L.PD_code()], 3), "| pour n trefles separes :", 2 * n, flush=True)
