# 02 Accès depuis le navigateur

Le PC ou le téléphone doit être connecté au **même réseau** que le Raspberry et la caméra.

## Adresses

| Ce qu'on veut voir | Adresse |
|---|---|
| **Modèle Edge Impulse** : photo en direct | `http://IP_CAMERA/` |
| **Modèle Edge Impulse** : image vue par le modèle | `http://IP_CAMERA/ai` |
| **Modèle YOLO** : réglages de la caméra (résolution SVGA 800x600 !) | `http://IP_CAMERA/` |
| **Modèle YOLO** : une photo | `http://IP_CAMERA/capture` |
| **Modèle YOLO** : flux vidéo | `http://IP_CAMERA:81/stream` |
| **Modèle YOLO** : image annotée | `http://IP_RASPBERRY:5001` |

## Trouver les adresses

| | Hotspot PEGASE | Autre réseau |
|---|---|---|
| Raspberry | `10.42.0.1` | `hostname -I` sur le Raspberry |
| Caméra | `10.42.0.xxx` | moniteur série, appuyer sur **RESET**, lire la ligne `IP` |

Depuis le Raspberry en hotspot, liste des appareils connectés :
```bash
ip neigh show dev wlan0
```

## Ça ne s'affiche pas

- Mauvais réseau : vérifier le Wi-Fi du PC.
- Flux vidéo bloqué : un seul client à la fois, fermer les autres onglets.
- Caméra redémarrée : refaire le réglage de résolution.

Détails : [esp32/03-acces-camera-esp32.md](esp32/03-acces-camera-esp32.md) et [raspberry/12-acces-image-annotee.md](raspberry/12-acces-image-annotee.md)
