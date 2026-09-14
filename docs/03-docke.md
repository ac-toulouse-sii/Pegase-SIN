# 02 Installation de Docker

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.

Docker permet de faire tourner les différents services du projet (détection IA, tri, envoi, affichage LCD) chacun dans son propre conteneur, isolé des autres.

## Lien page WEB docker

https://www.docker.com/


## Installer Docker

Connectez-vous en SSH à votre Raspberry Pi, puis :

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin docker-buildx-plugin
```
ou (plus lourd)

```bash
curl -sSL https://get.docker.com | sh
```

Ce script installe Docker Engine et Docker Compose (le plugin `docker compose`) directement depuis les dépôts officiels.

## Autoriser votre utilisateur à utiliser Docker sans sudo

Par défaut, seul l'utilisateur root peut utiliser Docker. Pour éviter de taper `sudo` à chaque commande :

```bash
sudo usermod -aG docker $USER
```

Déconnectez-vous puis reconnectez-vous en SSH pour que ce changement prenne effet :

```bash
exit
```

Puis reconnectez-vous normalement (`ssh utilisateur@nom-hote.local`).

## Vérifier l'installation

```bash
docker --version
docker compose version
```

Les deux commandes doivent afficher un numéro de version sans erreur.

## Activer Docker au démarrage

Pour que Docker démarre automatiquement à chaque redémarrage du Raspberry Pi :

```bash
sudo systemctl enable docker
```
