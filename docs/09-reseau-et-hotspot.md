# 09 : Réseau et hotspot

## Créer le hotspot PEGASE

```bash
sudo nmcli device wifi hotspot ifname wlan0 ssid PEGASE password "PEGASE123456"
```

Attribue automatiquement la plage `10.42.0.0/24` (mode "partagé" de NetworkManager), Raspberry Pi en `10.42.0.1`.

Démarrage automatique au redémarrage :

```bash
sudo nmcli connection modify Hotspot connection.autoconnect yes
```

## Deux configurations réseau possibles

### 1. Hotspot sur le Raspberry Pi (configuration actuelle)

Le Raspberry Pi crée le réseau `PEGASE`, la caméra s'y connecte directement.

- Autonome, aucun routeur nécessaire
- Plage fixe `10.42.0.x`, cohérente avec les IP codées en dur (`ia.py`, `http_wifi.h`)
- Pas d'accès Internet sauf connexion Ethernet partagée
- Sans Internet, `envoi.py` conserve les relevés dans `buffer.jsonl` jusqu'au retour du réseau

### 2. Connexion via un routeur externe

Tous les appareils rejoignent le même réseau WiFi (box, routeur, téléphone). Nécessite de modifier le code, les valeurs actuelles supposant le hotspot du Pi :

- Firmware ESP32 : SSID/mot de passe du routeur au lieu de `PEGASE`
- `http_wifi.h` : IP réelle du Pi au lieu de `10.42.0.1`
- `ia.py` : IP réelle de l'ESP32-CAM au lieu de `10.42.0.107`

IP attribuées par DHCP, peuvent changer après redémarrage.

# Commandes de base

```bash
nmcli device status
```
État des interfaces réseau (`wlan0`, `eth0`...).

```bash
nmcli connection show
```
Liste des connexions configurées.

```bash
nmcli connection up "<nom>"
nmcli connection down "<nom>"
```
Active / désactive une connexion.
