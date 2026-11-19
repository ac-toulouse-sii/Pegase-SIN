# 02 — Mises à jour et utilitaires

## Mettre à jour le système

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt autoremove -y
```

Redémarrez si une mise à jour du noyau a été installée :

```bash
sudo reboot
```

## Installer les utilitaires principaux

```bash
sudo apt install -y git tree btop i2c-tools net-tools zsh
```

- `git` : récupérer le projet depuis GitHub
- `tree` : afficher l'arborescence des dossiers/fichiers
- `btop` : équivalent plus moderne de `htop`, interface plus visuelle
- `i2c-tools` : vérifier que l'écran LCD est bien détecté sur le bus I2C
- `net-tools` : retrouver l'adresse IP du Raspberry Pi (`ifconfig`)
- `zsh` : shell alternatif à bash

## Vérifier la détection I2C (une fois le LCD branché)

```bash
i2cdetect -y 1
```

Le tableau affiché doit montrer les adresses `3e` et `62` (celles de l'écran Grove LCD RGB) si le câblage est correct.
