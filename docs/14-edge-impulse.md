# 0X : Edge Impulse (détection embarquée sur l'ESP32)

## Qu'est-ce qu'Edge Impulse ?

Plateforme web pour créer des modèles de machine learning conçus pour tourner **directement sur un microcontrôleur** (TinyML) — à l'inverse d'un modèle classique qui tourne sur un serveur ou un PC puissant.

## Pourquoi ici, en plus de YOLO sur le Raspberry Pi ?

PEGASE a deux pipelines de détection distincts et indépendants :

- `rasp-IA-architecture` : YOLO (ONNX) tourne **sur le Raspberry Pi**, qui analyse le flux vidéo envoyé par une ESP32-CAM
- `esp32-IA-architecture` : le modèle Edge Impulse tourne **directement sur l'ESP32**, qui décide localement s'il y a détection, avant même d'envoyer quoi que ce soit au Raspberry Pi

## Étapes du workflow Edge Impulse

1. Collecte d'images (via l'appareil ou upload manuel sur la plateforme)
2. Étiquetage des classes (ex. `Bouteille`)
4. Entraînement d'un modèle compact, adapté aux contraintes mémoire/CPU d'un microcontrôleur
5. Test / validation de la précision
6. Export en bibliothèque C++/Arduino (ex. `Pegase-test-chaise-bouteille_inferencing.h`) contenant le modèle entraîné et le moteur d'inférence

## Utilisation dans le sketch

1. Capture d'une image via la caméra
2. Appel de la fonction d'inférence de la bibliothèque
3. Récupération d'un score de confiance par classe (ex. `Bouteille` : `0.72`)
4. Si le score dépasse le seuil défini (`0.60` dans le projet) :  `envoyerSiDetection()` envoie le résultat au Raspberry Pi

## À retenir

- Aucun serveur ni cloud nécessaire pour l'inférence : tout se passe sur l'ESP32
- La bibliothèque générée est propre à ton modèle entraîné; un autre projet Edge Impulse donnerait un autre fichier
- Le nom du fichier (`Pegase-test-chaise-bouteille_inferencing.h`) reprend le nom du projet Edge Impulse, suivi de `_inferencing.h`

## Documentation officielle

https://www.edgeimpulse.com
