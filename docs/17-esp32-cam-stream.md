# 0X : Firmware ESP32-CAM (streaming vidéo)

## Rôle

Ce firmware tourne sur l'ESP32-CAM classique (AI-Thinker), pas l'ESP32-S3. Il diffuse un flux vidéo MJPEG consommé par `rasp-IA-architecture` (`ia.py`, `URL_STREAM`).

## Origine du code

C'est l'exemple standard "CameraWebServer" fourni par Espressif (bibliothèque `esp32-camera`), quasiment non modifié. La seule personnalisation : les identifiants WiFi, codés en dur dans `initWiFi()`.

## `initWiFi()`

- Identifiants hardcodés : `PEGASE` / `PEGASE123456`
- Le code contient un mécanisme de sauvegarde des identifiants via la bibliothèque `Preferences` (mémoire flash), avec saisie par le port série si aucun identifiant n'est enregistré : ce mécanisme n'est pas utilisé actuellement, les identifiants étant écrits directement dans le code

## `initCamera()`

- Résolution initiale `UXGA`, ajustée automatiquement selon la présence de PSRAM (qualité JPEG et nombre de buffers augmentés si PSRAM trouvée)
- Résolution finale ramenée à `QVGA` pour un meilleur débit d'images

## Serveur HTTP (`startCameraServer()`)

Deux serveurs sont démarrés : un serveur principal (port 80) avec les routes de contrôle et debug, et un serveur de flux (port 81).

| Route | Rôle |
|---|---|
| `/stream` (port 81) | Flux vidéo MJPEG continu : la seule route utilisée par PEGASE |
| `/capture` | Capture une image unique en JPEG |
| `/status` | Retourne les réglages actuels de la caméra en JSON |
| `/control` | Modifie un réglage de la caméra (résolution, qualité, luminosité, etc.) |
| `/` | Page HTML de contrôle intégrée à l'exemple Espressif |
| `/bmp`, `/xclk`, `/reg`, `/greg`, `/pll`, `/resolution` | Routes de debug et réglage avancé fournies par l'exemple, non utilisées par PEGASE |

## À noter

Seule la route `/stream` est réellement exploitée par le projet.
