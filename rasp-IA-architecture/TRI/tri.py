import json
import os
import time

with open("/app/classes_autorisees.txt", "r") as f:
    classes_autorisees = [ligne.strip() for ligne in f]

dernier_resultat = None

TAILLE_MIN = 5000

etat = {
    "dernier_objet": None,
    "dernier_temps": 0
}
BUFFER = "/data/buffer.jsonl"
LCD_FILE = "/data/lcd.json"

while True:

    if(not os.path.exists("/data/derniere-detection.json")):
        time.sleep(0.1)
        continue

    with open("/data/derniere-detection.json", "r") as f:
        detections = json.load(f)

    detection_tri = [
        detection
        for detection in detections
        if detection["confiance"] >= 0.7
        and detection["classe"] in classes_autorisees
        and detection["box"][2] * detection["box"][3]>= TAILLE_MIN
    ]

    resultat_a_envoyer= []

    for detection in detection_tri:
        resultat_a_envoyer.append({
            "objet": detection["classe"],
            "score": detection["confiance"]
        })

    with open("/data/detection_tri.json", "w") as f:
        json.dump(resultat_a_envoyer, f)

    if (detection_tri != dernier_resultat):
        if detection_tri:
            print("tri : ", resultat_a_envoyer)

        else:
            print("pas de donnée à trier")
        dernier_resultat = detection_tri

    for resultat in resultat_a_envoyer:
        objet = resultat["objet"]
        score = resultat["score"]

        temps = time.time()

        #test dernier objet capté

        if (objet == etat["dernier_objet"] and temps - etat["dernier_temps"]<1):
            continue

        etat["dernier_objet"] = objet
        etat["dernier_temps"] = temps

        with open(BUFFER, "a", encoding="utf-8") as f:
            f.write(json.dumps(resultat) + "\n")

        compteurs = {}

        if os.path.exists(LCD_FILE):
            try:
                with open(LCD_FILE, "r", encoding="utf-8") as f:
                    ancien = json.load(f)
                    compteurs = ancien.get("compteurs", {})
            except json.JSONDecodeError:
                compteurs = {}

        if objet:
            compteurs[objet] = compteurs.get(objet, 0) + 1

        with open(LCD_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "mode": "detection",
                "objet": objet,
                "score": score,
                "compteurs": compteurs
            }, f, indent=2)


    time.sleep(0.1)