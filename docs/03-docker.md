# 03 : Installation de Docker

Docker permet de faire tourner les différents services du projet (détection IA, tri, envoi, affichage LCD) chacun dans son propre conteneur, isolé des autres.

## Documentation officielle

https://docs.docker.com/engine/install/debian/

## Installer Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin docker-buildx-plugin
```

## Autoriser votre utilisateur à utiliser Docker sans sudo

```bash
sudo usermod -aG docker $USER
exit
```

Puis reconnectez-vous en SSH pour que ce changement prenne effet.

## Vérifier l'installation

```bash
docker --version
docker compose version
docker buildx version
```

## Activer Docker au démarrage

```bash
sudo systemctl enable docker
```

## En cas de conflit buildx

Si docker compose up --build échoue avec une erreur du type compose build requires buildx 0.17.0 or later:

```bash
sudo apt remove docker-buildx
sudo apt install docker-buildx-plugin
```
