# Seconde contre-lecture adverse : les deux nœuds à quatre de Lacan (ronds ordinaires et trèfles)

## Ce qui vous est demandé

Ce brief complète le premier. Il porte sur une question nouvelle : **dans un nœud borroméen à quatre, les quatre ronds jouent-ils le même rôle ?** Nous comparons deux objets que Lacan étudie en 1975 :

- le nœud borroméen à quatre **ronds ordinaires** (RSI, mai 1975 ; Le Sinthome, 18 novembre 1975) ;
- le nœud borroméen de quatre **trèfles** de Thomé et Soury (Le Sinthome, 16 décembre 1975), dont le motif est donné dans le premier brief.

Comme pour le premier, votre tâche est de **chercher les erreurs**. Recalculez par vos moyens, attaquez les raisonnements, lisez les programmes. Tout ce qui suit date d'un seul jour et n'a pas été relu.

Vous n'avez pas à interpréter Lacan. Une seule question de lecture vous est posée, à la fin.

## Définitions

- Un entrelacs de n composantes est *borroméen à n* si toute composante retirée laisse les n − 1 autres en réunion scindée, et si l'entier n'est pas scindé. Pour des ronds ordinaires, les composantes sont non nouées et la réunion scindée est un entrelacs trivial.
- *Chaîne témoin de quatre ronds* : fermeture de la tresse pure [[A12, A23], A34] sur quatre brins, où Aij est le tour complet du brin j autour du brin i, et [x, y] = x y x⁻¹ y⁻¹.

## Les énoncés à éprouver

Statut : **E** exact, **N** numérique (SnapPy, sans vérification par intervalles), **L** lecture d'une image par programme.

### F. Les figures de l'édition

- **F1 (L, puis E sur le diagramme lu).** La figure XI-7 de RSI (`images/edition-ALI/RSI-p171-figure-XI-7.png`), telle qu'elle est imprimée, n'est pas borroméenne à quatre. Le rond noir a un nombre d'enlacement ±1 avec l'un des trois cercles. Les trois cercles sans le noir sont libres. Le noir avec les deux autres cercles forme les anneaux borroméens. Aucune inversion d'un, deux ou trois croisements ne donne un entrelacs borroméen à quatre.
- **F2 (L, puis E).** Les figures I-8 et I-9 du Sinthome (`images/edition-ALI/Sinthome-p29-figures-I-8-et-I-9.png`) sont borroméennes à quatre : quatre ronds non noués, enlacements nuls, tout triplet se simplifie en un dessin sans croisement, l'ensemble garde 16 et 14 croisements après simplification.

### G. La structure du nœud à quatre ronds ordinaires

- **G1 (N).** Le complémentaire de la chaîne témoin contient un tore incompressible qui le découpe en deux morceaux, chacun à trois bords et de volume 7,3277, identifiés par SnapPy au complémentaire des anneaux borroméens (L6a4). Il en va de même pour les figures I-8 et I-9.
- **G2 (N).** Chaque morceau contient deux des quatre ronds. Les ronds vont donc par couples. Épreuve : chirurgie de pente 1/2, puis 1/3, sur deux ronds à la fois. Le volume restant vaut environ 12,47 et 13,62 quand les deux ronds sont du même couple, 12,28 et 13,57 sinon.
- **G3 (L et N).** Dans la figure I-8, les couples sont {noir, bleu} et {vert, rouge}. Lacan légende ces ronds, de gauche à droite, I, R, Σ, S. Les couples sont donc {I, R} et {Σ, S}. Même partition dans la figure I-9.
- **G4 (N).** Une chaîne de cinq ronds, fermeture de [[[A12, A23], A34], A45], a deux tores de découpe et trois morceaux borroméens en file. Nous en déduisons, sans l'avoir vérifié rond par rond, que le morceau du milieu ne contient qu'un rond, et que les cinq ronds ne jouent donc pas tous le même rôle.
- **G5 (non établi).** Nous ne savons pas si les quatre ronds de la chaîne de quatre sont tous équivalents sous les symétries de l'entrelacs. Les volumes après chirurgie de pente ±1, ±1/2, ±1/3 sur un seul rond sont les mêmes pour les quatre.

### H. La structure du nœud de quatre trèfles

- **H1 (N).** Le complémentaire de l'entrelacs de quatre trèfles (motif TS répété trois fois, `donnees/motif_tresse.json`, ou `pd_noir_corrige` dans `donnees/pd.json`) est hyperbolique, volume 102,1858, sans tore de découpe.
- **H2 (N).** Son groupe de symétrie est diédral d'ordre 12. Il agit sur les quatre composantes par le groupe de Klein, donc transitivement. L'entrelacs est amphichéiral.
- **H3 (conséquence).** Dans cet entrelacs, les quatre trèfles sont équivalents. Or le diagramme distingue un couple, noir et vert, qui alternent entre eux alors que les cinq autres couples sont en relation constante (énoncé D1 du premier brief). Cette distinction serait donc une propriété du diagramme, non de l'entrelacs.

