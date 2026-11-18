"""Les quatre cas de base (deux ecritures, deux sens du cycle) : comptage exact des coloriages par les transpositions de S4."""
import io, sys, contextlib, spherogram
src = io.open("coloriages_inv.py", encoding="utf-8").read()
exec(src.split("\nfor ", 1)[0].split("\nTESTS", 1)[0].split("\nCLASSES", 1)[0])
sys.argv = ["x", "3"]
with contextlib.redirect_stdout(io.StringIO()): import lacan_quatre as Q
Tb = table(classe_transpositions(4))
for g in ((1, 2, 1), (2, 1, 2)):
    for vals in ((True, False, True), (False, True, False)):
        L = spherogram.Link(braid_closure=Q.mot_emboite(g, dict(zip(Q.paires, vals))))
        c = compte([tuple(x) for x in L.PD_code()], Tb)[0]
        print("ecriture", g, "cycle", vals, ": coloriages", c, "(trois trefles separes : 27000) ->", "tient a trois, exact" if c != 27000 else "ne tranche pas")
