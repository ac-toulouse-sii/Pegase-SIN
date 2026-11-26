# 01 : Module caméra IA (ESP32-S3 CAM AI, DFRobot)

## Rôle dans le projet

Ce module caméra sert dans les deux architectures :

- **IA sur le Raspberry Pi (YOLO)** : il envoie les images au Pi (flux vidéo lu par
  `ia.py`, variable `URL_STREAM`) ;
- **IA sur l'ESP32 (Edge Impulse)** : il fait lui-même la détection et n'envoie au Pi
  que le résultat.

## Référence

Module ESP32-S3 CAM AI (DFR1154), DFRobot.

https://www.gotronic.fr/art-module-cam-ai-esp32-s3-47927.htm

## Caractéristiques principales

- Processeur ESP32-S3R8, Wi-Fi 2,4 GHz + Bluetooth 5
- Capteur caméra OV3660, 2 Mpx, champ de vision 160°, sensibilité infrarouge 940 nm
- 16 Mo de Flash, 8 Mo de PSRAM
- Alimentation : USB-C (5 V) ou bornier à vis (5 à 12 V)
