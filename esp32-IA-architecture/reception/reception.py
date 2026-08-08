"""
    code de recptions des donénes provenant de l'esp32

    Ce code est exécuté sur le Raspberry Pi et reçoit les données JSON envoyées par l'ESP32.
    Il les enregistre dans un fichier buffer.jsonl et met à jour un fichier lcd.json
    pour l'affichage sur un écran LCD.
"""
import json
import os
import time
from flask import Flask, request


app = Flask(__name__)

etat = {
    "dernier_objet": None,
    "dernier_temps": 0
}
BUFFER = "/data/buffer.jsonl"
LCD_FILE = "/data/lcd.json"

@app.route('/detection', methods=['POST'])
def reception():
    """
    Fonction appelée lorsqu'une donnée JSON est reçue par le Raspberry.

    Elle récupère les informations envoyées par l'ESP32,
    les affiche dans la console et renvoie une confirmation.
    """
    data = request.json
    objet=data.get("objet")
    score = data.get("score")

    ip_esp32 = request.remote_addr

    temps = time.time()
    if (objet == etat["dernier_objet"] and temps - etat["dernier_temps"] < 1 ):
        print("Objet déjà reçu récemment, on ignore cette détection.")
        return "OK", 200

    etat["dernier_objet"] = objet
    etat["dernier_temps"] = temps

    print ("objet detecte ", objet, "score", score, "ip", ip_esp32)


    with open(BUFFER, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

    # récupération des anciens compteurs
    compteurs = {}

    if os.path.exists(LCD_FILE):
        with open(LCD_FILE, "r", encoding="utf-8") as f:
            ancien = json.load(f)
            compteurs = ancien.get("compteurs", {})

    # ajout du nouvel objet
    if objet:
        compteurs[objet] = compteurs.get(objet, 0) + 1

    with open(LCD_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "mode": "detection",
            "objet": objet,
            "score": score,
            "esp32": ip_esp32,
            "compteurs": compteurs,
        }, f, indent=2)

    return "OK", 200

app.run(host="0.0.0.0", port=5000, debug=True)
