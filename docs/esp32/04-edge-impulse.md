# 04 : Edge Impulse (détection embarquée sur l'ESP32)

## Qu'est-ce que c'est ?

Edge Impulse est une plateforme web qui sert à créer un modèle de machine learning
capable de tourner directement sur un microcontrôleur, sans serveur ni cloud.

Dans PEGASE, c'est la deuxième façon de détecter un objet : la détection se fait
directement sur l'ESP32, et non sur le Raspberry Pi avec YOLO.

## Comment ça marche

1. On collecte et on étiquette des images sur la plateforme (ex. `Bouteille`).
2. On entraîne un modèle compact, adapté à un microcontrôleur.
3. On l'exporte en bibliothèque C++/Arduino (modèle + moteur d'inférence).
4. Sur l'ESP32 : capture de l'image, inférence, puis envoi du résultat au Raspberry Pi
   si le score dépasse le seuil.

## Documentation officielle

https://www.edgeimpulse.com
