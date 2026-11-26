# 01 : Architecture du projet

Le projet compare deux façons de détecter des objets par IA. Dans les deux cas, les
répertoires ci-dessous sont **sur le Raspberry Pi**. Le Pi envoie ensuite les résultats
à l'API Symfony et les affiche sur l'écran LCD.

| | IA sur le Raspberry Pi | IA sur l'ESP32 |
|---|---|---|
| Où tourne l'IA ? | sur le Pi | sur l'ESP32 |
| Modèle | YOLO | Edge Impulse |
| Ce que l'ESP32 envoie au Pi | des images (ESP32-CAM) | des détections déjà faites |
| Répertoire sur le Pi | `rasp-IA-architecture/` | `esp32-IA-architecture/` |

```text
Raspberry Pi
├── rasp-IA-architecture/
│   ├── IA/          inférence YOLO sur les images reçues
│   └── TRI/         filtrage et dédoublonnage des détections
└── esp32-IA-architecture/
    ├── reception/   serveur Flask qui reçoit les détections en HTTP
    ├── envoi/       envoi vers l'API Symfony (partagé)
    └── lcd/         affichage sur l'écran LCD (partagé)
```

## Architecture 1 : IA sur le Raspberry Pi (`rasp-IA-architecture/`)

ESP32-CAM → **images** → Pi (YOLO) → tri → API Symfony + LCD

- L'ESP32-CAM envoie des images au Pi.
- `IA/` : le Pi détecte les objets avec YOLO.
- `TRI/` : il filtre et dédoublonne les détections.
- Il réutilise `envoi/` et `lcd/` du répertoire `esp32-IA-architecture/` (code partagé).

## Architecture 2 : IA sur l'ESP32 (`esp32-IA-architecture/`)

ESP32 (Edge Impulse) → **détections** → Pi → API Symfony + LCD

- L'ESP32 fait lui-même la détection avec un modèle Edge Impulse.
- Il n'envoie au Pi que le résultat, pas les images.
- `reception/` : serveur Flask qui reçoit les détections en HTTP.
- `envoi/` : envoi des données vers l'API Symfony (partagé avec l'architecture 1).
- `lcd/` : affichage sur l'écran LCD (partagé avec l'architecture 1).





