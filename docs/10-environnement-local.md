# 0X — Configuration (fichier .env)

## Pourquoi un fichier `.env` ?

Le service `envoi` doit connaître votre API Symfony (URL, identifiants). Ces valeurs ne sont jamais écrites en dur dans le code ni committées : chaque déploiement a les siennes.

`.env.example` est le modèle (committé, sans valeur sensible). `.env` est votre copie personnelle, remplie avec vos vraies valeurs — listée dans `.gitignore`, jamais envoyée sur GitHub.

`env_file: - .env` dans `docker-compose.yml` indique au service `envoi` de lire ces variables au démarrage.

## Créer le fichier

Dans chacun des deux dossiers (`rasp-IA-architecture` et `esp32-IA-architecture`) :

```bash
cp .env.example .env
nano .env
```

## Variables

| Variable | Signification |
|---|---|
| `PEGASE_API_URL` | URL du serveur (méthode POST) |
| `PEGASE_API_DOMAIN` | Identifiant du déploiement côté API |
| `PEGASE_API_SIGNATURE` | Clé d'authentification du déploiement |
| `PEGASE_GROUPE` | Nom du groupe envoyé dans le JSON |

## Pas de guillemets

```dotenv
PEGASE_API_URL=https://votre-api.example.com/releve
```

## Sécurité

`.env` jamais commité. Une valeur committée par erreur doit être régénérée côté API

## Lien avec l'API

`PEGASE_GROUPE` correspond au champ `groupe` envoyé dans le JSON par `envoi.py`. Le serveur (API Symfony) attend précisément ces trois champs dans le corps de la requête `/releve` :

```json
{
  "groupe": "...",
  "unite": "...",
  "valeur": <entre 0 et 1; nombre décimal>
}
```

`unite` (la classe détectée) et `valeur` (le score de confiance) sont générés automatiquement par l'IA, `groupe` vient de `.env`.
