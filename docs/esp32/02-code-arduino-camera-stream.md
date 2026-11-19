# 18 : Firmware ESP32-CAM (streaming vidéo)

## Rôle

Tourne sur l'ESP32-CAM classique, diffuse le flux vidéo utilisé par `rasp-IA-architecture` (`ia.py`).

## Origine

Code d'exemple standard fourni par Espressif, quasiment pas modifié.

## Identifiants WiFi

Codés en dur dans `initWiFi()` : `PEGASE` / `PEGASE123456`

## Routes du serveur HTTP

| Route | Rôle |
|---|---|
| `/stream` | Flux vidéo MJPEG continu |
| `/capture` | Capture une image unique en JPEG |
| `/` | Page HTML de contrôle intégrée à l'exemple Espressif |
