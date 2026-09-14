# 0X : Module caméra IA (ESP32-S3 CAM AI, DFRobot)

Caméra utilisée par `rasp-IA-architecture` pour fournir le flux vidéo analysé par `ia.py` (`URL_STREAM`).

## Référence

Module ESP32-S3 CAM AI (DFR1154), DFRobot.

https://www.gotronic.fr/art-module-cam-ai-esp32-s3-47927.htm

## Caractéristiques principales

- Processeur ESP32-S3R8, WiFi 2.4 GHz + Bluetooth 5
- Capteur caméra OV3660, 2 Mpx, champ de vision 160°, sensibilité infrarouge 940 nm
- 16 Mo Flash, 8 Mo PSRAM
- Alimentation : USB-C (5V) ou bornier à vis (5-12V)

## Configuration

Programmation via l'IDE Arduino avec l'extension ESP32

Une fois configuré en diffusion vidéo sur le réseau local, relever son adresse IP et l'indiquer dans `rasp-IA-architecture/IA/ia.py` (`URL_STREAM`).
