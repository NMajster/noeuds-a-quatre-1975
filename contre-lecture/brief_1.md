# Contre-lecture adverse : nœuds borroméens de trèfles (calculs du 18 novembre 2026)

## Ce qui vous est demandé

Vous êtes contre-lecteur en topologie des nœuds et des entrelacs. Votre tâche est de **chercher les erreurs** dans les énoncés ci-dessous, pas de les confirmer. Ils ont été produits en une journée par un autre modèle, avec SnapPy et des programmes écrits pour l'occasion, sans relecture. Ils doivent devenir le centre d'un article. Une erreur trouvée maintenant vaut mieux qu'une erreur publiée.

Concrètement :

1. **Recalculez par vos propres moyens** ce que vous pouvez, à partir des tresses données plus bas, sans vous servir de nos programmes. Si vous disposez d'un environnement d'exécution, utilisez SnapPy, Sage, KnotTheory ou votre propre code. Sinon, raisonnez à la main sur les cas qui s'y prêtent.
2. **Attaquez les raisonnements**, en particulier les sept points faibles signalés à la fin.
3. **Lisez les programmes** fournis en cherchant des fautes de convention, d'indice ou de logique.

Vous n'avez pas à commenter Lacan ni la psychanalyse, ni à réécrire quoi que ce soit.

## Contexte, en bref

En décembre 1975, Lacan dit avoir trouvé comment nouer « borroméennement » trois nœuds de trèfle, et avoir cherché en vain pendant deux mois à en nouer quatre. Michel Thomé et Pierre Soury lui apportent une figure de quatre trèfles. Soury a publié quatre dessins de tresses : les dessins 0, 1, 2 pour trois trèfles, le dessin 3 pour quatre.

**Définition utilisée partout.** Un entrelacs de n nœuds de trèfle est dit *borroméen* si, quel que soit le rond retiré, les n − 1 autres forment une réunion scindée de trèfles, et si l'entrelacs entier n'est pas scindé.

## Conventions

- Une tresse est une liste d'entiers. L'entier i désigne le générateur σ_i, l'entier −i son inverse. La convention de signe est celle de `spherogram.Link(braid_closure=...)`.
- « Répétée k fois » veut dire : le mot écrit k fois de suite, puis la fermeture usuelle de la tresse.
- Dans les programmes, « G » veut dire que le brin venu de la gauche passe dessus, et il est codé +i. « D » est codé −i. **Vérifiez que cette lecture est cohérente avec la convention de spherogram**, ou dites ce que change une inversion.
- Les comparaisons par `is_isometric_to` ne distinguent pas un entrelacs de son image en miroir.

## Les objets

**Motif TS** (figure de Thomé et Soury, huit brins, 28 croisements), tiré d'une image, voir point faible 1 :

```
[-2, -1, -4, -3, 2, 1, 5, 4, -3, 7, 6, -5, -4, 3, 2, 2, -1, -3, 5, 7, -6, -6, -5, 4, 3, 5, -7, -6]
```

Rond de chaque brin, par rang de départ, de gauche à droite : noir, brun, noir, rouge, brun, rouge, vert, vert.

**Dessins de Soury pour trois trèfles** (six brins), une période chacun, lus par programme sur des pages numérisées :

```
dessin 0 : [4, -2, -5, 3, 1, 4, -2, 1, -5, 3, -2, 4, -5, 1, 3]
dessin 1 : [1, -5, 4, -2, -5, 1, 3, 4, -2, 1, 3, -5, 4, -2, 3]
dessin 2 : [2, -4, 3, -2, 4, 1, -5, 3, -2, 4, 3]
```

**Disposition emboîtée à n ronds** (2n brins). L'ombre d'une période est celle du demi-tour de Garside : chaque brin croise chaque autre une fois. Elle est écrite en trois morceaux : un mot réduit g du demi-tour sur les brins 1 à n, son image par i → 2n − i sur les brins n + 1 à 2n, puis le tissage carré n × n écrit en losange. Le rond du brin de rang s (compté de 0) est min(s, 2n − 1 − s). Chaque rond se croise lui-même une fois par période, toujours avec le signe +.

**Règle constante.** Entre deux ronds distincts, l'un passe dessus à tous leurs croisements. Une règle constante sur n ronds est un tournoi.

**Disposition parallèle à n ronds** (2n brins). À chacune des trois étapes, le bloc des n brins de gauche croise le bloc des n brins de droite par un tissage n × n, sans demi-tour dans les blocs. Le rond d'un brin est son rang dans son bloc.

## Les énoncés à éprouver

