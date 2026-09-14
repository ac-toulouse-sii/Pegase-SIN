# 0X : Détection YOLO, code Python (rasp-IA-architecture)

## `ia.py` : inférence YOLO

Rôle : lit le flux vidéo MJPEG de l'ESP32-CAM, exécute le modèle YOLO (ONNX) sur chaque image, et écrit la détection brute dans `/data/derniere-detection.json`.

Initialisation :
- Charge le modèle `yolo11s.onnx` via `onnxruntime`
- Charge la liste des classes COCO depuis `classes.txt`
- Ouvre le flux vidéo de l'ESP32-CAM avec OpenCV (`cv2.VideoCapture`)

Boucle principale, pour chaque image du flux :

1. Lecture de l'image (`cap.read()`)
2. Préparation de l'image pour le modèle : redimensionnement à 640×640, conversion BGR vers RGB, réorganisation des canaux HWC vers CHW, normalisation des pixels entre 0 et 1, ajout d'une dimension de batch
3. Inférence : `session.run(...)` sur l'image préparée
4. Analyse des 8400 propositions de détection renvoyées par le modèle, extraction de la classe la plus probable et de sa confiance pour chacune
5. Filtrage : seules les propositions avec une confiance supérieure à `0.6` sont conservées
6. Suppression des doublons : `cv2.dnn.NMSBoxes` élimine les boîtes qui se chevauchent pour un même objet
7. Écriture atomique du résultat : le JSON est d'abord écrit dans un fichier temporaire (`/data/detection.tmp`), puis renommé en `/data/derniere-detection.json` (`os.replace`), ce qui évite qu'un lecteur externe (`tri.py`) tombe sur un fichier à moitié écrit

À noter : les coordonnées des boîtes sont calculées dans l'espace 640×640, pas dans la résolution d'origine du flux. Si la lecture du flux échoue, la boucle s'arrête et le script se termine, c'est le redémarrage automatique du conteneur Docker qui relance la lecture.

## `tri.py` : filtrage des détections

Rôle : lit `/data/derniere-detection.json` (écrit par `ia.py`), filtre et déduplique les détections, puis alimente le buffer d'envoi et l'état du LCD.

Initialisation :
- Charge la liste des classes autorisées depuis `classes_autorisees.txt`
- `TAILLE_MIN = 5000` : aire minimale, en pixels², d'une boîte pour être retenue

Boucle principale, toutes les 0.1 seconde :

1. Attend que `/data/derniere-detection.json` existe
2. Filtre les détections selon trois critères combinés : confiance supérieure ou égale à `0.7`, classe présente dans `classes_autorisees.txt`, aire de la boîte supérieure ou égale à `TAILLE_MIN`
3. Écrit le résultat filtré dans `/data/detection_tri.json`
4. Affiche un message dans les logs uniquement si le résultat a changé depuis la dernière itération

Anti-doublon et écriture du buffer, pour chaque détection retenue :
- Si c'est le même objet que la dernière détection traitée, et que moins d'une seconde s'est écoulée, elle est ignorée
- Sinon, elle est ajoutée à `/data/buffer.jsonl`, lue ensuite par `envoi.py`
- `/data/lcd.json` est mis à jour : objet courant, score, et un compteur cumulé par type d'objet

À noter : l'anti-doublon ne mémorise qu'un seul dernier objet à la fois, pas un historique par classe. Contrairement à `ia.py`, l'écriture de `/data/detection_tri.json` n'est pas atomique.
