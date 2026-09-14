# 14 : Edge Impulse (détection embarquée sur l'ESP32)

## Qu'est-ce que c'est ?

Plateforme web pour créer un modèle de machine learning qui tourne directement sur un microcontrôleur, sans serveur ni cloud. C'est l'autre manière de détecter un objet dans PEGASE, en local sur l'ESP32.

## Comment ça marche

- Collecte et étiquetage d'images sur la plateforme (ex. `Bouteille`)
- Entraînement d'un modèle compact, adapté à un microcontrôleur
- Export en bibliothèque C++/Arduino, avec le modèle et le moteur d'inférence
- Sur l'ESP32 : capture, inférence, envoi du résultat au Raspberry Pi si le score dépasse le seuil

## Documentation officielle

https://www.edgeimpulse.com
