# Programmer l'ESP32 avec VS Code et PlatformIO

## Installation (une seule fois)

1. Installer **VS Code** : https://code.visualstudio.com
2. Dans VS Code, onglet **Extensions**, installer **PlatformIO IDE**.
3. Redémarrer VS Code. Une icône PlatformIO (tête de fourmi) apparaît dans la barre de gauche.

## Ouvrir le projet

1. **Fichier**, **Ouvrir le dossier**, choisir le dossier du code ESP32 (celui qui contient `platformio.ini`).
2. PlatformIO lit `platformio.ini` et **télécharge tout seul** la carte, le framework Arduino et les bibliothèques. La première fois, c'est long : attendre la fin dans la barre du bas.

Ne pas modifier `platformio.ini` : la carte et la PSRAM y sont déjà configurées.

## Compiler, téléverser, observer

Boutons de la barre bleue en bas de VS Code :

| Bouton | Rôle |
|---|---|
| Build | compiler le code |
| Upload | envoyer le code sur l'ESP32 |
| Prise (Serial Monitor) | voir les messages de l'ESP32 (IP de la caméra, détections) |

## À modifier avant de téléverser

Dans le code, le **Wi-Fi** (`WiFi.begin`) et, pour le modèle Edge Impulse, l'**adresse du Raspberry** (`http.begin`).

## En cas de problème

- **Upload impossible** : maintenir **BOOT**, appuyer sur **RESET**, relâcher **BOOT**, relancer Upload.
