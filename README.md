# Nœuds à quatre de 1975 : programmes et résultats

Ce dépôt accompagne une étude sur les nœuds borroméens que Lacan discute en 1975 : le nœud à quatre ronds (*R.S.I.*, *Le Sinthome*) et le nœud de quatre trèfles apporté par Michel Thomé et Pierre Soury (*Le Sinthome*, 16 décembre 1975).

Il contient les programmes qui ont servi aux calculs, leurs données, leurs résultats, les figures, et les rapports d'une contre-lecture indépendante. Il ne contient pas le texte de l'étude.

## Ce que les calculs établissent

| Résultat | Statut |
|---|---|
| La règle énoncée par Lacan le 9 décembre 1975 (entre deux trèfles, l'un passe toujours sur l'autre, les trois en cycle) donne un nœud borroméen de trois trèfles, celui des dessins 0 et 1 du texte 66 de Soury | démontré |
| Cette règle ne peut pas donner quatre trèfles borroméens, dans la disposition où elle en donne trois | démontré |
| La figure de Thomé et Soury (dessin 3 de Soury) est un nœud borroméen de quatre trèfles. C'est un motif à huit brins répété trois fois autour d'un axe. Elle reste borroméenne pour tout nombre impair de tours | démontré |
| Sur leur dessin, parmi 1 728 réglages à un couple alternant, seul le leur convient | énumération exacte |
| Le nœud à quatre ronds (figures I-8 et I-9 du *Sinthome*) se découpe en deux nœuds borroméens à trois. Ses ronds vont par couples | démontré |
| Le nœud des quatre trèfles ne se découpe pas | certifié par un calcul à intervalles |
| Ses quatre trèfles s'échangent, en admettant l'image en miroir | douze symétries trouvées, liste complète non certifiée |
| Les couples que Lacan voit dans la figure le 16 décembre 1975, rouge avec brun et vert avec noir, appartiennent au nœud. Le nœud porte trois partages en couples, dont celui-là | vérifié par le calcul (symétries, puis volumes après comblement) |
| Les quatre trèfles se séparent si chaque trèfle peut se traverser lui-même | démontré, par les invariants de Milnor |
| L'exemple à quatre éléments que Lacan énonce le 16 mars 1976 (la chaîne à deux éléments de Milnor, chaque élément doublé) ne se défait pas, même si chacun peut se traverser lui-même | vérifié par le calcul, sur l'objet construit d'après sa description |
| Le nœud borroméen ordinaire est un seul rond tourné trois fois autour d'un axe | vérifié par le calcul |
| Dans la figure de Thomé et Soury, à un tour les quatre ronds ne tiennent que par l'axe, à trois tours ils tiennent sans lui | vérifié par le calcul à un tour, démontré à trois |

« Borroméen » s'entend ici au sens de Lacan : un rond retiré, les autres sont libres, chacun gardant son nœud, et l'ensemble ne se sépare pas.

## Ce que ces résultats doivent à Lacan et à Soury

L'étude a été reprise le 19 novembre 2026 après une relecture complète des séances. Les calculs n'ont pas changé. Ce qui a changé est ce qui est attribué à Lacan : plusieurs points d'abord donnés pour neufs sont chez lui ou chez Soury, et les calculs les confirment.

- La règle en cycle, le principe qui interdit de passer de trois à quatre, les couples du nœud à quatre ronds et le tore qui prend deux ronds ensemble sont dits par Lacan (9 décembre 1975, 13 mai 1975, 18 novembre 1975, 10 février 1976).
- L'axe n'est pas une trouvaille de l'étude. Lacan fait passer une corde par le point central du nœud borroméen (10 février 1976, figure VI-1). Soury décrit l'axe d'une tresse cylindrique et un « cercle spécial » voué à disparaître (*Chaînes et nœuds*, textes 52 et 56).
- Restent propres à l'étude : la démonstration que la règle à trois ne s'étend pas à quatre, la construction de la figure de Thomé et Soury (motif répété, série), la règle à quatre avec un couple alternant, et ce que font les tours autour de l'axe.

## Contenu

