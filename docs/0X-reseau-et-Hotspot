## Deux configurations réseau possibles

### 1. Hotspot directement sur le Raspberry Pi (configuration actuelle)

Le Raspberry Pi crée lui-même le réseau `PEGASE`, et la caméra s'y connecte directement.

- Autonome : aucun routeur externe nécessaire
- Plage d'adresses fixe et prévisible (`10.42.0.x`), cohérente avec les IP codées en dur dans `ia.py` et `http_wifi.h`
- Limite : un seul Raspberry Pi peut héberger ce hotspot par interface WiFi ; pas d'accès à Internet sauf si la connexion filaire RJ45 a un accès à internet
- Sans accès à Internet, les relevés ne sont pas perdus : `envoi.py` les conserve dans `buffer.jsonl`.

### 2. Connexion via un routeur externe

Le Raspberry Pi et les ESP32 rejoignent tous le même réseau WiFi fourni par un routeur (box internet, routeur dédié, téléphone...).

Dans ce cas, il faut modifier le code, car les valeurs actuelles supposent le hotspot du Raspberry Pi :

- Firmware ESP32 (`WiFi.begin("PEGASE", "PEGASE123456")`): remplacer par le SSID et le mot de passe du routeur
- `http_wifi.h` (`http.begin("http://10.42.0.1:5000/detection")`) : remplacer `10.42.0.1` par l'IP réelle du Raspberry Pi sur le réseau du routeur (`hostname -I` sur le Pi)
- `rasp-IA-architecture/IA/ia.py` (`URL_STREAM = "http://10.42.0.107:81/stream"`) : remplacer par l'IP réelle de l'ESP32-CAM sur ce même réseau

Sur un réseau routeur, les IP sont généralement attribuées par DHCP et peuvent changer après un redémarrage.
