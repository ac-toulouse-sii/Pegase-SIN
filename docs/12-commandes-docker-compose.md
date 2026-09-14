## Se placer dans le bon dossier

Ces commandes doivent être lancées **depuis le dossier qui contient le `docker-compose.yml` concerné** (`rasp-IA-architecture` ou `esp32-IA-architecture`), sinon Docker ne le trouve pas :

```bash
cd rasp-IA-architecture
docker compose <votre-commande>
```

*(remplacez par `esp32-IA-architecture` selon la machine)*

# 12: Démarrage du système

```bash
docker compose up --build
```

En arrière-plan :

```bash
docker compose up -d --build
```

Voir les logs :

```bash
docker compose logs -f
```

Arrêter :

```bash
docker compose down
```

À faire sur les deux Raspberry Pi (`rasp-IA-architecture` et `esp32-IA-architecture`).

## Libérer de l'espace disque

Après plusieurs builds, les images inutilisées s'accumulent et prennent de la place sur la carte SD :

```bash
docker system prune -a
```

`-a` supprime aussi les images non utilisées mais encore taguées (pas seulement les images orphelines), contrairement à `docker system prune` seul.