### I. Le contraste

- **I1.** Avec des ronds ordinaires, le nœud borroméen à quatre se décompose en deux nœuds borroméens à trois recollés le long d'un tore, et ses ronds vont par couples. Avec les trèfles de Thomé et Soury, il n'y a ni tore ni couple dans l'entrelacs.

## Les points faibles que nous connaissons

1. **Les lectures d'image.** Les figures XI-7, I-8 et I-9 sont lues par `programmes/rsi/lire_figure.py`. Les images de contrôle montrent ce qui a été lu : la couleur du petit cercle à chaque croisement est celle du rond qui passe dessus (`images/controles/`). **Comparez-les aux figures**, croisement par croisement. La figure I-8 contient des traits en pointillé et deux endroits où un trait passe sous deux autres à la suite. La figure I-9 est dense. F1 est le résultat le plus surprenant : vérifiez en priorité les quatre croisements du rond noir avec le cercle auquel il serait enlacé.
2. **G3 dépend d'une correspondance fragile.** Le programme `couples_figures.py` retrouve la couleur de chaque composante de spherogram par un vote sur ses croisements. Une erreur dans cette correspondance changerait les couples. Refaites-la autrement.
3. **G1 et G2 sont numériques.** Les tores viennent de `splitting_surfaces()`, l'identification des morceaux de `identify()`. Existe-t-il un argument exact ? Par exemple : la chaîne témoin est-elle le double de Bing d'une composante des anneaux borroméens, ce qui donnerait la décomposition sans calcul ?
4. **G2 : l'épreuve par chirurgie.** Deux volumes proches (12,47 contre 12,28) sur des variétés non hyperboliques, calculés avec des solutions dégénérées. Est-ce probant ? Les volumes attendus se déduisent-ils de ceux des morceaux ?
5. **G4 est une déduction non contrôlée.**
6. **H2 repose sur le groupe de symétrie calculé par SnapPy** à partir d'une triangulation de 120 tétraèdres environ. Vérifiez que l'action sur les pointes est bien transitive, et que la symétrie respecte les méridiens.
7. **H3 et I1 sont des conséquences.** Dites si elles suivent bien de ce qui précède, et en particulier si « équivalents sous les symétries » autorise à dire que le couple noir et vert « n'est que dans le dessin ».
8. **La chaîne témoin est-elle le bon objet ?** Il existe plusieurs entrelacs borroméens à quatre composantes. Nous affirmons que I-8, I-9 et la chaîne témoin ont la même structure (volume, tore, morceaux), pas qu'ils sont le même entrelacs. Peut-on le décider ?

## La question de lecture

Deux passages de Lacan accompagnent ces figures. Dites seulement si notre lecture de chacun est fidèle au texte, sans autre commentaire.

- Sinthome, p. 28 (`images/edition-ALI/Sinthome-p28-figures-I-5-a-I-7.png`) : « chacun d'entre eux est échangeable, expressément, que un à deux peut s'invertir en deux à un, que trois à quatre peut s'invertir de quatre à trois », avec sous la figure I-8 le tableau I R Σ S, 1 2 3 4, 2 1 4 3. **Notre lecture** : Lacan dit que les ronds s'échangent à l'intérieur de deux couples, {I, R} et {Σ, S}, qui sont ceux de G3.
- RSI, p. 171 (`images/edition-ALI/RSI-p171-figure-XI-7.png`) : à partir de quatre, « une voie particulière qui ne va que jusqu'à six », celle « qui fait du cercle couplé ». **Notre lecture** : un couple de ronds tient la place d'un rond du nœud à trois, et six s'obtient en couplant chacun des trois. Cette lecture n'est pas calculée.

## Les documents joints

- `donnees/` : `I8.json`, `I9.json`, `XI7c.json` (codes PD lus sur les figures, couleur de chaque composante, couple dessous et dessus de chaque croisement), `pd.json`, `motif_tresse.json`.
- `programmes/rsi/` : `lire_figure.py` (lecture des figures), `calcule_figures.py`, `couples_figures.py`, `detail_xi7.py`, `rectifie_xi7.py`, `rectifie2_xi7.py`.
- `programmes/` : `decoupe_chaines.py`, `roles_des_ronds.py`, `symetries.py`, `symetries_chaines.py`, et les programmes du premier brief qui servent ici.
- `resultats/` : les sorties.
- `images/edition-ALI/` : RSI p. 170, 171 et 175 ; Le Sinthome p. 28, 29, 50, 51 et 57.
- `images/controles/` : ce que le programme a lu sur les figures XI-7, I-8 et I-9.

## Ce que nous attendons en retour

Comme pour le premier brief : une liste de constats du plus grave au moins grave, avec pour chacun l'énoncé visé, ce qui est faux ou non démontré, comment le vérifier, comment le réparer. Puis la liste des énoncés que vous avez recalculés vous-même, distincte de ceux que vous avez seulement relus.
