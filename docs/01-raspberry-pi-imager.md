# 01 Déploiement de Raspberry Pi OS avec Raspberry Pi Imager

On utilise la version **Lite** (sans interface graphique)

## Matériel nécessaire pour cette étape

- Une carte microSD (16 Go minimum, classe 10 / A1 recommandé)

## Télécharger Raspberry Pi Imager

Rendez-vous sur **[raspberrypi.com/software](https://www.raspberrypi.com/software/)** et téléchargez Raspberry Pi Imager

1. Insérez la carte microSD dans votre ordinateur.
2. Lancez **Raspberry Pi Imager**.
3. **Choisir l'appareil** : sélectionnez votre modèle de Raspberry Pi.
4. **Choisir le système d'exploitation** : `Raspberry Pi OS (other)` :  **`Raspberry Pi OS Lite (64-bit)`**.
5. **Choisir le stockage** : sélectionnez votre carte microSD.
6. Cliquez sur **Suivant**. Imager propose alors de personnaliser l'installation (**"Modifier les réglages" / "Edit Settings"**)

## Personnaliser avant le premier démarrage

Dans les réglages avancés proposés par Imager :

**Général**
- *Nom d'hôte* : donnez un nom unique à ce Raspberry Pi (ex. `pegase-rasp-ia` ou `pegase-groupe-dupont`)
- *Nom d'utilisateur et mot de passe* : définissez vos identifiants
- *Configurer le Wi-Fi* : renseignez le SSID et le mot de passe du réseau si le Raspberry Pi n'est pas branché en Ethernet (partage de connexion si besoin)
- *Paramètres régionaux* : fuseau horaire et disposition du clavier; important de resnigner le pays FR pour utilisation du WiFi

**Services**
- Activez **SSH** — cochez *"Utiliser un mot de passe"* (le plus simple pour démarrer) ou renseignez une clé publique SSH si vous en avez déjà une

Validez, puis lancez l'écriture

## Premier démarrage

1. Une fois l'écriture terminée, retirez la carte microSD de l'ordinateur et insérez-la dans le Raspberry Pi.
2. Branchez l'alimentation. Le premier démarrage prend 1 à 2 minutes
3. Trouvez l'adresse IP ou utilisez le nom d'hôte configuré

## Se connecter en SSH

Depuis votre ordinateur, sur le même réseau :

```bash
ssh <utilisateur>@<nom-hote>.local
```

```bash
ssh <utilisateur>@<adresse-ip>
```

À la première connexion, acceptez l'empreinte de sécurité (`yes`) et entrez le mot de passe défini plus haut.


