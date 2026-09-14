# 0X : Réception des détections, code Python (esp32-IA-architecture)

## `reception.py` : serveur Flask (port 5000)

- Route `POST /detection` : reçoit un JSON `{"objet": ..., "score": ...}` depuis les ESP32
- Anti-doublon : une détection identique (même `objet`) reçue moins d'1 seconde après la précédente est ignorée
- Écrit chaque détection valide dans `data/buffer.jsonl`
- Met à jour `data/lcd.json` : objet courant, score, IP de l'émetteur (`request.remote_addr`), compteur cumulé par type d'objet
- Répond toujours `"OK", 200`, même en cas de doublon ignoré
- Lancé avec `debug=True` : pratique en développement, à désactiver si exposé au-delà du réseau local

## `envoi.py` : envoi vers l'API Symfony (code partagé)

- Lit les variables d'environnement (`.env`) : `PEGASE_API_URL`, `PEGASE_API_DOMAIN`, `PEGASE_API_SIGNATURE`, `PEGASE_GROUPE`
- Lève une erreur au démarrage si une variable manque
- Lit `data/buffer.jsonl` ligne par ligne, envoie chaque relevé en `POST` vers l'API
- Si la réponse est `201`, retire la ligne du buffer (envoi confirmé)
- Sinon, laisse la ligne en attente et retente à la prochaine itération (environ une fois par seconde)

## `lcd.py` : affichage sur écran Grove LCD RGB (code partagé)

- Pilote l'écran via I2C : deux adresses, `0x3E` (texte) et `0x62` (rétroéclairage RGB)
- Affiche l'IP du Raspberry Pi au démarrage
- Puis alterne entre deux modes : dernière détection, et compteur cumulé

Ce dernier fichier n'a pas été recollé dans cette partie de la conversation. Le résumé ci-dessus vient de la description qu'on avait faite plus tôt. Dis-moi si tu veux que je vérifie sur le code réel.
