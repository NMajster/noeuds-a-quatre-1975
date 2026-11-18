"""Le motif general F pour cinq ronds : s1 s3 s5 s7 s9 . C5, C5 = commutateur itere des tours du brin 3 autour des brins 2, 5, 7, 9."""
import motif_bandes as B
C5 = B.comm(B.C4, B.A(3, 9)); w = [1, 3, 5, 7, 9] + C5
print("croisements par tour :", len(w), flush=True)
for k in (1, 3): B.rapport("F n=5", 10, w, k)
