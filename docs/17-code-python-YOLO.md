# 17 : Code Python, `ia.py` et `tri.py`

## `ia.py` : inférence YOLO

- Charge le modèle `yolo11s.onnx` et les classes COCO
- Lit en boucle le flux vidéo de l'ESP32-CAM
- Pour chaque image : redimensionne à 640×640, lance l'inférence, garde les détections avec confiance supérieure à `0.6`, supprime les doublons
- Écrit le résultat dans `/data/derniere-detection.json`

## `tri.py` : filtrage des détections

- Lit `/data/derniere-detection.json` toutes les 0.1 seconde
- Garde seulement les détections avec confiance supérieure ou égale à `0.7`, classe autorisée, et taille de boîte suffisante
- Ignore les doublons rapprochés (moins d'1 seconde, même objet)
- Écrit les détections retenues dans `/data/buffer.jsonl` (lues ensuite par `envoi.py`) et met à jour `/data/lcd.json`
