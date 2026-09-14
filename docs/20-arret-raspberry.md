# 20 : Arrêt du Raspberry Pi

Le système de fichiers est sur une carte SD : couper l'alimentation brutalement peut le corrompre. Toujours arrêter proprement avant de débrancher.

## Éteindre

```bash
sudo shutdown now
```

Équivalent :

```bash
sudo poweroff
```

Attendez que la LED verte (ACT) cesse de clignoter avant de débrancher l'alimentation : c'est le signal que l'écriture sur la carte SD est terminée.

## Redémarrer

```bash
sudo reboot
```
