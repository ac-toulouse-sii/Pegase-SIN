# 13 : Qu'est-ce que YOLO ?

YOLO ("You Only Look Once") est un modèle d'intelligence artificielle de détection d'objets : à partir d'une image, il repère plusieurs objets en une seule passe, avec pour chacun sa position dans l'image, sa classe (ce que c'est) et un score de confiance (à quel point le modèle en est sûr).

Le modèle est pré-entraîné sur un très grand jeu d'images (80 classes d'objets courants : personne, chaise, bouteille, etc.). Il existe en plusieurs tailles, plus le modèle est gros, plus il est précis mais lent : PEGASE utilise la taille "small", un bon compromis vitesse/précision pour tourner sur un Raspberry Pi.

Dans PEGASE, YOLO analyse en continu les images du flux vidéo de la caméra pour détecter les objets présents.

## Comment ça fonctionne en interne

- Pour une image de 640×640, le modèle produit 8400 propositions de détection en une seule passe
- La plupart sont inutiles (bruit, fond)
- Un seuil de confiance élimine les propositions faibles
- Une suppression des doublons fusionne les boîtes qui se chevauchent pour un même objet
- Résultat : quelques détections réelles par image
