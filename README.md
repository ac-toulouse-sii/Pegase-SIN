## Guide d'installation pas à pas

Pour un déploiement complet, depuis une carte SD vierge jusqu'à un système fonctionnel, suivre les guides de `docs/` dans l'ordre.

### Général

1. [Architecture du projet](docs/01-architecture-du-projet.md)
2. [Accès depuis le navigateur](docs/02-acces-navigateur.md)
3. [Module caméra IA](docs/03-module-camera-ai.md)
4. [Alternative non développée : Teachable Machine](docs/04-alternative-ia.md)

### ESP32

1. [Programmer l'ESP32 avec VS Code et PlatformIO](docs/esp32/01-vscode-platformio.md)
2. [Firmware ESP32-CAM (streaming vidéo)](docs/esp32/02-code-arduino-camera-stream.md)
3. [Accès aux images de la caméra](docs/esp32/03-acces-camera-esp32.md)
4. [Edge Impulse](docs/esp32/04-edge-impulse.md)
5. [Code Arduino, ESP32-S3 (Edge Impulse)](docs/esp32/05-code-arduino-esp32-ia.md)
6. [Code Python, réception des détections Edge Impulse](docs/esp32/06-code-python-edge-impulse.md)

### Raspberry Pi

1. [Déploiement de Raspberry Pi OS avec Raspberry Pi Imager](docs/raspberry/01-raspberry-pi-imager.md)
2. [Mises à jour et utilitaires](docs/raspberry/02-mises-a-jour-utilitaires.md)
3. [Réseau et hotspot](docs/raspberry/03-reseau-et-hotspot.md)
4. [Installation de Docker](docs/raspberry/04-docker.md)
5. [Configuration (.env)](docs/raspberry/05-environnement-local.md)
6. [Récupération du projet](docs/raspberry/06-recuperation-projet.md)
7. [Dockerfiles et dépendances](docs/raspberry/07-dockerfile-et-dependances.md)
8. [Commandes docker compose](docs/raspberry/08-commandes-docker-compose.md)
9. [Obtenir le modèle YOLO](docs/raspberry/09-yolo-ultralytics.md)
10. [Qu'est-ce que YOLO](docs/raspberry/10-detection-yolo.md)
11. [Code Python, ia.py et tri.py](docs/raspberry/11-code-python-yolo.md)
12. [Accès à l'image annotée YOLO](docs/raspberry/12-acces-image-annotee.md)
13. [Arrêt du Raspberry Pi](docs/raspberry/13-arret-raspberry.md)
