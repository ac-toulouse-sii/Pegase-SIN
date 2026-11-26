# 03 : Accès à distance avec Tailscale

## À quoi ça sert ?

Tailscale crée un réseau privé sécurisé entre tes appareils (PC, téléphone, Raspberry Pi),
même s'ils ne sont pas sur le même Wi-Fi. On peut ainsi se connecter en SSH au Raspberry
depuis n'importe où, sans ouvrir de port sur la box.

À installer maintenant, tant que le Raspberry a Internet (avant le hotspot, fiche 12).

## Documentation officielle

https://tailscale.com/kb/1031/install-linux

## Installer Tailscale sur le Raspberry Pi

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

## Connecter le Raspberry à son compte Tailscale

```bash
sudo tailscale up
```

Une adresse web s'affiche : l'ouvrir sur un ordinateur et se connecter à son compte
Tailscale pour autoriser le Raspberry. Le service redémarre tout seul à chaque démarrage.

## Trouver l'adresse Tailscale du Raspberry

```bash
tailscale ip -4
```

L'adresse commence par `100.` (ex. `100.64.12.34`).

## Se connecter depuis son ordinateur

1. Installer Tailscale sur l'ordinateur (https://tailscale.com/download) et se connecter
   avec **le même compte**.
2. Puis :

```bash
ssh <utilisateur>@<adresse-tailscale>
```

ou avec le nom d'hôte du Raspberry :

```bash
ssh <utilisateur>@<nom-hote>
```

## Attention avec le hotspot PEGASE

Tailscale a besoin d'Internet. Si le Raspberry est en hotspot PEGASE (fiche 12) sans
câble Ethernet branché, il n'a pas Internet et Tailscale ne fonctionne pas.

## Commandes utiles

```bash
tailscale status      # appareils du réseau Tailscale
sudo tailscale down   # se déconnecter
sudo tailscale up     # se reconnecter
```
