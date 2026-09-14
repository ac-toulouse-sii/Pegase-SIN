# 05 Obtenir le modèle YOLO (yolo11s.onnx)

Le fichier `IA/yolo11s.onnx` n'est pas récupérable directement en téléchargement.

## Documentation officielle

https://docs.ultralytics.com/modes/export/

## Installer Ultralytics (dans un environnement virtuel)

```bash
python3 -m venv yolo-export
source yolo-export/bin/activate
pip install ultralytics
```

## Exporter le modèle en ONNX

```bash
python3 -c "from ultralytics import YOLO; YOLO('yolo11s.pt').export(format='onnx')"
```

Le fichier `yolo11s.onnx` est généré dans le dossier courant. Copiez-le ensuite dans `rasp-IA-architecture/IA/`.

## Nettoyer

```bash
deactivate
rm -rf yolo-export
```

Cette commande télécharge automatiquement `yolo11s.pt` (le modèle pré-entraîné sur le jeu de données COCO) s'il n'est pas déjà présent, puis génère `yolo11s.onnx` dans le même dossier.

## Les différentes tailles disponibles

| Modèle | Taille | Vitesse | Précision |
|---|---|---|---|
| `yolo11n.pt` | nano | la plus rapide | la moins précise |
| `yolo11s.pt` | small | rapide | celle utilisée dans ce projet |
| `yolo11m.pt` | medium | moyenne | bonne |
| `yolo11l.pt` | large | lente | très bonne |
| `yolo11x.pt` | extra-large | la plus lente | la plus précise |

Pour changer de taille, remplacez `yolo11s.pt` par la variante voulue dans la commande d'export.

## Utiliser un autre fichier exporté

Une fois le fichier `.onnx` généré, copiez-le dans `rasp-IA-architecture/IA/`, et mettez à jour le nom du fichier chargé dans `ia.py` si vous changez de taille :

```python
session = ort.InferenceSession("yolo11s.onnx")
```
