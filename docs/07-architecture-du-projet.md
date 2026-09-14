# 07 : Architecture du projet

## rasp-IA-architecture

Reçoit le flux vidéo d'une ESP32-CAM, détecte les objets par IA, filtre les résultats.

- `IA/` : inférence YOLO sur le flux vidéo
- `TRI/` : filtrage et dédoublonnage des détections

Réutilise aussi `envoi/` et `lcd/` de `esp32-IA-architecture` (code partagé).

## esp32-IA-architecture

Reçoit des détections envoyées directement par des ESP32 capteurs, et fournit le code partagé entre les deux architectures.

- `reception/` : serveur Flask qui reçoit les détections en HTTP
- `envoi/` : envoi des données vers l'API Symfony (partagé)
- `lcd/` : affichage sur l'écran LCD (partagé)
