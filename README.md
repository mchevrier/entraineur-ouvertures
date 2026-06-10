# 🏆 Mon Entraîneur d'Ouvertures

Petite appli web pour apprendre un répertoire d'ouvertures par cœur (enfant ~1600 ELO).

## Utilisation

Double-cliquer sur **`index.html`** — fonctionne hors ligne, sur ordinateur ou tablette.
La progression (lignes apprises, étoiles) est sauvegardée dans le navigateur.

- **📖 Apprendre** : les coups sont expliqués, bouton 💡 Indice (entoure la pièce, puis la case).
- **🔥 Défi** : 3 ❤️, il faut retrouver les coups de mémoire. 0 erreur = ⭐⭐⭐.

## Modifier ou ajouter des lignes

Les lignes sont dans `gen_lines.py` (notation anglaise : N=Cavalier, B=Fou, R=Tour, Q=Dame, K=Roi),
avec un commentaire en français par coup de l'enfant. Puis :

```bash
python3 gen_lines.py                       # valide chaque coup avec python-chess -> lines.json
python3 build.py                           # injecte lines.json dans template.html -> index.html
```

Contraintes : pas de prise en passant ni de promotion dans les lignes ; chaque ligne doit
se terminer par un coup de l'enfant.

## Test automatique

Ouvrir `index.html#autotest` : joue les 10 lignes en simulant les clics et affiche
`AUTOTEST PASS` en bas de page.
