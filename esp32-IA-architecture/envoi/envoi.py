import json
import time
import requests
import os

BUFFER = "/data/buffer.jsonl"

GROUPE = os.environ.get("PEGASE_GROUPE", "PEGASE")

TIMEOUT = 2

URL = os.environ.get("PEGASE_API_URL")
API_TOKEN = os.environ.get("PEGASE_API_TOKEN")

if not URL or not API_TOKEN:
    raise RuntimeError("Variables manquantes : PEGASE_API_URL et PEGASE_API_TOKEN (voir .env)")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

if not URL or not API_TOKEN:
    raise RuntimeError(
        "Variables d'environnement manquantes : PEGASE_API_URL, "
        "PEGASE_TOKEN doivent être définies "
        "(voir le fichier .env, à créer à partir de .env.example)."
    )


def envoi_serveur(objet: str, score: float):
    """Envoie une détection vers l'API Symfony."""

    payload = {
        "groupe": GROUPE,
        "unite": objet,
        "valeur": score
    }

    try:
        r = requests.post(
            URL,
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        print("Envoi :", payload)
        print("Status :", r.status_code)

        return r.status_code == 201

    except requests.exceptions.RequestException as e:
        print("Erreur envoi :", e)
        return False



def traiter_buffer():
    """Lit le buffer et envoie les données valides."""

    if not os.path.exists(BUFFER):
        print("Buffer inexistant")
        return

    with open(BUFFER, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    if not lignes:
        print("Buffer vide")
        return

    reste = []

    for ligne in lignes:
        try:
            data = json.loads(ligne)

            objet = data.get("objet")
            score = data.get("score")

            if objet is None or score is None:
                print("Donnée invalide :", data)
                reste.append(ligne)
                continue

            if envoi_serveur(objet, score):
                print("Supprimé du buffer :", data)
            else:
                reste.append(ligne)

        except json.JSONDecodeError:
            print("JSON invalide :", ligne)
            reste.append(ligne)

    with open(BUFFER, "w", encoding="utf-8") as f:
        f.writelines(reste)



while True:
    traiter_buffer()
    time.sleep(1)