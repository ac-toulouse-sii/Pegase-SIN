# Accès aux images de la caméra ESP32

Remplacer `IP` par l'adresse de la caméra (voir en bas de la fiche).

## Architecture ESP32 + IA (Edge Impulse)

| Adresse | Contenu |
|---|---|
| `http://IP/` | photo en direct |
| `http://IP/ai` | image envoyée au modèle Edge Impulse |

## Architecture Raspberry + YOLO (caméra CameraWebServer)

| Adresse | Contenu |
|---|---|
| `http://IP/` | interface de réglage de la caméra |
| `http://IP/capture` | une photo |
| `http://IP:81/stream` | flux vidéo (un seul client à la fois) |

### Réglage obligatoire avant de lancer YOLO

1. Ouvrir `http://IP/`
2. Dans **Resolution**, choisir **SVGA (800x600)**

Sinon, l'image est trop petite pour le modèle YOLO.

Ce réglage est perdu à chaque redémarrage de la caméra : le refaire après chaque reset.

## Trouver l'IP de la caméra

- Moniteur série : ouvrir le moniteur, appuyer sur **RESET**, lire la ligne `IP address:`.
- Depuis le Raspberry en hotspot PEGASE :
  ```bash
  ip neigh show dev wlan0
  ```
