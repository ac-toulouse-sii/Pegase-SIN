import json
import os
import cv2
import onnxruntime as ort
from urllib.parse import urlparse


import json
import os
import time

import cv2
import numpy as np
import onnxruntime as ort
import requests

# adresse de la caméra a modifier si besoin
IP_ESP32 = "10.42.0.107"        #Reseau HotSpot par défaut Raspberry
#IP_ESP32 = "192.168.1.61"

#lien capture instantanée
URL_CAPTURE = f"http://{IP_ESP32}/capture"

MODELE = "yolo11s.onnx"         # modèle yolo, entrée 640x640
FICHIER_CLASSES = "classes.txt" # les 80 noms d'objets detectables

SEUIL_CONFIANCE = 0.5   # pas de détections en dessous de 50 %
SEUIL_NMS = 0.45        # pas de doublons
PERIODE = 1.0           # secondes entre deux analyses
NB_COEURS = 3           # cœurs CPU donnés au modèle /4

# Pour ne garder que certains objets, ex : {"bottle"}.
CLASSES_CIBLES = None

#Dossier de Travail partagé /data
DOSSIER = "/data"
FICHIER_JSON = f"{DOSSIER}/derniere-detection.json"
FICHIER_IMAGE = f"{DOSSIER}/annotee.jpg"


options = ort.SessionOptions()
options.intra_op_num_threads = NB_COEURS
session = ort.InferenceSession(MODELE, sess_options=options,
                               providers=["CPUExecutionProvider"])

entree = session.get_inputs()[0]
TAILLE = entree.shape[2]    # taille d'entrée lue (320 ou 640 selon modèle)
print(f"Modèle {MODELE} chargé, entrée {TAILLE}x{TAILLE}")

with open(FICHIER_CLASSES) as f:
    classes = [ligne.strip() for ligne in f]


def capturer():
    """Demande une photo à l'ESP32.
    """
    try:
        reponse = requests.get(URL_CAPTURE, timeout=3)
        reponse.raise_for_status()
    except requests.RequestException as erreur:
        print("Caméra injoignable :", erreur)
        return None

    octets = np.frombuffer(reponse.content, np.uint8)
    return cv2.imdecode(octets, cv2.IMREAD_COLOR)   # None si JPEG abîmé


def preparer(image):
    """Met l'image au format attendu par YOLO."""
    img = cv2.resize(image, (TAILLE, TAILLE))
    img = img[:, :, ::-1]                   # BGR (OpenCV) -> RGB (YOLO)
    img = img.transpose(2, 0, 1)            # (H, L, C) -> (C, H, L)
    img = img.astype("float32") / 255.0     # 0-255 -> 0-1
    return img[None, ...]                   # ajoute la dimension "llot (1, 3, 640, 640)"


def detecter(image):
    """Lance YOLO sur l'image et renvoie la liste des objets détectés."""
    hauteur, largeur = image.shape[:2]

    # Sortie brute du modèle : (1, 84, N) : N propositions de 84 valeurs
    #   4 valeurs de position (x centre, y centre, largeur, hauteur)
    #   + 80 scores, un par classe COCO
    sortie = session.run(None, {entree.name: preparer(image)})[0][0].T

    # Pour chaque proposition : la classe la plus probable et son score.
    scores_classes = sortie[:, 4:]
    ids = scores_classes.argmax(axis=1)
    confiances = scores_classes[np.arange(len(sortie)), ids]

    # On ne garde que les propositions assez sûres
    garder = confiances > SEUIL_CONFIANCE
    sortie, ids, confiances = sortie[garder], ids[garder], confiances[garder]

    # Carrés remis à l'échelle de l'image d'origine
    # (le modèle travaille en TAILLE x TAILLE, la caméra en 640x480 par ex.)
    coef_x, coef_y = largeur / TAILLE, hauteur / TAILLE
    carres = []
    for x, y, w, h in sortie[:, :4]:
        carres.append([int((x - w / 2) * coef_x),    # coin haut gauche x
                       int((y - h / 2) * coef_y),    # coin haut gauche y
                       int(w * coef_x),              # largeur
                       int(h * coef_y)])             # hauteur

    # Suppression des doublons : plusieurs carrés sur le même objet
    indices = cv2.dnn.NMSBoxes(carres, confiances.tolist(),
                               SEUIL_CONFIANCE, SEUIL_NMS)

    resultats = []
    for i in np.array(indices).flatten():
        nom = classes[ids[i]]
        if CLASSES_CIBLES and nom not in CLASSES_CIBLES:
            continue
        resultats.append({
            "classe": nom,
            "confiance": round(float(confiances[i]), 2),
            "box": carres[i],
            "ip_esp32": IP_ESP32,
        })
    return resultats


def dessiner(image, resultats):
    """Dessine un carré vert et le nom de l'objet pour chaque détection."""
    for r in resultats:
        x, y, w, h = r["box"]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        texte = f'{r["classe"]} {r["confiance"]:.2f}'
        cv2.putText(image, texte, (x, max(y - 5, 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return image


def enregistrer(resultats, image):
    """Écrit le JSON et l'image annotée de façon atomique :
    on écrit d'abord un fichier temporaire, puis on le renomme.
    Ainsi, celui qui lit ne tombe jamais sur un fichier à moitié écrit."""
    with open(f"{DOSSIER}/detection.tmp", "w") as f:
        json.dump(resultats, f)
    os.replace(f"{DOSSIER}/detection.tmp", FICHIER_JSON)

    cv2.imwrite(f"{DOSSIER}/annotee.tmp.jpg", image)
    os.replace(f"{DOSSIER}/annotee.tmp.jpg", FICHIER_IMAGE)



while True:
    debut = time.time()

    image = capturer()
    if image is None:
        time.sleep(1)
        continue

    resultats = detecter(image)
    enregistrer(resultats, dessiner(image, resultats))

    duree = time.time() - debut
    print(f"{len(resultats)} objet(s) en {duree * 1000:.0f} ms : {resultats}")

    #delai
    time.sleep(max(0, PERIODE - duree))
