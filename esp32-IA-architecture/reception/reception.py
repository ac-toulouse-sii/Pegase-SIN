from flask import Flask, request
import json
import time

app = Flask(__name__)

etat = {
    "dernier_objet": None,
    "dernier_temps": 0
}

@app.route('/detection', methods=['POST'])
def reception():
    """
    Fonction appelée lorsqu'une donnée JSON est reçue par le Raspberry.

    Elle récupère les informations envoyées par l'ESP32,
    les affiche dans la console et renvoie une confirmation.
    """
    data = request.json
    objet=data.get("objet")
    temps = time.time()
    if (objet == etat["dernier_objet"] and temps - etat["dernier_temps"] < 1 ):
        print("Objet déjà reçu récemment, on ignore cette détection.")
        return "OK", 200

    etat["dernier_objet"] = objet
    etat["dernier_temps"] = temps

    print ("objet detecte ")


    with open("buffer.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")


    return "OK", 200

app.run(host="0.0.0.0", port=5000, debug=True)