Statut : **E** exact (simplification de diagramme aboutissant à un dessin scindé, identité combinatoire de diagrammes, ou invariant entier), **N** numérique (structure hyperbolique trouvée par SnapPy, non vérifiée par intervalles), **H** heuristique (un programme n'a pas réussi à simplifier, ce qui ne prouve rien).

### A. La figure de Thomé et Soury

- **A1 (E).** Le motif TS répété 3 fois donne quatre ronds, chacun un trèfle, d'enlacements deux à deux nuls. Tout triplet se simplifie en trois trèfles disjoints.
- **A2 (E).** L'entrelacs entier n'est pas scindé. Argument : s'il l'était, il serait la réunion scindée de quatre trèfles, puisque tout triplet l'est. Or le nombre d'homomorphismes du groupe de l'entrelacs vers S4 envoyant les méridiens sur des transpositions vaut 144 144, contre 30⁴ = 810 000 pour quatre trèfles séparés.
- **A3 (N).** Volume hyperbolique 102,1858.
- **A4 (E).** Le diagramme a une symétrie d'ordre 3 (84 croisements en 28 orbites). Le motif refermé une seule fois se simplifie en quatre ronds sans croisement.
- **A5 (E).** On ajoute l'axe de la tresse comme cinquième composante. Privé de l'un quelconque des quatre ronds, le diagramme se simplifie en un diagramme à 12 croisements isomorphe, croisement pour croisement, à celui de la tresse σ1^±1 σ3^±1 σ5^±1 munie de son axe. On en déduit que, pour tout k, le motif répété k fois, privé d'un rond, est une réunion scindée de trois nœuds toriques (2, k).
- **A6 (N).** Le motif avec son axe est hyperbolique, volume 40,22. Répété 5 et 7 fois, le motif donne des entrelacs hyperboliques de volumes 190,53 et 274,06.
- **A7 (argument).** Si le motif avec son axe est hyperbolique, alors pour tout k impair au moins égal à 3, l'entrelacs à k tours n'est pas scindé. Preuve proposée : théorème de la sphère équivariante de Meeks, Simon et Yau appliqué à la rotation d'ordre k. Une sphère essentielle disjointe de ses images évite l'axe, descend dans le complémentaire du motif avec axe et y borde une boule. Une sphère invariante, k étant impair, est tournée avec deux points fixes, descend en une sphère coupant l'axe en deux points, donc en un anneau méridien du complémentaire, qui est parallèle au bord faute d'anneau essentiel. Dans les deux cas la sphère de départ borde une boule sans composante.

### B. Les trois trèfles

- **B1 (E pour les ronds et les couples, N pour le tout).** Les dessins 0 et 1 répétés 3 fois donnent trois trèfles, borroméens, et sont le même entrelacs (isométrie, volume 112,2693). Le dessin 2 répété 3 fois donne un autre entrelacs borroméen de trois trèfles (volume 38,19, 21 croisements après simplification).
- **B2 (E).** Dans les trois dessins, chaque couple de ronds est en relation constante, et les trois relations forment un cycle.
- **B3 (E).** En disposition emboîtée à trois ronds, avec g = (1, 2, 1), la règle constante en cycle donne un entrelacs isométrique à celui des dessins 0 et 1. Il n'est pas scindé : 48 coloriages par les transpositions de S4 contre 30³ = 27 000. Avec g = (2, 1, 2) : 11 280. Les deux sens du cycle donnent les mêmes nombres.
- **B4 (E).** En disposition parallèle à trois ronds, quel que soit le réglage des croisements pris parmi ceux qui laissent chaque couple libre, les trois trèfles se séparent.

### C. L'impossibilité pour quatre avec la règle constante

- **C1 (E).** Un tournoi sur quatre ronds est soit transitif, soit contient un cycle de trois.
- **C2.** S'il est transitif, les quatre ronds s'empilent et l'entrelacs est scindé.
- **C3.** En disposition emboîtée à quatre ronds, si le tournoi contient un cycle de trois, le sous-diagramme de ces trois ronds est un diagramme emboîté à trois ronds, d'écriture (1, 2, 1) ou (2, 1, 2), muni d'une règle en cycle. Par B3 il n'est pas scindé. Donc ce triplet ne se sépare pas quand on retire le quatrième rond, et l'entrelacs n'est pas borroméen.
- **C4 (conclusion).** En disposition emboîtée, aucune règle constante ne donne un entrelacs borroméen de quatre trèfles. Contrôle par calcul : 40 tournois non transitifs × 16 écritures, un triplet ne se sépare jamais.

### D. La règle à quatre

- **D1 (E).** Dans le motif TS, cinq couples sont en relation constante : rouge sur noir, rouge sur vert, noir sur brun, vert sur brun, brun sur rouge. Le couple noir et vert alterne : 12 passages dans un sens, 6 dans l'autre.
- **D2.** Sur l'ombre du motif TS, parmi tous les réglages périodiques où cinq couples sont constants, où un couple alterne et où les enlacements sont nuls (1 720 réglages), 8 seulement donnent un entrelacs borroméen. Tous ont le volume 102,1858 et 144 144 coloriages. Dans tous, le couple qui alterne est noir et vert, et le tournoi sur les autres est celui de D1 ou son inverse.
- **D3 (H en partie).** En disposition emboîtée à quatre ronds (16 écritures), aucun réglage périodique à un couple alternant ne donne un entrelacs borroméen, sur 12 288 essayés. Le rejet est exact quand le triplet fautif est un cycle constant, heuristique sinon.

### E. Familles générales

- **E1 (E pour la séparation, N pour le tout).** La tresse σ1 σ3 … σ(2n−1) · C_n, où C_n est le commutateur itéré des tours complets du brin 3 autour des brins 2, 5, 7, …, répétée 3 fois, donne n trèfles dont n − 1 quelconques se séparent. Non-scission calculée pour n = 3 (volume 63,45) et n = 4 (volume 168,9, solution imparfaite). Pour n = 5, non certifiée.

## Les points faibles que nous connaissons

1. **Le motif TS vient d'une image.** Il a été extrait par programme de la figure III-2 de l'édition (`images/edition-ALI/p57-figure-III-2.png`), puis un croisement a été inversé pour rétablir la symétrie d'ordre 3 : celui où le rond noir se croise lui-même, en bas à gauche de la figure. Le dessin 3 de Soury, qui en est l'original, est numérisé trop pauvrement pour être lu (`images/Soury-texte-66/texte66-page4-dessin-3.png`). **Contrôlez la lecture sur l'image** : comparez le motif TS à la figure, croisement par croisement si vous le pouvez, ou au moins sur les croisements du noir et sur les six couples de D1. Faites de même pour les dessins 0, 1 et 2 de Soury, dont les images de contrôle montrent ce que le programme a lu (`images/controles/`). Dites aussi si un énoncé de A ou D vous paraît fragile vis-à-vis d'une erreur de lecture d'un seul croisement.
2. **Les rejets heuristiques.** Chaque fois qu'un énoncé dit « ne se sépare pas » sans invariant exact, il repose sur l'échec de `simplify("global")`. Repérez ceux dont une conclusion dépend.
3. **Les deux lemmes de A2.** Premier lemme : si un entrelacs est réunion scindée de deux parties, et si chaque partie est une réunion scindée de nœuds, l'entrelacs entier l'est. Second lemme : le comptage de coloriages est multiplicatif sur les réunions scindées. Sont-ils corrects tels qu'énoncés, et le comptage programmé compte-t-il bien ce qui est dit ?
4. **Le pas C3.** Le sous-diagramme de trois ronds extrait du diagramme emboîté à quatre ronds est-il vraiment, pour les 16 écritures, un diagramme emboîté à trois ronds de l'une des deux écritures ? Les croisements propres et leur signe sont-ils conservés ? C'est le cœur de l'impossibilité.
5. **Le pas C2.** « Transitif, donc scindé » : est-ce correct pour des composantes nouées, dans un diagramme de tresse fermée ?
6. **L'argument A7.** Usage du théorème de la sphère équivariante, cas d'un sous-groupe stabilisateur propre, hypothèse k impair, passage de la sphère coupant l'axe à un anneau, conclusion.
7. **La portée de D2 et D3.** La recherche ne couvre que les réglages périodiques, d'enlacement nul, à un seul couple alternant. Dites si un énoncé du type « la seule règle qui marche » dépasse ce qui est calculé.

## Les documents joints

- `donnees/` : `pd.json` (codes PD de la figure imprimée et de la figure rectifiée), `motif_tresse.json`, `dessin0.json`, `dessin1.json`, `dessin2.json`, `lacan_couples.json`, `regle_dispositions_TS.json`.
- `programmes/` : les programmes Python. Les principaux, par énoncé : `periode.py`, `motif_tresse.py`, `axe.py`, `axe_preuve.py`, `famille.py` (A) ; `soury3/calcule.py`, `etagement.py`, `lacan_quatre.py`, `lacan_trois_sens.py`, `lacan_recherche.py` (B et C) ; `regle_dispositions.py`, `regle_ts_controle.py`, `regle_quatre.py` (D) ; `motif_bandes.py`, `motif_n5.py` (E) ; `coloriages_inv.py` (comptage de coloriages).
- `resultats/` : les sorties de ces programmes.

- `images/edition-ALI/` : les pages 51 et 55 à 58 de l'édition (texte de Lacan du 9 et du 16 décembre 1975, figure III-2 des quatre trèfles).
- `images/Soury-texte-66/` : les quatre pages du texte 66 de Soury, avec ses dessins 0 à 3.
- `images/controles/` : ce que les programmes ont lu sur les dessins de Soury et sur la figure de l'édition.
- `programmes/extraction/` : les programmes de lecture des images.

Le texte de Lacan de la page 51 donne la règle discutée en B et C. Vous pouvez dire si notre lecture de cette règle (« l'un passe toujours sur l'autre », trois trèfles en cycle) vous paraît fidèle à ce qu'il décrit, sans autre commentaire sur Lacan.

## Ce que nous attendons en retour

Une liste de constats, du plus grave au moins grave. Pour chacun :

- l'énoncé visé (A2, C3, etc.) ;
- ce qui est faux, douteux ou non démontré ;
- comment le reproduire ou le vérifier ;
- ce qu'il faudrait pour le réparer.

Terminez par la liste des énoncés que vous avez **recalculés vous-même** et retrouvés, distincte de ceux que vous avez seulement relus. Si vous ne trouvez rien à redire à un énoncé, dites si c'est faute d'erreur ou faute de moyen de le vérifier.
