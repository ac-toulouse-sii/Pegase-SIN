## Guide d'installation pas à pas

Pour un déploiement complet, depuis une carte SD vierge jusqu'à un système fonctionnel,
suivre les guides de `docs/` dans l'ordre.

### Général

1. [Architecture du projet](docs/01-architecture-du-projet.md)
2. [Alternative non développée : Teachable Machine](docs/02-alternative-ia.md)

### ESP32

1. [Module caméra IA](docs/esp32/01-module-camera-ai.md)
2. [Accès depuis le navigateur](docs/esp32/02-acces-navigateur.md)
3. [Programmer l'ESP32 avec VS Code et PlatformIO](docs/esp32/02-vscode-platformio.md)
4. [Firmware caméra streaming (YOLO)](docs/esp32/03-firmware-stream-yolo.md)
5. [Edge Impulse](docs/esp32/04-edge-impulse.md)
6. [Code ESP32-S3 (Edge Impulse)](docs/esp32/05-code-arduino-esp32-ia.md)
7. [Accès aux images de la caméra](docs/esp32/06-acces-camera-esp32.md)

### Raspberry Pi

1. [Déploiement de Raspberry Pi OS avec Raspberry Pi Imager](docs/raspberry/01-raspberry-pi-imager.md)
2. [Mises à jour et utilitaires](docs/raspberry/02-mises-a-jour-utilitaires.md)
3. [Accès à distance avec Tailscale](docs/raspberry/03-tailscale.md)
4. [Installation de Docker](docs/raspberry/04-docker.md)
5. [Récupération du projet](docs/raspberry/05-recuperation-projet.md)
6. [Configuration (.env)](docs/raspberry/06-configuration-env.md)
7. [Dockerfiles et dépendances](docs/raspberry/07-dockerfile-et-dependances.md)
8. [Qu'est-ce que YOLO ?](docs/raspberry/08-detection-yolo.md)
9. [Obtenir le modèle YOLO](docs/raspberry/09-yolo-ultralytics.md)
10. [Code Python, ia.py et tri.py](docs/raspberry/10-code-python-yolo.md)
11. [Code Python, réception des détections Edge Impulse](docs/raspberry/11-code-python-edge-impulse.md)
12. [Réseau et hotspot](docs/raspberry/12-reseau-et-hotspot.md)
13. [Démarrage du système (Docker Compose)](docs/raspberry/13-commandes-docker-compose.md)
14. [Accès à l'image annotée YOLO](docs/raspberry/14-acces-image-annotee.md)
15. [Arrêt du Raspberry Pi](docs/raspberry/15-arret-raspberry.md)
