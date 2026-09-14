# 0X : code ESP32-S3 pour Architecture Edge Impulse IA embarquée

Développé dans VS Code + PlatformIO

## `camera.cpp` : caméra OV2640

- `initCamera()` : configure les pins caméra, adapte résolution/qualité JPEG selon présence de PSRAM (UXGA et haute qualité si PSRAM, sinon repli SVGA en DRAM), puis redescend en VGA une fois initialisée
- `test_camera()` : capture une image, affiche résolution et taille. Appelée une seule fois dans `setup()`, vérification ponctuelle

## `http_wifi.cpp` : connexion et serveur HTTP

- `initWifi()` : connexion au hotspot `PEGASE`, démarre un serveur HTTP (port 80) avec deux routes : `/` (dernière image brute) et `/ai` (image réellement envoyée au modèle, pour debug)
- `envoyerSiDetection(objet, score)` : `POST` JSON vers `http://10.42.0.1:5000/detection`
- `handleWifi()` : traite les requêtes HTTP entrantes, appelée en boucle dans `loop()`

## `main.cpp` : orchestration et inférence

- `setup()` : appelle dans l'ordre `initCamera()`, `initWifi()`, `test_camera()`, passe `is_initialised` à `true`, puis appelle `initBuffers()` (allocation des buffers image)
- `loop()` : appelle `handleWifi()`, capture et prétraite l'image, lance `run_classifier()` (inférence Edge Impulse), et si le score de `"Bouteille"` dépasse `0.60`, appelle `envoyerSiDetection()`
- Pipeline image : capture JPEG (640×480), conversion en RGB888, redimensionnement à 96×96 (taille d'entrée du modèle), puis copie de debug ré-encodée en JPEG (utilisée par la route `/ai`)

## `platformio.ini` : configuration du projet

- Carte : DFRobot FireBeetle 2 ESP32-S3
- PSRAM activée (nécessaire : le buffer image brut fait environ 900 Ko)
- Port USB natif configuré comme port série
