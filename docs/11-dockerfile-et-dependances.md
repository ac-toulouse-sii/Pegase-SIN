# 11 : Dockerfiles et dépendances

Chaque service Python de PEGASE est packagé dans son propre conteneur Docker, construit à partir de deux fichiers présents dans son dossier :

* `Dockerfile` : instructions de construction de l'image
* `requirements.txt`: dépendances Python installées via `pip` (peut être **vide** si le service n'utilise que la bibliothèque standard Python.

## Base commune

Tous les Dockerfiles du projet partent de la même image :

```dockerfile
FROM python:3.12-slim
```

`slim` = version allégée de l'image Python officielle.

## Pourquoi un Dockerfile par service plutôt qu'un seul pour tout le projet ?

* Chaque image ne contient que ce dont son service a besoin : images plus légères, builds plus rapides
* Docker met en cache chaque étape (chaque ligne du Dockerfile) : modifier `tri.py` ne force pas à reconstruire l'image `IA`
* Un service qui tombe (ex. `lcd`) n'affecte pas les images des autres
