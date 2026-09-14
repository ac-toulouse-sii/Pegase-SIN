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
| `/stream` | Flux vidéo MJPEG continu : la seule route utilisée par PEGASE |
| `/capture` | Capture une image unique en JPEG |
| `/status` | Retourne les réglages actuels de la caméra en JSON |
| `/control` | Modifie un réglage de la caméra |
| `/` | Page HTML de contrôle intégrée à l'exemple Espressif |
| `/bmp`, `/xclk`, `/reg`, `/greg`, `/pll`, `/resolution` | Routes de debug et réglage avancé, non utilisées par PEGASE |

## À noter

Seule la route `/stream` est réellement exploitée par le projet.
