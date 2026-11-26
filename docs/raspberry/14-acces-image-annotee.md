# 14 : Accès à l'image annotée YOLO

L'image avec les carrés autour des objets détectés est servie par le Raspberry sur le **port 5001**.

| Adresse | Contenu |
|---|---|
| `http://IP_RASPBERRY:5001` | page qui se rafraîchit toute seule (1 image/s) |
| `http://IP_RASPBERRY:5001/annotee.jpg` | dernière image annotée (F5 pour rafraîchir) |

## Adresse du Raspberry

| Réseau | Adresse |
|---|---|
| Hotspot PEGASE | `http://10.42.0.1:5001` |
| Autre réseau | IP donnée par `hostname -I` sur le Raspberry |

Le PC ou le téléphone doit être connecté au **même réseau** que le Raspberry.

## Si la page ne s'affiche pas

```bash
docker compose ps                  # le service "page" doit être "Up"
curl -I http://localhost:5001      # doit renvoyer 200
```

Page blanche ou image figée : vérifier que le service `ia` tourne (`docker compose logs -f ia`).