- `calcul/` : les programmes. Les principaux :
  - `periode.py`, `motif_tresse.py`, `axe.py`, `axe_preuve.py`, `famille.py` : la répétition par trois, le motif, l'axe, la série à cinq et sept tours ;
  - `lacan_homologues.py`, `lacan_quatre.py`, `lacan_trois_sens.py`, `etagement.py` : la règle de Lacan à trois et l'impossibilité à quatre ;
  - `regle_dispositions.py`, `regle_ts_controle.py`, `regle_quatre.py` : la règle à quatre ;
  - `decoupe_chaines.py`, `symetries.py`, `roles_des_ronds.py`, `borromeen_axe.py` : découpe, symétries, axe du nœud borroméen ;
  - `couples_trefles.py`, `couples_trefles_invariant.py` : les couples des quatre trèfles (ajoutés le 19 novembre 2026) ;
  - `lacan_16_mars_link_double.py` : l'exemple à quatre éléments du 16 mars 1976, par les invariants de Milnor (ajouté le 19 novembre 2026) ;
  - `coloriages_inv.py` : comptage exact des coloriages par les transpositions d'un groupe de permutations ;
  - `soury3/` : lecture des dessins 0, 1 et 2 de Soury ;
  - `rsi/` : lecture des figures en couleurs (`lire_figure.py`) et calculs associés.
- `donnees/` : les dessins sous forme calculable (codes PD, mots de tresse).
- `resultats/` : les sorties des programmes.
- `figures/` : les figures et les programmes qui les tracent. Chaque figure de nœud est relue par programme et recalculée.
- `sources/` : les figures des éditions et les dessins de Soury qui ont été lus, avec les images de contrôle montrant ce que le programme a lu.
- `contre-lecture/` : les deux consignes de contre-lecture et les rapports rendus. Ces pièces datent d'avant la reprise du 19 novembre 2026 et sont laissées telles quelles. Les consignes prêtent encore à Lacan des silences que la relecture des séances a démentis. Les trois calculs ajoutés ce jour-là n'ont pas été contre-lus.

## Pour refaire les calculs

Python 3, avec `snappy` (3.3.2, qui installe `spherogram` 2.4.1), `numpy`, `scipy`, `opencv-python`, `matplotlib`, `pillow`.

Les programmes ont été écrits pour une arborescence précise, et les chemins y ont été remplacés par des chemins relatifs ou des repères (`PAGES-DES-EDITIONS/`, `SOURCES-SOURY/`). Il faut les adapter avant de les lancer. Les calculs eux-mêmes ne dépendent que des fichiers de `donnees/`.

Les pages entières des éditions ne sont pas reproduites ici. Seules les figures lues le sont.

## Limites

- Les dessins ont été lus par programme sur des images. La lecture a été contrôlée sur image par la contre-lecture.
- La figure III-2 de l'édition du *Sinthome* s'écarte du dessin 3 de Soury par un croisement, le dernier où le rond noir se croise lui-même. Les calculs portent sur le dessin rectifié, qui coïncide avec celui de Soury. Les deux versions sont dans `donnees/pd.json`.
- La figure XI-7 de l'édition de *R.S.I.*, telle qu'elle est imprimée, n'est pas borroméenne à quatre.
- La disposition prêtée aux trois trèfles de Lacan est celle des dessins de Soury. Lacan donne la règle, non le dessin.
- Les figures I-5 à I-9 du *Sinthome* ont été reconstituées par l'édition à partir de notes d'auditeur. Les calculs sur le nœud à quatre ronds portent sur cette reconstitution.
- L'exemple du 16 mars 1976 a été construit d'après la description de Lacan et la note de l'édition. La figure IX-4 n'a pas été lue par programme. Le calcul établit que les quatre éléments ne se séparent pas tous, non qu'aucun ne se détache.
- Les douze symétries du nœud des quatre trèfles forment une liste que le logiciel déclare complète, sans certification.
- Aucun topologue n'a relu ce travail.

## Qui a fait quoi

Les programmes ont été écrits et exécutés par Claude Fable (Anthropic), sous la direction de l'auteur de l'étude. La contre-lecture a été faite par ChatGPT (OpenAI), qui a recalculé les résultats avec ses propres programmes, corrigé plusieurs points et démontré plusieurs énoncés que nous n'avions que par le calcul numérique.

## Sources

- Jacques Lacan, *Le Sinthome. Séminaire 1975-1976*, édition de l'Association lacanienne internationale, hors commerce.
- Jacques Lacan, *R. S. I. Séminaire 1974-1975*, publication hors commerce de l'Association freudienne internationale.
- Jacques Lacan, *Encore*, séance du 15 mai 1973.
- Pierre Soury, *Chaînes et nœuds*, édité par Michel Thomé et Christian Léger, Paris, textes 12, 52, 56 et 66.
- John Milnor, « Link groups », *Annals of Mathematics* 59, 1954, p. 177-195.
- SnapPy, de M. Culler, N. Dunfield, M. Goerner et J. Weeks.
