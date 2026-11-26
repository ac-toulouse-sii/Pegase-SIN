# 03 : Firmware caméra streaming (architecture YOLO)

## Rôle

Ce firmware tourne sur la caméra et diffuse le flux vidéo utilisé par le Raspberry Pi
pour la détection YOLO (`rasp-IA-architecture`, script `ia.py`).

## Origine

Code d'exemple standard fourni par Espressif (CameraWebServer), quasiment pas modifié.

## Identifiants Wi-Fi

Codés en dur dans `initWiFi()` : `PEGASE` / `PEGASE123456`

## Routes du serveur HTTP

| Route | Rôle |
|---|---|
| `/` | page HTML de contrôle de l'exemple Espressif (réglage de la résolution) |
| `/capture` | capture une image unique en JPEG |
| `:81/stream` | flux vidéo MJPEG continu (un seul client à la fois) |

Avant de lancer YOLO, régler la résolution sur **SVGA (800x600)** depuis la page `/`
(voir la fiche 06).
